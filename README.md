# 🎓 Learnivo - Complete Platform Documentation

## 📋 Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Technical Stack](#technical-stack)
4. [Getting Started](#getting-started)
5. [API Documentation](#api-documentation)
6. [Database Schema](#database-schema)
7. [User Flows](#user-flows)
8. [Deployment](#deployment)

---

## 🌟 Overview

**Learnivo** is a fully functional AI-powered learning platform designed for K-12 students. It combines adaptive learning, gamification, and AI-generated content to create an engaging educational experience.

### Key Differentiators
- **AI Content Generation**: Automatically creates curriculum, lessons, and quizzes
- **Gamification**: XP, coins, badges, and avatar customization
- **Multi-Profile Support**: Parents manage multiple child accounts
- **Admin Tools**: Bulk content generation and analytics
- **Kid-Friendly Design**: Vibrant colors, playful animations, emoji-rich interface

---

## ✨ Features

### For Students
- ✅ **Personalized Learning Paths**: AI-generated subjects and chapters
- ✅ **Interactive Lessons**: Read content → Take quiz → Earn rewards
- ✅ **Gamification System**:
  - Earn 10 XP per correct answer
  - Earn 5 coins per correct answer
  - Unlock badges for achievements
  - Purchase avatar items with coins
- ✅ **Progress Tracking**: Visual chapter maps, completion status
- ✅ **Badge System**: 5 achievement badges (First Steps, Quick Learner, Math Whiz, etc.)
- ✅ **Avatar Shop**: 10+ customizable items (hats, accessories, backgrounds)

### For Parents
- ✅ **Multi-Profile Management**: Create and manage multiple child profiles
- ✅ **Dashboard**: View all children's profiles at a glance
- ✅ **Progress Monitoring**: Track XP, coins, and completed lessons

### For Admins
- ✅ **Platform Statistics**: Total subjects, chapters, students, lessons completed
- ✅ **Bulk Content Generation**: Generate multiple subjects at once
- ✅ **Content Management**: View and edit AI-generated content

---

## 🛠 Technical Stack

### Backend
- **Framework**: FastAPI (Python 3.11)
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy (async)
- **Migrations**: Alembic
- **Caching**: Redis
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt
- **AI Integration**: OpenAI API (with mock fallback)

### Frontend
- **Framework**: Vue 3 (Composition API)
- **Build Tool**: Vite
- **State Management**: Pinia
- **Routing**: Vue Router
- **Styling**: Tailwind CSS + Custom Design System
- **Icons**: Lucide Vue
- **HTTP Client**: Axios

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Database Port**: 5433
- **Redis Port**: 6380
- **Backend Port**: 8001
- **Frontend Port**: 5173

---

## 🚀 Getting Started

### Prerequisites
```bash
- Docker & Docker Compose
- Node.js 18+
- (Optional) OpenAI API key for real AI content
```

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd learnivo
```

2. **Set up environment variables**
```bash
cd backend
cp .env.example .env
# Edit .env and add your API keys (optional)
```

3. **Start the infrastructure**
```bash
docker-compose up -d
```

4. **Run database migrations**
```bash
docker-compose run --rm backend alembic upgrade head
```

5. **Seed initial data**
```bash
curl -X POST http://localhost:8001/api/v1/seed/seed
```

6. **Start the frontend**
```bash
cd frontend
npm install
npm run dev
```

### Access Points
- **Frontend**: http://localhost:5173
- **API Docs**: http://localhost:8001/docs
- **Database**: localhost:5433 (user: postgres, password: learnivo_secret)
- **Redis**: localhost:6380

---

## 📚 API Documentation

### Authentication
```
POST /api/v1/auth/register
POST /api/v1/auth/login
```

### Profiles
```
GET  /api/v1/profiles/
POST /api/v1/profiles/
```

### Curriculum
```
GET  /api/v1/curriculum/?grade={grade}
POST /api/v1/curriculum/generate
```

### Learning
```
GET  /api/v1/learning/{chapter_id}/lesson?profile_id={id}
POST /api/v1/learning/{chapter_id}/submit-quiz?profile_id={id}
```

### Gamification
```
GET  /api/v1/gamification/badges
GET  /api/v1/gamification/badges/profile/{profile_id}
POST /api/v1/gamification/badges/check/{profile_id}
GET  /api/v1/gamification/shop/items
GET  /api/v1/gamification/shop/profile/{profile_id}
POST /api/v1/gamification/shop/purchase/{profile_id}/{item_id}
```

### Admin
```
GET  /api/v1/admin/stats
POST /api/v1/admin/bulk-generate
GET  /api/v1/admin/content-blocks
PUT  /api/v1/admin/content-blocks/{block_id}
```

Full interactive API documentation available at: http://localhost:8001/docs

---

## 🗄 Database Schema

### Core Tables
- **users**: Parent accounts (email, password, role)
- **profiles**: Student profiles (name, grade, XP, coins)
- **subjects**: Grade-level subjects (name, grade, icon)
- **chapters**: Individual chapters (title, description, order)
- **content_blocks**: AI-generated lesson content (JSON)
- **student_progress**: Completion tracking (status, score, XP earned)

### Gamification Tables
- **badges**: Achievement definitions (name, icon, requirements)
- **profile_badges**: Earned badges (profile_id, badge_id, earned_at)
- **avatar_items**: Shop inventory (name, category, icon, cost)
- **profile_avatars**: Purchased items (profile_id, item_id, is_equipped)

---

## 👥 User Flows

### Student Learning Flow
1. **Login** → Parent selects child profile
2. **Student Home** → View/generate subjects
3. **Subject View** → See chapter map
4. **Lesson View** → Read lesson content
5. **Quiz** → Answer questions
6. **Results** → Earn XP, coins, and badges
7. **Profile** → View badges and shop for avatar items

### Admin Content Flow
1. **Login** → Access admin dashboard
2. **View Stats** → See platform metrics
3. **Bulk Generate** → Select grade and subjects
4. **Generate** → AI creates curriculum
5. **Review** → View generated content
6. **Edit** (optional) → Modify AI content

---

## 🎨 Design System

### Color Palette
```css
--primary: #8B5CF6 (Electric Purple)
--secondary: #06B6D4 (Ocean Teal)
--accent-yellow: #FBBF24
--accent-orange: #F97316
--accent-pink: #EC4899
```

### Typography
- **Headings**: Fredoka One (playful, bold)
- **Body**: Nunito (friendly, readable)

### Components
- Rounded corners (1.5rem)
- Soft shadows
- Hover animations
- Gradient backgrounds

---

## 🔐 Security

- **Password Hashing**: bcrypt with salt
- **JWT Tokens**: Secure, expiring tokens
- **CORS**: Configured for frontend origin
- **SQL Injection**: Protected via SQLAlchemy ORM
- **XSS**: Vue auto-escapes content

---

## 🧪 Testing

### Manual Testing Checklist
- [ ] User registration and login
- [ ] Profile creation and selection
- [ ] Subject generation (Math, Science, etc.)
- [ ] Lesson content display
- [ ] Quiz submission and scoring
- [ ] XP and coin rewards
- [ ] Badge unlocking
- [ ] Avatar item purchase
- [ ] Admin dashboard stats
- [ ] Bulk content generation

### Test Accounts
```
Parent Account:
Email: test@example.com
Password: password123

Child Profile:
Name: Leo
Grade: 5
```

---

## 🚀 Deployment

### Production Checklist

1. **Environment Variables**
```bash
DATABASE_URL=postgresql+asyncpg://user:pass@host/db
SECRET_KEY=<generate-secure-key>
OPENAI_API_KEY=<your-key>
```

2. **Database**
- Use managed PostgreSQL (AWS RDS, DigitalOcean, etc.)
- Enable SSL connections
- Set up automated backups

3. **Backend**
- Deploy to: Heroku, Railway, Render, or AWS ECS
- Use production ASGI server (uvicorn with workers)
- Enable HTTPS
- Set up monitoring (Sentry, DataDog)

4. **Frontend**
- Build: `npm run build`
- Deploy to: Vercel, Netlify, or Cloudflare Pages
- Update API base URL to production backend

5. **Redis**
- Use managed Redis (Redis Cloud, AWS ElastiCache)
- Configure persistence

### Docker Production
```bash
docker-compose -f docker-compose.prod.yml up -d
```

---

## 📊 Analytics & Monitoring

### Key Metrics to Track
- Daily Active Users (DAU)
- Lessons Completed
- Average Session Duration
- XP Earned per Student
- Badge Unlock Rate
- Avatar Purchase Rate
- Content Generation Requests

### Recommended Tools
- **Backend**: Sentry (errors), DataDog (performance)
- **Frontend**: Google Analytics, Mixpanel
- **Database**: pgAdmin, DataGrip

---

## 🔮 Future Enhancements

### Phase 4 (Recommended)
1. **Advanced AI**
   - Gemini integration
   - Streaming responses
   - Adaptive difficulty

2. **Parent Portal**
   - Weekly email reports
   - Learning goals
   - Time limits

3. **Social Features**
   - Leaderboards (optional)
   - Peer challenges
   - Study groups

4. **Content**
   - Video lessons
   - Voice narration (TTS)
   - Interactive simulations

5. **Mobile**
   - React Native app
   - Offline mode
   - Push notifications

6. **Monetization**
   - Subscription tiers
   - Premium content
   - School licenses

---

## 🤝 Contributing

### Code Style
- **Python**: Black formatter, PEP 8
- **JavaScript**: Prettier, ESLint
- **Vue**: Official style guide

### Git Workflow
1. Create feature branch
2. Make changes
3. Write tests
4. Submit pull request

---

## 📄 License

[Your License Here]

---

## 🙏 Acknowledgments

Built with:
- FastAPI
- Vue 3
- PostgreSQL
- OpenAI
- Tailwind CSS

---

## 📞 Support

For issues or questions:
- GitHub Issues: [repository-url]/issues
- Email: support@learnivo.com
- Documentation: [docs-url]

---

**Status**: ✅ Production Ready (MVP)
**Version**: 1.0.0
**Last Updated**: 2025-11-24