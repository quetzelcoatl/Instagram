import datetime
import os
import re
import sqlite3
import threading
import time
import random
from multiprocessing import Process

import spintax
import instagrapi
import instagrapi.exceptions
from datetime import datetime

from instagrapi.types import Usertag, Location

from Instagram_FINAL.reset_proxy import reset_proxy
from Instagram_FINAL.save_excel import save_excel


def name_pop():
    global read_from_mentions
    return read_from_mentions.pop(0)


def threaded_reels(proxy_temp, account_temp, _row_, reel_path, caption, code, hide_reel, location_reel, tag_users,
                   number_of_tags, enable_location):
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
    elif extention == "outlook.com":
        fname = acc_details[0].split("@")[0]
        PATH = "json_files_new/{}".format(fname + "outlook")
        print("outlook.com : ", PATH)
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
        elif extention == "outlook.com":
            cl.login(email, passw)

        #############################################################################################
        ################################### Account Details Fetching #########################################
        #############################################################################################
        cl.get_timeline_feed()
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

        #############################################################################################
        ################################### REELS CAPTION #########################################
        #############################################################################################

        c2 = spintax.spin(caption)

        if hide_reel:
            feedshow = '0'
        else:
            feedshow = '1'

        total_tag = []
        tagged = []

        for i in range(3):
            try:
                if tag_users:
                    print("Tagging These Many Users : ", number_of_tags)
                    for ele in range(number_of_tags):
                        total_tag.append(Usertag(user=cl.user_info_by_username(name_pop()), x=0.5, y=0.5))
                        tagged.append(total_tag)
                    print("Tagging users : ", total_tag, total_tag)

                if enable_location:
                    print("Location at : ", location_reel)
                    status = cl.clip_upload(reel_path, c2, feed_show=feedshow,
                                            location=Location(name=location_reel["location"], lat=location_reel["latitude"],
                                                              lng=location_reel["longitude"]), usertags=total_tag)
                else:
                    status = cl.clip_upload(reel_path, c2, feed_show=feedshow, usertags=total_tag)
                break
            except Exception as e:
                print("Retry : ", str(i))
                if i == 2:
                    print(f"{i} Retries Failed, RETURNING")
                    return
                print(e)

        append = status.dict()["pk"]
        rl = status.dict()["code"]
        reels_link = 'https://www.instagram.com/reel/' + rl
        print(reels_link)

        number_of_reels = len(views)
        reels_pk = append
        reels_views = views_string
        reels_likes = likes_string
        reel_name = reel_path
        to_add = str(_row_) + "::" + str(
            email) + "::" + str(passw) + "::" + str(code) + "::" + "Reels Working" + \
                 "::" + str(proxy) + "::" + str(number_of_reels) + "::" + str(reels_pk) + "::" + str(reels_views) + \
                 "::" + str(reels_likes) + "::" + str(reels_link) + "::" + str(reel_name) + "::" + str(last_login) + \
                 "::" + str(follower) + "::" + str(following) + "\n"

        file = open("tempfile.txt", "a")
        file.write(to_add)
        file.close()

        """
        2::Alfred Schmidt:Frankfurt::x::Reels Working::185.209.177.12:27419::1::987654321::9999::666::https://www.instagram.com/reel/Cbc9t1Qldus::BABU BUDANGAR::06:55 PM::111::222\n
        """

    except instagrapi.exceptions.ChallengeRequired:
        print("ChallengeRequired", acc_details)

        to_add = str(_row_) + "::" + str(
            email) + "::" + str(passw) + "::" + str(code) + "::" + "Reels Challenge Required" + "::" + \
                 "::" + str(proxy) + "::" + "_pass_" + "::" + "_pass_" + "::" + "_pass_" + \
                 "::" + "_pass_" + "::" + "_pass_" + "::" + "_pass_" + "::" + str(
            last_login) + "::" + "_pass_" + "::" + "_pass_" + "\n"

        file = open("tempfile.txt", "a")
        file.write(to_add)
        file.close()

        karambit = open("database/challenge_req.txt", "a")
        karambit.write(str(account_temp) + "\n")
        karambit.close()
        print("Challenge_required_statement")
        return

    except Exception as e:
        to_add = str(_row_) + "::" + str(
            email) + "::" + str(passw) + "::" + str(code) + "::" + "Error Posting Reels" + "::" + \
                 "::" + str(proxy) + "::" + "_pass_" + "::" + "_pass_" + "::" + "_pass_" + \
                 "::" + "_pass_" + "::" + "_pass_" + "::" + "_pass_" + "::" + str(
            last_login) + "::" + "_pass_" + "::" + "_pass_" + "\n"

        file = open("tempfile.txt", "a")
        file.write(to_add)
        file.close()

        print(to_add)
        print(e, acc_details)
        print(to_add)


def reel_posting(sheet_path_FINAL, code, id_arr, accounts_arr, number_of_accounts, threaded_proxy_list, proxy_code,
                 reel_folder_path, caption, hide_reel, location_reel, tag_users, read_from_mention, number_of_tags,
                 enable_location):  # To POST REELS
    row_number, retrieved_acc = id_arr, accounts_arr

    vids = []
    for ele in os.listdir(reel_folder_path):
        temp = ele.split(".")
        if temp[-1] == "mp4":
            vids.append(ele)

    global read_from_mentions
    read_from_mentions = read_from_mention

    print("Tagging these people : ", read_from_mentions)
    print("Posting reels in : ", retrieved_acc)
    print("Posting reels for the row numbers : ", row_number)
    print("Number of vids :", len(vids))
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
    stop_event = threading.Event()
    for i in range(0, len(row_number), len(threaded_proxy_list) * number_of_accounts):
        current_threads = []
        print("*************************************************************************", i)
        for proxy in threaded_proxy_list:
            for j in range(number_of_accounts):
                reel_path = reel_folder_path + "/{}".format(random.choice(vids))
                current_threads.append(Process(target=threaded_reels,
                                                        args=(
                                                        proxy, retrieved_acc[num], row_number[num], reel_path, caption,
                                                        code, hide_reel, location_reel, tag_users, number_of_tags,
                                                        enable_location)))
                num += 1

        for thread in current_threads:
            thread.start()
            time.sleep(1)
        for thread in current_threads:
            thread.join(timeout=500)  # times out after 300 seconds
            thread.terminate()
        reset_proxy_thread_list = []
        for ind, proxy in enumerate(threaded_proxy_list):
            reset_proxy_thread_list.append(threading.Thread(target=reset_proxy, args=(proxy, ind, proxy_code)))
        for r in reset_proxy_thread_list:
            r.start()
        for r in reset_proxy_thread_list:
            r.join()
        time.sleep(10)
    save_excel(sheet_path_FINAL)