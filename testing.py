import ast
import datetime
import json
import os
import threading
import time
import random
import re

import cv2
import emoji
import mysql.connector
from instagrapi.story import StoryBuilder
import requests
import spintax
from instagrapi.mixins.challenge import ChallengeChoice
from instagrapi.types import Usertag, Location, StoryLink
from selenium import webdriver
# from selenium.webdriver import Keys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import instagrapi
import instagrapi.exceptions
from openpyxl import load_workbook
import socket
import warnings
from datetime import datetime

#jasons9branderson@iralborz.bid:IEIKeagx433
#kennethf8vmmoore@iralborz.bid:OUAIaisu820
#steven18cjmartinez@iralborz.bid:OUGRieii828
#michael3czmwalker@iralborz.bid:KEONohuq020
#helenwfz1white@iralborz.bid:ZYADuoif437

threaded_proxy_list = ["Rjenkins313:Audit313@173.92.252.25:2002"]

account_temp = "mark29t6roberts@iralborz.bid:EALUkfee661"
#account_temp = "bulyhill@iralborz.bid:LGIJysaq221"
proxy = threaded_proxy_list[0]


print("Using account : ", account_temp)
print("Using Proxy : ", proxy)

acc_details = account_temp.split(":")
cl = instagrapi.Client()

email, passw = acc_details[0], acc_details[1]
extention = acc_details[0].split("@")[1]
print(acc_details)

fname = acc_details[0].split("@")[0]
PATH = "json_files_new/{}".format(fname + "iralborz")
print("iralborz.bid : ", PATH)
email, passw = acc_details[0], acc_details[1]

cl.set_proxy("http://" + proxy)
cl.load_settings(PATH)
cl.login(email, passw)

total_tag = []
tagged = []
feedshow = '1'
reel_path = r"C:\Users\user\pycharm_python\Instagram_FINAL\gui\FINAL\\testing\\reels\\cblbynzhng.mp4"
c2 = "Hello this is a tag"
story_image = "testing/story_pic/1.jpg"
list_of_link = "https://discord.gg/FKZFjsmVkA"
story = cl.photo_upload_to_story(story_image, "", links=[StoryLink(webUri=list_of_link, x=0.5126011, y=0.7,width=0.5, height=0.22)])
print(story)
#list_of_links_dict = {'enable': True, 'x': 0.5126011, 'y': 0.7, 'width': 0.5, 'height': 0.22}
#story = cl.photo_upload_to_story(story_image, "", links=[StoryLink(webUri=list_of_link, x=0.5126011, y=0.7, width=0.5, height=0.22)])
exit(4254)
#total_tag.append(Usertag(user=cl.user_info_by_username('loveletterthief'), x=0.5, y=0.5))
tagged.append(total_tag)
location_reel = {}
print("Tagging users : ", total_tag, total_tag)
location_reel["location"] = "Las Vegas"
location_reel["latitude"] = 36.16
location_reel["longitude"] = -115.13
caption = "just a plain old white background"
post_path = r"C:\Users\user\pycharm_python\Instagram_FINAL\gui\FINAL\testing\post\whit.jpg"

popped_account = "loveletterthief"
#lis = cl.user_following_v1((cl.user_id_from_username(popped_account)), 40000)
lis = cl.user_followers_v1((cl.user_id_from_username(popped_account)), 40000)
lis = emoji.demojize(str(lis))
reg = "username='[a-z|A-Z|0-9|_|.]+'"
usernames = re.findall(reg, str(lis))
for ele in usernames:
    print(ele)
usernames = [x.split("=")[1] for x in usernames]
for follower in usernames:
    file = open("additional_operations/ship/seed_output.txt", "a", encoding="utf-8")
    file.write(str(follower)[1:-1] + "\n")
    file.close()

#status = cl.photo_upload(path=post_path, caption=caption, usertags=total_tag, location=Location(name=location_reel["location"], lat=location_reel["latitude"], lng=location_reel["longitude"]))

