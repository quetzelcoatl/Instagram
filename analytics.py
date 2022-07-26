import re
import sqlite3

import mysql.connector
from openpyxl import load_workbook

def analytics(sheet_path_FINAL, code):
    try:
        row_number, retrieved_acc, video_links, video_likes, retrieved_views, video_names  = [], [], [], [], [], []

        connection = mysql.connector.connect(host='localhost', user="root", password="Nikzzkr19@",
                                             database=sheet_path_FINAL, auth_plugin='mysql_native_password')
        cursor = connection.cursor()
        fetcher = '''
                  SELECT id, email, reels_views, reels_likes, reels_link, reel_name from reels
                  where group_id = '{}'
                  '''.format(code)
        print(fetcher)
        cursor.execute(fetcher)
        result = cursor.fetchall()
        for ele in result:
            row_number.append(ele[0])
            retrieved_acc.append(ele[1])
            retrieved_views.append(ele[2])
            video_likes.append(ele[3])
            video_links.append(ele[4])
            video_names.append(ele[5])

        total_views = []
        for ele in retrieved_views:
            split = ele.split(",")
            total_views.append(split[::-1])
        retrieved_views = total_views

        total_sum_total = 0
        total_sum_total_video_number = 0
        for rrow in retrieved_views:
            if rrow == ['']:
                continue
            for row in rrow:
                total_sum_total_video_number += 1
                total_sum_total += int(row)

        temp_likes = []
        for ele in video_likes:
            split = ele.split(",")
            temp_likes.append(split[::-1])
        video_likes = temp_likes

        temp = []
        print("Insights only on the latest video\n")
        temp += [x[-1] for x in retrieved_views if x != []]
        retrieved_views = temp
        #print("Total video views ", total_views)

        eze = 0
        zero_to_hundred = 0
        hundred_to_thousand = 0
        thousand_to_two_thousand = 0
        two_to_three_thousand = 0
        three_to_four_thousand = 0
        four_to_five_thousand = 0
        five_thousand_plus = 0
        zeros = 0
        not_zero_views = []
        #print("Latest Videos are : ",retrieved_views)
        print("Total number of videos are : ", len(retrieved_views))
        #print("row numbers are : ", row_number)
        print("Row numbers selected are : ", len(row_number))
        print("Length of video links are : ", len(video_links))
        views_100 = []
        views_1000 = []
        views_2000 = []
        views_3000 = []
        views_4000 = []
        views_5000 = []
        views_above = []
        result = {}
        for ind, ele in enumerate(retrieved_views):
            if not ele:
                continue
            cunt = ele
            if ele[-1] == "\n":
                cunt = ele[:-1]
            eze += int(cunt)
            cunt = int(cunt)
            try:
                result[retrieved_acc[ind]] = [cunt, video_likes[ind][-1], video_names[ind], video_links[ind]]
                #print(ind, ele, cunt, video_likes[ind][-1], video_names[ind], video_links[ind])
                if cunt <= 3:
                    zeros += 1
                elif cunt <= 100:
                    zero_to_hundred += 1
                    views_100.append(video_links[ind])
                elif cunt >= 100 and cunt <= 1000:
                    hundred_to_thousand += 1
                    views_1000.append(video_links[ind])
                elif cunt >= 1000 and cunt <= 2000:
                    views_2000.append(video_links[ind])
                    thousand_to_two_thousand += 1
                elif cunt >= 2000 and cunt <= 3000:
                    two_to_three_thousand += 1
                    views_3000.append(video_links[ind])
                elif cunt >= 3000 and cunt <= 4000:
                    three_to_four_thousand += 1
                    views_4000.append(video_links[ind])
                elif cunt >= 4000 and cunt <= 5000:
                    four_to_five_thousand += 1
                    views_5000.append(video_links[ind])
                elif cunt >= 5000:
                    five_thousand_plus += 1
                    views_above.append(video_links[ind])
            except Exception as e:
                print(str(ind) + " " + str(row_number[ind]))
                continue

        print(f"Targetted {total_sum_total} number of people using {total_sum_total_video_number} number of videos/reels")

        print("total videos that are posted", zeros + zero_to_hundred + hundred_to_thousand + thousand_to_two_thousand + two_to_three_thousand + three_to_four_thousand + four_to_five_thousand + five_thousand_plus)
        print("sum total of latest views are ", eze)
        print("0 :", zeros)
        print("0 - 100 :", zero_to_hundred)
        print("100 - 1000 :", hundred_to_thousand)
        print("1000 - 2000 :", thousand_to_two_thousand)
        print("2000 - 3000 :", two_to_three_thousand)
        print("3000 - 4000 :", three_to_four_thousand)
        print("4000 - 5000 :", four_to_five_thousand)
        print(">5000 :", five_thousand_plus)
        print("*******************************************************************************************************************************************************************************************************************************************************************************************************")
        print("0 - 100 :", end = " ")
        for ele in views_100:
            print(ele, end = " ")
        print("")
        print("100 - 1000 :", end = " ")
        for ele in views_1000:
            print(ele, end = " ")
        print("")
        print("1000 - 2000 :", end = " ")
        for ele in views_2000:
            print(ele, end = " ")
        print("")
        print("2000 - 3000 :", end = " ")
        for ele in views_3000:
            print(ele, end = " ")
        print("")
        print("3000 - 4000 :", end = " ")
        for ele in views_4000:
            print(ele, end = " ")
        print("")
        print("4000 - 5000 :", end = " ")
        for ele in views_5000:
            print(ele, end = " ")
        print("")
        print(">5000 :", end = " ")
        for ele in views_above:
            print(ele, end = " ")
        print("\n\n")
        #print(result)
        """print("ACCOUNT \t\t VIEWS \t LIKES \t VIDEO NAME \t\t VIDEO LINK")
        for account, store in result.items():
            print(f"{account} ---> {store}")"""
            #print(f"{account} --> {store[0]} \t {store[1]} \t {store[2]} \t {store[3]}")
    except Exception as e:
        print(e)
    return eze
    '''
    from matplotlib import pyplot as plt
    test = retrieved_views
    y_axis_latest = [x[-1] for x in test if x != []]
    x_axis = [x + 1 for x in range(len(y_axis_latest))]
    y_axis_first_video = [x[0] for x in test if x != []]
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.bar(x_axis, y_axis_latest, color='b', width=0.25)
    x_axis = [x + 1.25 for x in range(len(y_axis_latest))]
    ax.bar(x_axis, y_axis_first_video, color='g', width=0.25)
    plt.show()'''

#analytics('vps1', "ReadyReels")