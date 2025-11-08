import aiosqlite
import asyncio

"""Fetch all users from the database."""
async def async_fetch_users():
    async with aiosqlite.connect("database.db") as db:
      async with db.cursor() as cursor:
        cursor.execute("SELECT * FROM users;")
        return await cursor.fetchall()
        
 """Fetch users older than 40."""
async def async_fetch_older_users():
   async with aiosqlite.connect("database.db") as db:
      async with db.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE age > 40 ;")
        return await cursor.fetchall()


def fetch_concurrently():
    results = asyncio.gather(
      async_fetch_users(),
      async_fetch_older_users()
    )
   all_users, older_users = results
    print("All Users:", all_users)
    print("Older Users:", older_users)


if __name__ = "__main__":
         asyncio.run(fetch_concurrently())
