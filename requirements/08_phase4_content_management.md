# Phase 4: Admin Content Management & Student Contributions

## Goal
Create a robust content management system where admins can manually create/edit educational content with images, and students can contribute content that requires admin approval.

## Task List

### 1. Role-Based Access Control (RBAC)
- [ ] **User Roles**: Add `is_admin` flag to User model
- [ ] **Admin Middleware**: Create route guards for admin-only pages
- [ ] **Frontend Guards**: Hide admin navigation for non-admin users
- [ ] **API Protection**: Secure admin endpoints with role checking

### 2. Admin Content Management Interface
- [ ] **Subject Browser**: Navigate through subjects and chapters
- [ ] **Content Editor**: Rich text editor for lesson content
- [ ] **Image Upload**: Upload and manage images for lessons
- [ ] **Chapter Details**: Edit title, description, order
- [ ] **Preview Mode**: Preview lesson as student would see it
- [ ] **Publish/Draft**: Save content as draft or publish

### 3. Image Management System
- [ ] **Image Upload API**: Handle file uploads (S3/local storage)
- [ ] **Image Model**: Store image metadata (URL, uploader, status)
- [ ] **Image Gallery**: Browse and select uploaded images
- [ ] **Image Association**: Link images to specific chapters/lessons
- [ ] **Image Optimization**: Resize/compress images automatically

### 4. Student Content Contribution
- [ ] **Contribution Form**: Students can submit images with context
- [ ] **Submission Model**: Store pending contributions
- [ ] **Upload Interface**: Simple, kid-friendly upload form
- [ ] **Contribution History**: Students see their submission status

### 5. Admin Approval Workflow
- [ ] **Pending Queue**: View all pending student contributions
- [ ] **Review Interface**: Approve/reject with feedback
- [ ] **Moderation Tools**: Flag inappropriate content
- [ ] **Notification System**: Notify students of approval/rejection

### 6. AI Content Generation from Admin Input
- [ ] **Manual Trigger**: Admin can trigger AI generation for chapter
- [ ] **Context Injection**: Use admin-provided images/text as context
- [ ] **Regeneration**: Ability to regenerate content with different prompts
- [ ] **Version Control**: Keep history of generated content

### 7. Content Workflow
- [ ] **Draft State**: Content can be saved without publishing
- [ ] **Review State**: Mark content for peer review
- [ ] **Published State**: Make content visible to students
- [ ] **Archived State**: Hide old content without deleting

## Implementation Order

### Sprint 1: RBAC & Admin Access
1. ✅ Add `is_admin` field to User model
2. ✅ Create admin role checking middleware
3. ✅ Add route guards to frontend
4. ✅ Secure admin API endpoints
5. ✅ Update navigation to show/hide admin link

### Sprint 2: Content Editor
1. ✅ Create admin content browser (subjects → chapters)
2. ✅ Build rich text editor component
3. ✅ Implement chapter detail editing
4. ✅ Add save/publish functionality
5. ⏳ Create preview mode (uses existing lesson view)

### Sprint 3: Image Management
1. Set up image upload API (local storage first)
2. Create Image model and migrations
3. Build image upload component
4. Create image gallery browser
5. Implement image-to-chapter association

### Sprint 4: Student Contributions
1. Create StudentContribution model
2. Build student upload interface
3. Create submission history view
4. Add contribution API endpoints

### Sprint 5: Admin Approval System
1. Create admin approval queue view
2. Build review interface
3. Add approve/reject API endpoints
4. Implement notification system
5. Update AI to use approved images

### Sprint 6: AI Integration
1. Update AI prompts to accept image context
2. Add manual generation trigger
3. Implement regeneration with feedback
4. Add version control for content

## Database Schema Changes

### New Tables
```sql
-- Image storage
CREATE TABLE images (
    id UUID PRIMARY KEY,
    url TEXT NOT NULL,
    filename TEXT,
    uploaded_by UUID REFERENCES users(id),
    upload_type TEXT, -- 'admin' or 'student'
    status TEXT, -- 'pending', 'approved', 'rejected'
    created_at TIMESTAMP
);

-- Student contributions
CREATE TABLE student_contributions (
    id UUID PRIMARY KEY,
    profile_id UUID REFERENCES profiles(id),
    chapter_id UUID REFERENCES chapters(id),
    contribution_type TEXT, -- 'image', 'text', 'question'
    content_data JSON,
    status TEXT, -- 'pending', 'approved', 'rejected'
    reviewed_by UUID REFERENCES users(id),
    review_notes TEXT,
    created_at TIMESTAMP,
    reviewed_at TIMESTAMP
);

-- Content versions
CREATE TABLE content_versions (
    id UUID PRIMARY KEY,
    content_block_id UUID REFERENCES content_blocks(id),
    version_number INT,
    content_data JSON,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP
);
```

### Modified Tables
```sql
-- Add admin flag
ALTER TABLE users ADD COLUMN is_admin BOOLEAN DEFAULT FALSE;

-- Add status to content blocks
ALTER TABLE content_blocks ADD COLUMN status TEXT DEFAULT 'draft';
ALTER TABLE content_blocks ADD COLUMN created_by UUID REFERENCES users(id);

-- Add image references
ALTER TABLE content_blocks ADD COLUMN image_ids JSON;
```

## API Endpoints

### Admin Content Management
```
GET    /api/v1/admin/subjects/{subject_id}/chapters
GET    /api/v1/admin/chapters/{chapter_id}/content
POST   /api/v1/admin/chapters/{chapter_id}/content
PUT    /api/v1/admin/content/{content_id}
DELETE /api/v1/admin/content/{content_id}
POST   /api/v1/admin/content/{content_id}/publish
POST   /api/v1/admin/content/{content_id}/regenerate
```

### Image Management
```
POST   /api/v1/images/upload
GET    /api/v1/images
GET    /api/v1/images/{image_id}
DELETE /api/v1/images/{image_id}
```

### Student Contributions
```
POST   /api/v1/contributions/submit
GET    /api/v1/contributions/my-submissions
GET    /api/v1/admin/contributions/pending
POST   /api/v1/admin/contributions/{id}/approve
POST   /api/v1/admin/contributions/{id}/reject
```

## UI Components

### Admin Components
- `AdminContentBrowser.vue` - Navigate subjects/chapters
- `ContentEditor.vue` - Rich text editor
- `ImageUploader.vue` - Drag-and-drop upload
- `ImageGallery.vue` - Browse/select images
- `ContributionQueue.vue` - Review pending submissions

### Student Components
- `ContributeButton.vue` - Quick contribution access
- `ContributionForm.vue` - Upload form
- `MyContributions.vue` - Submission history

## Security Considerations
- [ ] File type validation (only images)
- [ ] File size limits (max 5MB)
- [ ] Image scanning for inappropriate content
- [ ] Rate limiting on uploads
- [ ] Admin-only content editing
- [ ] CSRF protection on uploads

## Testing Checklist
- [ ] Admin can create content with images
- [ ] Non-admin cannot access admin routes
- [ ] Students can submit contributions
- [ ] Admin can approve/reject contributions
- [ ] AI uses approved images in generation
- [ ] Content versioning works correctly
- [ ] Image upload handles errors gracefully

---

**Priority**: High
**Estimated Time**: 2-3 weeks
**Dependencies**: Existing admin dashboard, gamification system
