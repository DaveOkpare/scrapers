import asyncio
import httpx
import selectolax
import aiohttp


async def setup(session, keyword, target_lang, source_lang="en"):
    clean_keyword = keyword.replace(" ", "%20")
    url = f"https://glosbe.com/{source_lang}/{target_lang}/{clean_keyword}"

    page_num = 1
    data = []

    if page_num == 1:
        fragment_url = url

    while True:
        output = await scrape_glosbe(session, fragment_url, target_lang, source_lang)

        if len(output) == 0:
            break

        data.extend(output)
        page_num += 1
        fragment_url = f"{url}/fragment/tmem?page={page_num}&mode=MUST&stem=true"

    return data


async def scrape_glosbe(session, url, target_lang, source_lang="en"):
    async with session.get(url) as r:
        html = await r.text()
        # html = httpx.get(url).text
        tree = selectolax.parser.HTMLParser(html)
        nodes = tree.css("div.py-2.flex")

        if len(nodes) == 0:
            return []

        data = []

        for node in nodes:
            data.append(
                {
                    source_lang: node.css_first("div.dir-aware-pr-1").text().strip(),
                    target_lang: node.css_first("div[lang]").text().strip(),
                }
            )

        return data


async def scrape_all(session, keywords, target_lang, source_lang="en"):
    tasks = []

    for keyword in keywords:
        task = asyncio.create_task(setup(session, keyword, target_lang, source_lang))
        tasks.append(task)

    res = await asyncio.gather(*tasks)
    return res


async def run(keywords, target_lang, source_lang="en"):
    async with aiohttp.ClientSession() as session:
        htmls = await scrape_all(
            session=session,
            keywords=keywords,
            target_lang=target_lang,
            source_lang=source_lang,
        )
        return htmls


if __name__ == "__main__":
    # print(asyncio.run(run(["how are you", "what is your name"], "yo")))
    lang = ["tiv", "ibb", "kr", "idu", "efi", "ish", "ff", "fuv", "iso", ""]

    common_nouns = [
        "time",
        "year",
        "people",
        "way",
        "day",
        "man",
        "government",
        "company",
        "hand",
        "part",
        "place",
        "case",
        "group",
        "problem",
        "fact",
        "eye",
        "friend",
        "charge",
        "home",
        "health",
        "system",
        "industry",
        "world",
        "school",
        "country",
        "family",
        "student",
        "government",
        "problem",
        "company",
        "number",
        "night",
        "group",
        "job",
        "issue",
        "side",
        "kind",
        "head",
        "house",
        "service",
        "problem",
        "fact",
        "research",
        "idea",
        "news",
        "course",
        "work",
        "life",
        "form",
        "interest",
        "hand",
        "food",
        "book",
        "point",
        "child",
        "program",
        "lot",
        "cause",
        "man",
        "basis",
        "moment",
        "name",
        "team",
        "minute",
        "reason",
        "experience",
        "goal",
        "value",
        "study",
        "action",
        "image",
        "result",
        "law",
        "theory",
        "girl",
        "boy",
        "picture",
        "surface",
        "history",
        "person",
        "art",
        "war",
        "area",
        "term",
        "school",
        "trade",
        "name",
        "story",
        "music",
        "method",
        "media",
        "travel",
        "thing",
        "day",
        "year",
        "month",
        "week",
        "night",
        "day",
        "hour",
        "minute",
        "second",
        "word",
        "number",
        "way",
        "place",
        "time",
        "work",
        "case",
        "point",
        "problem",
        "government",
        "company",
        "part",
        "hand",
        "home",
        "system",
        "fact",
        "eye",
        "friend",
        "charge",
        "industry",
        "world",
        "country",
        "family",
        "student",
        "program",
        "kind",
        "head",
        "house",
        "service",
        "research",
        "news",
        "course",
        "life",
        "form",
        "interest",
        "food",
        "book",
        "child",
        "cause",
        "lot",
        "man",
        "moment",
        "name",
        "minute",
        "reason",
        "goal",
        "value",
        "study",
        "image",
        "result",
        "law",
        "theory",
        "girl",
        "boy",
        "picture",
        "surface",
        "history",
        "person",
        "art",
        "war",
        "area",
        "term",
        "trade",
        "name",
        "story",
        "music",
        "method",
        "media",
        "travel",
        "thing",
    ]

    with open("words.txt", "r") as f:
        words = f.readlines()

    clean_words = [f.strip() for f in words]

    print(asyncio.run(run(common_nouns, "ig")))
