/**
 * Home Ops Agent Decision Tree
 * Determines task ownership and approval requirements based on task characteristics
 */

export interface TaskCharacteristics {
  title: string;
  description?: string;
  isRecurring: boolean;
  isRepeatable: boolean;
  estimatedImpact: number; // in dollars
  requiresSpecialist: boolean;
  specialistType?: 'legal' | 'tax' | 'medical' | 'insurance' | 'finance';
  isRelationshipSensitive: boolean;
  isStrategic: boolean;
  estimatedMinutes: number;
  category: string;
  involvesBrand: boolean;
  involvesCommunication: boolean;
  communicationTarget?: 'vip' | 'vendor' | 'routine' | 'internal';
}

export interface DecisionResult {
  owner: 'Luke' | 'Lucy' | 'AI' | 'HumanAssistant' | 'Specialist';
  requiresApproval: boolean;
  approvalReason?: string;
  autonomyLevel: 'none' | 'limited' | 'full';
  escalationPath: string;
  rationale: string;
}

export interface DecisionContext {
  currentPhase: 'phase1_shadow' | 'phase2_controlled' | 'phase3_selective';
  spendingThreshold: number;
  vipList: string[];
  customRules?: DecisionRule[];
}

export interface DecisionRule {
  id: string;
  condition: (task: TaskCharacteristics) => boolean;
  result: Partial<DecisionResult>;
  priority: number;
}

/**
 * Main decision tree implementation
 */
export class TaskOwnershipDecisionTree {
  constructor(private context: DecisionContext) {}

  /**
   * Determine ownership and approval for a task
   */
  decide(task: TaskCharacteristics): DecisionResult {
    // Apply custom rules first (highest priority)
    const customResult = this.applyCustomRules(task);
    if (customResult) return customResult;

    // Step 1: Is it recurring or repeatable?
    if (task.isRecurring || task.isRepeatable) {
      return this.handleRecurringTask(task);
    }

    // Step 2: Is it about relationships or vision?
    if (task.isRelationshipSensitive || task.isStrategic || task.involvesBrand) {
      return this.handleRelationshipOrVisionTask(task);
    }

    // Step 3: Does it require a licensed specialist?
    if (task.requiresSpecialist) {
      return this.handleSpecialistTask(task);
    }

    // Step 4: Time and leverage check
    return this.handleTimeAndLeverageCheck(task);
  }

  /**
   * Apply custom user-defined rules
   */
  private applyCustomRules(task: TaskCharacteristics): DecisionResult | null {
    if (!this.context.customRules) return null;

    const sortedRules = [...this.context.customRules].sort((a, b) => b.priority - a.priority);

    for (const rule of sortedRules) {
      if (rule.condition(task)) {
        return {
          owner: rule.result.owner || 'AI',
          requiresApproval: rule.result.requiresApproval !== undefined ? rule.result.requiresApproval : true,
          approvalReason: rule.result.approvalReason || `Custom rule: ${rule.id}`,
          autonomyLevel: rule.result.autonomyLevel || 'limited',
          escalationPath: rule.result.escalationPath || 'User',
          rationale: `Matched custom rule: ${rule.id}. ${rule.result.rationale || ''}`,
        };
      }
    }

    return null;
  }

  /**
   * Handle recurring or repeatable tasks
   */
  private handleRecurringTask(task: TaskCharacteristics): DecisionResult {
    const phaseAutonomy = this.getPhaseAutonomy();

    if (phaseAutonomy === 'none') {
      return {
        owner: 'AI',
        requiresApproval: true,
        approvalReason: 'Phase 1: All tasks require approval',
        autonomyLevel: 'none',
        escalationPath: 'User',
        rationale: 'Recurring/repeatable task, but in Phase 1 shadow mode',
      };
    }

    // Check if spending is involved
    if (task.estimatedImpact > this.context.spendingThreshold) {
      return {
        owner: 'AI',
        requiresApproval: true,
        approvalReason: `Spending exceeds threshold ($${this.context.spendingThreshold})`,
        autonomyLevel: 'limited',
        escalationPath: 'User',
        rationale: 'Recurring task but requires approval due to spending amount',
      };
    }

    // Phase 3: Full autonomy for recurring tasks
    if (phaseAutonomy === 'full') {
      return {
        owner: 'AI',
        requiresApproval: false,
        autonomyLevel: 'full',
        escalationPath: 'User notification only',
        rationale: 'Recurring/repeatable task with full autonomy in Phase 3',
      };
    }

    // Phase 2: Limited autonomy
    return {
      owner: 'AI',
      requiresApproval: false,
      autonomyLevel: 'limited',
      escalationPath: 'User notification',
      rationale: 'Recurring/repeatable task with controlled autonomy in Phase 2',
    };
  }

  /**
   * Handle relationship-sensitive or strategic tasks
   */
  private handleRelationshipOrVisionTask(task: TaskCharacteristics): DecisionResult {
    // Check if it's operational vs. truly strategic
    const isOperational = this.isOperationalTask(task);

    if (isOperational) {
      return {
        owner: 'AI',
        requiresApproval: true,
        approvalReason: 'Operational task with strategic implications',
        autonomyLevel: 'limited',
        escalationPath: 'User for final approval',
        rationale: 'AI can research and prepare, but user makes final decision',
      };
    }

    // High-stakes relationship/creative decision
    return {
      owner: this.determineUserOwner(task),
      requiresApproval: true,
      approvalReason: 'High-stakes relationship, reputation, or creative decision',
      autonomyLevel: 'none',
      escalationPath: 'User owns decision',
      rationale: 'Strategic decision requiring user ownership. AI provides support.',
    };
  }

  /**
   * Handle tasks requiring licensed specialists
   */
  private handleSpecialistTask(task: TaskCharacteristics): DecisionResult {
    return {
      owner: 'Specialist',
      requiresApproval: true,
      approvalReason: `Requires ${task.specialistType || 'licensed'} specialist`,
      autonomyLevel: 'limited',
      escalationPath: 'Specialist, AI coordinates',
      rationale: `${task.specialistType || 'Specialist'} owns decision. AI handles scheduling, paperwork, and follow-ups.`,
    };
  }

  /**
   * Handle time and leverage check
   */
  private handleTimeAndLeverageCheck(task: TaskCharacteristics): DecisionResult {
    const phaseAutonomy = this.getPhaseAutonomy();

    // Quick task (<15 min) and not strategic
    if (task.estimatedMinutes < 15 && !task.isStrategic) {
      if (phaseAutonomy === 'none') {
        return {
          owner: 'AI',
          requiresApproval: true,
          approvalReason: 'Phase 1: All tasks require approval',
          autonomyLevel: 'none',
          escalationPath: 'User',
          rationale: 'Quick task but in shadow mode',
        };
      }

      return {
        owner: 'AI',
        requiresApproval: phaseAutonomy === 'limited',
        approvalReason: phaseAutonomy === 'limited' ? 'Phase 2: Notification required' : undefined,
        autonomyLevel: phaseAutonomy,
        escalationPath: phaseAutonomy === 'full' ? 'User notification only' : 'User approval',
        rationale: 'Quick, non-strategic task suitable for AI execution',
      };
    }

    // High-impact task (>$10k or brand IP or key relationships)
    if (
      task.estimatedImpact > 10000 ||
      task.involvesBrand ||
      (task.involvesCommunication && task.communicationTarget === 'vip')
    ) {
      return {
        owner: this.determineUserOwner(task),
        requiresApproval: true,
        approvalReason: 'High impact: >$10k, brand IP, or key relationships involved',
        autonomyLevel: 'limited',
        escalationPath: 'User decides, AI executes',
        rationale: 'High-impact task requiring user decision with AI execution support',
      };
    }

    // Default: AI with approval based on phase
    return {
      owner: 'AI',
      requiresApproval: phaseAutonomy !== 'full',
      approvalReason: phaseAutonomy !== 'full' ? 'Standard approval process' : undefined,
      autonomyLevel: phaseAutonomy,
      escalationPath: 'User',
      rationale: 'Standard task with approval based on current phase',
    };
  }

  /**
   * Determine if a task is operational vs. truly strategic
   */
  private isOperationalTask(task: TaskCharacteristics): boolean {
    const operationalKeywords = [
      'research',
      'gather',
      'compare',
      'quote',
      'option',
      'schedule',
      'coordinate',
      'organize',
    ];

    const titleLower = task.title.toLowerCase();
    const descLower = (task.description || '').toLowerCase();

    return operationalKeywords.some(
      (keyword) => titleLower.includes(keyword) || descLower.includes(keyword)
    );
  }

  /**
   * Determine which user should own a task
   */
  private determineUserOwner(task: TaskCharacteristics): 'Luke' | 'Lucy' {
    // This is a simplified heuristic. In practice, this would use more context
    // about task category, historical patterns, or explicit rules.

    const lucyCategories = ['ciao_lucia', 'social', 'kids'];
    const lukeCategories = ['business_support', 'travel', 'home_maintenance'];

    if (lucyCategories.includes(task.category)) return 'Lucy';
    if (lukeCategories.includes(task.category)) return 'Luke';

    // Default to Luke for ambiguous cases
    return 'Luke';
  }

  /**
   * Get autonomy level based on current phase
   */
  private getPhaseAutonomy(): 'none' | 'limited' | 'full' {
    switch (this.context.currentPhase) {
      case 'phase1_shadow':
        return 'none';
      case 'phase2_controlled':
        return 'limited';
      case 'phase3_selective':
        return 'full';
    }
  }
}

/**
 * Approval checker - determines if a specific action requires approval
 */
export class ApprovalChecker {
  constructor(private context: DecisionContext) {}

  /**
   * Check if communication requires approval
   */
  requiresCommunicationApproval(
    recipientEmail: string,
    messageType: 'email' | 'sms' | 'calendar_invite',
    category: string
  ): { required: boolean; reason?: string } {
    // Phase 1: All communication requires approval
    if (this.context.currentPhase === 'phase1_shadow') {
      return { required: true, reason: 'Phase 1: All communications require approval' };
    }

    // VIP check
    if (this.context.vipList.includes(recipientEmail)) {
      return { required: true, reason: 'Recipient is on VIP list' };
    }

    // Phase 2: Only drafts, no sending
    if (this.context.currentPhase === 'phase2_controlled') {
      if (messageType === 'email' || messageType === 'sms') {
        return { required: true, reason: 'Phase 2: Email/SMS require approval' };
      }
    }

    // Phase 3: Selective approval
    const autoApproveCategories = ['kids_rsvp', 'routine_appointments', 'vendor_scheduling'];
    if (autoApproveCategories.includes(category)) {
      return { required: false };
    }

    return { required: true, reason: 'Default: approval required for external communication' };
  }

  /**
   * Check if spending requires approval
   */
  requiresSpendingApproval(
    amount: number,
    category: string
  ): { required: boolean; reason?: string } {
    // Always require approval in Phase 1
    if (this.context.currentPhase === 'phase1_shadow') {
      return { required: true, reason: 'Phase 1: All spending requires approval' };
    }

    // Above threshold always requires approval
    if (amount > this.context.spendingThreshold) {
      return {
        required: true,
        reason: `Amount exceeds threshold ($${this.context.spendingThreshold})`,
      };
    }

    // Phase 3: Auto-approve small routine purchases
    if (this.context.currentPhase === 'phase3_selective') {
      const autoApproveCategories = ['inventory_orders', 'routine_maintenance'];
      if (autoApproveCategories.includes(category) && amount <= 200) {
        return { required: false };
      }
    }

    return { required: true, reason: 'Standard spending approval' };
  }

  /**
   * Check if schedule change requires approval
   */
  requiresScheduleChangeApproval(
    eventPriority: 'Critical' | 'High' | 'Medium' | 'Low',
    changeType: 'reschedule' | 'cancel' | 'modify_attendees'
  ): { required: boolean; reason?: string } {
    // Phase 1: All changes require approval
    if (this.context.currentPhase === 'phase1_shadow') {
      return { required: true, reason: 'Phase 1: All schedule changes require approval' };
    }

    // High-priority events always require approval
    if (eventPriority === 'Critical' || eventPriority === 'High') {
      return { required: true, reason: 'High-priority event' };
    }

    // Cancellations always require approval
    if (changeType === 'cancel') {
      return { required: true, reason: 'Cancellations always require approval' };
    }

    // Phase 3: Low-priority rescheduling can be autonomous
    if (this.context.currentPhase === 'phase3_selective' && changeType === 'reschedule') {
      return { required: false };
    }

    return { required: true, reason: 'Default: schedule changes require approval' };
  }
}

/**
 * Example usage and test cases
 */
export function runDecisionTreeExamples() {
  const context: DecisionContext = {
    currentPhase: 'phase2_controlled',
    spendingThreshold: 500,
    vipList: ['investor@example.com', 'lawyer@example.com'],
  };

  const decisionTree = new TaskOwnershipDecisionTree(context);
  const approvalChecker = new ApprovalChecker(context);

  // Example 1: Weekly calendar sync
  const recurringTask: TaskCharacteristics = {
    title: 'Sync weekly family calendar',
    isRecurring: true,
    isRepeatable: true,
    estimatedImpact: 0,
    requiresSpecialist: false,
    isRelationshipSensitive: false,
    isStrategic: false,
    estimatedMinutes: 10,
    category: 'calendar',
    involvesBrand: false,
    involvesCommunication: false,
  };

  console.log('Example 1 - Weekly Calendar Sync:');
  console.log(decisionTree.decide(recurringTask));

  // Example 2: Investor email
  const vipCommunication: TaskCharacteristics = {
    title: 'Reply to investor about Q4 plans',
    isRecurring: false,
    isRepeatable: false,
    estimatedImpact: 50000,
    requiresSpecialist: false,
    isRelationshipSensitive: true,
    isStrategic: true,
    estimatedMinutes: 30,
    category: 'business_support',
    involvesBrand: true,
    involvesCommunication: true,
    communicationTarget: 'vip',
  };

  console.log('\nExample 2 - VIP Communication:');
  console.log(decisionTree.decide(vipCommunication));

  // Example 3: Tax filing
  const specialistTask: TaskCharacteristics = {
    title: 'File quarterly business taxes',
    isRecurring: true,
    isRepeatable: true,
    estimatedImpact: 0,
    requiresSpecialist: true,
    specialistType: 'tax',
    isRelationshipSensitive: false,
    isStrategic: false,
    estimatedMinutes: 120,
    category: 'business_support',
    involvesBrand: false,
    involvesCommunication: false,
  };

  console.log('\nExample 3 - Tax Filing:');
  console.log(decisionTree.decide(specialistTask));

  // Example 4: Quick routine task
  const quickTask: TaskCharacteristics = {
    title: 'Confirm tennis court booking',
    isRecurring: false,
    isRepeatable: true,
    estimatedImpact: 50,
    requiresSpecialist: false,
    isRelationshipSensitive: false,
    isStrategic: false,
    estimatedMinutes: 5,
    category: 'activities',
    involvesBrand: false,
    involvesCommunication: true,
    communicationTarget: 'routine',
  };

  console.log('\nExample 4 - Quick Routine Task:');
  console.log(decisionTree.decide(quickTask));

  // Approval checks
  console.log('\n--- Approval Checks ---');
  console.log(
    'VIP Email:',
    approvalChecker.requiresCommunicationApproval('investor@example.com', 'email', 'business')
  );
  console.log(
    'Routine Email:',
    approvalChecker.requiresCommunicationApproval('tennis@club.com', 'email', 'kids_rsvp')
  );
  console.log('$600 Purchase:', approvalChecker.requiresSpendingApproval(600, 'home_maintenance'));
  console.log('$150 Inventory:', approvalChecker.requiresSpendingApproval(150, 'inventory_orders'));
  console.log(
    'Cancel High Priority:',
    approvalChecker.requiresScheduleChangeApproval('High', 'cancel')
  );
}

export default TaskOwnershipDecisionTree;
