from selenium import webdriver
import re
from datetime import datetime
from match import match1
import operator
import pandas as pd



from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


driver = webdriver.Firefox()


def hasClass(element, classsearched):
    parent = element.find_element_by_xpath('.')
    classes = parent.get_attribute('class')
    classes = classes.split()
    for class1 in classes:
        if class1 == classsearched:
            return True
    return False




def saveToExcel(code,url):
    driver.get(url)
    elements = driver.find_elements_by_xpath('//a')

    present = 1
    while present:
        present = 0
        for element in elements:
            if element.get_attribute('innerHTML') == 'Show more matches' and element.is_displayed():
                driver.execute_script("arguments[0].click();", element)
                present = 1

    tbody = driver.find_element_by_css_selector('table.soccer > tbody:nth-child(3)')
    matches = tbody.find_elements_by_xpath('*')

    roundmatches = {}
    round = ""
    id = 1
    year = 2018
    updated = 0
    earliermonth=0
    for match in matches:

        if hasClass(match, "event_round"):
            round = match.get_attribute('innerText')
            # if round not in roundmatches:
            # roundmatches[round]={}
            print(round)
        if match.find_elements_by_css_selector('.team-home'):
            roundmatches[id] = []
            home = match.find_element_by_css_selector('.team-home')
            away = match.find_element_by_css_selector('.team-away')
            score = match.find_element_by_css_selector('.score')
            r = score.get_attribute('innerHTML').split("&nbsp;:&nbsp;")
            time = match.find_element_by_css_selector('.time')
            time = datetime.strptime(time.get_attribute('innerHTML'), '%d.%m. %H:%M')

            if time.month > earliermonth and updated==0 and (earliermonth==1 or earliermonth==2):
                print(earliermonth)
                print(time.month)
                year -= 1
                updated=1
            time = datetime(year, time.month, time.day, time.hour, time.minute)
        #  print(time)
            homescore = r[0]
            awayscore = 0
            try:
                awayscore = r[1]
            except:
                continue

            hometeamname = re.findall("\w+", home.find_element_by_xpath('span').get_attribute('innerText'))
            awayteamname = re.findall("\w+", away.find_element_by_xpath('span').get_attribute('innerText'))
            hometeamname = (' '.join(hometeamname))
            awayteamname = (' '.join(awayteamname))
            earliermonth = time.month
        #   print (home.find_element_by_xpath('span').get_attribute('innerText')+"-"+ away.find_element_by_xpath('span').get_attribute('innerText') + " "+homescore + ":" + awayscore)
            roundmatches[id] = (match1(hometeamname, awayteamname, time, homescore, awayscore, round))
            id += 1

# print (roundmatches)
    roundmatches = sorted(roundmatches.items(), key=operator.itemgetter(0), reverse=True)

    B = []
    C = []
    F = []
    G = []
    H = []
    I = []
    D = []
    E = []

    for i in roundmatches:
        F.append(getattr(i[1], 'hometeam'))
        G.append(getattr(i[1], 'awayteam'))
        H.append(getattr(i[1], 'homescore'))
        I.append(getattr(i[1], 'awayscore'))
        timematch = getattr(i[1], 'date')
        E.append(datetime.time(timematch))
        D.append(datetime.date(timematch))
        B.append("")

        C.append(2018)
    print(F)
    print(G)
    print(H)
    print(I)

    df = pd.DataFrame({'B': B, 'C': C, 'D': D, 'E': E, 'F': F, 'G': G, 'H': H, 'I': I})
    writer = pd.ExcelWriter('C:\\Users\\danida\\Desktop\\excels2\\'+code+'.xls', engine='xlwt')
    df.to_excel(writer, sheet_name='Sheet1')

# Close the Pandas Excel writer and output the Excel file.
    writer.save()
    print(roundmatches)

# Show more matches
# pagesource = driver.page_source
# print(pagesource)

def loadAll():
    present = 1
    try:
        while present:
            element = driver.find_element_by_css_selector('.event__more')
            present = 0
            if element.is_displayed():
                driver.execute_script("arguments[0].click();", element)
                import time
                time.sleep(4)
                try:
                    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".event__more")))
                    print("loaded")
                except TimeoutException:
                    print(element)
                    print("still loads")
                    present = 0
                    return 1

                present = 1
            element = None
    except Exception:
        return

def getScheduledMatches(code,year,url):
    driver.get(url)
    loadAll()
    print(code)
    tbody = driver.find_element_by_css_selector('.sportName')
    matches = tbody.find_elements_by_xpath('*')

    roundmatches = {}
    round = ""
    id = 12
    formermonth=1
    year+=2
    for match in matches:
        if hasClass(match, "event__round"):
            round = match.get_attribute('innerText')
            print(round)
        if len(match.find_elements_by_css_selector('.event__participant--home'))!=0:
            roundmatches[id] = []
            home = match.find_element_by_css_selector('.event__participant--home')
            away = match.find_element_by_css_selector('.event__participant--away')
            score = match.find_element_by_css_selector('.event__scores')
            r = score.find_elements_by_css_selector('span')

            time = match.find_element_by_css_selector('.event__time')
            time.__setattr__('year',year)
            print(year)
            time = datetime.strptime(time.get_attribute('innerHTML')+' '+str(year), '%d.%m. %H:%M %Y')
            if time.month > formermonth:
                year -= 1
                formermonth = time.month
            time = datetime(year, time.month, time.day, time.hour, time.minute)

            homescore = r[0].get_attribute('innerText')
            awayscore = r[1].get_attribute('innerText')

            hometeamname = re.findall("\w+", home.get_attribute('innerText'))
            awayteamname = re.findall("\w+", away.get_attribute('innerText'))
            hometeamname = (' '.join(hometeamname))
            awayteamname = (' '.join(awayteamname))

        #   print (home.find_element_by_xpath('span').get_attribute('innerText')+"-"+ away.find_element_by_xpath('span').get_attribute('innerText') + " "+homescore + ":" + awayscore)
            roundmatches[id] = (match1(hometeamname, awayteamname, time, homescore, awayscore, round))
            id += 1
          #  print(roundmatches)
            formermonth=time.month

    roundmatches = sorted(roundmatches.items(), key=operator.itemgetter(0), reverse=True)

    B = []
    C = []
    F = []
    G = []
    H = []
    I = []
    D = []
    E = []

    for i in roundmatches:
        F.append(getattr(i[1], 'hometeam'))
        G.append(getattr(i[1], 'awayteam'))
        H.append(int(getattr(i[1], 'homescore')))
        I.append(int(getattr(i[1], 'awayscore')))
        timematch = getattr(i[1], 'date')
        E.append(datetime.time(timematch))
        D.append(datetime.date(timematch))
        B.append("")

        C.append(timematch.year)
    print(F)
    print(G)
    print(H)
    print(I)

    df = pd.DataFrame({'B': B, 'C': C, 'D': D, 'E': E, 'F': F, 'G': G, 'H': H, 'I': I})
    writer = pd.ExcelWriter('C:\\Users\\danida\\Desktop\\excels2\\'+code+'.xls', engine='xlwt')
    df.to_excel(writer, sheet_name='Sheet1')

# Close the Pandas Excel writer and output the Excel file.
    writer.save()
    print(roundmatches)

# Show more matches
# pagesource = driver.page_source
# print(pagesource)


countries = {}
#countries["CRO1_"]="https://www.flashscore.com/football/croatia/1-hnl/results/"
#countries["MEX"] = "https://www.flashscore.com/football/mexico/primera-division/results/"
#countries["COL"]="https://www.flashscore.com/football/colombia/liga-aguila/results/"
#countries["EGYPT"]="https://www.flashscore.com/football/egypt/premier-league/results/"
countries["ENG"]="https://www.flashscore.com/football/england/premier-league/results/"
countries["Championship"]="https://www.flashscore.com/football/england/championship/results/"
#countries["FRA"]="https://www.flashscore.com/football/france/ligue-1/results/"
#countries["IRAN"]="https://www.flashscore.com/football/iran/persian-gulf-pro-league/results/"
#countries["ITA"]="https://www.flashscore.com/football/italy/serie-a/results/"
#countries["NED"]="https://www.flashscore.com/football/netherlands/eredivisie/results/"
countries["SCO"]="https://www.flashscore.com/football/scotland/premiership/results/"
#countries["SPA"]="https://www.flashscore.com/football/spain/laliga/results/"
countries["USARAB"]="https://www.flashscore.com/football/united-arab-emirates/uae-league/results/"
#countries["IRAK"]="https://www.flashscore.com/football/iraq/super-league/results/"
countries["SAUD"]="https://www.flashscore.com/football/saudi-arabia/saudi-professional-league/results/"
#countries["FRA2_"] = "https://www.flashscore.com/football/france/ligue-2/results/"
#countries["FRA3_"] = "https://www.flashscore.com/football/france/national/results/"
#countries["GER"] ="https://www.flashscore.com/football/germany/bundesliga/results/"
#countries["NED2_"] ="https://www.flashscore.com/football/netherlands/eerste-divisie/results/"
#countries["POR"] = "https://www.flashscore.com/football/portugal/primeira-liga/results/"
#countries["SPA2_"] = "https://www.flashscore.com/football/spain/laliga2/results/"
countries["TUR"] = "https://www.flashscore.com/football/turkey/super-lig/results/"
#countries["GRE"] = "https://www.flashscore.com/football/greece/super-league/results/"
#countries["IRL2019"] = "https://www.flashscore.com/football/ireland/premier-division/results/"
countries["MAROC"] = "https://www.flashscore.com/football/morocco/botola-pro/results/"
#countries["FIN2019"] = "https://www.flashscore.com/football/finland/veikkausliiga/results/"

for key, value in countries.items():
    getScheduledMatches(key,2019,value)


driver.close()
