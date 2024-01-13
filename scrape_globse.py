import httpx
import selectolax


def setup(keyword, target_lang, source_lang="en"):
    clean_keyword = keyword.replace(" ", "%20")
    url = f"https://glosbe.com/{source_lang}/{target_lang}/{clean_keyword}"

    page_num = 1
    data = []

    if page_num == 1:
            fragment_url = url

    while True:
        output = scrape_glosbe(fragment_url, target_lang, source_lang)

        if len(output) == 0:
            break

        data.extend(output)
        page_num += 1
        fragment_url = f"{url}/fragment/tmem?page={page_num}&mode=MUST&stem=true"

    return data


def scrape_glosbe(url, target_lang, source_lang="en"):
    html = httpx.get(url).text
    tree = selectolax.parser.HTMLParser(html)
    nodes = tree.css("div.py-2.flex")

    if len(nodes) == 0:
        return []
    
    data = []

    for node in nodes:
        data.append({
            source_lang: node.css_first("div.dir-aware-pr-1").text().strip(), 
            target_lang: node.css_first("div[lang]").text().strip()
        })

    return data

if __name__ == "__main__":
    print(setup("how are you", "yo"))