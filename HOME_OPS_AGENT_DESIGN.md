# Home Operations Agent - "Wonderland" Design Document

## Executive Summary

The Home Ops Agent is an AI-powered assistant designed to manage family logistics, home operations, and light business-adjacent admin for Luke Reyes and Lucy. The agent follows a structured, machine-readable approach to task management while maintaining strict boundaries around financial, legal, and medical decisions.

## Core Philosophy

The Home Ops Agent operates on three fundamental principles:

1. **Structure Over Chaos**: Convert unstructured information into actionable, tracked tasks
2. **Transparency**: Always provide clear ownership, deadlines, and priorities
3. **Human Oversight**: Flag conflicts and uncertainties rather than making assumptions

## Agent Architecture

### 1. Agent Identity & Mission

**Name**: Home Operations Assistant

**Primary Mission**: Manage family logistics, home operations, and light business-adjacent admin while keeping Luke and Lucy focused on high-value activities: kids, creative work, and strategic decisions.

**Core Constraints**:
- NEVER make financial, legal, or medical decisions
- ALWAYS summarize, prioritize, and propose clear options
- ALWAYS assign ownership (Luke / Lucy / AI / Human Assistant)
- ALWAYS propose due dates and priorities

### 2. Output Contract

All agent responses follow a strict machine-readable format:

```json
{
  "tasks": [
    {
      "id": "string",
      "title": "string",
      "description": "string",
      "owner": "Luke | Lucy | AI | HumanAssistant",
      "dueDate": "ISO-8601 date",
      "priority": "Critical | High | Medium | Low",
      "category": "string",
      "status": "Draft | Pending Approval | Approved | In Progress | Completed",
      "dependencies": ["task-id-1", "task-id-2"],
      "estimatedMinutes": "number",
      "requiredApproval": "boolean",
      "approvalReason": "string | null"
    }
  ],
  "summary": "string - Brief executive summary of the situation",
  "questions": [
    {
      "question": "string",
      "context": "string",
      "urgency": "Immediate | This Week | This Month",
      "blockedTasks": ["task-id-1"]
    }
  ],
  "conflicts": [
    {
      "type": "Schedule | Resource | Priority",
      "description": "string",
      "affectedTasks": ["task-id-1", "task-id-2"],
      "suggestedResolution": "string"
    }
  ],
  "updates": [
    {
      "entity": "Person | Vendor | Event | Task | Project",
      "entityId": "string",
      "updateType": "Create | Update | Delete",
      "changes": "object"
    }
  ]
}
```

## Decision Tree: Task Ownership & Autonomy

### Step 1: Is it Recurring or Repeatable?

**YES → Default to Assistant**
- Weekly calendar syncs
- Recurring kids' activities
- Bill reminders
- Pantry stock checks
- Vendor maintenance
- Previously executed travel patterns

**NO → Go to Step 2**

### Step 2: Is it About Relationships or Vision?

**High-Stakes Relationship/Reputation/Creative?**
- Investor negotiations
- Core brand decisions (Rita's, Café Esca, Ciao Lucia)
- Sensitive conflict resolution
→ **Luke or Lucy own**, assistant supports with prep

**Operational or Informational?**
- Getting quotes
- Gathering options
- Researching schools/camps/programs
- Summarizing choices
→ **Assistant owns**, final call by Luke/Lucy

### Step 3: Does it Require a Licensed Specialist?

**Legal, Tax, Medical, Insurance, Complex Finance**
→ **Specialist owns**, assistant coordinates
- Scheduling
- Paperwork management
- Follow-ups
- Document storage

### Step 4: Time and Leverage Check

**< 15 minutes AND not strategic** → **Assistant owns**

**Impacts > $10k, brand IP, or key relationships** → **Luke/Lucy decide**
- Assistant prepares info
- Assistant executes follow-through

### Default Rule

> "If it's repeatable, clerical, logistical, or less than a $10k decision, you own it by default unless I pull it back."

## Human-in-the-Loop Framework

### AI Can Do Autonomously:
- Create and update tasks
- Draft emails and texts
- Propose time slots for meetings
- Schedule low-stakes appointments (tennis, haircuts, dentist)

### AI Must Get Approval Before:
- Confirming any spend above threshold ($500 default, configurable)
- Replying to VIPs, legal/financial contacts, press, investors
- Changing flights, hotels, major travel
- Making commitments on behalf of Luke or Lucy
- Canceling or rescheduling important meetings

### Approval Workflow

```
AI drafts action → Sends notification with:
  - Subject/Context
  - Proposed action
  - "Approve / Edit / Cancel" options

User clicks "Approve" → Automation executes action
User clicks "Edit" → Returns to AI with feedback
User clicks "Cancel" → Task marked cancelled with reason
```

## Domain Coverage

### 1. Family Calendar & Time Management
- **Master Calendar Maintenance**
  - Kids' school, activities, appointments
  - Family trips, visitors, events
  - House maintenance and vendor visits

- **Weekly Command Center**
  - Monday AM snapshot: key events, pickups/drop-offs, meals, conflicts
  - Weekly 10-15 minute huddle

- **Conflict Detection**
  - Automatically flag overlapping commitments
  - Suggest resolutions based on priority

### 2. Kids' Logistics & Admin
- School forms, sign-ups, tuition reminders
- Activities: enrollment, schedules, payment, equipment needs
- Medical: scheduling, reminders, vaccine tracking
- Social: RSVPs, gift purchasing/wrapping, party logistics

### 3. Home Operations & Vendors
- **Vendor Directory Maintenance**
  - All vendors with contacts, rates, frequency
  - Last visit and next scheduled visit
  - Service history and notes

- **Scheduling & Supervision**
  - Regular cleanings, maintenance, repairs
  - Project tracking (e.g., gate project, garage setup)

### 4. Household Inventory & Purchasing
- Standardized shopping lists
- Replenishment system with preferred vendors
- Special event preparation
- Stock monitoring and alerts

### 5. Personal Admin (Luke & Lucy)
- **Inbox Triage**
  - Flag urgent/high-stakes emails
  - Draft simple logistics responses

- **Appointment Management**
  - Doctors, hair, wellness, car service

- **Document Organization**
  - IDs, insurance, warranties, loan docs, travel records

### 6. Travel & Hospitality
- **Pre-Trip**
  - Research and propose options
  - Build day-by-day itineraries
  - Gather confirmations and contacts

- **During Trip**
  - On-call for changes (within agreed hours)

- **Hosting**
  - Guest arrival/departure coordination
  - Room prep checklists
  - Welcome items

### 7. Light Business Support
- Schedule meetings and calls
- Manage calendars where business/family overlap
- Simple project trackers
- Receipt gathering for bookkeeper/CPA

### 8. Lucy/Ciao Lucia Support (Home Overlap)
- Coordinate at-home events (influencer dinners, fittings, shoots)
- Manage invite lists and RSVPs
- Handle packages, samples, messengers, returns

## Data Model

### Core Entities

```typescript
interface Person {
  id: string;
  name: string;
  role: 'Family' | 'Extended Family' | 'Friend' | 'VIP' | 'Contact';
  contactInfo: {
    email?: string;
    phone?: string;
    address?: string;
  };
  relationships: string[]; // IDs of related people
  preferences?: object;
  vipStatus: boolean;
  approvalRequired: boolean; // for communications
}

interface Vendor {
  id: string;
  name: string;
  category: string;
  contactInfo: {
    name: string;
    phone: string;
    email?: string;
  };
  services: string[];
  rate: {
    amount: number;
    frequency: string;
  };
  schedule: {
    frequency: string;
    lastVisit?: string;
    nextVisit?: string;
  };
  notes: string[];
  status: 'Active' | 'Inactive' | 'Archived';
}

interface Event {
  id: string;
  title: string;
  type: 'School' | 'Activity' | 'Social' | 'Medical' | 'Travel' | 'Home' | 'Business';
  dateTime: string;
  duration: number;
  location: string;
  attendees: string[]; // Person IDs
  owner: 'Luke' | 'Lucy' | 'Kids';
  requiresPrep: boolean;
  prepTasks?: string[]; // Task IDs
  conflicts?: string[]; // Event IDs
  priority: 'Critical' | 'High' | 'Medium' | 'Low';
}

interface Task {
  id: string;
  title: string;
  description: string;
  owner: 'Luke' | 'Lucy' | 'AI' | 'HumanAssistant';
  assignee?: string; // Person ID
  dueDate: string;
  priority: 'Critical' | 'High' | 'Medium' | 'Low';
  category: string;
  status: 'Draft' | 'Pending Approval' | 'Approved' | 'In Progress' | 'Completed' | 'Cancelled';
  estimatedMinutes: number;
  dependencies: string[];
  relatedEntity?: {
    type: 'Person' | 'Vendor' | 'Event' | 'Project';
    id: string;
  };
  requiresApproval: boolean;
  approvalReason?: string;
  completedAt?: string;
  createdAt: string;
}

interface Project {
  id: string;
  name: string;
  description: string;
  category: 'Home' | 'Kids' | 'Personal' | 'Business';
  status: 'Planning' | 'In Progress' | 'On Hold' | 'Completed';
  owner: 'Luke' | 'Lucy' | 'Joint';
  startDate?: string;
  targetEndDate?: string;
  tasks: string[]; // Task IDs
  vendors?: string[]; // Vendor IDs
  budget?: {
    estimated: number;
    actual: number;
  };
  notes: string[];
}
```

## Three-Phase Rollout Plan

### Phase 1: Shadow Assistant (Weeks 1-3)

**Objective**: Build trust and train the model on Luke & Lucy's preferences.

**AI Capabilities**:
- Parse emails into tasks
- Send daily and weekly briefs
- Flag conflicts and missing information
- Draft responses (no sending)

**No Autonomy**:
- No auto-sending
- No auto-booking
- No auto-purchasing

**Human Actions**:
- Review all AI outputs
- Correct mistakes
- Note patterns where AI is incorrect
- Approve all proposed tasks

**Success Metrics**:
- 90%+ accuracy on task categorization
- Zero missed critical items
- Reduced time reviewing vs. doing logistics

### Phase 2: Controlled Autonomy (Weeks 4-8)

**Objective**: Allow AI to take action on low-risk items.

**AI Can Now**:
- Auto-create tasks in Notion/Airtable
- Auto-update records (vendor visits, inventory)
- Send calendar invites for approved categories
- Confirm simple appointments (haircuts, tennis)

**Still Requires Approval**:
- All outbound emails to people
- Any financial transactions
- Schedule changes to existing commitments
- New vendor contracts

**Human Actions**:
- Review daily summary of AI actions
- Spot-check automated tasks
- Provide feedback on quality

**Success Metrics**:
- 5+ hours saved per week
- Zero significant errors
- Positive feedback on proactive flagging

### Phase 3: Selective Full Autonomy (Week 9+)

**Objective**: Full automation for pre-approved categories.

**Fully Autonomous Categories**:
- Kids' activity RSVPs
- Basic appointment confirmations
- Routine vendor scheduling (within pre-set time windows)
- Inventory replenishment orders (under $200)
- Calendar sync and conflict resolution

**Approval Still Required**:
- VIP communications
- Travel changes
- Purchases > $500
- New commitments
- Schedule changes to high-priority events

**Success Metrics**:
- 10+ hours saved per week
- Luke and Lucy spending <30 min/day on logistics
- Zero critical mistakes in 4 weeks

## Technical Implementation

### System Prompt Location
`/config/agents/home-ops-agent-prompt.md`

### Configuration Files
- `/config/agents/home-ops-config.json` - Agent settings and thresholds
- `/config/schemas/` - JSON schemas for all entities and outputs
- `/config/workflows/` - Approval workflow templates

### Integration Points
- Email (Gmail API)
- Calendar (Google Calendar API)
- Task Management (Notion/Airtable API)
- Communication (SMS, Email for notifications)

### Monitoring & Logging
- All AI decisions logged with reasoning
- Approval requests tracked
- Error patterns analyzed weekly
- User corrections captured for training

## Key Performance Indicators

### Efficiency Metrics
- Time saved per week (target: 10+ hours by Phase 3)
- Tasks auto-completed vs. requiring approval
- Average time from task creation to completion

### Quality Metrics
- Error rate (target: <2%)
- User correction frequency
- Missed deadline rate (target: 0%)
- Conflict detection accuracy (target: 95%+)

### User Satisfaction
- Weekly review time (target: <30 min/day)
- Number of "pulls" (Luke/Lucy take task back from AI)
- Proactive value adds noted

## Risk Mitigation

### Financial Safeguards
- Hard limits on autonomous spending
- Tiered approval based on amount
- No access to financial accounts (coordination only)

### Relationship Protection
- VIP list maintained and respected
- Tone analysis before sending communications
- Escalation for sensitive topics

### Privacy & Security
- All data encrypted at rest and in transit
- Access controls for sensitive information
- Regular audit logs
- GDPR/CCPA compliance for any external data

## Future Enhancements

- Voice interface for quick updates
- Predictive scheduling based on patterns
- Integration with smart home devices
- Meal planning and recipe suggestions
- Travel optimization (best times, routes, deals)
- Budget tracking and reporting
- Kids' development milestone tracking

---

**Document Version**: 1.0
**Last Updated**: 2025-11-10
**Owner**: Luke Reyes
**Review Frequency**: Monthly during Phase 1-2, Quarterly in Phase 3
