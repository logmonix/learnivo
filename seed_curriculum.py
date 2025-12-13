import asyncio, sys
sys.path.append('backend')

from app.core.database import AsyncSessionLocal
from app.services.seed_curriculum import seed_standard_4

async def main():
    async with AsyncSessionLocal() as db:
        await seed_standard_4(db)
        print('✅ Curriculum seeded')

if __name__ == '__main__':
    asyncio.run(main())
