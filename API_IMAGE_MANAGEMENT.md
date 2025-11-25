# Image Management API Reference

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication
All admin endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer YOUR_ADMIN_TOKEN
```

## Image Management Endpoints

### 1. Upload Image
**POST** `/images/upload`

Upload a new image file.

**Headers:**
- `Authorization: Bearer {token}` (Admin only)
- `Content-Type: multipart/form-data`

**Body:**
- `file`: Image file (JPEG, PNG, GIF, WebP, max 5MB)

**Response:** `200 OK`
```json
{
  "id": "uuid",
  "filename": "unique-filename.jpg",
  "original_filename": "my-image.jpg",
  "file_size": 1024000,
  "mime_type": "image/jpeg",
  "width": 1920,
  "height": 1080,
  "created_at": "2025-11-24T21:20:00Z",
  "url": "/api/v1/images/{id}/file"
}
```

**Errors:**
- `400`: Invalid file type or size
- `401`: Unauthorized
- `500`: Server error

---

### 2. List Images
**GET** `/images`

Get a paginated list of all images.

**Headers:**
- `Authorization: Bearer {token}` (Admin only)

**Query Parameters:**
- `page` (optional): Page number, default: 1
- `page_size` (optional): Items per page, default: 20, max: 100
- `search` (optional): Search term for filename

**Response:** `200 OK`
```json
{
  "images": [
    {
      "id": "uuid",
      "filename": "unique-filename.jpg",
      "original_filename": "my-image.jpg",
      "file_path": "images/unique-filename.jpg",
      "file_size": 1024000,
      "mime_type": "image/jpeg",
      "width": 1920,
      "height": 1080,
      "uploaded_by": "user-uuid",
      "created_at": "2025-11-24T21:20:00Z",
      "updated_at": "2025-11-24T21:20:00Z",
      "url": "/api/v1/images/{id}/file"
    }
  ],
  "total": 42,
  "page": 1,
  "page_size": 20,
  "total_pages": 3
}
```

---

### 3. Get Image Details
**GET** `/images/{image_id}`

Get metadata for a specific image.

**Headers:**
- `Authorization: Bearer {token}` (Admin only)

**Response:** `200 OK`
```json
{
  "id": "uuid",
  "filename": "unique-filename.jpg",
  "original_filename": "my-image.jpg",
  "file_path": "images/unique-filename.jpg",
  "file_size": 1024000,
  "mime_type": "image/jpeg",
  "width": 1920,
  "height": 1080,
  "uploaded_by": "user-uuid",
  "created_at": "2025-11-24T21:20:00Z",
  "updated_at": "2025-11-24T21:20:00Z",
  "url": "/api/v1/images/{id}/file"
}
```

**Errors:**
- `404`: Image not found

---

### 4. Delete Image
**DELETE** `/images/{image_id}`

Delete an image file and database record.

**Headers:**
- `Authorization: Bearer {token}` (Admin only)

**Response:** `200 OK`
```json
{
  "message": "Image deleted successfully"
}
```

**Errors:**
- `403`: Not authorized (non-admin trying to delete)
- `404`: Image not found

---

### 5. Serve Image File
**GET** `/images/{image_id}/file`

Get the actual image file. **This endpoint is public** (no authentication required).

**Response:** `200 OK`
- Content-Type: `image/jpeg` (or appropriate MIME type)
- Body: Image file binary data

**Errors:**
- `404`: Image not found or file missing

---

## Chapter-Image Association Endpoints

### 6. Add Image to Chapter
**POST** `/admin/chapters/{chapter_id}/images`

Associate an image with a chapter.

**Headers:**
- `Authorization: Bearer {token}` (Admin only)
- `Content-Type: application/json`

**Body:**
```json
{
  "image_id": "uuid",
  "caption": "Optional caption text",
  "display_order": 0
}
```

**Response:** `200 OK`
```json
{
  "id": "uuid",
  "chapter_id": "chapter-uuid",
  "image_id": "image-uuid",
  "display_order": 0,
  "caption": "Optional caption text",
  "created_at": "2025-11-24T21:20:00Z",
  "image": {
    "id": "uuid",
    "filename": "unique-filename.jpg",
    "original_filename": "my-image.jpg",
    "file_path": "images/unique-filename.jpg",
    "file_size": 1024000,
    "mime_type": "image/jpeg",
    "width": 1920,
    "height": 1080,
    "uploaded_by": "user-uuid",
    "created_at": "2025-11-24T21:20:00Z",
    "updated_at": "2025-11-24T21:20:00Z",
    "url": "/api/v1/images/{id}/file"
  }
}
```

**Errors:**
- `400`: Image already associated with chapter
- `404`: Chapter or image not found

---

### 7. List Chapter Images
**GET** `/admin/chapters/{chapter_id}/images`

Get all images associated with a chapter.

**Headers:**
- `Authorization: Bearer {token}` (Admin only)

**Response:** `200 OK`
```json
{
  "chapter_images": [
    {
      "id": "uuid",
      "chapter_id": "chapter-uuid",
      "image_id": "image-uuid",
      "display_order": 0,
      "caption": "Optional caption text",
      "created_at": "2025-11-24T21:20:00Z",
      "image": {
        "id": "uuid",
        "filename": "unique-filename.jpg",
        "original_filename": "my-image.jpg",
        "file_path": "images/unique-filename.jpg",
        "file_size": 1024000,
        "mime_type": "image/jpeg",
        "width": 1920,
        "height": 1080,
        "uploaded_by": "user-uuid",
        "created_at": "2025-11-24T21:20:00Z",
        "updated_at": "2025-11-24T21:20:00Z",
        "url": "/api/v1/images/{id}/file"
      }
    }
  ],
  "total": 5
}
```

**Errors:**
- `404`: Chapter not found

---

### 8. Remove Image from Chapter
**DELETE** `/admin/chapters/{chapter_id}/images/{image_id}`

Remove an image association from a chapter (does not delete the image itself).

**Headers:**
- `Authorization: Bearer {token}` (Admin only)

**Response:** `200 OK`
```json
{
  "message": "Image removed from chapter successfully"
}
```

**Errors:**
- `404`: Association not found

---

### 9. Update Image Order
**PUT** `/admin/chapters/{chapter_id}/images/{image_id}/order`

Update the display order of an image in a chapter.

**Headers:**
- `Authorization: Bearer {token}` (Admin only)
- `Content-Type: application/json`

**Body:**
```json
{
  "display_order": 2
}
```

**Response:** `200 OK`
```json
{
  "id": "uuid",
  "chapter_id": "chapter-uuid",
  "image_id": "image-uuid",
  "display_order": 2,
  "caption": "Optional caption text",
  "created_at": "2025-11-24T21:20:00Z",
  "image": {
    "id": "uuid",
    "filename": "unique-filename.jpg",
    "original_filename": "my-image.jpg",
    "file_path": "images/unique-filename.jpg",
    "file_size": 1024000,
    "mime_type": "image/jpeg",
    "width": 1920,
    "height": 1080,
    "uploaded_by": "user-uuid",
    "created_at": "2025-11-24T21:20:00Z",
    "updated_at": "2025-11-24T21:20:00Z",
    "url": "/api/v1/images/{id}/file"
  }
}
```

**Errors:**
- `400`: display_order is required
- `404`: Association not found

---

## Example Usage

### Upload an Image (cURL)
```bash
curl -X POST "http://localhost:8000/api/v1/images/upload" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -F "file=@/path/to/image.jpg"
```

### Upload an Image (JavaScript)
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

const response = await fetch('http://localhost:8000/api/v1/images/upload', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${adminToken}`
  },
  body: formData
});

const data = await response.json();
console.log('Uploaded image:', data);
```

### List Images (JavaScript)
```javascript
const response = await fetch('http://localhost:8000/api/v1/images?page=1&page_size=20', {
  headers: {
    'Authorization': `Bearer ${adminToken}`
  }
});

const data = await response.json();
console.log('Images:', data.images);
console.log('Total:', data.total);
```

### Add Image to Chapter (JavaScript)
```javascript
const response = await fetch(`http://localhost:8000/api/v1/admin/chapters/${chapterId}/images`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${adminToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    image_id: imageId,
    caption: 'A helpful diagram',
    display_order: 0
  })
});

const data = await response.json();
console.log('Chapter image added:', data);
```

### Display an Image (HTML)
```html
<img src="http://localhost:8000/api/v1/images/{image_id}/file" alt="Image" />
```

---

## Error Responses

All endpoints return errors in the following format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

Common HTTP status codes:
- `200`: Success
- `400`: Bad Request (validation error)
- `401`: Unauthorized (missing or invalid token)
- `403`: Forbidden (insufficient permissions)
- `404`: Not Found
- `500`: Internal Server Error

---

## File Upload Constraints

- **Allowed MIME types:**
  - `image/jpeg`
  - `image/jpg`
  - `image/png`
  - `image/gif`
  - `image/webp`

- **Maximum file size:** 5 MB (5,242,880 bytes)

- **Filename handling:**
  - Original filename is preserved in metadata
  - Actual stored filename is a UUID with the original extension
  - Example: `a1b2c3d4-e5f6-7890-abcd-ef1234567890.jpg`

---

## Notes

1. **Image URLs**: The `url` field in responses is a relative path. Prepend your API base URL to get the full URL.

2. **Public Access**: Only the `/images/{image_id}/file` endpoint is public. All other endpoints require admin authentication.

3. **Cascade Deletes**: 
   - Deleting an image removes all chapter associations
   - Deleting a chapter removes all its image associations
   - The actual image files are deleted from disk when the image record is deleted

4. **Pagination**: The list endpoint supports pagination. Use `page` and `page_size` parameters to navigate through results.

5. **Search**: The `search` parameter performs a case-insensitive search on both `filename` and `original_filename` fields.
