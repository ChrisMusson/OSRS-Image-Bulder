import aiohttp
import asyncio
from osrsbox import items_api


async def fetch(session, item):
    async with session.get(f"https://www.osrsbox.com/osrsbox-db/items-icons/{item.id}.png") as response:
        with open(f"images/{item.id}.png", "wb") as handler:
            handler.write(await response.read())

async def main():
    items = items_api.load()
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[fetch(session, item) for item in items])

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())