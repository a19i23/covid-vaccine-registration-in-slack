import time
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')

def render_page(url):
    driver = webdriver.Chrome(executable_path=r'/Users/villaa/Downloads/chromedriver', options=options)
    driver.get(url)
    # time.sleep(3)
    driver.find_element_by_link_text("Make an appointment to be vaccinated by LAC DPH and partners").click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="btnClosePopup"]').click()
    # time.sleep(3)
    r = driver.page_source


    #driver.quit()
    return r

def extractDate(string):
    # lowerCaseStr = string.lower()
    if 'Full' in string:
        string = string[0:string.index('Full')-1]
    elif 'Register' in string:
        string = string[0:string.index('Register')-1]
    elif 'Appointments' in string:
        string = string[0:string.index('Appointments')-1]
    return string
    
def extractProvider(string):
    if 'Run' in string:
        string = string.split('Run')
        location = string[0]
        provider = string[1]
        return location, provider
    return string    