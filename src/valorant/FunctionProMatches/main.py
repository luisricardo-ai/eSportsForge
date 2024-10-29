import requests
from selectolax.parser import HTMLParser
from time import sleep
import json


URL = "https://www.vlr.gg/matches/results/"


def get_matches_pages() -> int:
    result = requests.get(url=URL)
    html = HTMLParser(html=result.text)
    last_page_path = html.css("a.mod-page")[-1].attributes["href"]
    
    # The slice is based on "/matches/results/?page=[NUMBER_OF_PAGES]"
    last_page = int(last_page_path[23:])
    return last_page


def get_page(page: int) -> list[dict]:
    print(f"Requesting Page: {page}")
    page_url = str(URL + f"?page={page}")
    result = requests.get(url=page_url)
    html = HTMLParser(html=result.text)

    result = []
    for item in html.css("a.wf-module-item"):
        url_path = item.attributes["href"]
        
        rounds = (
            item.css_first("div.match-item-event-series")
            .text()
            .replace("\u2013", "-")
            .replace("\n", "")
            .replace("\t", "")
        )
        tourney = (
            item.css_first("div.match-item-event")
            .text()
            .replace("\t", " ")
            .strip()
            .split("\n")[1]
            .strip()
        )

        try:
            team_array = (
                item.css_first("div.match-item-vs").css_first("div:nth-child(2)").text()
            )
        except Exception:
            team_array = "TBD"
        team_array = (
            team_array.replace("\t", " ")
            .replace("\n", " ")
            .strip()
            .split("                                  ")
        )
        team1 = team_array[0]
        score1 = team_array[1].replace(" ", "").strip()
        team2 = team_array[4].strip()
        score2 = team_array[-1].replace(" ", "").strip()

        result.append(
            {
                "match_page": url_path,
                "team1": team1,
                "team2": team2,
                "score1": score1,
                "score2": score2,
                "tournament_name": tourney,
                "round_info": rounds,
            }
        )

    return result
    

def main(event, context=None):
    pages = 0

    if "amount_pages" not in event:
        pages = get_matches_pages()

    else:
        pages = event["amount_pages"]
    
    for page in range(1, pages + 1):
        games = get_page(page=page)

        # TODO FUNCTION TO SAVE TEMP DATA FILE
        # TODO FUNCTION TO SEND DATA TO S3

        # We are not requesting data from an API, so takecare.
        sleep(0.5)