from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import asyncio, urllib, json, random, requests, time
from create_bot import dp, bot
from configs.config import  member_id
from modules import sqlite_logic
import traceback
from aiogram import types, Dispatcher
HEADERS = {
    "user-agent": f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
    "accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}

async def get_mathes_html(url):
    list_id = sqlite_logic.get_treeID()

    with urllib.request.urlopen(url) as url:
        memory = json.loads(url.read().decode())
        try:
            if len(memory) == 0:
                print('Матчей нет')
                return #Матчей нет
            else:
                for i in memory:
                    if len(list_id) == 0:
                        logic = sqlite_logic.add_stavki(i['treeId'], i['name'])
                    else:
                        result = sqlite_logic.check_stavki(i['treeId'],  i['name'])
                    await get_time_score(i['treeId'])
        except Exception as i:
            print(i)

async def get_time_score(treeID):
    try:
        url = f"https://www.marathonbet.ru/su/live/{treeID}?marketIds={treeID}"
        browser = webdriver.Chrome()
        browser.get(url)
        await asyncio.sleep(random.randint(3, 7))
        soup = BeautifulSoup(browser.page_source, 'lxml')
        country_league = soup.find_all("span", class_ = "nowrap")
        country = str(country_league[0])
        country = country.partition('"nowrap">')[2].replace('.</span>', ' ')
        league = str(country_league[1])
        league = league.partition('"nowrap">')[2].replace('.</span>', ' ')
        logic = sqlite_logic.add_stavki_league(league, country, treeID)
        time_match =  soup.find_all("div", class_ = "green bold nobr")
        time_match = str(time_match)
        time_match = time_match.partition('>')[2].rpartition('<')[0]#.split(':', 1)
        if "Пер." in time_match:
            time_match == 'Пер'
        else:
            time_match = time_match.split(':', 1)
        if int(time_match[-2]) >= 45 or str(time_match) == 'Пер.':
            score_match = soup.find_all("div", class_="cl-left red")
            score_match = str(score_match[0])
            score_match = score_match.partition('red">')[2].rpartition('<span')[0].partition('(')[2].replace(')', ' ')
            if score_match[:3] == '0:1':
                await get_score(treeID)
            else:
                pass
        else:
            pass
    except Exception as e:
        print(traceback.format_exc())


async def get_score(treeID):
    try:
        url_score = f"https://www.marathonbet.ru/su/live/animation/statistic.htm?treeId={treeID}"
        browser = webdriver.Chrome()
        browser.get(url_score)
        await asyncio.sleep(random.randint(10, 15))
        soup = BeautifulSoup(browser.page_source, "lxml")
        score =  soup.find_all("div", class_ =  "chart-football-table_result_value left")
        match = str(score[3])
        match = match.partition('>')[2].rpartition('<')[0]
        if int(match) == 4:
            check = sqlite_logic.finish_check(treeID)
            if check[0] == 0:
                name, country, league = sqlite_logic.get_text(treeID)
                await bot.send_message(member_id, f"<b>{name[0]}</b>\n<i>{country[0]} {league[0]}</i>", parse_mode=types.ParseMode.HTML)
                sqlite_logic.update_finish(treeID)
            else:
                pass
    except Exception as i:
        print(i)


async def main():
    while True:
        await get_mathes_html(url = "https://mobile.marathonbet.ru/mobile-gate/api/v1/events/live-featured-events?tree-id=26418&elected-markets=true")
        await asyncio.sleep(random.randint(15,30))

