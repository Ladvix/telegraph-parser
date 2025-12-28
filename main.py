import asyncio
import aiohttp
from typing import List

MAX_CONCURRENT_CHECKS = 20
BASE_URL = 'https://telegra.ph/'

async def check_sequence(session: aiohttp.ClientSession, semaphore: asyncio.Semaphore, base_url: str) -> List[str]:
    async with semaphore:
        valid_urls = []
        index = 1
        while True:
            url = base_url
            if index > 1:
                url = f'{base_url}-{index}'

            async with session.get(url) as r:
                if r.status == 200:
                    valid_urls.append(url)
                    index += 1
                else:
                    break

        return valid_urls

async def parse(months: List[str], days: List[str], key_words: List[str]) -> List[str]:
    tasks = []
    connector = aiohttp.TCPConnector(limit=20)
    timeout = aiohttp.ClientTimeout(total=15)
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_CHECKS)

    async with aiohttp.ClientSession(
        connector=connector,
        timeout=timeout,
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36'}
    ) as session:
        tasks = []
        for word in key_words:
            print(f'Search by word "{word}"')
            for month in months:
                for day in days:
                    url = f'{BASE_URL}{word}-{month}-{day}'
                    tasks.append(check_sequence(session, semaphore, url))

        results = await asyncio.gather(*tasks)

    return [url for sublist in results for url in sublist]

async def main():
    days = [f'{i:02d}' for i in range(1, 32)]
    months = [f'{i:02d}' for i in range(1, 13)]
    key_words = ['github']

    valid_urls = await parse(months, days, key_words)
    print(valid_urls)

if __name__ == '__main__':
    asyncio.run(main())