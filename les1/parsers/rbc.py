import json
import re
import bs4
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def _clear_string(string: str) -> str:
    string = string.strip()
    return " ".join(re.findall(r"\S+", string))


def get_html(url: str) -> str:
    with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
        driver.get(url)
        time.sleep(1)
        height = driver.execute_script("return document.body.scrollHeight")

        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == height:
                break
            height = new_height
            time.sleep(0.1)
        return driver.page_source


def parse_html() -> None:
    url = "https://www.rbc.ru"
    soup = bs4.BeautifulSoup(get_html(url), 'html.parser')

    news_div = soup.find("div", class_="l-table l-table-min-height")
    all_news = news_div.findAll("div", class_="js-index-central-column-main js-index-doscroll")
    json_result = []

    for news in all_news:
        a_category = news.find("a", class_="item__category")
        a_news = news.find("a", class_="item__link")
        image = news.find("img", class_="item__image")

        if a_category is not None:
            category_title = _clear_string(a_category.text)
            category_href = a_category.get("href")
        else:
            a_category = news.find("a", class_="item-quote__category")
            category_title = _clear_string(a_category.text)
            category_href = a_category.get("href")

        if a_news is not None:
            news_href = a_news.get("href")
            news_title = _clear_string(a_news.find("span", class_="item__title").text)
        else:
            a_news = news.find("a", class_="item-quote__title")
            news_title = _clear_string(a_news.text)
            news_href = a_news.get("href")

        if image:
            image_href = image.get("src")
        else:
            image_href = ""

        json_result.append({
            "category": {
                "title": category_title,
                "href": category_href
            },
            "news": {
                "title": news_title,
                "href": news_href,
                "image": image_href
            }
        })

    with open("rbc_result.json", "w") as file:
        json.dump(json_result, file, indent=4)


if __name__ == '__main__':
    parse_html()
