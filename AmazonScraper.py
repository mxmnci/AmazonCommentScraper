from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime  
from datetime import timedelta 
from random import randint
from time import sleep
from tqdm import tqdm
import sys
import csv
import os

def descWordCount(str1):
    total = 1
    for i in range(len(str1)):
        if(str1[i] == ' ' or str1 == '\n' or str1 == '\t'):
            total = total + 1
    return total

def containsWord(description, words):
    containsWord = False
    for word in words:
        if word in description.lower():
            containsWord = True
    return containsWord

def scrape(AMAZONURL, PRODUCTHANDLE, RATINGLIMIT, COMMENTLIMIT, EXCLUDE):
    print(EXCLUDE)
    try:
        os.remove("comments.csv")
    except OSError:
        pass
    if getattr(sys, 'frozen', False):
        if (sys.platform == "darwin"):
            chromedriver_path = os.path.join(sys._MEIPASS, 'chromedriver')
        elif (sys.platform == "win32"):
            chromedriver_path = os.path.join(sys._MEIPASS, 'chromedriver.exe')
        else:
            print("Chrome Driver not found...")
    else:
        if (sys.platform == "darwin"):
            chromedriver_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"chromedriver")
        elif (sys.platform == "win32"):
            chromedriver_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"chromedriver.exe")
        else:
            print("Chrome Driver not found...")
    browser = webdriver.Chrome(chromedriver_path)
    url = AMAZONURL
    browser.get(url)
    print("Please be patient while the comments are gathered. \nDO NOT close the browser window.")
    try:
        currentButton = browser.find_element_by_xpath("//*[@id='reviews-medley-footer']/div[2]/a")
        currentButton.click()
    except:
        print("There are no comments to extract, terminating process...")
        sys.exit()
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    REVIEWCOUNT = int(soup.find("span", {"class" : "totalReviewCount"}).get_text().replace(",",""))
    loop = tqdm(total=REVIEWCOUNT, position=0, leave=False)
    TOTALCOMMENTCOUNT = 0
    COMMENTCOUNT = 10
    sleep(1)
    with open('DONOTUSE.csv', 'w', encoding='utf-8') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        filewriter.writerow(['product_handle', 'state', 'rating', 'title','author', 'email', 'body', 'created_at'])
        productHandle = PRODUCTHANDLE
        while COMMENTCOUNT == 10 and (TOTALCOMMENTCOUNT < COMMENTLIMIT or COMMENTLIMIT == 0):
            loop.set_description("Status: ")
            loop.update(COMMENTCOUNT)
            COMMENTCOUNT = 0
            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            for i in soup.find_all("div", {"class" : "a-section celwidget"}):
                rating = int(i.find("span", {"class" : "a-icon-alt"}).get_text()[0])
                profileName = i.find("span", {"class" : "a-profile-name"}).get_text()
                description = i.find("span", {"class" : "review-text-content"}).get_text()[:-1]
                title = i.find("a", {"class" : "review-title-content"}).contents[0].get_text()
                fakeTime = str(datetime.now().replace(microsecond=0) - timedelta(days=randint(0,100), minutes=randint(0,60), seconds=randint(0,60))) + " -0700"

                if (rating >= RATINGLIMIT and profileName != "Amazon Customer" and "\"" not in description and not containsWord(description, EXCLUDE) and not containsWord(title, EXCLUDE)):
                    filewriter.writerow([productHandle, 'published', "\"" + str(rating) + "\"", "\"" + title + "\"", "\"" + profileName + "\"", 'imported@review.com', "\"" + description + "\"", fakeTime])

                COMMENTCOUNT += 1
                TOTALCOMMENTCOUNT += 1
            try:
                currentButton = browser.find_element_by_xpath("//*[@id='cm_cr-pagination_bar']/ul/li[2]")
                currentButton.click()
            except: 
                print("There are no comments to extract, terminating process...")
                sys.exit()
            sleep(1)

    loop.close()

    text = open("DONOTUSE.csv", "r", encoding='utf-8')
    text = ''.join([i for i in text]).replace("|", "")
    out = open("comments.csv","w", encoding='utf-8')
    out.writelines(text)
    out.close()
    os.remove("DONOTUSE.csv")
    s = open("comments.csv", mode='r', encoding='utf-8-sig').read() #CONVERT UTF-8 TO NO BOM - Necessary for shopify import
    open("comments.csv", mode='w', encoding='utf-8').write(s)

    with open("comments.csv", 'rb') as open_file: # CONVERT LINE ENDINGS TO UNIX - Necessary for shopify import
        content = open_file.read()
    WINDOWS_LINE_ENDING = b'\r\n'
    UNIX_LINE_ENDING = b'\n'
    content = content.replace(WINDOWS_LINE_ENDING, UNIX_LINE_ENDING)
    with open("comments.csv", 'wb') as open_file:
        open_file.write(content)

    print("Comments have been gathered successfully, your file is located at: " + os.path.abspath("comments.csv"))
