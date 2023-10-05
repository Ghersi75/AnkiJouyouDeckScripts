import asyncio
import aiohttp
import json

async def fetch(session, url):
    async with session.get(url) as response:
        content = await response.text()
        if response.status == 200 and response.content_type == 'application/json':
            # print(f"Content for {url}:\n{content}")
            # print(f"Done with: {url}")
            if content:
                # print(json.loads(content))
                return json.loads(content)
            return await response.json()
        if response.status == 429:
            print("Sleep zzzz")
            await asyncio.sleep(1)
            return await fetch(session, url)
        else:
            print(f"Error with URL {url}. Status: {response.status}, Content-Type: {response.content_type}")
            return None


async def asyncRequests(request_list):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, req) for req in request_list]
        results = await asyncio.gather(*tasks)
        return results

def test():
    url = "https://kanjiapi.dev/v1/kanji/"
    kanji = ['軟', '郊', '隅', '隻', '邸']
    requests = []
    for i in kanji:
        req = f"{url}{i}"
        requests.append(req)
    res = asyncio.run(asyncRequests(requests))

    print(res)

# test()