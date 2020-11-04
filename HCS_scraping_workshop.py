# Django API that scrapes data from League of Legends website by rank number

from django.shortcuts import render
from django.http import HttpResponse
import json
import requests
from bs4 import BeautifulSoup


def make(request):

    Drive = requests.get("https://www.op.gg/ranking/ladder/")

    LOLList = []

    Dictionary = {}

    Content = BeautifulSoup(Drive.content, "lxml")

    Rank = int(request.POST["rank"])  
    UserName = ""

    if Rank < 6: 
        TotalList = Content.find("div",{"class":"LadderRankingLayoutWrap"})
        List = TotalList.find("div",{"class":"Content"})
        TopList = List.find_all("li") 

        Individual = TopList[Rank-1] 
        Top5 = Individual.find("a",{"class":"ranking-highest__name"})
        if Top5 != None: 
            Dictionary["Top 5 Players"]=Top5.text
        UserName = Top5.text

        TierRankInfo = Individual.find("div",{"class":"ranking-highest__tierrank first"})

    else: 
        SecondList = Content.find("table",{"class":"ranking-table"})
        SecondListBody = SecondList.find("tbody")
        TopListSecond = SecondListBody.find_all("tr")

        SecondIndividual = TopListSecond[Rank-6] 
        TopAll = SecondIndividual.find("td",{"class":"select_summoner ranking-table__cell ranking-table__cell--summoner"})
        Dictionary["Top Rest Players"]=TopAll.text
        UserName = TopAll.text

    
    SecondDrive = requests.get("https://www.op.gg/summoner/userName="+UserName)

    SecondContent = BeautifulSoup(SecondDrive.content,"lxml")

    StatBox = SecondContent.find("div",{"class":"GameAverageStatsBox"})
    StatBoxSmall = StatBox.find("table",{"class":"GameAverageStats"})
    KDA = StatBoxSmall.find("div",{"class":"KDARatio"})

    Dictionary["KDA Stats"]=KDA.text.replace("\n","")

    LOLList.append(Dictionary)


    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}

    params = {'name':UserName}
    url = "http://api.ifi.gg/search" 
    response = requests.get(url=url, params=params, headers=headers)
    Result = response.json()

    FirstResult = Result["data"]
    SecondResult = FirstResult["times"]
    for x in SecondResult:
        LOLDictionary = {}
        LOLDictionary["Season"]=x["date"]
        LOLDictionary["Time"]=str(x["time"])
        LOLDictionary["Number of Games"]=x["games"]
        LOLList.append(LOLDictionary)


    return HttpResponse(json.dumps(LOLList)) 