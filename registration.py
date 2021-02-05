import requests 
from bs4 import BeautifulSoup
import re 
import slack
from slackMessageCreator import SlackMessage
from utilities import *
import os
from dotenv import load_dotenv
load_dotenv()

slackToken = os.environ.get("slack-api-token")
client = slack.WebClient(token=slackToken)

URL = "http://publichealth.lacounty.gov/acd/ncorona2019/vaccine/hcwsignup/pods/"
r = render_page(URL)
soup = BeautifulSoup(r, "lxml")

# array that will contain available locations
availableOptions = []
dphTags = soup.findAll("div", id="pods-dph")
# laFireTags = soup.findAll("div", id="pods-lafire")

for tag in dphTags[0]:
    if tag == ' ':
        continue
    location = tag.find("h6", class_="card-header").find("strong").contents[0]
    provider = tag.find("h6", class_="card-header").find("strong").find("small").text
    company = tag.find("h6", class_="card-header").find("span", {"title" : re.compile(r".*")}).text

    availableDates = tag.find("div", class_="card-body").find("div")
    appointmentsAvailable = 'Currently booking up to 2-14-21' in availableDates.text
    
    if appointmentsAvailable:
        availableDates = availableDates.contents[0]
        link = tag.find("div", class_="card-body").find("div").find("a")

        availableOptions.append(
            { 
                "date": availableDates, 
                "location": location,
                "provider": provider,
                "company": company, 
                "link": link['href']
            }
        )
#     print(location)

# for tag in laFireTags[0]:
#     if tag == ' ':
#         continue
#     location = tag.find("h6", class_="card-header").find("strong").contents[0]
#     provider = tag.find("h6", class_="card-header").find("strong").find("small").text
#     company = tag.find("h6", class_="card-header").find("span").text
#     # method = tag.find("h6", class_="card-header").find("span", class_="text-warning").text

#     availableDates = tag.find("div", class_="card-body").find("div").text

#     if 'Appointments' in availableDates:
#         link = tag.find("div", class_="card-body").find("div").find("a")
#         availableDates = extractDate(availableDates)
#         availableOptions.append(
#             { 
#                 "date": availableDates, 
#                 "location": location,
#                 "provider": provider,
#                 "company": company, 
#                 "link": link['href']
#             }
#         )
#     # print(location)
print(availableOptions)

if not availableOptions:
     client.chat_postMessage(channel='covid-registration-info', text='No appointments available')
else:
    registrationMessage = SlackMessage()

    for option in availableOptions:
        registrationMessage.appendSection(
            option.get('company'),
            option.get('date'), 
            option.get('location'),
            option.get('provider'),
            option.get('link'))
# print (registrationMessage.blocks)  
    client.chat_postMessage(
        channel='covid-registration-info',
        blocks = registrationMessage.blocks
    )


