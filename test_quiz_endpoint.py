import asyncio, subprocess, sys, os

# Ensure the backend package is on PYTHONPATH
sys.path.append('backend')

from app.core.database import AsyncSessionLocal
from app.models.curriculum import Chapter
from app.models.user import Profile
from sqlalchemy import select

async def get_ids():
    async with AsyncSessionLocal() as db:
        ch_res = await db.execute(select(Chapter).limit(1))
        chapter = ch_res.scalars().first()
        prof_res = await db.execute(select(Profile).limit(1))
        profile = prof_res.scalars().first()
        return (chapter.id if chapter else None, profile.id if profile else None)

async def main():
    chapter_id, profile_id = await get_ids()
    print('chapter_id:', chapter_id)
    print('profile_id:', profile_id)
    if chapter_id and profile_id:
        url = f'http://127.0.0.1:8000/api/v1/learning/{chapter_id}/quiz?profile_id={profile_id}'
        result = subprocess.run(['curl', '-s', url], capture_output=True, text=True)
        print('Response:', result.stdout)
    else:
        print('No chapter or profile found in DB')

if __name__ == '__main__':
    asyncio.run(main())
