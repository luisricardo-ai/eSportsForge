import requests
from selectolax.parser import HTMLParser

URL = "https://www.vlr.gg/"
event = {"matches": [425936]}


if __name__ == "__main__":
    for match in event["matches"]:
        page_url = str(URL + f"{match}/")
        result = requests.get(url=page_url)
        html = HTMLParser(html=result.text)

        ## DEBUG!
        with open("teste.html", 'w', encoding='utf-8') as file:
            file.write(result.text)

        ## FIM DEBUG!