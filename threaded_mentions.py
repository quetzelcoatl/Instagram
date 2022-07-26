import ast
import datetime
import json
import os
import re
import sqlite3
import threading
import time
import instagrapi
import instagrapi.exceptions
from datetime import datetime

from Instagram_FINAL.save_excel import save_excel

global read_from_mentions
from Instagram_FINAL.reset_proxy import reset_proxy


def name_pop():
    global read_from_mentions
    temp = ""
    for i in range(9):
        temp += "@" + read_from_mentions.pop(0) + " "
    return temp


def mentions_helper(proxy_temp, account_temp, _row_, mentions_post_url, code):
    last_login = str(datetime.today().strftime("%d/%m/%y    %I:%M %p"))
    print("Using account : ", account_temp)
    print("Using Proxy : ", proxy_temp)

    acc_details = account_temp.split(":")
    cl = instagrapi.Client()

    # global email, passw, lent, checker, xusernamex, extention
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

    proxy = proxy_temp
    cl.set_proxy("http://" + proxy)
    cl.load_settings(PATH)

    try:

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
        media_id = cl.media_id(cl.media_pk_from_url(mentions_post_url))
        iter = 1
        max_retries = 5
        final_popped_mentions = ""
        while iter > 0 and max_retries > 0:
            max_retries -= 1
            print(media_id, type(media_id))
            try:
                popped_users = name_pop()
                comment = cl.media_comment(media_id, popped_users)
            except Exception as e:
                print(e)
                continue
            final_popped_mentions += str(popped_users)
            iter -= 1
            print(comment)
        mentions_list = final_popped_mentions

        to_add = str(_row_) + "::" + str(email) + "::" + str(passw) + "::" + str(code) + "::" + "Mentions Done" \
                 + "::" + "Working" + "::" + str(proxy) + "::" + str(mentions_list) + "::" + str(last_login) + \
                 "::" + str(follower) + "::" + str(following) + "\n"
        file = open("tempfile.txt", "a")
        file.write(to_add)
        file.close()

    except instagrapi.exceptions.ChallengeRequired:
        print("ChallengeRequired", acc_details)
        to_add = str(_row_) + "::" + str(email) + "::" + str(passw) + "::" + str(code) + "::" + "Error Mentions" \
                 + "::" + "Not Working" + "::" + str(proxy) + "::" + "_pass_" + "::" + str(last_login) + \
                 "::" + "_pass_" + "::" + "_pass_" + "\n"
        file = open("tempfile.txt", "a")
        file.write(to_add)
        file.close()
        karambit = open("database/challenge_req.txt", "a")
        karambit.write(str(account_temp) + "\n")
        karambit.close()
        return

    except Exception as e:
        to_add = str(_row_) + "::" + str(email) + "::" + str(passw) + "::" + str(
            code) + "::" + "Error Mentions" + "::" + "Working" \
                 + "::" + str(proxy) + "::" + "_pass_" + "::" + str(last_login) + \
                 "::" + "_pass_" + "::" + "_pass_" + "\n"
        file = open("tempfile.txt", "a")
        file.write(to_add)
        file.close()
        print(to_add)
        print(e, acc_details)
        print(to_add)


def mentions(sheet_path_FINAL, code, id_arr, accounts_arr, number_of_accounts, threaded_proxy_list, proxy_code,
             read_from_mention, mentions_post_url):
    row_number, retrieved_acc = id_arr, accounts_arr

    global read_from_mentions
    read_from_mentions = read_from_mention

    print("Using accounts for posting comments : ", retrieved_acc)
    print("Accounts used in Comments : ", read_from_mentions)
    print("Posting reels for the row numbers : ", row_number)
    print("Number of accs :", len(retrieved_acc))
    print("Posting comments in post : ", mentions_post_url)

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
                current_threads.append(threading.Thread(target=mentions_helper,
                                                        args=(
                                                        proxy, retrieved_acc[num], row_number[num], mentions_post_url,
                                                        code)))
                num += 1

        for thread in current_threads:
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
        time.sleep(7)

    save_excel(sheet_path_FINAL)
