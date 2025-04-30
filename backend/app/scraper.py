import asyncio, re
from dataclasses import dataclass
import trafilatura

@dataclass
class Article:
    url: str
    title: str
    text: str

async def scrape(url: str) -> Article:
    loop = asyncio.get_event_loop()
    downloaded = await loop.run_in_executor(None, trafilatura.fetch_url, url)
    text = trafilatura.extract(downloaded, include_comments=False) or ""
    title_match = re.search(r"<title>(.*?)</title>", downloaded or "", re.I|re.S)
    title = title_match.group(1).strip() if title_match else ""
    return Article(url=url, title=title, text=text)
