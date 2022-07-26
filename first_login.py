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

filejsonlol = open("testing/kapoof.txt", "r")
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
    sheet_acc = account_details
    if account_details[-1] == "\n":
        sheet_acc = account_details[:-1]

    print(proxy, sheet_acc, row_ + 1, code)
    details = sheet_acc.split(":")
    cl = instagrapi.Client()
    login_time = str(datetime.today().strftime("%d/%m/%y    %I:%M %p"))

    cl.set_proxy("http://" + proxy)
    _dic_ = random.choice(_dicks_)
    cl.set_device(_dic_)
    # cl.set_locale('ru_RU')
    # cl.set_country_code(7)
    # cl.set_timezone_offset(3 * 3600)

    #############################################################################################
    ################################### CHANGING LOCALE #########################################
    #############################################################################################

    cl.set_locale('en_US')
    cl.set_country_code(1)
    cl.set_timezone_offset(-25200)

    #############################################################################################
    ################################### CHANGING LOCALE #########################################
    #############################################################################################
    fname = details[0].split("@")[0]
    extentionZ = details[0].split("@")[1]

    if extentionZ == "shoezgodz.com":
        PATH = "json_files_new/{}".format(details[1])
        email, xusernamex, passw = details[0], details[1], details[2]
    elif extentionZ == "mail.com.tr":
        PATH = "json_files_new/{}".format(fname + "mailcomtr")
        email, passw = details[0], details[1]
    elif extentionZ == "iralborz.bid":
        PATH = "json_files_new/{}".format(fname + "iralborz")
        email, passw = details[0], details[1]
    elif extentionZ == "protonmail.com":
        PATH = "json_files_new/{}".format(fname + "protonmail")
        email, passw = details[0], details[1]

    password = passw
    def challenge_code_handler(username, choice):
        return 111111

    try:
        cl.challenge_code_handler = challenge_code_handler
    except:
        file3 = open("src/thread_helper.txt", "a")
        file3.write(sheet_acc + "\n")
        file3.close()

    username_ = "Could_not_fetch"
    try:
        if extentionZ == "shoezgodz.com":
            cl.login(xusernamex, passw)
            cl.dump_settings(PATH)
            json = cl.get_settings()
            print("THE JSON IS : ", json)
            dictionary = cl.account_info()
            username_ = dictionary.dict()["username"]
            print("username of this account is : ", username_)

        elif extentionZ == "mail.com.tr":
            cl.login(email, passw)
            cl.dump_settings(PATH)
            json = cl.get_settings()
            print("THE JSON IS : ", json)
            dictionary = cl.account_info()
            username_ = dictionary.dict()["username"]
            print("username of this account is : ", username_)

        elif extentionZ == "iralborz.bid":
            cl.login(email, passw)
            cl.dump_settings(PATH)
            json = cl.get_settings()
            print("THE JSON IS : ", json)
            dictionary = cl.account_info()
            username_ = dictionary.dict()["username"]
            print("username of this account is : ", username_)

        elif extentionZ == "protonmail.com":
            cl.login(email, passw)
            cl.dump_settings(PATH)
            json = cl.get_settings()
            print("THE JSON IS : ", json)
            dictionary = cl.account_info()
            username_ = dictionary.dict()["username"]
            print("username of this account is : ", username_)


        regex_following = "follower_count=\d+"
        regex_follower = "following_count=\d+"
        info = str(cl.user_info_by_username(username_))
        info = info.replace("\n", "")
        info = info.replace("\t", "")
        following = re.findall(regex_following, info)[0].split("=")[1]
        follower = re.findall(regex_follower, info)[0].split("=")[1]
        print("Number Following are : ", following)
        print("Number Followers are : ", follower)

        password = passw
        number_of_posts = 0

        to_add = str(row_) + "::" + str(
                email) + "::" + str(password) + "::" + code + "::" + "Initial Login" + "::" + "Working" + "::" + str(
                proxy) + "::" + username_ + "::" + str(follower) + "::" + str(following) + "::" + str(
                number_of_posts) + "::" + \
                     "No" + "::" + "No" + "::" + login_time  + "\n"

        file = open("tempfile.txt", "a")
        file.write(to_add)
        file.close()

    except Exception as e:
        print("%%%%%%%%%%%%%%%% ERROR %%%%%%%%%%%%%%% ", e)
        file3 = open("thread_helper.txt", "a")
        file3.write(sheet_acc + "\n")
        file3.close()

        to_add = str(row_) + "::" + str(
                email) + "::" + str(
                password) + "::" + code + "::" + "Error Initial Login" + "::" + "Not Working" + "::" + str(
                proxy) + "::" + "_pass_" + "::" + "_pass_" + "::" + "_pass_" + "::" + \
                "_pass_" + "::" + \
                     "No" + "::" + "No" + "::" + login_time + "\n"

        file = open("tempfile.txt", "a")
        file.write(to_add)
        file.close()

def first_login(sheet_path_FINAL, account_list_path, number_of_accounts, threaded_proxy_list, proxy_code, code_status):
    #code_status = input("Enter the Code to represent the accounts : ")

    account_list = get_account_list(account_list_path)
    modd = len(account_list) - len(account_list) % (len(threaded_proxy_list) * number_of_accounts)
    print("Truncating these many accounts : ", len(account_list) % (len(threaded_proxy_list) * number_of_accounts))
    account_list = account_list[:modd]
    print("Accounts to be added : ", account_list)
    print("Total Accounts added : ", len(account_list))
    print("The Proxies used : ", threaded_proxy_list)
    num = 0

    #filtering
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
    """file = open("testing/accounts.txt", "r")
    file = file.readlines()
    file = [x[:-1] if x[-1] == "\n" else x for x in file]"""

    for acc in account_list:
        a = acc.split(":")[0]
        if a in rows_dic:
            account_list.remove(acc)
            print(f"{a} exists in DB, not skipping account")


    for i in range(0, len(account_list), len(threaded_proxy_list) * number_of_accounts):
        current_threads = []
        print("*************************************************************************", i)
        for proxy in threaded_proxy_list:
            for j in range(number_of_accounts):
                current_threads.append(threading.Thread(target=dump_settings,
                                                        args=(proxy, account_list[num], num, code_status)))
                #$print(num, j, i)
                num += 1
        for thread in current_threads:
            time.sleep(0.25)
            thread.start()
        for thread in current_threads:
            thread.join()

        reset_proxy_thread_list = []
        for ind, proxy in enumerate(threaded_proxy_list):
            reset_proxy_thread_list.append(threading.Thread(target=reset_proxy, args=(proxy, ind, proxy_code)))
        for r in reset_proxy_thread_list:
            r.start()
        for r in reset_proxy_thread_list:
            r.join()
        time.sleep(15)
    save_excel(sheet_path_FINAL)
