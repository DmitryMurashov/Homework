import aiohttp
import asyncio
import json
import bs4


async def async_get_html(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def parse_page(html: str) -> list:
    soup = bs4.BeautifulSoup(html, "html.parser")
    all_news = soup.select("li[class=parts-page__item]")
    json_news = []
    for news in all_news:
        title = news.find("h3").text
        category = news.find("span", class_="card-full-news__rubric")
        if category:
            category = category.text
        else:
            category = ""
        json_news.append({
            "title": title,
            "category": category
        })
    return json_news


async def parse_html(page_count: int) -> None:
    data = []
    url = f"https://lenta.ru/parts/news/"
    tasks = [async_get_html(url + str(page)) for page in range(1, page_count + 1)]

    for html in await asyncio.gather(*tasks):
        data.extend(await parse_page(html))

    with open("lenta_result.json", "w") as file:
        json.dump(data, file, indent=4)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(parse_html(10))
