import ast
import datetime
import json
import os
import time
import random
import re

import requests
from instagrapi.mixins.challenge import ChallengeChoice
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import instagrapi
import instagrapi.exceptions
import ast
import datetime
import re
import time
import instagrapi
import instagrapi.exceptions
from datetime import datetime
import ast
import datetime
import json
import os
import re
import threading
import time
import random
import instagrapi
import instagrapi.exceptions
from datetime import datetime
import mysql.connector
from Instagram_FINAL.reset_proxy import reset_proxy
from Instagram_FINAL.save_excel import save_excel
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


def get_iralborz(email_id):
    PATH = "C:\selenium\chromedriver.exe"
    # PATH = r"D:\Programming\INSTAGRAM\InstaBot\openbeta\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    driver.get("http://ruu.kr/")
    time.sleep(1)
    sel = Select(driver.find_element_by_id("domain"))
    sel.select_by_visible_text("iralborz.bid")

    search_email = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[1]/form/input[3]")
    time.sleep(1)
    search_email.send_keys(email_id.split("@")[0])
    time.sleep(3)

    # /html/body/div[1]/div[1]/div/div[1]/form/span
    refresh = driver.find_element_by_id("mailList")
    timeout = 1
    while (1):
        if timeout == 10:
            return 111111
        element = driver.find_element_by_xpath("/html/body").text
        find = element
        match = re.search(r'Verify your account', find)
        if match:
            one = driver.find_element_by_xpath(
                "/html/body/div[1]/div[1]/div/div[3]/table/tbody/tr[1]/td[2]/font")

            if one.text == "Verify your account":
                one.click()
                break

            two = driver.find_element_by_xpath(
                "/html/body/div[1]/div[1]/div/div[3]/table/tbody/tr[2]/td[2]/font")

            if two.text == "Verify your account":
                two.click()
                break
            else:
                refresh.click()
                time.sleep(3)
                print("WAITING")
        else:
            refresh.click()
            time.sleep(3)
            print("WAITING")
            timeout += 1

    time.sleep(3)
    code = driver.find_element_by_xpath(
        "/html/body/div[1]/div[1]/div/div[2]/table/tbody/tr/td/table/tbody/tr[4]/td/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td/p[4]/font")
    # code = driver.find_element_by_xpath('//*[@id="email_content"]/table/tbody/tr[4]/td/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td/p[4]/font')
    return code.text


# SELENIUM FOR HOSTINGER
def get_hostinger(email, password):
    today = datetime.datetime.now()
    date_time = today.strftime("%H:%M")
    search_curr = "Today " + date_time[:-2]
    print(search_curr)
    PATH = "C:\selenium\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    driver.get("https://mail.hostinger.com/")
    time.sleep(1)
    search_email = driver.find_element_by_id("rcmloginuser")
    search_email.send_keys(email)
    search_pass = driver.find_element_by_id("rcmloginpwd")
    search_pass.send_keys("Hello123.")
    search_pass.send_keys(Keys.ENTER)

    while (1):
        element = driver.find_element_by_xpath("/html/body").text
        refresh = driver.find_element_by_id("rcmbtn110")
        find = element
        match = re.search(r'{}'.format(search_curr), find)
        if match:
            one = driver.find_element_by_xpath(
                "/html/body/div[1]/div[3]/div[4]/table[2]/tbody/tr[1]/td[2]/span[3]/a/span")
            two = driver.find_element_by_xpath(
                "/html/body/div[1]/div[3]/div[4]/table[2]/tbody/tr[2]/td[2]/span[3]/a/span")
            if one.text == "Verify your account":
                one.click()
                break
            elif two.text == "Verify your account":
                two.click()
                break
            else:
                refresh.click()
                print("REFRESHING")
                time.sleep(3)
        else:
            refresh.click()
            print("REFRESHING")
            time.sleep(3)

    time.sleep(5)
    driver.switch_to.frame("messagecontframe")
    body = driver.find_element_by_xpath("/html/body")
    matcher = re.search(r'\d{6}', body.text).group(0)

    print(matcher)
    if matcher:
        driver.switch_to.default_content()
        delete = driver.find_element_by_id("rcmbtn122")
        two.click()
        delete.click()
        one.click()
        delete.click()
        driver.close()
        return matcher


# SELENIUM PART for mail.com.tr
def get_code(email, password):
    # PATH = "C:\Program Files (x86)\chromedriver.exe"
    PATH = "C:\selenium\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    driver.get("https://mail.com.tr")
    time.sleep(1)
    search_email = driver.find_element_by_id("imapuser")
    search_email.send_keys(email)
    search_pass = driver.find_element_by_id("pass")
    search_pass.send_keys(password)
    search_pass.send_keys(Keys.ENTER)
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "inbox"))
        )
    except:
        pass
    time.sleep(1)
    search_inbox = driver.find_element_by_id("inbox")
    search_inbox.click()

    try:
        element = WebDriverWait(driver, 10).until(
            driver.find_element_by_xpath("/html/body").text
        )
    except:
        pass
    time.sleep(1)

    while (1):
        element = driver.find_element_by_xpath("/html/body").text
        find = element
        #match = re.search(r'\bdakika önce\b', find)
        match = ""
        if match:
            one = driver.find_element_by_xpath(
                "/html/body/div[5]/div[2]/div[6]/div[10]/div[1]/div[4]/div[1]/a/div/span")
            two = driver.find_element_by_xpath(
                "/html/body/div[5]/div[2]/div[6]/div[10]/div[1]/div[4]/div[2]/a/div/span")
            if one.text == "Verify your account":
                one.click()
                break
            elif two.text == "Verify your account":
                two.click()
                break
        else:
            time.sleep(1)

    time.sleep(5)
    driver.switch_to.frame("mail_content_body_frame")
    body = driver.find_element_by_xpath("/html/body")
    matcher = re.search(r'\d{6}', body.text).group(0)
    driver.close()
    return matcher


def challenge_code_handler(username, choice):
    global extention
    if extention == "shoezgodz.com":
        if choice == ChallengeChoice.EMAIL:
            return get_hostinger(email, passw)

    elif extention == "mail.com.tr":
        if choice == ChallengeChoice.EMAIL:
            return get_code(email, passw)

    elif extention == "iralborz.bid":
        if choice == ChallengeChoice.EMAIL:
            return get_iralborz(email)
    return False

# To Get Random Device ID
filejsonlol = open("src/kapoof.txt", "r")
devicejsonfiles = filejsonlol.readlines()
_dicks_ = []
for ele in devicejsonfiles:
    dicccc = ast.literal_eval(ele)
    _dicks_.append(dicccc)

def get_account_list(account_list_path):  # To Get Accounts
    acc_reader = open(account_list_path, "r")
    acc_list = []
    for ele in acc_reader.readlines():
        acc_list.append(ele)
    acc_reader.close()
    return acc_list

def dump_settings(proxy, account_details, row_, code):  # To Store JSON Dump (First Login with Code Verification Handler)
    if account_details[-1] == "\n":
        account_details = account_details[:-1]

    details = account_details.split(":")
    cl = instagrapi.Client()
    print(account_details, proxy, row_)

    cl.set_proxy("http://" + proxy)

    _dic_ = random.choice(_dicks_)
    cl.set_device(_dic_)
    # cl.set_locale('ru_RU')
    # cl.set_country_code(7)
    # cl.set_timezone_offset(3 * 3600)
    cl.set_locale('en_US')
    cl.set_country_code(1)
    cl.set_timezone_offset(-25200)

    global email, passw, lent, checker, xusernamex, extention
    fname = details[0].split("@")[0]
    extention = details[0].split("@")[1]

    if extention == "shoezgodz.com":
        PATH = "json_files_new/{}".format(details[1])
        email, xusernamex, passw = details[0], details[1], details[2]
    elif extention == "mail.com.tr":
        PATH = "json_files_new/{}".format(fname + "mailcomtr")
        email, passw = details[0], details[1]
    elif extention == "iralborz.bid":
        PATH = "json_files_new/{}".format(fname + "iralborz")
        email, passw = details[0], details[1]

    #checker += 1
    # print("EMAIL, USERNAME, PASSW ",email, xusernamex, passw)
    try:
        cl.challenge_code_handler = challenge_code_handler
    except requests.exceptions.HTTPError:
        time.sleep(1)
        cl.challenge_code_handler = challenge_code_handler

    username_ = "Could_not_fetch"
    try:
        if extention == "shoezgodz.com":
            print("ACCOUNT TYPE DETECTED : shoezgodz")
            cl.login(xusernamex, passw)
            print("Login Successful", account_details)
            cl.dump_settings(PATH)
            json = cl.get_settings()
            print("THE JSON IS : ", json)
            dictionary = cl.account_info()
            print(dictionary)
            username_ = dictionary.dict()["username"]
            print("username of this account is : ", username_)

        elif extention == "mail.com.tr":
            cl.login(email, passw)
            print("ACCOUNT TYPE DETECTED : mail.com.tr")
            print("Login Successful", account_details)
            cl.dump_settings(PATH)
            json = cl.get_settings()
            print("THE JSON IS : ", json)
            dictionary = cl.account_info()
            print(dictionary)
            username_ = dictionary.dict()["username"]
            print("username of this account is : ", username_)

        elif extention == "iralborz.bid":
            cl.login(email, passw)
            print("ACCOUNT TYPE DETECTED : iralborz.bid")
            print("Login Successful", account_details)
            cl.dump_settings(PATH)
            json = cl.get_settings()
            print("THE JSON IS : ", json)
            dictionary = cl.account_info()
            print(dictionary)
            username_ = dictionary.dict()["username"]
            print("username of this account is : ", username_)

    except Exception as e:
        print("EXCEPTION", e)
        return
    follower = 0
    following = 0
    number_of_posts = 0
    password = passw
    login_time = str(datetime.today().strftime("%d/%m/%y    %I:%M %p"))
    to_add = str(row_) + "::" + str(
        email) + "::" + str(password) + "::" + code + "::" + "Initial Login" + "::" + "Working" + "::" + str(
        proxy) + "::" + username_ + "::" + str(follower) + "::" + str(following) + "::" + str(
        number_of_posts) + "::" + \
             "No" + "::" + "No" + "::" + login_time + "\n"

    file = open("tempfile.txt", "a")
    file.write(to_add)
    file.close()

def seq_initial_login(sheet_path_FINAL, account_list_path, number_of_accounts, threaded_proxy_list, proxy_code, code_status):
    threaded_proxy_list = list(threaded_proxy_list)
    account_list = get_account_list(account_list_path)
    modd = len(account_list) - len(account_list) % (1 * number_of_accounts)
    print("Truncating these many accounts : ", len(account_list) % (1 * number_of_accounts))
    account_list = account_list[:modd]
    print("Accounts to be added : ", account_list)
    print("Total Accounts added : ", len(account_list))
    print("Only One Proxy used : ", threaded_proxy_list[0])

    num = 0
    # filtering
    select_from_acc = "select email from accounts"
    connection = mysql.connector.connect(host='localhost', user="root", password="Nikzzkr19@",
                                         database=sheet_path_FINAL,
                                         auth_plugin='mysql_native_password')
    c = connection.cursor()
    c.execute(select_from_acc)
    rows = c.fetchall()
    rows = [list(x) for x in rows]
    rows_dic = {}
    for ele in rows:
        rows_dic[ele[0]] = 1

    for acc in account_list:
        a = acc.split(":")[0]
        if a in rows_dic:
            account_list.remove(acc)
            print(f"{a} exists in DB, skipping account")

    print("Truncating these many accounts : ", len(account_list) % (1 * number_of_accounts))
    modd = len(account_list) - len(account_list) % (1 * number_of_accounts)
    account_list = account_list[:modd]

    proxy = threaded_proxy_list[0]

    for i in range(0, len(account_list), 1 * number_of_accounts):
        print("****************************************************************************")
        for account in range(number_of_accounts):
            dump_settings(proxy, account_list[num], num, code_status)
            num += 1
        reset_proxy(proxy, 0, proxy_code[0])
        time.sleep(7)
    save_excel(sheet_path_FINAL)






"""import ast
import datetime
import json
import os
import time
import random
import re

import requests
from instagrapi.mixins.challenge import ChallengeChoice
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import instagrapi
import instagrapi.exceptions
import ast
import datetime
import re
import time
import instagrapi
import instagrapi.exceptions
from datetime import datetime
import ast
import datetime
import json
import os
import re
import threading
import time
import random
import instagrapi
import instagrapi.exceptions
from datetime import datetime
import mysql.connector
from Instagram_FINAL.reset_proxy import reset_proxy
from Instagram_FINAL.save_excel import save_excel
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

def get_proton(email_id, password):
    #aprilwheeler.81818@protonmail.com:Hello123.
    PATH = "C:\selenium\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    driver.get("https://account.protonmail.com/login")
    time.sleep(3)
    email_input = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/main/div[2]/form/label[1]/div[2]/div/div/input")
    password_input = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/main/div[2]/form/label[2]/div[2]/div/div[1]/input")
    log_in_input = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/main/div[2]/form/button")

    email_input.send_keys(email_id)
    password_input.send_keys(password)
    log_in_input.send_keys(Keys.ENTER)

    delete_button = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/div[2]/div/nav/div[1]/button[4]")
    timeout = 0
    code_regex = "\d+"
    while (1):
        if timeout == 10:
            print("Exiting - No Code received")
            return 111111
        one = driver.find_element_by_xpath(
            "/html/body/div[1]/div[3]/div/div/div[2]/div/main/div/div[1]/div/div[2]/div/div[2]/div[1]/span")
        two = driver.find_element_by_xpath(
            "/html/body/div[1]/div[3]/div/div/div[2]/div/main/div/div[1]/div/div[3]/div/div[2]/div[1]/span")

        if "is your Instagram code" in one.text:
            t = one.text
            code_final = re.findall(code_regex, str(t))
            delete_button.click()
            return code_final[0]

        elif "is your Instagram code" in two.text:
            t = two.text
            code_final = re.findall(code_regex, str(t))
            delete_button.click()
            return code_final[0]
        else:
            driver.refresh()
            time.sleep(3)
            print("WAITING")
            timeout += 1

def get_iralborz(email_id):
    PATH = "C:\selenium\chromedriver.exe"
    # PATH = r"D:\Programming\INSTAGRAM\InstaBot\openbeta\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    driver.get("http://ruu.kr/")
    time.sleep(1)
    sel = Select(driver.find_element_by_id("domain"))
    sel.select_by_visible_text("iralborz.bid")

    search_email = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div[1]/form/input[3]")
    time.sleep(1)
    search_email.send_keys(email_id.split("@")[0])
    time.sleep(3)

    # /html/body/div[1]/div[1]/div/div[1]/form/span
    refresh = driver.find_element_by_id("mailList")
    timeout = 1
    while (1):
        if timeout == 10:
            return 111111
        element = driver.find_element_by_xpath("/html/body").text
        find = element
        match = re.search(r'Verify your account', find)
        if match:
            one = driver.find_element_by_xpath(
                "/html/body/div[1]/div[1]/div/div[3]/table/tbody/tr[1]/td[2]/font")

            if one.text == "Verify your account":
                one.click()
                break

            two = driver.find_element_by_xpath(
                "/html/body/div[1]/div[1]/div/div[3]/table/tbody/tr[2]/td[2]/font")

            if two.text == "Verify your account":
                two.click()
                break
            else:
                refresh.click()
                time.sleep(3)
                print("WAITING")
        else:
            refresh.click()
            time.sleep(3)
            print("WAITING")
            timeout += 1

    time.sleep(3)
    code = driver.find_element_by_xpath(
        "/html/body/div[1]/div[1]/div/div[2]/table/tbody/tr/td/table/tbody/tr[4]/td/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td/p[4]/font")
    # code = driver.find_element_by_xpath('//*[@id="email_content"]/table/tbody/tr[4]/td/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr/td/p[4]/font')
    return code.text


# SELENIUM FOR HOSTINGER
def get_hostinger(email, password):
    today = datetime.datetime.now()
    date_time = today.strftime("%H:%M")
    search_curr = "Today " + date_time[:-2]
    print(search_curr)
    PATH = "C:\selenium\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    driver.get("https://mail.hostinger.com/")
    time.sleep(1)
    search_email = driver.find_element_by_id("rcmloginuser")
    search_email.send_keys(email)
    search_pass = driver.find_element_by_id("rcmloginpwd")
    search_pass.send_keys("Hello123.")
    search_pass.send_keys(Keys.ENTER)

    while (1):
        element = driver.find_element_by_xpath("/html/body").text
        refresh = driver.find_element_by_id("rcmbtn110")
        find = element
        match = re.search(r'{}'.format(search_curr), find)
        if match:
            one = driver.find_element_by_xpath(
                "/html/body/div[1]/div[3]/div[4]/table[2]/tbody/tr[1]/td[2]/span[3]/a/span")
            two = driver.find_element_by_xpath(
                "/html/body/div[1]/div[3]/div[4]/table[2]/tbody/tr[2]/td[2]/span[3]/a/span")
            if one.text == "Verify your account":
                one.click()
                break
            elif two.text == "Verify your account":
                two.click()
                break
            else:
                refresh.click()
                print("REFRESHING")
                time.sleep(3)
        else:
            refresh.click()
            print("REFRESHING")
            time.sleep(3)

    time.sleep(5)
    driver.switch_to.frame("messagecontframe")
    body = driver.find_element_by_xpath("/html/body")
    matcher = re.search(r'\d{6}', body.text).group(0)

    print(matcher)
    if matcher:
        driver.switch_to.default_content()
        delete = driver.find_element_by_id("rcmbtn122")
        two.click()
        delete.click()
        one.click()
        delete.click()
        driver.close()
        return matcher


# SELENIUM PART for mail.com.tr
def get_code(email, password):
    # PATH = "C:\Program Files (x86)\chromedriver.exe"
    PATH = "C:\selenium\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    driver.get("https://mail.com.tr")
    time.sleep(1)
    search_email = driver.find_element_by_id("imapuser")
    search_email.send_keys(email)
    search_pass = driver.find_element_by_id("pass")
    search_pass.send_keys(password)
    search_pass.send_keys(Keys.ENTER)
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "inbox"))
        )
    except:
        pass
    time.sleep(1)
    search_inbox = driver.find_element_by_id("inbox")
    search_inbox.click()

    try:
        element = WebDriverWait(driver, 10).until(
            driver.find_element_by_xpath("/html/body").text
        )
    except:
        pass
    time.sleep(1)

    while (1):
        element = driver.find_element_by_xpath("/html/body").text
        find = element
        match = "jamoon"
        #match = re.search(r'\\bdakika önce\\b', find)
        if match:
            one = driver.find_element_by_xpath(
                "/html/body/div[5]/div[2]/div[6]/div[10]/div[1]/div[4]/div[1]/a/div/span")
            two = driver.find_element_by_xpath(
                "/html/body/div[5]/div[2]/div[6]/div[10]/div[1]/div[4]/div[2]/a/div/span")
            if one.text == "Verify your account":
                one.click()
                break
            elif two.text == "Verify your account":
                two.click()
                break
        else:
            time.sleep(1)

    time.sleep(5)
    driver.switch_to.frame("mail_content_body_frame")
    body = driver.find_element_by_xpath("/html/body")
    matcher = re.search(r'\d{6}', body.text).group(0)
    driver.close()
    return matcher


def challenge_code_handler(username, choice):
    global extention
    if extention == "shoezgodz.com":
        if choice == ChallengeChoice.EMAIL:
            return get_hostinger(email, passw)

    elif extention == "mail.com.tr":
        if choice == ChallengeChoice.EMAIL:
            return get_code(email, passw)

    elif extention == "iralborz.bid":
        if choice == ChallengeChoice.EMAIL:
            return get_iralborz(email)

    elif extention == "protonmail.com":
        if choice == ChallengeChoice.EMAIL:
            return get_proton(email, passw)

    return False

# To Get Random Device ID
filejsonlol = open("src/kapoof.txt", "r")
devicejsonfiles = filejsonlol.readlines()
_dicks_ = []
for ele in devicejsonfiles:
    dicccc = ast.literal_eval(ele)
    _dicks_.append(dicccc)

def get_account_list(account_list_path):  # To Get Accounts
    acc_reader = open(account_list_path, "r")
    acc_list = []
    for ele in acc_reader.readlines():
        acc_list.append(ele)
    acc_reader.close()
    return acc_list

def dump_settings(proxy, account_details, row_, code):  # To Store JSON Dump (First Login with Code Verification Handler)
    if account_details[-1] == "\n":
        account_details = account_details[:-1]

    details = account_details.split(":")
    cl = instagrapi.Client()
    print(account_details, proxy, row_)

    cl.set_proxy("http://" + proxy)

    _dic_ = random.choice(_dicks_)
    cl.set_device(_dic_)
    # cl.set_locale('ru_RU')
    # cl.set_country_code(7)
    # cl.set_timezone_offset(3 * 3600)
    cl.set_locale('en_US')
    cl.set_country_code(1)
    cl.set_timezone_offset(-25200)

    global email, passw, lent, checker, xusernamex, extention
    fname = details[0].split("@")[0]
    extention = details[0].split("@")[1]

    if extention == "shoezgodz.com":
        PATH = "json_files_new/{}".format(details[1])
        email, xusernamex, passw = details[0], details[1], details[2]
    elif extention == "mail.com.tr":
        PATH = "json_files_new/{}".format(fname + "mailcomtr")
        email, passw = details[0], details[1]
    elif extention == "iralborz.bid":
        PATH = "json_files_new/{}".format(fname + "iralborz")
        email, passw = details[0], details[1]
    elif extention == "protonmail.com":
        PATH = "json_files_new/{}".format(fname + "protonmail")
        email, passw = details[0], details[1]

    #checker += 1
    # print("EMAIL, USERNAME, PASSW ",email, xusernamex, passw)
    try:
        cl.challenge_code_handler = challenge_code_handler
    except requests.exceptions.HTTPError:
        time.sleep(1)
        cl.challenge_code_handler = challenge_code_handler

    username_ = "Could_not_fetch"
    try:
        if extention == "shoezgodz.com":
            print("ACCOUNT TYPE DETECTED : shoezgodz")
            cl.login(xusernamex, passw)
            print("Login Successful", account_details)
            cl.dump_settings(PATH)
            json = cl.get_settings()
            print("THE JSON IS : ", json)
            dictionary = cl.account_info()
            print(dictionary)
            username_ = dictionary.dict()["username"]
            print("username of this account is : ", username_)

        elif extention == "mail.com.tr":
            cl.login(email, passw)
            print("ACCOUNT TYPE DETECTED : mail.com.tr")
            print("Login Successful", account_details)
            cl.dump_settings(PATH)
            json = cl.get_settings()
            print("THE JSON IS : ", json)
            dictionary = cl.account_info()
            print(dictionary)
            username_ = dictionary.dict()["username"]
            print("username of this account is : ", username_)

        elif extention == "iralborz.bid":
            cl.login(email, passw)
            print("ACCOUNT TYPE DETECTED : iralborz.bid")
            print("Login Successful", account_details)
            cl.dump_settings(PATH)
            json = cl.get_settings()
            print("THE JSON IS : ", json)
            dictionary = cl.account_info()
            print(dictionary)
            username_ = dictionary.dict()["username"]
            print("username of this account is : ", username_)

        elif extention == "protonmail.com":
            cl.login(email, passw)
            print("ACCOUNT TYPE DETECTED : protonmail.com")
            print("Login Successful", account_details)
            cl.dump_settings(PATH)
            json = cl.get_settings()
            print("THE JSON IS : ", json)
            dictionary = cl.account_info()
            print(dictionary)
            username_ = dictionary.dict()["username"]
            print("username of this account is : ", username_)

    except Exception as e:
        print("EXCEPTION", e)
        return
    follower = 0
    following = 0
    number_of_posts = 0
    password = passw
    login_time = str(datetime.today().strftime("%d/%m/%y    %I:%M %p"))
    to_add = str(row_) + "::" + str(
        email) + "::" + str(password) + "::" + code + "::" + "Initial Login" + "::" + "Working" + "::" + str(
        proxy) + "::" + username_ + "::" + str(follower) + "::" + str(following) + "::" + str(
        number_of_posts) + "::" + \
             "No" + "::" + "No" + "::" + login_time + "\n"

    file = open("tempfile.txt", "a")
    file.write(to_add)
    file.close()

def seq_initial_login(sheet_path_FINAL, account_list_path, number_of_accounts, threaded_proxy_list, proxy_code, code_status):
    account_list = get_account_list(account_list_path)
    modd = len(account_list) - len(account_list) % (1 * number_of_accounts)
    print("Truncating these many accounts : ", len(account_list) % (1 * number_of_accounts))
    account_list = account_list[:modd]
    print("Accounts to be added : ", account_list)
    print("Total Accounts added : ", len(account_list))
    print("The Proxies used : ", threaded_proxy_list[0])
    num = 0
    # filtering
    select_from_acc = "select email from accounts"
    connection = mysql.connector.connect(host='localhost', user="root", password="Nikzzkr19@",
                                         database=sheet_path_FINAL,
                                         auth_plugin='mysql_native_password')
    c = connection.cursor()
    c.execute(select_from_acc)
    rows = c.fetchall()
    rows = [list(x) for x in rows]
    rows_dic = {}
    for ele in rows:
        rows_dic[ele[0]] = 1

    for acc in account_list:
        a = acc.split(":")[0]
        if a in rows_dic:
            account_list.remove(acc)
            print(f"{a} exists in DB, skipping account")

    print("Truncating these many accounts : ", len(account_list) % (1 * number_of_accounts))
    modd = len(account_list) - len(account_list) % (1 * number_of_accounts)
    account_list = account_list[:modd]

    proxy = threaded_proxy_list[0]
    for i in range(0, len(account_list), 1 * number_of_accounts):
        print("****************************************************************************")
        for account in range(number_of_accounts):
            dump_settings(proxy, account_list[num], num, code_status)
            num += 1
        reset_proxy(proxy, 0, proxy_code[0])
        time.sleep(7)
    save_excel(sheet_path_FINAL)




"""