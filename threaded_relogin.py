import ast
import datetime
import json
import os
import random
import re
import sqlite3
import threading
import time
import instagrapi
import instagrapi.exceptions
from datetime import datetime
from Instagram_FINAL.reset_proxy import reset_proxy
from Instagram_FINAL.save_excel import save_excel

filejsonlol = open("testing/kapoof.txt", "r")
devicejsonfiles = filejsonlol.readlines()
_dicks_ = []
for ele in devicejsonfiles:
    dicccc = ast.literal_eval(ele)
    _dicks_.append(dicccc)

def json_relogin(proxy, code, account_details, row_, condition):
    sheet_acc = account_details
    if account_details[-1] == "\n":
        sheet_acc = account_details[:-1]

    print(proxy, sheet_acc, row_)
    details = sheet_acc.split(":")
    cl = instagrapi.Client()
    login_time = str(datetime.today().strftime("%d/%m/%y    %I:%M %p"))

    cl.set_proxy("http://" + proxy)
    extention = details[0].split("@")[1]
    print(details)

    if extention == "shoezgodz.com":
        PATH = "json_files_new/{}".format(details[1])
        print("shoezgodz.com : ", PATH)
        email, xusernamex, passw = details[0], details[1], details[2]
    elif extention == "mail.com.tr":
        fname = details[0].split("@")[0]
        PATH = "json_files_new/{}".format(fname + "mailcomtr")
        print("mail.com.tr : ", PATH)
        email, passw = details[0], details[1]
    elif extention == "iralborz.bid":
        fname = details[0].split("@")[0]
        PATH = "json_files_new/{}".format(fname + "iralborz")
        print("iralborz.bid : ", PATH)
        email, passw = details[0], details[1]
    elif extention == "protonmail.com":
        fname = details[0].split("@")[0]
        PATH = "json_files_new/{}".format(fname + "protonmail")
        print("protonmail.com : ", PATH)
        email, passw = details[0], details[1]

    cl.set_proxy("http://" + proxy)
    if condition == 2:
        cl.set_locale('en_US')
        cl.set_country_code(1)
        cl.set_timezone_offset(-25200)
        _dic_ = random.choice(_dicks_)
        cl.set_device(_dic_)

    if condition == 1:
        cl.load_settings(PATH)

    fname = details[0].split("@")[0]
    extentionZ = details[0].split("@")[1]

    def challenge_code_handler(username, choice):
        return 111111

    try:
        cl.challenge_code_handler = challenge_code_handler
    except:
        file3 = open("thread_helper.txt", "a")
        file3.write(sheet_acc + "\n")
        file3.close()

    try:
        if extentionZ == "shoezgodz.com":
            cl.login(xusernamex, passw)
            cl.get_timeline_feed()
            if condition == 2:
                cl.dump_settings(PATH)

        elif extentionZ == "mail.com.tr":
            cl.login(email, passw)
            cl.get_timeline_feed()
            if condition == 2:
                cl.dump_settings(PATH)

        elif extentionZ == "iralborz.bid":
            cl.login(email, passw)
            cl.get_timeline_feed()
            if condition == 2:
                cl.dump_settings(PATH)

        elif extention == "protonmail.com":
            cl.login(email, passw)
            cl.get_timeline_feed()
            if condition == 2:
                cl.dump_settings(PATH)

        print("Login Succesful")
        likes_regex = "like_count=\d+"
        views_regex = "view_count=\d+"
        regex_following = "follower_count=\d+"
        regex_follower = "following_count=\d+"
        regex_biography = "biography=.+ e"
        regex_external_url = "external_url=.+ i"
        dictionary = cl.account_info()
        username_ = dictionary.dict()["username"]
        info = str(cl.user_info_by_username(username_))
        pk_regex = "pk='\d+"
        pk_temp = re.findall(pk_regex, info)
        pk = pk_temp[0].split("=")[1][1:]
        info = info.replace("\n", "")
        info = info.replace("\t", "")
        view_raw = cl.user_medias(pk)
        print("*****")
        following = re.findall(regex_following, info)[0].split("=")[1]
        follower = re.findall(regex_follower, info)[0].split("=")[1]
        biography = re.findall(regex_biography, info)[0].split("'")[1]
        external_url = re.findall(regex_external_url, info)[0][:-2].split("=")[1]
        views = re.findall(views_regex, str(view_raw))
        likes = re.findall(likes_regex, str(view_raw))
        views = [x.split("=")[1] for x in views]
        likes = [x.split("=")[1] for x in likes]
        s = ""
        l = ""
        for ele in views:
            s += str(ele) + ","
        for ele in likes:
            l += str(ele) + ","
        views_string = s[:-1]
        likes_string = l[:-1]
        print("Views Are : ", views_string)
        print("Number Following are : ", following)
        print("Number Followers are : ", follower)
        print("Current Bio : ", biography)
        print("Likes : ", likes_string)
        print("External URL used in BIO : ", external_url)

        number_of_reels = len(views)
        reels_views = views_string
        reels_likes = likes_string
        to_add = str(row_) + "::" + str(
            email) + "::" + str(passw) + "::" + str(code) + "::" + "Relogin Working" + \
                 "::" + str(proxy) + "::" + str(number_of_reels) + "::" + str(reels_views) + \
                 "::" + str(reels_likes) + "::" + str(biography) + "::" + str(external_url) + "::" + str(login_time) + \
                 "::" + str(follower) + "::" + str(following) + "\n"

        file = open("tempfile.txt", "a")
        file.write(to_add)
        file.close()

    except instagrapi.exceptions.ChallengeRequired:
        print("ChallengeRequired", sheet_acc)

        to_add = str(row_) + "::" + str(
            email) + "::" + str(passw) + "::" + str(code) + "::" + "Relogin Challenge Required" + \
                 "::" + str(proxy) + "::" + "_pass_" + "::" + "_pass_" + \
                 "::" + "_pass_" + "::" + "_pass_" + "::" + "_pass_" + "::" + str(login_time) + \
                 "::" + "_pass_" + "::" + "_pass_" + "\n"

        file = open("tempfile.txt", "a")
        file.write(to_add)
        file.close()

        karambit = open("database/challenge_req.txt", "a")
        karambit.write(str(sheet_acc) + "\n")
        karambit.close()
        print("Challenge_required_statement")
        return

    except Exception as e:
        print(e)
        to_add = str(row_) + "::" + str(
            email) + "::" + str(passw) + "::" + str(code) + "::" + "Relogin Error" + \
                 "::" + str(proxy) + "::" + "_pass_" + "::" + "_pass_" + \
                 "::" + "_pass_" + "::" + "_pass_" + "::" + "_pass_" + "::" + str(login_time) + \
                 "::" + "_pass_" + "::" + "_pass_" + "\n"

        file = open("tempfile.txt", "a")
        file.write(to_add)
        file.close()

        print(to_add)

def threaded_relogin(sheet_path_FINAL, code, id_arr, accounts_arr ,number_of_accounts, threaded_proxy_list, proxy_code):
    row_number, retrieved_acc = id_arr, accounts_arr,

    print("Accounts Under Scruitiny : ", retrieved_acc)
    print("Row numbers Under Scruitiny : ", row_number)
    print("Number of accs :", len(retrieved_acc))

    modd = len(row_number) - len(row_number) % (len(threaded_proxy_list) * number_of_accounts)
    print("Truncating these many accounts : ", len(row_number) % (len(threaded_proxy_list) * number_of_accounts))
    row_number = row_number[:modd]
    print("Row Numbers are : ", row_number)
    print("Length of row numbers are : ", len(row_number))
    print("The Proxies used are : ", threaded_proxy_list)
    num = 0

    condition = 0
    inpp = input("Press 1) For Account Checker and 2) For New JSON Relogin\n")
    if inpp == "1":
        condition = 1
    else:
        condition = 2

    if condition == 0:
        return

    for i in range(0, len(row_number), len(threaded_proxy_list) * number_of_accounts):
        current_threads = []
        print("*************************************************************************", i)
        for proxy in threaded_proxy_list:
            for j in range(number_of_accounts):
                current_threads.append(threading.Thread(target=json_relogin,
                                                        args=(proxy, code, retrieved_acc[num], row_number[num], condition)))
                num += 1

        for thread in current_threads:
            time.sleep(0.5)
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
        time.sleep(50)
    save_excel(sheet_path_FINAL)