import requests
from selectolax.parser import HTMLParser
from time import sleep
import json
import os
from datetime import datetime, date
import boto3


URL = "https://www.vlr.gg/matches/results/"
S3 = boto3.client('s3')


def get_matches_pages() -> int:
    result = requests.get(url=URL)
    html = HTMLParser(html=result.text)
    last_page_path = html.css("a.mod-page")[-1].attributes["href"]
    
    # The slice is based on "/matches/results/?page=[NUMBER_OF_PAGES]"
    last_page = int(last_page_path[23:])
    return last_page


def get_page(page: int, today: str) -> dict[list]:
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
                "dat_load": today
            }
        )

    return {"result": result}


def save_tmp_file(data: dict[int]) -> str:
    tmp_dir = "/tmp"
    file_name = datetime.now().strftime("%Y%m%d%H%M%S%f")

    file_path = f"{tmp_dir}/{file_name}.json"
    with open(file_path, "w") as file:
        json.dump(data, file)

    return file_name


def send_to_s3(file_name: str, today: str):
    partition = f"game=valorant/dt={today}/"
    S3.upload_file(f'/tmp/{file_name}.json', os.getenv('RAW_S3_BUCKET'), f'{partition}{file_name}.json')


def main(event, context=None):
    pages = 0
    today = date.today()

    if "amount_pages" not in event:
        pages = get_matches_pages()

    else:
        pages = event["amount_pages"]
    
    for page in range(1, pages + 1):
        games = get_page(page=page, today=str(today))

        file_name = save_tmp_file(data=games)
        send_to_s3(file_name, today=today)

        # We are not requesting data from an API, so takecare.
        print(f"DATA FROM PAGE {page} UPLOADED TO S3")
        sleep(0.5)