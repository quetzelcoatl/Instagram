import ast
import datetime
import json
import os
import re
import sqlite3
import threading
import time
import random
import instagrapi
import instagrapi.exceptions
from Instagram_FINAL.reset_proxy import reset_proxy
from datetime import datetime

from Instagram_FINAL.save_excel import save_excel


def follow_helper(proxy_temp, code, account_temp, _row_, start_follow, stop_follow, follow_arr):
    acc_details = account_temp.split(":")
    cl = instagrapi.Client()

    global email, passw, lent, checker, xusernamex, extention
    email, passw = acc_details[0], acc_details[1]
    extention = acc_details[0].split("@")[1]
    print(acc_details)

    if extention == "shoezgodz.com":
        PATH = "json_files_new/{}".format(acc_details[1])
        print("shoezgodz.com : ", PATH)
        email, xusernamex, passw = acc_details[0], acc_details[1], acc_details[2]
    elif extention == "mail.com.tr":
        fname = acc_details[0].split("@")[0]
        PATH = "json_files_new/{}".format(fname + "mailcomtr")
        print("mail.com.tr : ", PATH)
        email, passw = acc_details[0], acc_details[1]
    elif extention == "iralborz.bid":
        fname = acc_details[0].split("@")[0]
        PATH = "json_files_new/{}".format(fname + "iralborz")
        print("iralborz.bid : ", PATH)
        email, passw = acc_details[0], acc_details[1]
    elif extention == "protonmail.com":
        fname = acc_details[0].split("@")[0]
        PATH = "json_files_new/{}".format(fname + "protonmail")
        print("protonmail.com : ", PATH)
        email, passw = acc_details[0], acc_details[1]

    cl.set_proxy("http://" + proxy_temp)
    cl.load_settings(PATH)
    last_login = str(datetime.today().strftime("%d/%m/%y    %I:%M %p"))

    if extention == "shoezgodz.com":
        cl.login(xusernamex, passw)
    elif extention == "mail.com.tr":
        cl.login(email, passw)
    elif extention == "iralborz.bid":
        cl.login(email, passw)
    elif extention == "protonmail.com":
        cl.login(email, passw)

    cl.get_timeline_feed()
    regex_following = "follower_count=\d+"
    regex_follower = "following_count=\d+"
    dictionary = cl.account_info()
    username_ = dictionary.dict()["username"]
    info = str(cl.user_info_by_username(username_))
    info = info.replace("\n", "")
    info = info.replace("\t", "")
    following = re.findall(regex_following, info)[0].split("=")[1]
    follower = re.findall(regex_follower, info)[0].split("=")[1]
    print("Number Following are : ", following)
    print("Number Followers are : ", follower)

    print("Login Successful with account : ", acc_details)
    number_rand = random.randrange(start_follow, stop_follow)
    to_follow = random.choices(follow_arr, k=number_rand)

    for element in to_follow:
        try:
            cl.user_follow(cl.user_id_from_username(element))
            print("followed", element)
        except instagrapi.exceptions.ChallengeRequired:
            print("ChallengeRequired", acc_details)

            to_add = str(_row_) + "::" + "Follow Done" \
                     + "::" + "Challenge Required" + "::" + str(proxy_temp) + "::" + str(last_login) + \
                     "::" + "_pass_" + "::" + "_pass_" + "\n"

            file = open("tempfile.txt", "a")
            file.write(to_add)
            file.close()

            karambit = open("database/challenge_req.txt", "a")
            karambit.write(str(account_temp) + "\n")
            karambit.close()
            print("Challenge_required_statement")
            return

        except Exception as e:
            print("error while following : ", e)
            follow_error = True
            to_add = str(_row_) + "::" + "Error Follow" \
                     + "::" + "Working" + "::" + str(proxy_temp) + "::" + str(last_login) + \
                     "::" + "_pass_" + "::" + "_pass_" + "\n"

            file = open("tempfile.txt", "a")
            file.write(to_add)
            file.close()
            return

    follower = int(follower) + number_rand
    #follower, following = following, follower
    to_add = str(_row_) + "::" + "Follow Done" \
             + "::" + "Working" + "::" + str(proxy_temp) + "::" + str(last_login) + \
             "::" + str(follower) + "::" + str(following) + "\n"

    file = open("tempfile.txt", "a")
    file.write(to_add)
    file.close()


def threaded_follow_only(sheet_path_FINAL, code, id_arr, accounts_arr, number_of_accounts, threaded_proxy_list,
                         proxy_code, follow_path, start_follow, stop_follow):
    row_number, retrieved_acc = id_arr, accounts_arr

    #start_follow, stop_follow = input("Select The start and stop follow random number range\n").split()
    #start_follow = int(start_follow)
    #stop_follow = int(stop_follow)

    follow_arr = []
    follow_file = open(follow_path, "r")
    for ele in follow_file.readlines():
        follow_arr.append(ele)
    follow_file.close()
    follow_arr = [x[:-1] if x[-1] == "\n" else x for x in follow_arr]
    print("Posting reels in : ", retrieved_acc)
    print("Posting reels for the row numbers : ", row_number)
    print("Number of accs :", len(retrieved_acc))
    print("Following these accounts : ", follow_arr)

    modd = len(row_number) - len(row_number) % (len(threaded_proxy_list) * number_of_accounts)
    print("Truncating these many accounts : ", len(row_number) % (len(threaded_proxy_list) * number_of_accounts))
    row_number = row_number[:modd]
    print("Row Numbers are : ", row_number)
    print("Length of row numbers are : ", len(row_number))
    print("The Proxies used are : ", threaded_proxy_list)
    num = 0

    for i in range(0, len(row_number), len(threaded_proxy_list) * number_of_accounts):
        current_threads = []
        print("*************************************************************************", i)
        for proxy in threaded_proxy_list:
            for j in range(number_of_accounts):
                current_threads.append(threading.Thread(target=follow_helper, args=(
                    proxy, code, retrieved_acc[num], row_number[num], start_follow, stop_follow, follow_arr)))
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
        time.sleep(30)
    save_excel(sheet_path_FINAL)