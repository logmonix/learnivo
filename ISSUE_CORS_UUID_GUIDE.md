# 🔧 CORS & UUID Error Resolution Guide

## ❌ Errors Encountered

### Error 1: CORS Policy Blocked
```
Access to XMLHttpRequest at 'http://localhost:8001/api/v1/learning/1/lesson' 
from origin 'http://localhost:5173' has been blocked by CORS policy
```

### Error 2: 500 Internal Server Error
```
invalid input for query argument $1: '1' 
(invalid UUID '1': length must be between 32..36 characters, got 1)
```

## 🔍 Root Causes

### 1. CORS Configuration
**Status**: ✅ Already Configured Correctly

The CORS middleware in `/backend/app/main.py` is properly configured:
```python
origins = [
    "http://localhost:5173",  # Vue Frontend ✅
    "http://127.0.0.1:5173",
    "http://localhost:3000",
]
```

**However**, the backend is running on port **8001** (not 8000) due to Docker port mapping:
```yaml
# docker-compose.yml
backend:
  ports:
    - "8001:8000"  # External:Internal
```

### 2. UUID Validation Error
**Status**: ❌ Frontend Issue

The frontend is passing `chapter_id=1` but the database uses UUIDs:
- ❌ Frontend: `/api/v1/learning/1/lesson`
- ✅ Should be: `/api/v1/learning/d339e776-1bf8-4abe-8a92-ee17b7945858/lesson`

## ✅ Solutions

### Solution 1: Update Frontend to Use Actual UUIDs

The frontend needs to fetch the actual chapter UUID from the API before making the lesson request.

**Current Code (Broken)**:
```javascript
// LessonView.vue or similar
const chapterId = route.params.id; // This is "1"
const response = await api.get(`/learning/${chapterId}/lesson`);
```

**Fixed Code**:
```javascript
// First, get the chapter list with UUIDs
const chapters = await api.get('/curriculum/subjects/{subjectId}/chapters');

// Then use the actual UUID
const chapter = chapters.data.find(c => c.order_index === 1);
const response = await api.get(`/learning/${chapter.id}/lesson`);
```

### Solution 2: Update Router to Use UUIDs

**Frontend Router** (`/frontend/src/router/index.js`):

Instead of using numeric IDs in routes, use the actual chapter UUIDs:

```javascript
// Before (Broken)
{
  path: '/lesson/:id',
  name: 'lesson',
  component: LessonView
}

// After (Fixed)
{
  path: '/lesson/:chapterId',  // This should be a UUID
  name: 'lesson',
  component: LessonView,
  props: true
}
```

### Solution 3: Verify API Base URL

Make sure the frontend is pointing to the correct backend URL.

**Check** `/frontend/src/api/axios.js`:
```javascript
const api = axios.create({
  baseURL: 'http://localhost:8001/api/v1',  // ✅ Port 8001
  // NOT http://localhost:8000  ❌
});
```

## 🧪 Testing

### 1. Get Actual Chapter UUIDs
```bash
# Query database for chapter IDs
docker-compose exec db psql -U learnivo -d learnivo_db -c \
  "SELECT id, title, order_index FROM chapters ORDER BY order_index LIMIT 10;"
```

**Example Output**:
```
                  id                  |        title         | order_index
--------------------------------------+----------------------+-------------
 d339e776-1bf8-4abe-8a92-ee17b7945858 | The Magic of Numbers |           1
 bc2f3b3b-7fa7-4349-8d22-5399035be4d8 | Adding Apples        |           2
 c315ee03-aae4-4a20-a8be-18832b38db7a | Taking Away Toys     |           3
```

### 2. Test API with Correct UUID
```bash
# Use a real UUID from the database
UUID="d339e776-1bf8-4abe-8a92-ee17b7945858"
PROFILE_ID="da739e36-0901-49e9-bbe8-07d2c498f404"

curl "http://localhost:8001/api/v1/learning/${UUID}/lesson?profile_id=${PROFILE_ID}"
```

### 3. Verify CORS Headers
```bash
curl -H "Origin: http://localhost:5173" \
     -H "Access-Control-Request-Method: GET" \
     -H "Access-Control-Request-Headers: Content-Type" \
     -X OPTIONS \
     http://localhost:8001/api/v1/learning/health \
     -v
```

Should return:
```
Access-Control-Allow-Origin: http://localhost:5173
Access-Control-Allow-Methods: *
Access-Control-Allow-Headers: *
```

## 🔧 Quick Fixes

### Option A: Frontend Navigation Fix

Update the component that navigates to lessons:

```vue
<!-- SubjectView.vue or ChapterList.vue -->
<script setup>
const startChapter = async (chapter) => {
  // Use the actual chapter UUID, not order_index
  await router.push({
    name: 'lesson',
    params: { chapterId: chapter.id }  // ✅ Use UUID
  });
};
</script>
```

### Option B: Backend Integer ID Support (Not Recommended)

If you really need to support integer IDs, you'd need to:
1. Add an `order_index` lookup in the backend
2. Convert order_index to UUID before querying

**Not recommended** because UUIDs are more secure and scalable.

## 📋 Checklist

- [ ] Verify backend is running on port 8001
- [ ] Check frontend API baseURL uses port 8001
- [ ] Update frontend to use actual chapter UUIDs
- [ ] Test with a real UUID from database
- [ ] Verify CORS headers are present
- [ ] Check browser console for errors

## 🎯 Expected Behavior

### Before Fix
```
❌ Frontend: /lesson/1
❌ API Call: GET /api/v1/learning/1/lesson
❌ Error: Invalid UUID '1'
```

### After Fix
```
✅ Frontend: /lesson/d339e776-1bf8-4abe-8a92-ee17b7945858
✅ API Call: GET /api/v1/learning/d339e776-1bf8-4abe-8a92-ee17b7945858/lesson
✅ Response: Lesson data returned successfully
```

## 🔍 Debugging Steps

### 1. Check Frontend Route Parameters
```javascript
// In LessonView.vue
console.log('Route params:', route.params);
console.log('Chapter ID:', route.params.chapterId);
// Should log a UUID, not "1"
```

### 2. Check API Request
```javascript
// In LessonView.vue
const loadLesson = async () => {
  console.log('Requesting lesson for chapter:', chapterId);
  console.log('Full URL:', `/learning/${chapterId}/lesson`);
  // Verify the URL contains a UUID
};
```

### 3. Check Backend Logs
```bash
docker-compose logs backend --tail 50 -f
# Watch for incoming requests and errors
```

## 📝 Summary

**Main Issue**: Frontend is using integer IDs (`1`, `2`, `3`) instead of UUIDs

**Solution**: Update frontend to:
1. Fetch chapters with their UUIDs
2. Navigate using the UUID, not order_index
3. Pass UUID to API endpoints

**CORS**: Already configured correctly, just need to use correct port (8001)

---

**Status**: Issue identified, solution documented  
**Next Step**: Update frontend code to use UUIDs  
**Estimated Fix Time**: 10-15 minutes
