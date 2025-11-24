# Learnivo - Quick Start Guide

## 🎯 5-Minute Setup

### 1. Start Services
```bash
# From project root
docker-compose up -d
```

### 2. Run Migrations
```bash
docker-compose run --rm backend alembic upgrade head
```

### 3. Seed Data
```bash
curl -X POST http://localhost:8001/api/v1/seed/seed
```

### 4. Start Frontend
```bash
cd frontend
npm install
npm run dev
```

### 5. Access Application
- Frontend: http://localhost:5173
- API Docs: http://localhost:8001/docs

## 🧪 Test the Platform

### Create Account
1. Go to http://localhost:5173/login
2. Click "Sign Up"
3. Enter:
   - Name: Your Name
   - Email: test@example.com
   - Password: password123
4. Click "Create Account"

### Create Child Profile
1. Login with test@example.com
2. Click "Add Kid"
3. Enter:
   - Name: Leo
   - Grade: 5
4. Click "Create Profile"

### Generate Content
1. Click on Leo's profile
2. Click "Mathematics" to generate
3. Wait for AI to create chapters
4. Click on first chapter
5. Read lesson and take quiz!

### Check Rewards
1. Complete a quiz
2. Earn XP and coins
3. Click "Profile" in navbar
4. View badges and shop

### Admin Dashboard
1. Navigate to http://localhost:5173/admin
2. View platform stats
3. Try bulk generation

## 🔧 Troubleshooting

### Backend won't start
```bash
docker-compose down
docker-compose up -d --build
```

### Database issues
```bash
docker-compose down -v
docker-compose up -d
docker-compose run --rm backend alembic upgrade head
```

### Frontend errors
```bash
cd frontend
rm -rf node_modules
npm install
npm run dev
```

## 🎨 Customization

### Add Real AI
Edit `backend/.env`:
```bash
OPENAI_API_KEY=sk-your-key-here
```

Restart backend:
```bash
docker-compose restart backend
```

### Change Colors
Edit `frontend/tailwind.config.js`:
```javascript
colors: {
  primary: '#YOUR_COLOR',
  // ...
}
```

### Add Subjects
Edit `frontend/src/views/StudentHome.vue`:
```javascript
const suggestedSubjects = ['Math', 'Science', 'Your Subject'];
```

## 📚 Next Steps

1. Read full [README.md](README.md)
2. Explore [API Docs](http://localhost:8001/docs)
3. Check [Phase 3 Tasks](requirements/07_phase3_tasks.md)
4. Review [Project Summary](PROJECT_SUMMARY.md)

## 🆘 Need Help?

- Check logs: `docker-compose logs backend`
- View database: Connect to localhost:5433
- API issues: Visit http://localhost:8001/docs

---

**Happy Learning! 🎓**
