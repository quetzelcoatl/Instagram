import ast
import datetime
import json
import os
import re
import sqlite3
import threading
import time
import spintax
import instagrapi
import instagrapi.exceptions
from datetime import datetime
from Instagram_FINAL.reset_proxy import reset_proxy
from Instagram_FINAL.save_excel import save_excel

global read_from_dm_file

def dm_pop():
    temp = ""
    for i in range(1):
        temp += read_from_dm_file.pop(0) + "::"
    return temp

def dm_helper(proxy_temp, account_temp, _row_, dm_message, code):
    last_login = str(datetime.today().strftime("%d/%m/%y    %I:%M %p"))
    print("Using account : ", account_temp)
    print("Using Proxy : ", proxy_temp)

    acc_details = account_temp.split(":")
    cl = instagrapi.Client()

    #global email, passw, lent, checker, xusernamex, extention
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
        #dm_message = "{Hello|Hi|Hi!|Shukriya!|Myself} {I have something of value|I have somthing insane! |How are you doing?|Hope you're doing well? |I have a very important message to deliver.} {If you follow me back good things will happen to you|I have a heart made of silicon!|I would like to elicit response from yourside, dear sire.} {What does not kill me only makes me stronger.|Above all, don't lie to yourself!|The darker the night, the brighter the stars|The Gold is in the Dark|Error is the force that welds men together; Truth is communicated to men only by deeds of truth.}"
        if extention == "shoezgodz.com":
            cl.login(xusernamex, passw)
        elif extention == "mail.com.tr":
            cl.login(email, passw)
        elif extention == "iralborz.bid":
            cl.login(email, passw)
        elif extention == "protonmail.com":
            cl.login(email, passw)

        cl.get_timeline_feed()
        dm_final = dm_pop().split("::")
        dm_final_here = []
        for ele in dm_final:
            if ele != "":
                dm_final_here.append(ele)
        print("Sending Messages to Users {} from Account {} : ".format(dm_final_here, account_temp))
        for ele in dm_final:
            try:
                msg_send = spintax.spin(dm_message)
                print("Sending Message '{}' To User {} : ".format(msg_send, ele))
                user_id_temp = cl.user_id_from_username(ele)
                cl.direct_send(msg_send, user_ids=[user_id_temp])
            except Exception as e:
                ##print(e)
                continue
        targetted_users = ""
        for ele in dm_final:
            targetted_users += str(ele) + ","
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

        to_add = str(_row_) + "::" + str(email) + "::" + str(passw) + "::" + str(code) + "::" + "DirectMessage Done" + "::" \
                     + "Working" + "::" + str(proxy) + "::" + str(targetted_users) + "::" + str(last_login) + \
                    "::" + str(follower) + "::" + str(following) + "\n"


        file = open("tempfile.txt", "a")
        file.write(to_add)
        file.close()


    except Exception as e:
        to_add = str(_row_) + "::" + str(email) + "::" + str(passw) + "::" + str(code) + "::" + "DirectMessage Error" + "::" \
                     + str(e) + "::" + str(proxy) + "::" + "_pass_" + "::" + "_pass_" + \
                 "::" + "_pass_" + "::" + "_pass_" + "\n"
        file = open("tempfile.txt", "a")
        file.write(to_add)
        file.close()

        print(to_add)
        print(e, acc_details)
        print(to_add)

def dm(sheet_path_FINAL, code, id_arr, accounts_arr, number_of_accounts, threaded_proxy_list, proxy_code, read_from_dm_fil, dm_message):
    row_number, retrieved_acc = id_arr, accounts_arr

    global read_from_dm_file
    read_from_dm_file = read_from_dm_fil

    print("Using accounts for posting DMs : ", retrieved_acc)
    print("Targetted User Accounts : ", read_from_dm_file)
    print("The row numbers : ", row_number)
    print("Number of accs used :", len(retrieved_acc))

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
                current_threads.append(threading.Thread(target=dm_helper,
                                      args=(proxy, retrieved_acc[num], row_number[num], dm_message, code)))
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
        time.sleep(40)
    save_excel(sheet_path_FINAL)