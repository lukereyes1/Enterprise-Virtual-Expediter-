# Home Ops Agent - Implementation Guide

## Quick Start

This guide will help you implement the Home Ops Agent system from scratch. Follow these steps in order.

## Prerequisites

### Required Accounts & Access
- [ ] Google Workspace account (Gmail + Calendar)
- [ ] Notion or Airtable account
- [ ] OpenAI API key or Anthropic Claude API key
- [ ] Twilio account (for SMS notifications)
- [ ] Domain for webhooks (or ngrok for testing)

### Technical Requirements
- [ ] Node.js 18+ or Python 3.10+
- [ ] Database (PostgreSQL recommended)
- [ ] Message queue (Redis recommended)
- [ ] Hosting environment (AWS, GCP, or similar)

---

## Step 1: Set Up Infrastructure

### 1.1 Database Setup

Create the following tables:

```sql
-- Tasks table
CREATE TABLE tasks (
  id VARCHAR(255) PRIMARY KEY,
  title VARCHAR(500) NOT NULL,
  description TEXT,
  owner VARCHAR(50) NOT NULL,
  assignee VARCHAR(255),
  due_date DATE NOT NULL,
  priority VARCHAR(20) NOT NULL,
  category VARCHAR(50) NOT NULL,
  status VARCHAR(50) NOT NULL,
  estimated_minutes INTEGER,
  actual_minutes INTEGER,
  requires_approval BOOLEAN DEFAULT TRUE,
  approval_reason TEXT,
  approved_by VARCHAR(100),
  approved_at TIMESTAMP,
  completed_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  created_by VARCHAR(50),
  tags JSONB,
  notes JSONB,
  dependencies JSONB,
  related_entity JSONB,
  recurrence JSONB
);

-- People table
CREATE TABLE people (
  id VARCHAR(255) PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  role VARCHAR(50) NOT NULL,
  contact_info JSONB,
  relationships JSONB,
  preferences JSONB,
  vip_status BOOLEAN DEFAULT FALSE,
  approval_required BOOLEAN DEFAULT FALSE,
  approval_reason TEXT,
  birthday DATE,
  notes JSONB,
  tags JSONB,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Vendors table
CREATE TABLE vendors (
  id VARCHAR(255) PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  category VARCHAR(50) NOT NULL,
  contact_info JSONB NOT NULL,
  services JSONB,
  rate JSONB,
  schedule JSONB,
  rating DECIMAL(2,1),
  notes JSONB,
  service_history JSONB,
  status VARCHAR(20) DEFAULT 'Active',
  preferred_contact VARCHAR(20),
  insurance JSONB,
  license JSONB,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Events table
CREATE TABLE events (
  id VARCHAR(255) PRIMARY KEY,
  title VARCHAR(500) NOT NULL,
  description TEXT,
  type VARCHAR(50) NOT NULL,
  date_time TIMESTAMP NOT NULL,
  end_date_time TIMESTAMP,
  duration INTEGER,
  all_day BOOLEAN DEFAULT FALSE,
  location JSONB,
  attendees JSONB,
  owner VARCHAR(50) NOT NULL,
  priority VARCHAR(20) DEFAULT 'Medium',
  requires_prep BOOLEAN DEFAULT FALSE,
  prep_tasks JSONB,
  conflicts JSONB,
  status VARCHAR(20) DEFAULT 'Tentative',
  rsvp_required BOOLEAN DEFAULT FALSE,
  rsvp_deadline DATE,
  rsvp_status VARCHAR(20),
  reminders JSONB,
  recurrence JSONB,
  cost JSONB,
  notes JSONB,
  tags JSONB,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Projects table
CREATE TABLE projects (
  id VARCHAR(255) PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  category VARCHAR(50) NOT NULL,
  status VARCHAR(50) DEFAULT 'Planning',
  owner VARCHAR(50) NOT NULL,
  start_date DATE,
  target_end_date DATE,
  actual_end_date DATE,
  priority VARCHAR(20) DEFAULT 'Medium',
  tasks JSONB,
  vendors JSONB,
  budget JSONB,
  milestones JSONB,
  documents JSONB,
  notes JSONB,
  tags JSONB,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Workflows table (for tracking approvals)
CREATE TABLE workflow_instances (
  id VARCHAR(255) PRIMARY KEY,
  workflow_id VARCHAR(100) NOT NULL,
  entity_type VARCHAR(50),
  entity_id VARCHAR(255),
  status VARCHAR(50) DEFAULT 'pending',
  current_step VARCHAR(100),
  context JSONB,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  completed_at TIMESTAMP
);

-- Audit log
CREATE TABLE audit_log (
  id SERIAL PRIMARY KEY,
  workflow_id VARCHAR(100),
  entity_type VARCHAR(50),
  entity_id VARCHAR(255),
  action VARCHAR(100),
  actor VARCHAR(100),
  details JSONB,
  timestamp TIMESTAMP DEFAULT NOW()
);
```

### 1.2 Environment Configuration

Create a `.env` file:

```env
# AI Configuration
AI_PROVIDER=anthropic  # or openai
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
AI_MODEL=claude-3-5-sonnet-20241022

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/homeops

# Email (Gmail)
GMAIL_CLIENT_ID=your_client_id
GMAIL_CLIENT_SECRET=your_client_secret
GMAIL_REFRESH_TOKEN=your_refresh_token

# Calendar (Google)
GOOGLE_CALENDAR_CLIENT_ID=your_client_id
GOOGLE_CALENDAR_CLIENT_SECRET=your_client_secret
GOOGLE_CALENDAR_REFRESH_TOKEN=your_refresh_token

# Task Management (Notion)
NOTION_API_KEY=your_notion_key
NOTION_DATABASE_ID=your_database_id

# SMS (Twilio)
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890

# Notifications
USER_EMAIL=luke@example.com
USER_PHONE=+1234567890
LUCY_EMAIL=lucy@example.com
LUCY_PHONE=+1234567890

# Application
APP_URL=https://your-domain.com
WEBHOOK_SECRET=your_webhook_secret
JWT_SECRET=your_jwt_secret

# Phase Configuration
CURRENT_PHASE=phase1_shadow
SPENDING_THRESHOLD=500
```

---

## Step 2: Implement Core Components

### 2.1 AI Agent Core

```typescript
// src/agents/homeOpsAgent.ts
import Anthropic from '@anthropic-ai/sdk';
import { readFile } from 'fs/promises';
import { TaskOwnershipDecisionTree } from '../config/agents/decision-tree';

export class HomeOpsAgent {
  private client: Anthropic;
  private systemPrompt: string;
  private decisionTree: TaskOwnershipDecisionTree;

  constructor(config: AgentConfig) {
    this.client = new Anthropic({
      apiKey: process.env.ANTHROPIC_API_KEY,
    });
    this.loadSystemPrompt();
    this.decisionTree = new TaskOwnershipDecisionTree(config.decisionContext);
  }

  async loadSystemPrompt() {
    this.systemPrompt = await readFile(
      './config/agents/home-ops-agent-prompt.md',
      'utf-8'
    );
  }

  async processInput(input: string, context: any) {
    const response = await this.client.messages.create({
      model: 'claude-3-5-sonnet-20241022',
      max_tokens: 4096,
      system: this.systemPrompt,
      messages: [
        {
          role: 'user',
          content: this.buildPrompt(input, context),
        },
      ],
    });

    return this.parseAgentOutput(response.content);
  }

  private buildPrompt(input: string, context: any): string {
    return `
Context:
- Current date: ${new Date().toISOString()}
- Current phase: ${context.currentPhase}
- User: ${context.userName}

Recent events:
${JSON.stringify(context.recentEvents, null, 2)}

Pending tasks:
${JSON.stringify(context.pendingTasks, null, 2)}

Input:
${input}

Please analyze this input and provide your response in the standard JSON format.
    `;
  }

  private parseAgentOutput(content: any): AgentOutput {
    // Extract JSON from response
    const jsonMatch = content[0].text.match(/```json\n([\s\S]*?)\n```/);
    if (jsonMatch) {
      return JSON.parse(jsonMatch[1]);
    }
    throw new Error('Failed to parse agent output');
  }
}
```

### 2.2 Email Parser

```typescript
// src/integrations/emailParser.ts
import { gmail_v1, google } from 'googleapis';

export class EmailParser {
  private gmail: gmail_v1.Gmail;

  constructor() {
    const auth = new google.auth.OAuth2(
      process.env.GMAIL_CLIENT_ID,
      process.env.GMAIL_CLIENT_SECRET
    );
    auth.setCredentials({
      refresh_token: process.env.GMAIL_REFRESH_TOKEN,
    });
    this.gmail = google.gmail({ version: 'v1', auth });
  }

  async fetchUnprocessedEmails(): Promise<Email[]> {
    const response = await this.gmail.users.messages.list({
      userId: 'me',
      labelIds: ['INBOX'],
      q: 'is:unread -label:processed',
    });

    const messages = response.data.messages || [];
    const emails = await Promise.all(
      messages.map((msg) => this.fetchEmailDetails(msg.id!))
    );

    return emails;
  }

  private async fetchEmailDetails(messageId: string): Promise<Email> {
    const response = await this.gmail.users.messages.get({
      userId: 'me',
      id: messageId,
      format: 'full',
    });

    const headers = response.data.payload?.headers || [];
    const subject = headers.find((h) => h.name === 'Subject')?.value || '';
    const from = headers.find((h) => h.name === 'From')?.value || '';
    const date = headers.find((h) => h.name === 'Date')?.value || '';

    const body = this.extractBody(response.data.payload);

    return {
      id: messageId,
      subject,
      from,
      date: new Date(date),
      body,
    };
  }

  private extractBody(payload: any): string {
    if (payload.body?.data) {
      return Buffer.from(payload.body.data, 'base64').toString('utf-8');
    }
    if (payload.parts) {
      for (const part of payload.parts) {
        if (part.mimeType === 'text/plain' || part.mimeType === 'text/html') {
          return Buffer.from(part.body.data, 'base64').toString('utf-8');
        }
      }
    }
    return '';
  }

  async markAsProcessed(messageId: string): Promise<void> {
    await this.gmail.users.messages.modify({
      userId: 'me',
      id: messageId,
      requestBody: {
        addLabelIds: ['processed'],
      },
    });
  }
}
```

### 2.3 Workflow Engine

```typescript
// src/workflows/workflowEngine.ts
import { readFile } from 'fs/promises';

export class WorkflowEngine {
  async executeWorkflow(
    workflowId: string,
    context: any
  ): Promise<WorkflowResult> {
    const workflow = await this.loadWorkflow(workflowId);
    const instance = await this.createWorkflowInstance(workflow, context);

    return this.executeSteps(workflow, instance, context);
  }

  private async loadWorkflow(workflowId: string): Promise<Workflow> {
    const content = await readFile(
      `./config/workflows/${workflowId}.json`,
      'utf-8'
    );
    return JSON.parse(content);
  }

  private async createWorkflowInstance(
    workflow: Workflow,
    context: any
  ): Promise<string> {
    // Save to database
    const instance = {
      id: generateId(),
      workflow_id: workflow.workflow.id,
      status: 'pending',
      current_step: workflow.steps[0].id,
      context: context,
      created_at: new Date(),
    };

    await db.workflow_instances.insert(instance);
    return instance.id;
  }

  private async executeSteps(
    workflow: Workflow,
    instanceId: string,
    context: any
  ): Promise<WorkflowResult> {
    let currentStep = workflow.steps[0];

    while (currentStep) {
      const result = await this.executeStep(currentStep, context);

      if (currentStep.wait_for_response) {
        // Pause execution, will resume on user response
        await this.updateWorkflowInstance(instanceId, {
          status: 'waiting',
          current_step: currentStep.id,
        });
        return { status: 'waiting', instanceId };
      }

      currentStep = this.getNextStep(workflow, currentStep, result);
    }

    await this.updateWorkflowInstance(instanceId, {
      status: 'completed',
      completed_at: new Date(),
    });

    return { status: 'completed', instanceId };
  }

  private async executeStep(step: WorkflowStep, context: any): Promise<any> {
    switch (step.type) {
      case 'notification':
        return this.sendNotification(step, context);
      case 'action':
        return this.executeAction(step, context);
      case 'ai_action':
        return this.executeAIAction(step, context);
      case 'conditional':
        return this.evaluateCondition(step, context);
      default:
        throw new Error(`Unknown step type: ${step.type}`);
    }
  }

  // Implement other methods...
}
```

---

## Step 3: Set Up Integrations

### 3.1 Google Calendar Integration

```typescript
// src/integrations/calendarIntegration.ts
import { google } from 'googleapis';

export class CalendarIntegration {
  private calendar: any;

  constructor() {
    const auth = new google.auth.OAuth2(
      process.env.GOOGLE_CALENDAR_CLIENT_ID,
      process.env.GOOGLE_CALENDAR_CLIENT_SECRET
    );
    auth.setCredentials({
      refresh_token: process.env.GOOGLE_CALENDAR_REFRESH_TOKEN,
    });
    this.calendar = google.calendar({ version: 'v3', auth });
  }

  async getEvents(startDate: Date, endDate: Date): Promise<Event[]> {
    const response = await this.calendar.events.list({
      calendarId: 'primary',
      timeMin: startDate.toISOString(),
      timeMax: endDate.toISOString(),
      singleEvents: true,
      orderBy: 'startTime',
    });

    return response.data.items || [];
  }

  async createEvent(event: Event): Promise<string> {
    const response = await this.calendar.events.insert({
      calendarId: 'primary',
      requestBody: {
        summary: event.title,
        description: event.description,
        start: {
          dateTime: event.dateTime,
          timeZone: 'America/Los_Angeles',
        },
        end: {
          dateTime: event.endDateTime,
          timeZone: 'America/Los_Angeles',
        },
        location: event.location?.address,
        attendees: event.attendees?.map((id) => ({ email: id })),
      },
    });

    return response.data.id!;
  }

  async detectConflicts(events: Event[]): Promise<Conflict[]> {
    // Implementation for conflict detection
    const conflicts: Conflict[] = [];

    for (let i = 0; i < events.length; i++) {
      for (let j = i + 1; j < events.length; j++) {
        if (this.eventsOverlap(events[i], events[j])) {
          conflicts.push({
            type: 'Schedule',
            affectedEvents: [events[i].id, events[j].id],
            description: `${events[i].title} conflicts with ${events[j].title}`,
          });
        }
      }
    }

    return conflicts;
  }

  private eventsOverlap(event1: Event, event2: Event): boolean {
    const start1 = new Date(event1.dateTime);
    const end1 = new Date(event1.endDateTime);
    const start2 = new Date(event2.dateTime);
    const end2 = new Date(event2.endDateTime);

    return start1 < end2 && start2 < end1;
  }
}
```

### 3.2 Notion Integration

```typescript
// src/integrations/notionIntegration.ts
import { Client } from '@notionhq/client';

export class NotionIntegration {
  private notion: Client;

  constructor() {
    this.notion = new Client({ auth: process.env.NOTION_API_KEY });
  }

  async createTask(task: Task): Promise<string> {
    const response = await this.notion.pages.create({
      parent: { database_id: process.env.NOTION_DATABASE_ID! },
      properties: {
        Title: { title: [{ text: { content: task.title } }] },
        Owner: { select: { name: task.owner } },
        'Due Date': { date: { start: task.dueDate } },
        Priority: { select: { name: task.priority } },
        Category: { select: { name: task.category } },
        Status: { select: { name: task.status } },
      },
    });

    return response.id;
  }

  async updateTask(taskId: string, updates: Partial<Task>): Promise<void> {
    await this.notion.pages.update({
      page_id: taskId,
      properties: {
        // Map updates to Notion properties
        ...(updates.status && {
          Status: { select: { name: updates.status } },
        }),
        // ... other fields
      },
    });
  }
}
```

---

## Step 4: Deploy & Configure

### 4.1 Deploy Application

```bash
# Build the application
npm run build

# Deploy to your hosting provider (example: AWS)
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
docker build -t homeops-agent .
docker tag homeops-agent:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/homeops-agent:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/homeops-agent:latest

# Update ECS service
aws ecs update-service --cluster homeops --service agent --force-new-deployment
```

### 4.2 Set Up Scheduled Jobs

```yaml
# k8s/cronjobs.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: email-processor
spec:
  schedule: "*/5 * * * *"  # Every 5 minutes
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: processor
            image: homeops-agent:latest
            command: ["node", "dist/jobs/processEmails.js"]
---
apiVersion: batch/v1
kind: CronJob
metadata:
  name: daily-brief
spec:
  schedule: "0 7 * * *"  # 7 AM daily
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: brief
            image: homeops-agent:latest
            command: ["node", "dist/jobs/sendDailyBrief.js"]
```

---

## Step 5: Initial Setup & Training

### 5.1 First-Time Setup

1. **Import Initial Data**
   ```bash
   npm run setup:import-vendors
   npm run setup:import-contacts
   npm run setup:configure-vip-list
   ```

2. **Configure Preferences**
   - Set working hours
   - Define approval thresholds
   - Set notification preferences
   - Configure calendar access

3. **Test Workflows**
   - Send test email
   - Create test task
   - Trigger test approval

### 5.2 Training Period (Phase 1)

**Week 1:**
- Review all AI outputs
- Correct categorization errors
- Build preference profile
- Document feedback patterns

**Week 2:**
- Fine-tune system prompt based on corrections
- Adjust approval thresholds
- Test conflict detection
- Review metrics

**Week 3:**
- Finalize Phase 1 configuration
- Measure time savings
- Gather user satisfaction
- Prepare for Phase 2

---

## Monitoring & Maintenance

### Key Metrics Dashboard

```typescript
// Example metrics to track
const metrics = {
  daily: {
    emails_processed: 0,
    tasks_created: 0,
    conflicts_detected: 0,
    approvals_sent: 0,
    time_saved_minutes: 0,
  },
  quality: {
    categorization_accuracy: 0,
    approval_rate: 0,
    error_rate: 0,
    response_time_minutes: 0,
  },
  user_satisfaction: {
    review_time_minutes: 0,
    corrections_count: 0,
    satisfaction_score: 0,
  },
};
```

### Health Checks

- API response times
- Integration connectivity
- Workflow completion rates
- Error rates by category

---

## Troubleshooting

### Common Issues

**AI not parsing emails correctly**
- Check system prompt configuration
- Verify email format extraction
- Review training examples

**Approval notifications not sending**
- Verify Twilio/email credentials
- Check webhook endpoints
- Review notification queue

**Calendar conflicts not detected**
- Verify calendar API access
- Check event fetching logic
- Review conflict detection algorithm

---

## Next Steps

Once Phase 1 is successful:
1. Review [ROLLOUT_PLAN.md](ROLLOUT_PLAN.md) for Phase 2 transition
2. Enable autonomous task creation
3. Gradually expand AI autonomy
4. Monitor metrics closely

---

**Questions or Issues?**
- Review full design: [HOME_OPS_AGENT_DESIGN.md](HOME_OPS_AGENT_DESIGN.md)
- Check system prompt: [config/agents/home-ops-agent-prompt.md](config/agents/home-ops-agent-prompt.md)
- Review workflows: [config/workflows/](config/workflows/)
