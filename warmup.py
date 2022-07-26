import datetime
import re
import sqlite3
import threading
import time
import random
import spintax
import instagrapi
import instagrapi.exceptions
from datetime import datetime
from Instagram_FINAL.reset_proxy import reset_proxy
from Instagram_FINAL.save_excel import save_excel


def warmup_helper(proxy_temp, account_temp, _row_, random_pic_path, warmup_spintax, link_checkbox, link_spintax, profile_pic_checkbox):
    timenow = str(datetime.today().strftime("%d/%m/%y    %I:%M %p"))
    try:
        acc_details = account_temp.split(":")
        cl = instagrapi.Client()

        email = acc_details[0]
        passw = acc_details[1]
        extention = acc_details[0].split("@")[1]

        if extention == "shoezgodz.com":
            PATH = "json_files_new/{}".format(acc_details[1])
            email, xusernamex, passw = acc_details[0], acc_details[1], acc_details[2]
        elif extention == "mail.com.tr":
            fname = acc_details[0].split("@")[0]
            PATH = "json_files_new/{}".format(fname + "mailcomtr")
            email, passw = acc_details[0], acc_details[1]
        elif extention == "iralborz.bid":
            fname = acc_details[0].split("@")[0]
            PATH = "json_files_new/{}".format(fname + "iralborz")
            email, passw = acc_details[0], acc_details[1]
        elif extention == "protonmail.com":
            fname = acc_details[0].split("@")[0]
            PATH = "json_files_new/{}".format(fname + "protonmail")
            print("protonmail.com : ", PATH)
            email, passw = acc_details[0], acc_details[1]

        cl.set_proxy("http://" + proxy_temp)
        cl.load_settings(PATH)

        if extention == "shoezgodz.com":
            cl.login(xusernamex, passw)
        elif extention == "mail.com.tr":
            cl.login(email, passw)
        elif extention == "iralborz.bid":
            cl.login(email, passw)
        elif extention == "protonmail.com":
            cl.login(email, passw)
        print("Login Successful")

    except Exception as e:
        print(e, acc_details)

    try:
        if profile_pic_checkbox:
            print("Using this path for profile picture : ",random_pic_path)
            print(cl.account_change_picture(random_pic_path))
        spinbio = spintax.spin(warmup_spintax)
        regex = re.compile(r'[\n\r\t]')
        spinbio_rip = regex.sub(" ", spinbio)

        if link_checkbox:
            bio_link = link_spintax
            print(cl.account_edit(biography=spinbio, external_url=link_spintax))
        else:
            bio_link = "_pass_"
            print(cl.account_edit(biography=spinbio))

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

        to_add = str(_row_) + "::" + "Warmup Done" + "::" + "Working" + "::" \
                + str(random_pic_path) + "::" + str(spinbio_rip) + "::" + str(bio_link) + "::" + str(proxy_temp) + "::" +\
                 str(timenow) + "::" + str(follower) + "::" + str(following) + "\n"
        file = open("tempfile.txt", "a")
        file.write(to_add)
        file.close()

    except instagrapi.exceptions.ChallengeRequired:
        print("ChallengeRequired", acc_details)

        to_add = str(_row_) + "::" + "Warmup Error" + "::" + "Challenge Required" + "::" \
                + "_pass_" + "::" + "_pass_" + "::" + "_pass_" "::" + str(proxy_temp) + "::" + \
                 str(timenow) + "::" + "_pass_" + "::" + "_pass_" + "\n"
        file = open("tempfile.txt", "a")
        file.write(to_add)
        file.close()
        karambit = open("database/challenge_req.txt", "a")
        karambit.write(str(account_temp) + "\n")
        karambit.close()
        print("Challenge_required_statement")
        return

    except Exception as e:
        print(e)
        to_add = str(_row_) + "::" + "Warmup Error" + "::" + "Error" + "::" \
                + "_pass_" + "::" + "_pass_" + "::" + "_pass_" "::" + str(proxy_temp) + "::" + \
                 str(timenow) + "::" + "_pass_" + "::" + "_pass_" + "\n"
        file = open("tempfile.txt", "a")
        file.write(to_add)
        file.close()

def warmup(sheet_path_FINAL, code, id_arr, accounts_arr, number_of_accounts, threaded_proxy_list, proxy_code, pics, profile_pics_path, warmup_spintax, link_checkbox, link_spintax, profile_pic_checkbox):
    row_number, retrieved_acc = id_arr, accounts_arr
    if profile_pic_checkbox:
        print("No Profile Picture Requirement detected")
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
                random_pic_path = profile_pics_path + "/" + random.choice(pics)
                current_threads.append(threading.Thread(target=warmup_helper, args=(
                proxy, retrieved_acc[num], row_number[num], random_pic_path, warmup_spintax, link_checkbox, link_spintax, profile_pic_checkbox)))
                num += 1

        for thread in current_threads:
            time.sleep(0.1)
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
        time.sleep(5)
    save_excel(sheet_path_FINAL)
