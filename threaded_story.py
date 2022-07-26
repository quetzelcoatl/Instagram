import datetime
import sqlite3
import threading
import time
import random
import re
from instagrapi.story import StoryBuilder
from instagrapi.types import StoryMention, StoryMedia, StoryLink, StoryHashtag, Usertag
import instagrapi
import instagrapi.exceptions
from datetime import datetime
from Instagram_FINAL.reset_proxy import reset_proxy
from Instagram_FINAL.save_excel import save_excel


def name_pop():
    global read_from_mentions
    return read_from_mentions.pop(0)

def story_helper(proxy_temp, account_temp, _row_, story_image, list_of_link, code, story_text_spintax, story_spintax_dict, list_of_links_dict, tag_users, number_of_tags):
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
        if extention == "shoezgodz.com":
            cl.login(xusernamex, passw)
        elif extention == "mail.com.tr":
            cl.login(email, passw)
        elif extention == "iralborz.bid":
            cl.login(email, passw)
        elif extention == "protonmail.com":
            cl.login(email, passw)
        print(list_of_link)
        print(story_image)
        print("list_of_links_dict : ", list_of_links_dict)
        print("story_spintax_dict", story_spintax_dict)
        print("story_text_spintax : ", story_text_spintax)

        total_tag = []
        tagged = []
        if tag_users:
            print("Tagging These Many Users : ", number_of_tags)
            for i in range(number_of_tags):
                #total_tag.append(Usertag(user=cl.user_info_by_username(name_pop()), x=0.5, y=0.5))
                total_tag = cl.user_info_by_username(name_pop())
                mentions = StoryMention(user=total_tag)
                tagged.append(mentions)
            print("Tagging users : ", tagged)
        print("Using link : ", list_of_link)
        if list_of_links_dict["enable"] == True:
            story = cl.photo_upload_to_story(story_image, "", links=[
                StoryLink(webUri=list_of_link, x=(list_of_links_dict["x"]), y=(list_of_links_dict["y"]),
                          width=(list_of_links_dict["width"]), height=(list_of_links_dict["height"]))], mentions=tagged)
            #print("Posting Story")
            #story = cl.photo_upload_to_story(story_image, "", links=[
            #StoryLink(webUri=list_of_link, x=0.5126011, y=0.70, width=0.5, height=0.22)])
        else:
            story = cl.photo_upload_to_story(story_image, "", mentions=tagged)

        highlights_pk = ""
        highlights_link = ""
        story_status= ""
        funnel_link = ""

        if story_spintax_dict["highlight"]:
            print("Creating new Highlight")
            story_id = story.dict()["id"]
            highlight_metadata = cl.highlight_create("Join Now", [story_id])
            highlight_id = highlight_metadata.dict()["id"]

            highlights_pk = highlight_id
            highlights_link = "https://www.instagram.com/"
            story_status = ""
            funnel_link = list_of_link

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

        to_add = str(_row_) + "::" + str(
                    email) + "::" + str(passw) + "::" + str(code) + "::" + "Story Working" + \
                    "::"+str(proxy) + "::" + str(highlights_pk) + "::" + str(highlights_link) + "::" + str(story_status) + "::" + str(
                    funnel_link) + "::" + str(last_login) + "::" + str(follower) + "::" + str(following) + "\n"


        file = open("tempfile.txt", "a")
        file.write(to_add)
        file.close()

    except instagrapi.exceptions.ChallengeRequired:
        print("ChallengeRequired", acc_details)
        to_add = str(_row_) + "::" + str(
                    email) + "::" + str(passw) + "::" + str(code) + "::" + "Challenge Required" + \
                    "::"+str(proxy) + "::" + "_pass_" + "::" + "_pass_" + "::" + "_pass_" + "::" + \
                    "_pass_" + "::" + str(last_login) + "::" + "_pass_" + "::" + "_pass_" + "\n"

        file = open("tempfile.txt", "a")
        file.write(to_add)
        file.close()

        karambit = open("database/challenge_req.txt", "a")
        karambit.write(str(account_temp) + "\n")
        karambit.close()
        print("Challenge_required_statement")
        return

    except Exception as e:
        print("Exception is : ", e)
        to_add = str(_row_) + "::" + str(
                    email) + "::" + str(passw) + "::" + str(code) + "::" + "Error Posting Story" + \
                    "::"+str(proxy) + "::" + "_pass_" + "::" + "_pass_" + "::" + "_pass_" + "::" + \
                    "_pass_" + "::" + str(last_login) + "::" + "_pass_" + "::" + "_pass_" + "\n"

        file = open("tempfile.txt", "a")
        file.write(to_add)
        file.close()
        print(to_add)

def threaded_story(sheet_path_FINAL, code, id_arr, accounts_arr,
                   number_of_accounts, threaded_proxy_list, proxy_code, story_images,
                   list_of_links, story_text_spintax, story_spintax_dict,
                   list_of_links_dict, tag_users, number_of_tags, read_from_mention):  # To POST REELS

    row_number, retrieved_acc = id_arr, accounts_arr
    global read_from_mentions
    read_from_mentions = read_from_mention
    print("Accounts Under Scruitiny : ", retrieved_acc)
    print("Row numbers Under Scruitiny : ", row_number)
    print("Number of accs :", len(retrieved_acc))

    modd = modd = len(row_number) - len(row_number) % (len(threaded_proxy_list) * number_of_accounts)
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
                story_image, list_of_link = random.choice(story_images), random.choice(list_of_links)
                current_threads.append(threading.Thread(target=story_helper, args=(
                proxy, retrieved_acc[num], row_number[num], story_image,
                list_of_link, code, story_text_spintax, story_spintax_dict,
                list_of_links_dict, tag_users, number_of_tags)))
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
        time.sleep(20)
    save_excel(sheet_path_FINAL)