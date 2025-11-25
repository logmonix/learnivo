# Sprint 4: Student Contributions

## 🎯 Objectives
Enable students to contribute content (questions, explanations, notes) to chapters, creating a collaborative learning environment.

## 📋 Features

### Core Features
1. ✅ Students can submit questions about chapter content
2. ✅ Students can submit their own explanations/notes
3. ✅ Students can upvote/downvote contributions
4. ✅ Contributions are tagged by chapter and topic
5. ✅ Students earn XP for approved contributions
6. ✅ Leaderboard for top contributors

### Admin Features
1. ✅ View all pending contributions
2. ✅ Approve/reject contributions
3. ✅ Edit contributions before approval
4. ✅ Moderate inappropriate content
5. ✅ Set XP rewards for contributions

## 🗄️ Database Schema

### Contribution Model
```python
class Contribution(Base):
    __tablename__ = "contributions"
    
    id = UUID (Primary Key)
    chapter_id = UUID (Foreign Key to chapters)
    student_id = UUID (Foreign Key to users)
    
    # Type: 'question', 'explanation', 'note', 'tip'
    contribution_type = String
    
    # Content
    title = String (required)
    content = Text (required, markdown supported)
    
    # Status: 'pending', 'approved', 'rejected'
    status = String (default: 'pending')
    
    # Moderation
    reviewed_by = UUID (Foreign Key to users, nullable)
    reviewed_at = DateTime (nullable)
    rejection_reason = Text (nullable)
    
    # Engagement
    upvotes = Integer (default: 0)
    downvotes = Integer (default: 0)
    
    # Metadata
    created_at = DateTime
    updated_at = DateTime
```

### ContributionVote Model
```python
class ContributionVote(Base):
    __tablename__ = "contribution_votes"
    
    id = UUID (Primary Key)
    contribution_id = UUID (Foreign Key to contributions)
    student_id = UUID (Foreign Key to users)
    
    # Vote: 1 for upvote, -1 for downvote
    vote = Integer
    
    created_at = DateTime
    
    # Unique constraint: one vote per student per contribution
    __table_args__ = (
        UniqueConstraint('contribution_id', 'student_id'),
    )
```

### ContributionReward Model
```python
class ContributionReward(Base):
    __tablename__ = "contribution_rewards"
    
    id = UUID (Primary Key)
    contribution_id = UUID (Foreign Key to contributions)
    student_id = UUID (Foreign Key to users)
    
    xp_earned = Integer
    coins_earned = Integer
    
    awarded_at = DateTime
```

## 🔧 Backend Implementation

### Phase 1: Models & Schemas

#### 1.1 Create Models
**File**: `/backend/app/models/contribution.py`
- Contribution model
- ContributionVote model
- ContributionReward model

#### 1.2 Create Schemas
**File**: `/backend/app/schemas/contribution.py`
- ContributionCreate
- ContributionUpdate
- ContributionResponse
- ContributionListResponse
- ContributionVoteCreate
- ContributionReviewRequest

#### 1.3 Database Migration
```bash
alembic revision --autogenerate -m "Add student contributions"
alembic upgrade head
```

### Phase 2: Services

#### 2.1 Contribution Service
**File**: `/backend/app/services/contribution_service.py`

Functions:
- `create_contribution(student_id, chapter_id, type, title, content)`
- `get_contribution_by_id(contribution_id)`
- `list_contributions(filters, pagination)`
- `update_contribution(contribution_id, updates)`
- `delete_contribution(contribution_id, user_id)`
- `approve_contribution(contribution_id, admin_id)`
- `reject_contribution(contribution_id, admin_id, reason)`
- `vote_contribution(contribution_id, student_id, vote)`
- `get_contribution_votes(contribution_id)`
- `get_student_contributions(student_id, status)`
- `get_chapter_contributions(chapter_id, status)`
- `get_top_contributors(limit)`

#### 2.2 Reward Service Integration
**File**: `/backend/app/services/contribution_service.py`

Functions:
- `award_contribution_xp(contribution_id, student_id)`
- Calculate XP based on:
  - Contribution type (question: 10 XP, explanation: 20 XP, note: 15 XP)
  - Upvotes (1 XP per upvote)
  - Quality bonus (admin can add bonus XP)

### Phase 3: API Endpoints

#### 3.1 Student Contribution Endpoints
**File**: `/backend/app/api/v1/contributions.py`

```python
# Student endpoints
POST   /api/v1/contributions                    # Create contribution
GET    /api/v1/contributions                    # List all approved contributions
GET    /api/v1/contributions/{id}               # Get contribution details
PUT    /api/v1/contributions/{id}               # Update own contribution (if pending)
DELETE /api/v1/contributions/{id}               # Delete own contribution (if pending)

# Voting
POST   /api/v1/contributions/{id}/vote          # Upvote/downvote
DELETE /api/v1/contributions/{id}/vote          # Remove vote

# Student's own contributions
GET    /api/v1/contributions/my                 # Get my contributions

# Chapter contributions
GET    /api/v1/chapters/{id}/contributions      # Get approved contributions for chapter
```

#### 3.2 Admin Moderation Endpoints
**File**: `/backend/app/api/v1/admin_contributions.py`

```python
# Admin endpoints
GET    /api/v1/admin/contributions/pending      # List pending contributions
GET    /api/v1/admin/contributions              # List all contributions (any status)
POST   /api/v1/admin/contributions/{id}/approve # Approve contribution
POST   /api/v1/admin/contributions/{id}/reject  # Reject contribution
PUT    /api/v1/admin/contributions/{id}         # Edit contribution
DELETE /api/v1/admin/contributions/{id}         # Delete contribution

# Analytics
GET    /api/v1/admin/contributions/stats        # Contribution statistics
GET    /api/v1/admin/contributions/leaderboard  # Top contributors
```

## 🎨 Frontend Implementation

### Phase 1: Student Components

#### 1.1 Contribution Form
**File**: `/frontend/src/components/student/ContributionForm.vue`

Features:
- Contribution type selector (question, explanation, note, tip)
- Title input
- Markdown editor for content
- Preview mode
- Submit button
- Character count
- Validation

#### 1.2 Contribution Card
**File**: `/frontend/src/components/student/ContributionCard.vue`

Features:
- Display contribution type icon
- Show title and content (markdown rendered)
- Upvote/downvote buttons
- Vote count display
- Author name and avatar
- Timestamp
- Status badge (pending/approved/rejected)

#### 1.3 Contribution List
**File**: `/frontend/src/components/student/ContributionList.vue`

Features:
- List of contributions
- Filter by type
- Sort by: newest, most upvoted, most helpful
- Pagination
- Empty state

#### 1.4 My Contributions View
**File**: `/frontend/src/views/student/MyContributions.vue`

Features:
- Tabs: All, Pending, Approved, Rejected
- Contribution cards
- Edit button (for pending)
- Delete button (for pending)
- XP earned display
- Statistics (total contributions, approval rate)

### Phase 2: Chapter Integration

#### 2.1 Update Chapter View
**File**: `/frontend/src/views/student/ChapterView.vue` (update)

Add:
- "Contributions" tab
- "Add Contribution" button
- List of approved contributions
- Sort/filter options

#### 2.2 Contribution Section
**File**: `/frontend/src/components/student/ChapterContributions.vue`

Features:
- Display approved contributions for chapter
- Filter by type
- Sort by votes
- Vote on contributions
- "Add your own" button

### Phase 3: Admin Components

#### 3.1 Moderation Dashboard
**File**: `/frontend/src/views/admin/ContributionModeration.vue`

Features:
- Pending contributions queue
- Contribution preview
- Approve/reject buttons
- Edit before approval
- Rejection reason input
- Batch actions
- Statistics overview

#### 3.2 Contribution Review Modal
**File**: `/frontend/src/components/admin/ContributionReviewModal.vue`

Features:
- Full contribution display
- Student info
- Chapter context
- Edit content
- XP bonus input
- Approve/reject buttons
- Rejection reason textarea

#### 3.3 Leaderboard View
**File**: `/frontend/src/views/admin/ContributionLeaderboard.vue`

Features:
- Top contributors list
- Contribution count
- XP earned from contributions
- Approval rate
- Time period filter (week, month, all-time)

### Phase 4: Services

#### 4.1 Contribution Service
**File**: `/frontend/src/services/contributionService.js`

```javascript
export default {
  // Student actions
  createContribution(chapterId, type, title, content),
  getMyContributions(status),
  updateContribution(id, updates),
  deleteContribution(id),
  voteContribution(id, vote),
  
  // Public
  getChapterContributions(chapterId, filters),
  getContribution(id),
  
  // Admin
  getPendingContributions(),
  getAllContributions(filters),
  approveContribution(id, xpBonus),
  rejectContribution(id, reason),
  getContributionStats(),
  getLeaderboard(period)
}
```

## 🎮 Gamification Integration

### XP Rewards
- **Question submitted & approved**: 10 XP
- **Explanation submitted & approved**: 20 XP
- **Note submitted & approved**: 15 XP
- **Tip submitted & approved**: 10 XP
- **Per upvote received**: 1 XP
- **Quality bonus** (admin discretion): 0-50 XP

### Badges
Create new badges:
- **First Contributor**: Submit first contribution
- **Helpful Student**: 10 approved contributions
- **Knowledge Sharer**: 50 approved contributions
- **Community Leader**: 100 approved contributions
- **Top Voted**: Contribution with 50+ upvotes

### Leaderboard
- Weekly top contributors
- Monthly top contributors
- All-time top contributors
- Most upvoted contributions

## 🔒 Security & Moderation

### Content Validation
1. **Length limits**:
   - Title: 5-200 characters
   - Content: 10-5000 characters

2. **Rate limiting**:
   - Max 10 contributions per day per student
   - Max 1 contribution per minute

3. **Spam prevention**:
   - Duplicate content detection
   - Profanity filter
   - Link spam detection

### Moderation Rules
1. All contributions start as "pending"
2. Admin must review before approval
3. Students can edit only pending contributions
4. Rejected contributions show reason to student
5. Students can resubmit after rejection

## 📊 Analytics

### Student Analytics
- Total contributions
- Approval rate
- Total XP earned from contributions
- Most upvoted contribution
- Contribution streak

### Admin Analytics
- Pending contributions count
- Average review time
- Approval/rejection rates
- Most active contributors
- Most contributed chapters

## 🧪 Testing Checklist

### Backend
- [ ] Create contribution
- [ ] List contributions with filters
- [ ] Update pending contribution
- [ ] Delete pending contribution
- [ ] Approve contribution (awards XP)
- [ ] Reject contribution
- [ ] Vote on contribution
- [ ] Remove vote
- [ ] Get chapter contributions
- [ ] Get student contributions
- [ ] Get leaderboard
- [ ] Prevent duplicate votes
- [ ] Prevent voting on own contribution

### Frontend
- [ ] Submit contribution form
- [ ] View my contributions
- [ ] Edit pending contribution
- [ ] Delete pending contribution
- [ ] View chapter contributions
- [ ] Upvote/downvote contribution
- [ ] Admin: Review pending contributions
- [ ] Admin: Approve with XP bonus
- [ ] Admin: Reject with reason
- [ ] View leaderboard
- [ ] Markdown rendering works
- [ ] Validation works

## 🚀 Deployment Steps

1. **Database Migration**
   ```bash
   alembic revision --autogenerate -m "Add student contributions"
   alembic upgrade head
   ```

2. **Update Environment Variables**
   ```
   MAX_CONTRIBUTIONS_PER_DAY=10
   CONTRIBUTION_XP_QUESTION=10
   CONTRIBUTION_XP_EXPLANATION=20
   CONTRIBUTION_XP_NOTE=15
   ```

3. **Seed Initial Data** (optional)
   - Create sample contributions for testing
   - Set up contribution type configurations

4. **Deploy Backend**
   ```bash
   # Restart backend service
   docker-compose restart backend
   ```

5. **Deploy Frontend**
   ```bash
   cd frontend
   npm run build
   ```

## 📈 Success Metrics

- ✅ Students can submit contributions
- ✅ Contributions require admin approval
- ✅ Students earn XP for approved contributions
- ✅ Voting system works correctly
- ✅ Leaderboard displays top contributors
- ✅ Admin can moderate efficiently
- ✅ Content is properly validated
- ✅ Gamification integration works

## 🎯 Next Steps After Sprint 4

**Sprint 5: Admin Approval System**
- Workflow automation
- Notification system
- Bulk moderation tools
- Content quality scoring
- Auto-approval for trusted students
