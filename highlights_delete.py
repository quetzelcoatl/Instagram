import datetime
import os
import re
import sqlite3
import threading
import time
import random

import mysql.connector
import spintax
import instagrapi
import instagrapi.exceptions
from datetime import datetime

from instagrapi.types import Usertag, Location

from Instagram_FINAL.reset_proxy import reset_proxy
from Instagram_FINAL.save_excel import save_excel

def highlights_helper(proxy_temp, account_temp, _row_, code):
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
    print("GOT SETTINGS FROM PATH")

    def challenge_code_handler(username, choice):
        return 111111

    try:
        cl.challenge_code_handler = challenge_code_handler
    except:
        file3 = open("thread_helper.txt", "a")
        file3.write(account_temp + "\n")
        file3.close()

    try:
        if extention == "shoezgodz.com":
            cl.login(xusernamex, passw)
        elif extention == "mail.com.tr":
            cl.login(email, passw)
        elif extention == "iralborz.bid":
            cl.login(email, passw)
        elif extention == "protonmail.com":
            cl.login(email, passw)

        dictionary = cl.account_info()
        username_ = dictionary.dict()["username"]
        highlights_regex = "Highlight\(pk='\d+'"
        list_of_highlights = cl.user_highlights(user_id=int(cl.user_id_from_username(username_)))
        print(str(list_of_highlights))
        find = re.findall(highlights_regex, str(list_of_highlights))
        findx = [x.split("=")[1][1:-1] for x in find]
        for highlight in findx:
            cl.highlight_delete(highlight)
            print("Deleted Highlight : ", highlight)
        """for highlight in list_of_highlights:
            find = re.findall(highlights_regex, str(highlight))
            cl.highlight_delete(find)
            print("Deleted Highlight : ", highlight)"""

    except Exception as e:
        print(e)


def highlights_delete(sheet_path_FINAL, code, id_arr, accounts_arr, number_of_accounts, threaded_proxy_list, proxy_code):  # To POST REELS
    row_number, retrieved_acc = id_arr, accounts_arr

    print("Posting reels in : ", retrieved_acc)
    print("Posting reels for the row numbers : ", row_number)
    print("Number of accs :", len(retrieved_acc))
    print("Number of Proxies used : ", len(threaded_proxy_list))
    print("Number of operations done per cycle : ", len(threaded_proxy_list) * number_of_accounts)
    # print("Press Y To continue or N to exit")

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
                current_threads.append(threading.Thread(target=highlights_helper,
                                                        args=(proxy, retrieved_acc[num], row_number[num], code)))
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
        time.sleep(20)

    print("Deleting Highlights from the highlights table")
    connection = mysql.connector.connect(host='localhost', user="root", password="Nikzzkr19@",database=sheet_path_FINAL, auth_plugin='mysql_native_password')
    cursor = connection.cursor()
    for ele in accounts_arr:
        delete_highlight_query = """
                                 DELETE FROM story where email = '{}';
                                 """.format(ele.split(":")[0])
        print(delete_highlight_query)
        cursor.execute(delete_highlight_query)
    connection.commit()
    cursor.close()