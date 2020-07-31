import re
import datetime
from time import sleep
import pyautogui as pya
from datetime import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


def openclass(index, timet):
    # The line with current class link
    t = timet[index]
    st = t[1:6]
    et = t[7:12]
    link = t[14:]
    index = index + 1

    # Open current class
    browser.get(link)
    sleep(10)

    # Block Video
    browser.find_element_by_css_selector(
        '#yDmH0d > c-wiz > div > div > div:nth-child(4) > div.crqnQb > div > div.vgJExf > div > div > div.oORaUb.NONs6c > div.mFzCLe > div.EhAUAc > div.GOH7Zb > div > div > span > span > div > div > svg').click()
    sleep(1)

    # Block Audio
    browser.find_element_by_css_selector(
        '#yDmH0d > c-wiz > div > div > div:nth-child(4) > div.crqnQb > div > div.vgJExf > div > div > div.oORaUb.NONs6c > div.mFzCLe > div.EhAUAc > div.ZB88ed > div > div > div > span > span').click()
    sleep(3)

    # Calculate start time and end time of current class
    sth = st[:2]
    stm = st[3:]
    eth = et[:2]
    etm = et[3:]
    stime = time(hour=int(sth), minute=int(stm))
    etime = time(hour=int(eth), minute=int(etm))

    # Get current time
    hh = datetime.datetime.now().hour
    mm = datetime.datetime.now().minute
    ttime = time(hour=hh, minute=mm)

    # Check if class has ended or we can still attend it
    if etime > ttime:
        while stime > ttime:
            sleep(30)
            hh = datetime.datetime.now().hour
            mm = datetime.datetime.now().minute
            ttime = time(hour=hh, minute=mm)
    else:
        return index

    # Join class
    browser.minimize_window()
    browser.maximize_window()
    sleep(5)
    x, y = pya.locateCenterOnScreen(r"D:\JoinNow.png")#TODO: Change with your own loaction of JoinNow pic
    pya.moveTo(x, y, 1)
    pya.click()

    # Wait for class to end
    # Get current time
    hh = datetime.datetime.now().hour
    mm = datetime.datetime.now().minute
    ttime = time(hour=hh, minute=mm)

    # Check if class has ended or we can still atttend it
    while etime > ttime:
        sleep(300)
        hh = datetime.datetime.now().hour
        mm = datetime.datetime.now().minute
        ttime = time(hour=hh, minute=mm)

    # To end the class
    browser.minimize_window()
    browser.maximize_window()
    sleep(5)
    pya.moveRel(200, 0, 1)
    if (browser.find_element_by_css_selector(
            '#ow3 > div.T4LgNb > div > div:nth-child(4) > div.crqnQb > div.rG0ybd.LCXT6 > div.q2u11 > div.s1GInc.zCbbgf > div') is not None):
        browser.find_element_by_css_selector(
            '#ow3 > div.T4LgNb > div > div:nth-child(4) > div.crqnQb > div.rG0ybd.LCXT6 > div.q2u11 > div.s1GInc.zCbbgf > div').click()
    else:
        browser.get("http:\\google.com")
    return index

# Disabling notifications and allowing access to mic and camera
opt = Options()
opt.add_argument("--disable-infobars")
opt.add_argument("start-maximized")
opt.add_argument("--disable-extensions")
opt.add_experimental_option("prefs", {
    "profile.default_content_setting_values.media_stream_mic": 1,
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.geolocation": 1,
    "profile.default_content_setting_values.notifications": 2
})

# initializing the browser
chromedriver = r"C:\Users\Dell\Downloads\chromedriver" #TODO: Change with your own loaction for driver
browser = webdriver.Chrome(options=opt, executable_path=chromedriver)
browser.maximize_window()

# opening home page
browser.get("http:\\google.com")
sleep(3)  # waiting for it to load

# logging into google account
browser.find_element_by_css_selector('#gb_70').click()
sleep(5)

# Enter email
browser.find_element_by_css_selector('#identifierId').send_keys('<Your-email-id>')
browser.find_element_by_css_selector('#identifierNext > div > button > div.VfPpkd-RLmnJb').click()
sleep(10)

# Enter password
browser.find_element_by_css_selector('#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input').send_keys('<Your-password>')
browser.find_element_by_css_selector('#passwordNext > div > button > div.VfPpkd-RLmnJb').click()
sleep(5)

# Opening new tab
action = ActionChains(browser)
find = browser.find_element_by_link_text('About')
action.key_down(Keys.CONTROL).click(find).key_up(Keys.CONTROL).perform()
browser.switch_to.window(browser.window_handles[-1])
sleep(7)

# Reading the time table and making a list
file = open(r'D:\timetable.txt', "r")#TODO: Change with your own loaction for timetable
tt = file.readlines()
for i in range(len(tt)):
    tt[i] = tt[i].strip('\n')

# Calculate the day
i = -1
day = datetime.datetime.today().weekday()
if day == 0:
    i = tt.index("Monday") + 1
if day == 1:
    i = tt.index("Tuesday") + 1
if day == 2:
    i = tt.index("Wednesday") + 1
if day == 3:
    i = tt.index("Thursday") + 1
if day == 4:
    i = tt.index("Friday") + 1

# Checking if classes for the day have ended
day = re.compile(r'(Mon|Tues|Wednes|Thurs|Fri|Satur)day')
while not re.match(day, tt[i]):
    i = openclass(i, tt)