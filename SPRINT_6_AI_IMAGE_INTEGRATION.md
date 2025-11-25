# Sprint 6: AI Integration with Images

## 🎯 Objectives
Integrate AI capabilities with the image management system to automatically generate educational content, analyze images, create descriptions, and enhance the learning experience with intelligent image-based features.

## 📋 Features

### Core Features
1. ✅ AI-powered image analysis and tagging
2. ✅ Automatic alt text generation for accessibility
3. ✅ Image-based content generation (lessons, quizzes)
4. ✅ Visual concept extraction
5. ✅ Diagram interpretation and explanation
6. ✅ Smart image recommendations for chapters
7. ✅ Image quality assessment
8. ✅ Duplicate image detection

## 🗄️ Database Schema

### ImageAnalysis Model
```python
class ImageAnalysis(Base):
    __tablename__ = "image_analysis"
    
    id = UUID (Primary Key)
    image_id = UUID (Foreign Key to images)
    
    # AI-generated metadata
    description = Text  # AI-generated description
    alt_text = String  # Accessibility text
    tags = JSON  # List of detected tags/concepts
    
    # Visual analysis
    detected_objects = JSON  # Objects detected in image
    detected_text = Text  # OCR extracted text
    color_palette = JSON  # Dominant colors
    
    # Educational context
    educational_concepts = JSON  # Math concepts, science topics, etc.
    difficulty_level = String  # 'beginner', 'intermediate', 'advanced'
    suggested_subjects = JSON  # Subjects this image is relevant for
    
    # Quality metrics
    quality_score = Float  # 0-100
    clarity_score = Float  # 0-100
    educational_value_score = Float  # 0-100
    
    # AI model info
    ai_model_used = String  # e.g., "gpt-4-vision", "gemini-pro-vision"
    analyzed_at = DateTime
    
    created_at = DateTime
    updated_at = DateTime
```

### AIGeneratedContent Model
```python
class AIGeneratedContent(Base):
    __tablename__ = "ai_generated_content"
    
    id = UUID (Primary Key)
    chapter_id = UUID (Foreign Key to chapters)
    
    # Source images
    source_image_ids = JSON  # List of image IDs used for generation
    
    # Generated content
    content_type = String  # 'lesson', 'explanation', 'quiz', 'flashcard'
    content_data = JSON  # The actual generated content
    
    # Generation parameters
    prompt_used = Text
    ai_model = String
    temperature = Float
    
    # Quality & review
    quality_score = Float
    requires_review = Boolean (default: True)
    reviewed_by = UUID (Foreign Key to users, nullable)
    review_status = String  # 'pending', 'approved', 'rejected', 'edited'
    
    # Usage tracking
    times_used = Integer (default: 0)
    student_feedback_score = Float (nullable)
    
    created_at = DateTime
    updated_at = DateTime
```

### ImageRecommendation Model
```python
class ImageRecommendation(Base):
    __tablename__ = "image_recommendations"
    
    id = UUID (Primary Key)
    chapter_id = UUID (Foreign Key to chapters)
    image_id = UUID (Foreign Key to images)
    
    # Recommendation details
    relevance_score = Float  # 0-100
    reason = Text  # Why this image is recommended
    
    # AI analysis
    matching_concepts = JSON  # Concepts that match chapter
    ai_confidence = Float  # 0-100
    
    # Status
    status = String  # 'suggested', 'accepted', 'rejected'
    reviewed_by = UUID (Foreign Key to users, nullable)
    
    created_at = DateTime
```

## 🔧 Backend Implementation

### Phase 1: Image Analysis Service

#### 1.1 AI Vision Service
**File**: `/backend/app/services/ai_vision_service.py`

Functions:
```python
# Image analysis
async def analyze_image(image_id: UUID) -> ImageAnalysis:
    """
    Analyze image using AI vision model.
    - Generate description
    - Extract tags and concepts
    - Detect objects
    - Perform OCR
    - Assess quality
    """

async def generate_alt_text(image_id: UUID) -> str:
    """Generate accessibility-friendly alt text."""

async def extract_educational_concepts(image_id: UUID) -> List[str]:
    """Extract educational concepts from image."""

async def detect_diagram_type(image_id: UUID) -> str:
    """Identify if image is a diagram and what type."""

async def assess_image_quality(image_id: UUID) -> Dict:
    """Assess technical and educational quality."""

# Batch operations
async def batch_analyze_images(image_ids: List[UUID]):
    """Analyze multiple images in batch."""
```

#### 1.2 Content Generation Service
**File**: `/backend/app/services/ai_content_generator.py`

Functions:
```python
# Content generation with images
async def generate_lesson_from_images(
    chapter_id: UUID,
    image_ids: List[UUID],
    topic: str,
    difficulty: str
) -> Dict:
    """Generate lesson content incorporating images."""

async def generate_quiz_from_diagram(
    image_id: UUID,
    question_count: int = 5
) -> Dict:
    """Generate quiz questions based on diagram."""

async def explain_diagram(image_id: UUID) -> str:
    """Generate detailed explanation of a diagram."""

async def create_flashcards_from_image(
    image_id: UUID,
    card_count: int = 10
) -> List[Dict]:
    """Create flashcards based on image content."""

async def generate_image_based_exercise(
    image_id: UUID,
    exercise_type: str
) -> Dict:
    """Generate practice exercises using image."""
```

#### 1.3 Image Recommendation Service
**File**: `/backend/app/services/image_recommendation_service.py`

Functions:
```python
# Recommendations
async def recommend_images_for_chapter(
    chapter_id: UUID,
    limit: int = 10
) -> List[ImageRecommendation]:
    """Recommend relevant images for a chapter."""

async def find_similar_images(
    image_id: UUID,
    limit: int = 5
) -> List[UUID]:
    """Find visually or conceptually similar images."""

async def suggest_missing_visuals(chapter_id: UUID) -> List[str]:
    """Suggest what types of images would enhance chapter."""

async def match_images_to_concepts(
    concepts: List[str]
) -> List[UUID]:
    """Find images matching specific concepts."""
```

#### 1.4 Duplicate Detection Service
**File**: `/backend/app/services/duplicate_detection_service.py`

Functions:
```python
# Duplicate detection
async def detect_duplicate_images(
    image_id: UUID,
    threshold: float = 0.95
) -> List[UUID]:
    """Find duplicate or near-duplicate images."""

async def generate_image_hash(image_id: UUID) -> str:
    """Generate perceptual hash for image."""

async def compare_images(
    image_id_1: UUID,
    image_id_2: UUID
) -> float:
    """Compare similarity between two images (0-1)."""
```

### Phase 2: API Endpoints

#### 2.1 Image Analysis Endpoints
**File**: `/backend/app/api/v1/ai_vision.py`

```python
# Admin endpoints
POST   /api/v1/admin/images/{id}/analyze         # Analyze single image
POST   /api/v1/admin/images/batch-analyze        # Batch analyze
GET    /api/v1/admin/images/{id}/analysis        # Get analysis results
PUT    /api/v1/admin/images/{id}/analysis        # Update analysis
DELETE /api/v1/admin/images/{id}/analysis        # Delete analysis

# Public endpoints
GET    /api/v1/images/{id}/alt-text              # Get alt text
GET    /api/v1/images/{id}/tags                  # Get tags
GET    /api/v1/images/{id}/concepts              # Get educational concepts
```

#### 2.2 AI Content Generation Endpoints
**File**: `/backend/app/api/v1/ai_content.py`

```python
# Admin endpoints
POST   /api/v1/admin/ai/generate-lesson          # Generate lesson with images
POST   /api/v1/admin/ai/generate-quiz            # Generate quiz from diagram
POST   /api/v1/admin/ai/explain-diagram          # Explain diagram
POST   /api/v1/admin/ai/generate-flashcards      # Generate flashcards
POST   /api/v1/admin/ai/generate-exercise        # Generate exercise

# Content management
GET    /api/v1/admin/ai/generated-content        # List generated content
GET    /api/v1/admin/ai/generated-content/{id}   # Get content details
PUT    /api/v1/admin/ai/generated-content/{id}   # Edit content
POST   /api/v1/admin/ai/generated-content/{id}/approve  # Approve
DELETE /api/v1/admin/ai/generated-content/{id}   # Delete
```

#### 2.3 Image Recommendation Endpoints
**File**: `/backend/app/api/v1/image_recommendations.py`

```python
# Admin endpoints
GET    /api/v1/admin/chapters/{id}/image-recommendations  # Get recommendations
POST   /api/v1/admin/chapters/{id}/generate-recommendations  # Generate new
POST   /api/v1/admin/recommendations/{id}/accept  # Accept recommendation
POST   /api/v1/admin/recommendations/{id}/reject  # Reject recommendation

# Image similarity
GET    /api/v1/admin/images/{id}/similar         # Find similar images
GET    /api/v1/admin/images/{id}/duplicates      # Find duplicates
```

### Phase 3: AI Integration

#### 3.1 OpenAI GPT-4 Vision Integration
**File**: `/backend/app/integrations/openai_vision.py`

```python
class OpenAIVisionClient:
    async def analyze_image(self, image_url: str, prompt: str) -> Dict
    async def generate_alt_text(self, image_url: str) -> str
    async def extract_concepts(self, image_url: str, subject: str) -> List[str]
    async def explain_diagram(self, image_url: str) -> str
    async def generate_quiz_questions(self, image_url: str, count: int) -> List[Dict]
```

#### 3.2 Google Gemini Vision Integration
**File**: `/backend/app/integrations/gemini_vision.py`

```python
class GeminiVisionClient:
    async def analyze_image(self, image_path: str) -> Dict
    async def generate_description(self, image_path: str) -> str
    async def detect_objects(self, image_path: str) -> List[str]
    async def extract_text_ocr(self, image_path: str) -> str
    async def assess_educational_value(self, image_path: str, subject: str) -> float
```

#### 3.3 Image Processing Integration
**File**: `/backend/app/integrations/image_processing.py`

```python
class ImageProcessor:
    def extract_dominant_colors(self, image_path: str) -> List[str]
    def calculate_quality_score(self, image_path: str) -> float
    def generate_perceptual_hash(self, image_path: str) -> str
    def compare_images(self, image1_path: str, image2_path: str) -> float
    def detect_blur(self, image_path: str) -> float
    def detect_brightness(self, image_path: str) -> float
```

## 🎨 Frontend Implementation

### Phase 1: Image Analysis UI

#### 1.1 Image Analysis Panel
**File**: `/frontend/src/components/admin/ImageAnalysisPanel.vue`

Features:
- Display AI-generated description
- Show detected tags
- List educational concepts
- Display quality scores
- Show detected objects
- OCR text display
- Edit analysis button
- Re-analyze button

#### 1.2 Batch Analysis Tool
**File**: `/frontend/src/components/admin/BatchImageAnalysis.vue`

Features:
- Select multiple images
- Start batch analysis
- Progress indicator
- Results summary
- Error handling
- Export results

### Phase 2: AI Content Generator

#### 2.1 AI Content Generator Wizard
**File**: `/frontend/src/views/admin/AIContentGenerator.vue`

Features:
- Step 1: Select content type (lesson, quiz, flashcards)
- Step 2: Select images
- Step 3: Configure parameters (difficulty, length, style)
- Step 4: Generate content
- Step 5: Review and edit
- Step 6: Approve and publish

#### 2.2 Diagram Explainer
**File**: `/frontend/src/components/admin/DiagramExplainer.vue`

Features:
- Upload/select diagram
- Generate explanation button
- AI-generated explanation display
- Edit explanation
- Add to chapter button
- Save as content block

#### 2.3 Quiz Generator from Image
**File**: `/frontend/src/components/admin/ImageQuizGenerator.vue`

Features:
- Select diagram/image
- Set question count
- Set difficulty level
- Generate quiz button
- Preview questions
- Edit questions
- Save quiz

### Phase 3: Image Recommendations

#### 3.1 Image Recommendation Panel
**File**: `/frontend/src/components/admin/ImageRecommendations.vue`

Features:
- List of recommended images
- Relevance score display
- Reason for recommendation
- Preview image
- Accept/reject buttons
- View similar images
- Add to chapter button

#### 3.2 Smart Image Picker
**File**: `/frontend/src/components/admin/SmartImagePicker.vue`

Features:
- Search by concept
- AI-powered suggestions
- Filter by relevance
- Sort by quality score
- Preview with analysis
- Select multiple
- Add to chapter

### Phase 4: Quality Dashboard

#### 4.1 Image Quality Dashboard
**File**: `/frontend/src/views/admin/ImageQualityDashboard.vue`

Features:
- Quality score distribution
- Low-quality images list
- Duplicate images list
- Missing alt text list
- Untagged images list
- Bulk actions
- Quality improvement suggestions

## 🤖 AI Prompts & Templates

### Image Analysis Prompt
```
Analyze this educational image and provide:
1. A detailed description (2-3 sentences)
2. Educational concepts depicted (list)
3. Suggested subject areas (list)
4. Difficulty level (beginner/intermediate/advanced)
5. Educational value score (0-100)
6. Accessibility-friendly alt text (1 sentence)

Image context: {chapter_title}, {subject}, {grade_level}
```

### Lesson Generation Prompt
```
Generate a comprehensive lesson on "{topic}" for grade {grade_level} students.

Use the following images as visual aids:
{image_descriptions}

Requirements:
- Length: {word_count} words
- Difficulty: {difficulty_level}
- Include: Introduction, main content, examples, summary
- Reference images at appropriate points
- Use markdown formatting
- Include 3-5 key takeaways
```

### Quiz Generation Prompt
```
Create {question_count} multiple-choice questions based on this diagram:

{diagram_description}

Requirements:
- Difficulty: {difficulty_level}
- 4 options per question
- Include explanations for correct answers
- Vary question types (identification, analysis, application)
- Reference specific parts of the diagram
```

### Diagram Explanation Prompt
```
Explain this {diagram_type} diagram in detail for {grade_level} students:

{diagram_description}

Include:
1. Overview of what the diagram shows
2. Explanation of each component
3. How the components relate to each other
4. Real-world applications or examples
5. Common misconceptions to avoid

Use clear, age-appropriate language.
```

## 📊 Quality Scoring Algorithm

### Image Quality Score (0-100)
```python
def calculate_image_quality_score(image_path: str) -> float:
    # Technical quality (0-40 points)
    resolution_score = assess_resolution(image_path) * 10
    clarity_score = assess_clarity(image_path) * 10
    brightness_score = assess_brightness(image_path) * 10
    color_quality = assess_color_quality(image_path) * 10
    
    # Educational value (0-40 points)
    concept_clarity = assess_concept_clarity(image_path) * 20
    relevance_score = assess_educational_relevance(image_path) * 20
    
    # Accessibility (0-20 points)
    has_alt_text = 10 if has_alt_text(image_path) else 0
    text_readability = assess_text_readability(image_path) * 10
    
    total = (
        resolution_score +
        clarity_score +
        brightness_score +
        color_quality +
        concept_clarity +
        relevance_score +
        has_alt_text +
        text_readability
    )
    
    return min(100, total)
```

## 🔄 Automated Workflows

### Workflow 1: Auto-Analyze on Upload
```
1. Image uploaded
2. Trigger AI analysis
3. Generate alt text
4. Extract tags and concepts
5. Calculate quality score
6. If quality < 50: Flag for review
7. If quality >= 80: Auto-approve
8. Generate recommendations for relevant chapters
```

### Workflow 2: Smart Content Generation
```
1. Admin selects chapter
2. System analyzes chapter content
3. Identifies missing visual aids
4. Recommends relevant images from library
5. Suggests AI-generated content types
6. Admin selects images and content type
7. AI generates content
8. Admin reviews and approves
9. Content published to chapter
```

### Workflow 3: Duplicate Detection
```
1. New image uploaded
2. Generate perceptual hash
3. Compare with existing images
4. If similarity > 95%: Flag as duplicate
5. Notify admin
6. Admin decides: keep, replace, or delete
```

## 🧪 Testing Checklist

### Backend
- [ ] Analyze image with GPT-4 Vision
- [ ] Analyze image with Gemini Vision
- [ ] Generate alt text
- [ ] Extract educational concepts
- [ ] Detect diagram type
- [ ] Generate lesson from images
- [ ] Generate quiz from diagram
- [ ] Explain diagram
- [ ] Recommend images for chapter
- [ ] Find similar images
- [ ] Detect duplicate images
- [ ] Batch analyze images
- [ ] Calculate quality scores

### Frontend
- [ ] View image analysis
- [ ] Batch analyze images
- [ ] Generate AI content wizard
- [ ] Explain diagram
- [ ] Generate quiz from image
- [ ] View image recommendations
- [ ] Accept/reject recommendations
- [ ] Smart image picker
- [ ] Quality dashboard
- [ ] Duplicate detection UI

## 🚀 Deployment Steps

1. **Install AI Dependencies**
   ```bash
   pip install openai google-generativeai pillow opencv-python imagehash
   ```

2. **Configure API Keys**
   ```bash
   # .env file
   OPENAI_API_KEY=your_openai_key
   GEMINI_API_KEY=your_gemini_key
   ```

3. **Database Migration**
   ```bash
   alembic revision --autogenerate -m "Add AI image analysis"
   alembic upgrade head
   ```

4. **Analyze Existing Images**
   ```bash
   python scripts/batch_analyze_existing_images.py
   ```

5. **Set Up Webhooks** (optional)
   - Configure webhooks for real-time analysis
   - Set up background job queue (Celery/Redis)

## 📈 Success Metrics

- ✅ All images have AI-generated alt text
- ✅ 80%+ images have quality scores
- ✅ AI-generated content approval rate > 70%
- ✅ Duplicate detection accuracy > 95%
- ✅ Image recommendation relevance > 80%
- ✅ Time saved on content creation > 50%
- ✅ Student engagement with AI content

## 💰 Cost Optimization

### API Usage Optimization
1. **Batch Processing**: Analyze multiple images in single API call
2. **Caching**: Store analysis results, don't re-analyze
3. **Selective Analysis**: Only analyze new/updated images
4. **Model Selection**: Use cheaper models for simple tasks
5. **Rate Limiting**: Prevent excessive API calls

### Cost Estimates (Monthly)
- **Image Analysis** (1000 images): ~$20-30
- **Content Generation** (100 lessons): ~$50-100
- **Quiz Generation** (500 quizzes): ~$30-50
- **Total Estimated**: ~$100-180/month

## 🎯 Future Enhancements

1. **Custom AI Models**: Train custom models for specific subjects
2. **Multi-modal Learning**: Combine images, text, and video
3. **Interactive Diagrams**: AI-powered interactive visualizations
4. **Personalized Content**: Generate content based on student level
5. **Real-time Feedback**: AI tutoring with image-based explanations

---

**Status**: Ready for implementation
**Dependencies**: OpenAI API, Google Gemini API, Image processing libraries
**Estimated Time**: 3-4 weeks
