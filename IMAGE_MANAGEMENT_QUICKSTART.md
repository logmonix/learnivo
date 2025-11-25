# Image Management Quick Start Guide

## 🚀 Getting Started

This guide will help you quickly set up and test the image management system.

## Prerequisites

- Docker and Docker Compose installed
- Python 3.9+ with virtual environment
- PostgreSQL database running (via Docker)

## Step 1: Start the Database

```bash
cd /Users/j41304/Documents/projects/learnivo
docker-compose up -d
```

Wait a few seconds for the database to initialize.

## Step 2: Activate Virtual Environment

```bash
source .venv/bin/activate
```

## Step 3: Run Database Migration

```bash
cd backend
alembic upgrade head
```

You should see output indicating the migration was successful:
```
INFO  [alembic.runtime.migration] Running upgrade 47e7404de0e1 -> 8f9e5b2c3d4a, Add image management tables
```

## Step 4: Start the Backend Server

```bash
# From the backend directory
uvicorn app.main:app --reload --port 8000
```

Or if you prefer to use Docker:
```bash
# From the project root
docker-compose up backend
```

## Step 5: Access API Documentation

Open your browser and navigate to:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Step 6: Get an Admin Token

You'll need an admin token to test the image management endpoints.

### Option A: Use existing admin account
If you already have an admin account, log in via the API:

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@learnivo.com&password=your_password"
```

### Option B: Create a new admin user
Use the dev endpoint (if available):

```bash
curl -X POST "http://localhost:8000/api/v1/dev/create-admin" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@test.com",
    "password": "admin123",
    "full_name": "Admin User"
  }'
```

Save the `access_token` from the response.

## Step 7: Test Image Upload

### Using cURL

```bash
# Replace YOUR_TOKEN with the actual token
curl -X POST "http://localhost:8000/api/v1/images/upload" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@/path/to/your/image.jpg"
```

### Using Swagger UI

1. Go to http://localhost:8000/docs
2. Click the "Authorize" button (lock icon)
3. Enter your token in the format: `Bearer YOUR_TOKEN`
4. Click "Authorize"
5. Find the `POST /api/v1/images/upload` endpoint
6. Click "Try it out"
7. Choose a file
8. Click "Execute"

## Step 8: View Uploaded Images

### List all images

```bash
curl -X GET "http://localhost:8000/api/v1/images?page=1&page_size=20" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### View an image in browser

After uploading, you'll get an `id` in the response. Use it to view the image:

```
http://localhost:8000/api/v1/images/{image_id}/file
```

Example:
```
http://localhost:8000/api/v1/images/a1b2c3d4-e5f6-7890-abcd-ef1234567890/file
```

## Step 9: Associate Image with Chapter

First, get a chapter ID from your database or create one:

```bash
# List subjects
curl -X GET "http://localhost:8000/api/v1/curriculum/subjects" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Get chapters for a subject
curl -X GET "http://localhost:8000/api/v1/admin/subjects/{subject_id}/chapters" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

Then associate an image:

```bash
curl -X POST "http://localhost:8000/api/v1/admin/chapters/{chapter_id}/images" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "image_id": "your-image-uuid",
    "caption": "A helpful diagram explaining fractions",
    "display_order": 0
  }'
```

## Step 10: View Chapter Images

```bash
curl -X GET "http://localhost:8000/api/v1/admin/chapters/{chapter_id}/images" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Common Tasks

### Upload Multiple Images

Create a simple script:

```bash
#!/bin/bash
TOKEN="your-token-here"

for file in /path/to/images/*.jpg; do
  echo "Uploading $file..."
  curl -X POST "http://localhost:8000/api/v1/images/upload" \
    -H "Authorization: Bearer $TOKEN" \
    -F "file=@$file"
  echo ""
done
```

### Search Images

```bash
curl -X GET "http://localhost:8000/api/v1/images?search=diagram" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Delete an Image

```bash
curl -X DELETE "http://localhost:8000/api/v1/images/{image_id}" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Reorder Chapter Images

```bash
curl -X PUT "http://localhost:8000/api/v1/admin/chapters/{chapter_id}/images/{image_id}/order" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "display_order": 2
  }'
```

## Troubleshooting

### Issue: "role 'learnivo' does not exist"

**Solution**: The database hasn't fully started. Wait a few more seconds and try again.

```bash
docker-compose restart db
sleep 5
cd backend && alembic upgrade head
```

### Issue: "File too large"

**Solution**: The maximum file size is 5MB. Compress your image or use a smaller file.

### Issue: "Invalid file type"

**Solution**: Only JPEG, PNG, GIF, and WebP files are allowed. Convert your image to one of these formats.

### Issue: "Unauthorized"

**Solution**: Make sure you're including the Bearer token in the Authorization header:
```
Authorization: Bearer YOUR_TOKEN
```

### Issue: "Image not found on disk"

**Solution**: Check that the uploads directory exists and has proper permissions:
```bash
ls -la backend/uploads/images/
chmod 755 backend/uploads/images/
```

## File Locations

- **Uploaded images**: `/backend/uploads/images/`
- **Database**: PostgreSQL running in Docker on port 5433
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Validation Rules

- **File types**: JPEG, JPG, PNG, GIF, WebP
- **Max file size**: 5 MB (5,242,880 bytes)
- **Filename**: Automatically generated UUID with original extension
- **Dimensions**: Automatically extracted and stored

## Database Schema

### images table
- `id` (UUID) - Primary key
- `filename` (String) - Unique storage filename
- `original_filename` (String) - Original upload name
- `file_path` (String) - Relative path
- `file_size` (Integer) - Size in bytes
- `mime_type` (String) - MIME type
- `width` (Integer) - Image width in pixels
- `height` (Integer) - Image height in pixels
- `uploaded_by` (UUID) - Foreign key to users
- `created_at` (DateTime) - Upload timestamp
- `updated_at` (DateTime) - Last update timestamp

### chapter_images table
- `id` (UUID) - Primary key
- `chapter_id` (UUID) - Foreign key to chapters
- `image_id` (UUID) - Foreign key to images
- `display_order` (Integer) - Order in chapter
- `caption` (Text) - Optional caption
- `created_at` (DateTime) - Association timestamp

## Next Steps

1. **Test all endpoints** using Swagger UI
2. **Upload sample images** for your chapters
3. **Associate images with chapters** to prepare for content generation
4. **Build frontend components** to provide a user-friendly interface

## Support

For more detailed information, see:
- `API_IMAGE_MANAGEMENT.md` - Complete API reference
- `SPRINT_3_PROGRESS.md` - Implementation details
- `SPRINT_3_SUMMARY.md` - Overview and architecture

## Example Workflow

Here's a complete workflow from start to finish:

```bash
# 1. Start services
docker-compose up -d
source .venv/bin/activate

# 2. Run migration
cd backend
alembic upgrade head

# 3. Start server
uvicorn app.main:app --reload --port 8000

# 4. In another terminal, get admin token
TOKEN=$(curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@learnivo.com&password=your_password" \
  | jq -r '.access_token')

# 5. Upload an image
IMAGE_ID=$(curl -X POST "http://localhost:8000/api/v1/images/upload" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@diagram.jpg" \
  | jq -r '.id')

# 6. Get a chapter ID (example)
CHAPTER_ID="your-chapter-uuid"

# 7. Associate image with chapter
curl -X POST "http://localhost:8000/api/v1/admin/chapters/$CHAPTER_ID/images" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"image_id\": \"$IMAGE_ID\",
    \"caption\": \"Helpful diagram\",
    \"display_order\": 0
  }"

# 8. View the image
echo "Image URL: http://localhost:8000/api/v1/images/$IMAGE_ID/file"
```

---

**Ready to go!** Start with Step 1 and work your way through. Happy coding! 🚀
