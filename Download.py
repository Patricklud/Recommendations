import asyncio
import aiohttp
from ratelimit import limits, sleep_and_retry

class APIManager:
    def __init__(self):
        self.apis = {
            'music': {'url': 'https://api.spotify.com/v1/', 'limit': 100, 'period': 60},
            'games': {'url': 'https://api.igdb.com/v4/', 'limit': 50, 'period': 60},
            'movies': {'url': 'https://api.themoviedb.org/3/', 'limit': 40, 'period': 60}
        }

    @sleep_and_retry
    @limits(calls=100, period=60)
    async def fetch_music(self, session, endpoint):
        async with session.get(f"{self.apis['music']['url']}{endpoint}") as response:
            return await response.json()

    @sleep_and_retry
    @limits(calls=50, period=60)
    async def fetch_games(self, session, endpoint):
        async with session.get(f"{self.apis['games']['url']}{endpoint}") as response:
            return await response.json()

    @sleep_and_retry
    @limits(calls=40, period=60)
    async def fetch_movies(self, session, endpoint):
        async with session.get(f"{self.apis['movies']['url']}{endpoint}") as response:
            return await response.json()

    async def fetch_all(self):
        async with aiohttp.ClientSession() as session:
            music_task = asyncio.create_task(self.fetch_music(session, 'tracks'))
            games_task = asyncio.create_task(self.fetch_games(session, 'games'))
            movies_task = asyncio.create_task(self.fetch_movies(session, 'movie/popular'))

            results = await asyncio.gather(music_task, games_task, movies_task)
            return results

async def main():
    manager = APIManager()
    results = await manager.fetch_all()
    print(results)

asyncio.run(main())
