# Sprint 3: Image Management Implementation Plan

## 🎯 Objectives
1. ✅ Add image upload functionality
2. ✅ Create image gallery browser for admins
3. ✅ Associate images with chapters
4. ✅ Enable image use in AI content generation
5. ✅ Implement secure file storage

## 📋 Implementation Steps

### Phase 1: Backend - Database & Models

#### 1.1 Create Image Model
**File**: `/backend/app/models/image.py`

```python
- Image table with fields:
  - id (UUID)
  - filename (String)
  - original_filename (String)
  - file_path (String)
  - file_size (Integer)
  - mime_type (String)
  - width (Integer, optional)
  - height (Integer, optional)
  - uploaded_by (UUID, FK to users)
  - created_at (DateTime)
  - updated_at (DateTime)
```

#### 1.2 Create ChapterImage Association Model
**File**: `/backend/app/models/curriculum.py` (update)

```python
- ChapterImage association table:
  - id (UUID)
  - chapter_id (UUID, FK)
  - image_id (UUID, FK)
  - display_order (Integer)
  - caption (Text, optional)
  - created_at (DateTime)
```

#### 1.3 Create Database Migration
**File**: `/backend/alembic/versions/xxx_add_image_management.py`

```bash
- Add images table
- Add chapter_images association table
- Add indexes for performance
```

### Phase 2: Backend - Schemas & Services

#### 2.1 Image Schemas
**File**: `/backend/app/schemas/image.py`

```python
- ImageUploadResponse
- ImageResponse
- ImageListResponse
- ChapterImageCreate
- ChapterImageResponse
```

#### 2.2 Image Service
**File**: `/backend/app/services/image_service.py`

```python
Functions:
- save_uploaded_file(file, user_id)
- delete_image(image_id, user_id)
- get_image_by_id(image_id)
- list_images(filters, pagination)
- associate_image_with_chapter(chapter_id, image_id)
- remove_image_from_chapter(chapter_id, image_id)
- get_chapter_images(chapter_id)
```

#### 2.3 File Storage Configuration
**File**: `/backend/app/core/config.py` (update)

```python
- UPLOAD_DIR path
- MAX_FILE_SIZE
- ALLOWED_IMAGE_TYPES
- IMAGE_QUALITY_SETTINGS
```

### Phase 3: Backend - API Endpoints

#### 3.1 Image Management Endpoints
**File**: `/backend/app/api/v1/images.py`

```python
POST   /api/v1/admin/images/upload
GET    /api/v1/admin/images
GET    /api/v1/admin/images/{image_id}
DELETE /api/v1/admin/images/{image_id}
GET    /api/v1/images/{image_id}/file (public, for serving)
```

#### 3.2 Chapter-Image Association Endpoints
**File**: `/backend/app/api/v1/content_management.py` (update)

```python
POST   /api/v1/admin/chapters/{chapter_id}/images
GET    /api/v1/admin/chapters/{chapter_id}/images
DELETE /api/v1/admin/chapters/{chapter_id}/images/{image_id}
PUT    /api/v1/admin/chapters/{chapter_id}/images/{image_id}/order
```

### Phase 4: Frontend - Image Gallery Component

#### 4.1 Image Gallery Browser
**File**: `/frontend/src/views/AdminImageGallery.vue`

Features:
- Grid view of uploaded images
- Upload button with drag-and-drop
- Image preview modal
- Delete confirmation
- Search/filter by filename
- Pagination
- Image metadata display (size, dimensions, upload date)

#### 4.2 Image Upload Component
**File**: `/frontend/src/components/admin/ImageUploader.vue`

Features:
- Drag-and-drop zone
- File selection button
- Progress bar during upload
- Preview before upload
- Multiple file upload support
- Validation (file type, size)
- Error handling

#### 4.3 Image Picker Component
**File**: `/frontend/src/components/admin/ImagePicker.vue`

Features:
- Modal dialog
- Gallery view of available images
- Upload new image option
- Search functionality
- Select/deselect images
- Preview selected images

### Phase 5: Frontend - Content Editor Integration

#### 5.1 Update Content Browser
**File**: `/frontend/src/views/AdminContentBrowser.vue` (update)

Add:
- "Manage Images" button for each chapter
- Image count badge
- Quick preview of chapter images

#### 5.2 Chapter Image Manager
**File**: `/frontend/src/components/admin/ChapterImageManager.vue`

Features:
- List of images associated with chapter
- Add images button (opens ImagePicker)
- Remove image from chapter
- Reorder images (drag-and-drop)
- Add captions to images
- Preview images

### Phase 6: Frontend - Services & API Integration

#### 6.1 Image API Service
**File**: `/frontend/src/services/imageService.js`

```javascript
Functions:
- uploadImage(file, onProgress)
- getImages(page, limit, search)
- getImageById(imageId)
- deleteImage(imageId)
- getImageUrl(imageId)
```

#### 6.2 Chapter Image API Service
**File**: `/frontend/src/services/chapterImageService.js`

```javascript
Functions:
- addImageToChapter(chapterId, imageId, caption)
- getChapterImages(chapterId)
- removeImageFromChapter(chapterId, imageId)
- updateImageOrder(chapterId, imageId, newOrder)
```

### Phase 7: AI Content Generation Integration

#### 7.1 Update AI Service
**File**: `/backend/app/services/ai_service.py` (update)

Add:
- Include chapter images in context when generating content
- Generate image descriptions for accessibility
- Suggest relevant images for content blocks

#### 7.2 Content Block Schema Update
**File**: `/backend/app/models/curriculum.py` (update)

Update ContentBlock to support:
- Image references in content_data
- Image placement hints
- Alt text for images

## 🔒 Security Considerations

1. **File Upload Security**
   - Validate file types (whitelist: jpg, jpeg, png, gif, webp)
   - Limit file size (e.g., 5MB max)
   - Sanitize filenames
   - Store files outside web root
   - Generate unique filenames (UUID-based)

2. **Access Control**
   - Only admins can upload/delete images
   - Public read access for serving images (with rate limiting)
   - Verify image ownership before deletion

3. **Storage Security**
   - Use secure file permissions
   - Implement virus scanning (optional, future)
   - Regular backup of uploaded files

## 📁 Directory Structure

```
backend/
├── app/
│   ├── models/
│   │   ├── image.py (NEW)
│   │   └── curriculum.py (UPDATE)
│   ├── schemas/
│   │   └── image.py (NEW)
│   ├── services/
│   │   └── image_service.py (NEW)
│   └── api/v1/
│       ├── images.py (NEW)
│       └── content_management.py (UPDATE)
└── uploads/
    └── images/ (NEW - file storage)

frontend/
└── src/
    ├── views/
    │   ├── AdminImageGallery.vue (NEW)
    │   └── AdminContentBrowser.vue (UPDATE)
    ├── components/admin/
    │   ├── ImageUploader.vue (NEW)
    │   ├── ImagePicker.vue (NEW)
    │   └── ChapterImageManager.vue (NEW)
    └── services/
        ├── imageService.js (NEW)
        └── chapterImageService.js (NEW)
```

## 🧪 Testing Checklist

### Backend Tests
- [ ] Image upload with valid file
- [ ] Image upload with invalid file type
- [ ] Image upload exceeding size limit
- [ ] Image deletion by owner
- [ ] Image deletion by non-owner (should fail)
- [ ] Associate image with chapter
- [ ] Get chapter images
- [ ] Remove image from chapter
- [ ] Serve image file

### Frontend Tests
- [ ] Upload single image
- [ ] Upload multiple images
- [ ] Drag-and-drop upload
- [ ] View image gallery
- [ ] Search images
- [ ] Delete image with confirmation
- [ ] Add image to chapter
- [ ] Remove image from chapter
- [ ] Reorder chapter images
- [ ] Preview images

## 🚀 Deployment Steps

1. **Database Migration**
   ```bash
   cd backend
   alembic revision --autogenerate -m "Add image management"
   alembic upgrade head
   ```

2. **Create Upload Directory**
   ```bash
   mkdir -p backend/uploads/images
   chmod 755 backend/uploads/images
   ```

3. **Update Environment Variables**
   ```
   UPLOAD_DIR=/path/to/backend/uploads
   MAX_FILE_SIZE=5242880  # 5MB in bytes
   ```

4. **Install Dependencies**
   ```bash
   # Backend
   pip install python-multipart pillow

   # Frontend (if needed)
   npm install
   ```

5. **Restart Services**
   ```bash
   # Backend
   uvicorn app.main:app --reload

   # Frontend
   npm run dev
   ```

## 📊 Success Metrics

- ✅ Admins can upload images via drag-and-drop
- ✅ Images are stored securely with unique filenames
- ✅ Image gallery displays all uploaded images
- ✅ Images can be associated with chapters
- ✅ Chapter images are displayed in content browser
- ✅ Images are served efficiently for frontend display
- ✅ All security validations are in place
- ✅ Error handling works correctly

## 🎯 Next Steps After Sprint 3

**Sprint 4: AI Content Editor**
- Rich text editor for content blocks
- AI-powered content generation UI
- Image insertion in content
- Preview mode
- Version history

**Sprint 5: Student Content Viewer**
- Render lessons with images
- Interactive quizzes
- Progress tracking
- Gamification integration
