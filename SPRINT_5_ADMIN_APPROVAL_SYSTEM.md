# Sprint 5: Admin Approval System

## 🎯 Objectives
Create an efficient workflow system for admins to review and approve student contributions, AI-generated content, and user-submitted resources with automation and quality controls.

## 📋 Features

### Core Features
1. ✅ Centralized approval queue
2. ✅ Automated workflow routing
3. ✅ Bulk approval/rejection
4. ✅ Content quality scoring
5. ✅ Notification system
6. ✅ Approval history & audit trail
7. ✅ Auto-approval for trusted users
8. ✅ Escalation system

## 🗄️ Database Schema

### ApprovalWorkflow Model
```python
class ApprovalWorkflow(Base):
    __tablename__ = "approval_workflows"
    
    id = UUID (Primary Key)
    
    # What needs approval
    item_type = String  # 'contribution', 'ai_content', 'image', 'chapter'
    item_id = UUID  # Foreign key to the item
    
    # Workflow status
    status = String  # 'pending', 'in_review', 'approved', 'rejected', 'escalated'
    priority = Integer  # 1-5 (5 = highest)
    
    # Assignment
    assigned_to = UUID (Foreign Key to users, nullable)
    assigned_at = DateTime (nullable)
    
    # Submitter info
    submitted_by = UUID (Foreign Key to users)
    submitted_at = DateTime
    
    # Review info
    reviewed_by = UUID (Foreign Key to users, nullable)
    reviewed_at = DateTime (nullable)
    review_notes = Text (nullable)
    
    # Quality scoring
    quality_score = Float (nullable)  # 0-100
    auto_approved = Boolean (default: False)
    
    # Metadata
    created_at = DateTime
    updated_at = DateTime
```

### ApprovalRule Model
```python
class ApprovalRule(Base):
    __tablename__ = "approval_rules"
    
    id = UUID (Primary Key)
    
    # Rule definition
    name = String
    description = Text
    item_type = String  # 'contribution', 'ai_content', etc.
    
    # Conditions (JSON)
    conditions = JSON  # e.g., {"min_quality_score": 80, "user_trust_level": "high"}
    
    # Actions
    action = String  # 'auto_approve', 'auto_reject', 'escalate', 'assign_to'
    action_params = JSON  # e.g., {"assign_to_user_id": "uuid"}
    
    # Status
    is_active = Boolean (default: True)
    priority = Integer  # Rule execution order
    
    created_at = DateTime
    updated_at = DateTime
```

### UserTrustLevel Model
```python
class UserTrustLevel(Base):
    __tablename__ = "user_trust_levels"
    
    id = UUID (Primary Key)
    user_id = UUID (Foreign Key to users)
    
    # Trust metrics
    trust_score = Float  # 0-100
    trust_level = String  # 'new', 'basic', 'trusted', 'expert'
    
    # Contribution stats
    total_submissions = Integer (default: 0)
    approved_submissions = Integer (default: 0)
    rejected_submissions = Integer (default: 0)
    approval_rate = Float  # Percentage
    
    # Quality metrics
    average_quality_score = Float
    average_upvotes = Float
    
    # Auto-approval eligibility
    can_auto_approve = Boolean (default: False)
    auto_approve_types = JSON  # List of item types eligible for auto-approval
    
    # Last updated
    last_calculated = DateTime
    updated_at = DateTime
```

### ApprovalNotification Model
```python
class ApprovalNotification(Base):
    __tablename__ = "approval_notifications"
    
    id = UUID (Primary Key)
    
    # Recipient
    user_id = UUID (Foreign Key to users)
    
    # Notification details
    notification_type = String  # 'approval_needed', 'approved', 'rejected', 'escalated'
    title = String
    message = Text
    
    # Related workflow
    workflow_id = UUID (Foreign Key to approval_workflows)
    
    # Status
    is_read = Boolean (default: False)
    read_at = DateTime (nullable)
    
    created_at = DateTime
```

## 🔧 Backend Implementation

### Phase 1: Models & Schemas

#### 1.1 Create Models
**File**: `/backend/app/models/approval.py`
- ApprovalWorkflow model
- ApprovalRule model
- UserTrustLevel model
- ApprovalNotification model

#### 1.2 Create Schemas
**File**: `/backend/app/schemas/approval.py`
- WorkflowCreate
- WorkflowResponse
- WorkflowListResponse
- WorkflowReview
- RuleCreate
- RuleUpdate
- RuleResponse
- TrustLevelResponse
- NotificationResponse

#### 1.3 Database Migration
```bash
alembic revision --autogenerate -m "Add approval system"
alembic upgrade head
```

### Phase 2: Services

#### 2.1 Approval Workflow Service
**File**: `/backend/app/services/approval_service.py`

Functions:
```python
# Workflow management
create_workflow(item_type, item_id, submitted_by, priority)
get_workflow_by_id(workflow_id)
list_workflows(filters, pagination)
assign_workflow(workflow_id, admin_id)
review_workflow(workflow_id, admin_id, action, notes)
escalate_workflow(workflow_id, reason)

# Bulk operations
bulk_approve(workflow_ids, admin_id)
bulk_reject(workflow_ids, admin_id, reason)
bulk_assign(workflow_ids, admin_id)

# Quality scoring
calculate_quality_score(item_type, item_id)
update_quality_score(workflow_id, score)

# Auto-approval
check_auto_approval_eligibility(item_type, item_id, user_id)
apply_approval_rules(workflow_id)
```

#### 2.2 Trust Level Service
**File**: `/backend/app/services/trust_service.py`

Functions:
```python
# Trust calculation
calculate_user_trust_score(user_id)
update_user_trust_level(user_id)
get_user_trust_level(user_id)

# Auto-approval eligibility
check_auto_approve_eligibility(user_id, item_type)
grant_auto_approve_permission(user_id, item_types)
revoke_auto_approve_permission(user_id, item_types)

# Trust metrics
get_user_submission_stats(user_id)
update_submission_stats(user_id, approved)
```

#### 2.3 Notification Service
**File**: `/backend/app/services/notification_service.py`

Functions:
```python
# Notifications
create_notification(user_id, type, title, message, workflow_id)
get_user_notifications(user_id, unread_only)
mark_notification_read(notification_id)
mark_all_notifications_read(user_id)
delete_notification(notification_id)

# Bulk notifications
notify_admins_new_submission(workflow_id)
notify_user_approval_decision(workflow_id, decision)
notify_escalation(workflow_id)
```

#### 2.4 Rule Engine Service
**File**: `/backend/app/services/rule_engine.py`

Functions:
```python
# Rule management
create_rule(name, description, item_type, conditions, action)
update_rule(rule_id, updates)
delete_rule(rule_id)
list_rules(item_type, active_only)

# Rule execution
evaluate_rules(workflow_id)
execute_rule_action(rule, workflow_id)
get_matching_rules(item_type, context)
```

### Phase 3: API Endpoints

#### 3.1 Workflow Endpoints
**File**: `/backend/app/api/v1/approval.py`

```python
# Admin endpoints
GET    /api/v1/admin/approvals                  # List all workflows
GET    /api/v1/admin/approvals/pending          # Pending workflows
GET    /api/v1/admin/approvals/{id}             # Get workflow details
POST   /api/v1/admin/approvals/{id}/assign      # Assign to admin
POST   /api/v1/admin/approvals/{id}/approve     # Approve
POST   /api/v1/admin/approvals/{id}/reject      # Reject
POST   /api/v1/admin/approvals/{id}/escalate    # Escalate
POST   /api/v1/admin/approvals/bulk-approve     # Bulk approve
POST   /api/v1/admin/approvals/bulk-reject      # Bulk reject

# Analytics
GET    /api/v1/admin/approvals/stats            # Approval statistics
GET    /api/v1/admin/approvals/queue-stats      # Queue statistics
```

#### 3.2 Rule Management Endpoints
**File**: `/backend/app/api/v1/approval_rules.py`

```python
# Admin endpoints
GET    /api/v1/admin/approval-rules             # List rules
POST   /api/v1/admin/approval-rules             # Create rule
GET    /api/v1/admin/approval-rules/{id}        # Get rule
PUT    /api/v1/admin/approval-rules/{id}        # Update rule
DELETE /api/v1/admin/approval-rules/{id}        # Delete rule
POST   /api/v1/admin/approval-rules/{id}/toggle # Enable/disable rule
```

#### 3.3 Trust Level Endpoints
**File**: `/backend/app/api/v1/trust.py`

```python
# Admin endpoints
GET    /api/v1/admin/trust-levels               # List user trust levels
GET    /api/v1/admin/trust-levels/{user_id}     # Get user trust level
POST   /api/v1/admin/trust-levels/{user_id}/recalculate  # Recalculate
POST   /api/v1/admin/trust-levels/{user_id}/auto-approve # Grant auto-approve
DELETE /api/v1/admin/trust-levels/{user_id}/auto-approve # Revoke auto-approve

# User endpoints
GET    /api/v1/trust/my-level                   # Get my trust level
```

#### 3.4 Notification Endpoints
**File**: `/backend/app/api/v1/notifications.py`

```python
# User endpoints
GET    /api/v1/notifications                    # Get my notifications
GET    /api/v1/notifications/unread             # Get unread notifications
POST   /api/v1/notifications/{id}/read          # Mark as read
POST   /api/v1/notifications/read-all           # Mark all as read
DELETE /api/v1/notifications/{id}               # Delete notification
```

## 🎨 Frontend Implementation

### Phase 1: Admin Dashboard

#### 1.1 Approval Queue Dashboard
**File**: `/frontend/src/views/admin/ApprovalQueue.vue`

Features:
- Pending items count
- Queue statistics (avg wait time, completion rate)
- Priority filter
- Item type filter
- Assigned to me filter
- Search functionality
- Bulk selection
- Bulk actions (approve, reject, assign)

#### 1.2 Workflow Review Panel
**File**: `/frontend/src/components/admin/WorkflowReviewPanel.vue`

Features:
- Item preview (contribution, image, content)
- Submitter info with trust level badge
- Quality score display
- Review history
- Approve/reject buttons
- Review notes textarea
- Escalate button
- Assign to another admin

#### 1.3 Bulk Actions Modal
**File**: `/frontend/src/components/admin/BulkActionsModal.vue`

Features:
- Selected items count
- Action selector (approve, reject, assign)
- Reason input (for rejection)
- Admin selector (for assignment)
- Confirmation dialog
- Progress indicator

### Phase 2: Rule Management

#### 2.1 Approval Rules View
**File**: `/frontend/src/views/admin/ApprovalRules.vue`

Features:
- List of rules
- Rule status (active/inactive)
- Priority ordering
- Create new rule button
- Edit rule button
- Delete rule button
- Toggle active/inactive
- Rule testing tool

#### 2.2 Rule Editor Modal
**File**: `/frontend/src/components/admin/RuleEditorModal.vue`

Features:
- Rule name input
- Description textarea
- Item type selector
- Condition builder (visual)
- Action selector
- Action parameters
- Priority input
- Save/cancel buttons
- Validation

### Phase 3: Trust Level Management

#### 3.1 Trust Levels View
**File**: `/frontend/src/views/admin/TrustLevels.vue`

Features:
- User list with trust scores
- Trust level badges
- Submission statistics
- Approval rate
- Auto-approve status
- Grant/revoke auto-approve
- Recalculate trust score
- Search users

#### 3.2 User Trust Detail Modal
**File**: `/frontend/src/components/admin/UserTrustDetailModal.vue`

Features:
- Trust score chart
- Submission history
- Quality metrics
- Auto-approve permissions
- Grant/revoke buttons
- Trust level timeline

### Phase 4: Notifications

#### 4.1 Notification Center
**File**: `/frontend/src/components/NotificationCenter.vue`

Features:
- Notification bell icon with badge
- Dropdown list of notifications
- Unread indicator
- Mark as read
- Delete notification
- View all link
- Real-time updates (WebSocket)

#### 4.2 Notification List View
**File**: `/frontend/src/views/NotificationList.vue`

Features:
- All notifications
- Filter by type
- Filter by read/unread
- Mark all as read
- Delete all
- Pagination
- Click to navigate to item

### Phase 5: Analytics

#### 5.1 Approval Analytics Dashboard
**File**: `/frontend/src/views/admin/ApprovalAnalytics.vue`

Features:
- Approval rate chart
- Average review time
- Queue length over time
- Top reviewers
- Approval by type
- Rejection reasons breakdown
- Auto-approval rate

## 🤖 Automation Rules Examples

### Rule 1: Auto-Approve Trusted Users
```json
{
  "name": "Auto-approve trusted user contributions",
  "item_type": "contribution",
  "conditions": {
    "user_trust_level": "trusted",
    "quality_score": ">= 70"
  },
  "action": "auto_approve"
}
```

### Rule 2: Escalate Low Quality
```json
{
  "name": "Escalate low quality submissions",
  "item_type": "contribution",
  "conditions": {
    "quality_score": "< 30"
  },
  "action": "escalate",
  "action_params": {
    "reason": "Low quality score"
  }
}
```

### Rule 3: Assign by Type
```json
{
  "name": "Assign AI content to senior admin",
  "item_type": "ai_content",
  "conditions": {},
  "action": "assign_to",
  "action_params": {
    "admin_role": "senior_admin"
  }
}
```

### Rule 4: Auto-Reject Spam
```json
{
  "name": "Auto-reject spam content",
  "item_type": "contribution",
  "conditions": {
    "spam_score": "> 80"
  },
  "action": "auto_reject",
  "action_params": {
    "reason": "Detected as spam"
  }
}
```

## 📊 Quality Scoring Algorithm

### Contribution Quality Score (0-100)
```python
def calculate_contribution_quality_score(contribution):
    score = 0
    
    # Content length (0-20 points)
    content_length = len(contribution.content)
    if 100 <= content_length <= 1000:
        score += 20
    elif content_length > 1000:
        score += 15
    else:
        score += 10
    
    # User trust level (0-30 points)
    trust_level = get_user_trust_level(contribution.student_id)
    score += trust_level.trust_score * 0.3
    
    # Grammar/spelling (0-20 points)
    grammar_score = check_grammar(contribution.content)
    score += grammar_score * 0.2
    
    # Formatting (0-10 points)
    if has_proper_markdown(contribution.content):
        score += 10
    
    # Relevance to chapter (0-20 points)
    relevance_score = check_relevance(contribution, contribution.chapter)
    score += relevance_score * 0.2
    
    return min(100, score)
```

### Trust Score Calculation
```python
def calculate_user_trust_score(user_id):
    stats = get_user_submission_stats(user_id)
    
    # Base score from approval rate (0-40 points)
    approval_rate_score = stats.approval_rate * 0.4
    
    # Volume bonus (0-20 points)
    volume_score = min(20, stats.approved_submissions * 0.5)
    
    # Quality bonus (0-30 points)
    quality_score = stats.average_quality_score * 0.3
    
    # Engagement bonus (0-10 points)
    engagement_score = min(10, stats.average_upvotes * 0.5)
    
    total_score = (
        approval_rate_score +
        volume_score +
        quality_score +
        engagement_score
    )
    
    return min(100, total_score)
```

## 🔔 Notification Types

### For Admins
1. **New Submission**: "New contribution awaiting review"
2. **Escalation**: "Workflow escalated - requires attention"
3. **Assignment**: "Workflow assigned to you"
4. **Queue Alert**: "Approval queue exceeds threshold"

### For Students
1. **Approved**: "Your contribution has been approved! +20 XP"
2. **Rejected**: "Your contribution was not approved"
3. **In Review**: "Your contribution is being reviewed"
4. **Trust Level Up**: "You've reached Trusted status!"

## 🧪 Testing Checklist

### Backend
- [ ] Create workflow
- [ ] Assign workflow
- [ ] Approve workflow
- [ ] Reject workflow
- [ ] Escalate workflow
- [ ] Bulk approve
- [ ] Bulk reject
- [ ] Calculate quality score
- [ ] Calculate trust score
- [ ] Auto-approve eligible items
- [ ] Apply approval rules
- [ ] Create notification
- [ ] Send notifications
- [ ] Create approval rule
- [ ] Evaluate rules

### Frontend
- [ ] View approval queue
- [ ] Filter workflows
- [ ] Review workflow
- [ ] Approve workflow
- [ ] Reject workflow
- [ ] Bulk actions
- [ ] Create approval rule
- [ ] Edit approval rule
- [ ] View trust levels
- [ ] Grant auto-approve
- [ ] View notifications
- [ ] Mark notification as read
- [ ] Analytics dashboard

## 🚀 Deployment Steps

1. **Database Migration**
   ```bash
   alembic revision --autogenerate -m "Add approval system"
   alembic upgrade head
   ```

2. **Seed Initial Rules**
   ```bash
   python scripts/seed_approval_rules.py
   ```

3. **Calculate Trust Scores**
   ```bash
   python scripts/calculate_trust_scores.py
   ```

4. **Configure Notifications**
   - Set up email/push notification service
   - Configure notification templates

## 📈 Success Metrics

- ✅ Approval queue is manageable
- ✅ Average review time < 24 hours
- ✅ Auto-approval rate > 30%
- ✅ Admin satisfaction with workflow
- ✅ Reduced manual review burden
- ✅ Trust system works accurately
- ✅ Notifications are timely

## 🎯 Next Steps After Sprint 5

**Sprint 6: AI Integration with Images**
- AI-powered quality scoring
- Automated content suggestions
- Image-based content generation
- Smart tagging and categorization
