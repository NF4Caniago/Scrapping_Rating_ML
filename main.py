from selenium import webdriver
from time import sleep
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import pandas as pd
#tes contribution github


#driver = webdriver.Chrome("D:\chromedriver")

# #activate GL first
# print("Activated WebGL")
# driver.get("chrome://flags")
# search = driver.find_element_by_id("search")
# search.send_keys("WebGL")
# search.send_keys(Keys.RETURN)
# sleep(3)
# #driver.find_element_by_xpath("//select[@class='experiment-enable-disable']/option[text() ='Enabled']").click()
# #SD.send_keys(Keys.RETURN)
# SD = Select(driver.find_element_by_xpath("//select[@class='experiment-enable-disable']"))
# SD.select_by_value("enabled")
# enable = driver.find_element_by_xpath("//option[@value='enabled']")
# enable.selectByValue("enabled")
# experiment = driver.find_element_by_id("experiment-restart-button")
# experiment.click()
# sleep(10)
# print("WebGL Activated")

#activate GL first
options = Options()
#options.add_argument("--kiosk")#fullscreen
options.add_argument('--enable-webgl-draft-extensions')
driver = webdriver.Chrome('D:\chromedriver', chrome_options = options)
driver.maximize_window()
print("WebGL Activated")

#open google play
driver.get("https://play.google.com/store/apps/details?id=com.mobile.legends&showAllReviews=true")
sleep(10)
action = ActionChains(driver)

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")
SCROLL_PAUSE_TIME = 10
click = 0

while not(click == 100):
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        try:
            sleep(7)
            showMore = driver.find_element_by_class_name("U26fgb.O0WRkf.oG5Srb.C0oVfc.n9lfJ.M9Bg4d")
            action.move_to_element(showMore)
            action.click(showMore)
            action.perform()
            sleep(10)            
            #showMore.click()
            print("Click Showmore "+str(click))
            click += 1
        except: 
            print("------Scroll selesai-------")
            print("Click ShowMore Counts = " + str(click))
            break
    last_height = new_height

#klik full review
sleep(3)
btn = driver.find_elements_by_xpath("//button[@jsname='gxjVle']")
for b in btn:
    try:
        b.click()
    except:
        print("g ada tombol") 

#element komentar
comments = driver.find_elements_by_xpath("//span[@jsname='fbQN7e']")
comments2 = driver.find_elements_by_xpath("//span[@jsname='bN97Pc']")

#element rating
elRating = driver.find_elements_by_xpath("//div[@role='img']")
rating = []
for rat in elRating:
    temp = rat.get_attribute('aria-label')
    temp.replace("Rated ","")
    temp.replace(" stars out of five stars","")
    rating.append(str(temp))


#salin komentar ke dataframe
i = 0
dataset = pd.DataFrame([["init dataframe","999"]],columns=["comments","rating"])

for comment in comments:
    if comment.text == "":
        dataset = dataset.append([[ comments2[i].text , rating[i]]])
    else:
        dataset = dataset.append([[ comment.text , rating[i] ]])
    i += 1

#konversi ke csv
dataset.to_csv("datasetML.csv",sep="+")
sleep(4)
driver.quit()
