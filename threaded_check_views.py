
import sqlite3
import threading
import time
import instagrapi
import instagrapi.exceptions
from Instagram_FINAL.reset_proxy import reset_proxy

def check_views(proxy, account, row_number, reels_pk, top, turn_comments, comment_file):
    login_account = account.split(":")
    extention = login_account[0].split("@")[1]

    if extention == "shoezgodz.com":
        PATH = "json_files_new/{}".format(login_account[1])
        print("shoezgodz.com : ", PATH)

    elif extention == "mail.com.tr":
        fname = login_account[0].split("@")[0]
        PATH = "json_files_new/{}".format(fname + "mailcomtr")
        print("mail.com.tr : ", PATH)

    elif extention == "iralborz.bid":
        fname = login_account[0].split("@")[0]
        PATH = "json_files_new/{}".format(fname + "iralborz")
        print("iralborz.bid : ", PATH)

    cl = instagrapi.Client()
    cl.set_proxy("http://" + proxy)
    cl.load_settings(PATH)
    cl.login(login_account[0], login_account[1])


    row_number_number_reels = 0
    comments = []

    for ind, ele in enumerate(reels_pk):
        print(ele)
        views = []
        code = []
        row_number_number_reels += 1

        if top == "N" or top == "n":
            for subreels in ele:
                reel_pk = subreels
                if subreels[0] == "'":
                    reel_pk = subreels[1:]
                if not str(reel_pk).isnumeric():
                    continue
                print("Checking Reel : ", reel_pk)
                reel_pk = int(reel_pk)
                try:
                    dic = cl.media_info(reel_pk).dict()
                except Exception as e:
                    print(e)
                    views.append("Deleted")
                    continue
                if turn_comments:
                    for comm in cl.media_comments(reel_pk):
                        dicc = comm.dict()["text"]
                        comments.append(dicc)
                views.append(dic["view_count"])
                code.append(dic["code"])

        else:
            subreels = ele[-1]
            reel_pk = subreels
            if subreels[0] == "'":
                reel_pk = subreels[1:]
            if not str(reel_pk).isnumeric():
                continue
            print("Checking Reel : ", reel_pk)
            reel_pk = int(reel_pk)
            try:
                dic = cl.media_info(reel_pk).dict()
            except Exception as e:
                print(e)
                views.append("Deleted")
                continue
            if turn_comments:
                for comm in cl.media_comments(reel_pk):
                    dicc = comm.dict()["text"]
                    comments.append(dicc)
            views.append(dic["view_count"])
            code.append(dic["code"])

        #to_add = str(row_number[ind]) + "::" + str(views) + "\n"
        to_add = str(row_number[ind]) + "::" + \
                 "_pass_" + "::" + "_pass_" + "::" + "Checked Views" + "::" + "Working" + "::" + \
                 "_pass_" + "::" + "_pass_" + "::" + "_pass_" + "::" + "_pass_" + "::" + \
                 "_pass_" + "::" + str(views) + "::" + "_pass_" + "::" + "_pass_" + "\n"
        file = open("tempfile.txt", "a")
        file.write(to_add)
        file.close()

        if turn_comments:
            file = open(comment_file, "a")
            for ele in comments:
                adding = str(ele) + "\n"
                file.write(adding)
            file.close()

        print("Views gotten : ", views)

def threaded_check_views(sheet_path_FINAL, threaded_proxy_list, proxy_code, login_accounts_views, comment_file):
    code = (input("SELECT THE CODE\n"))

    top = (input("Enter Y for Checking only latest video and N to check all\n"))
    row_number, retrieved_acc, reels_pk = [], [], []
    conn = sqlite3.connect(sheet_path_FINAL)
    c = conn.cursor()
    fetcher = '''
              SELECT account_uid, account, pk FROM Accounts WHERE group_id = '{}';
              '''.format(code)
    c.execute(fetcher)
    result = c.fetchall()
    for ele in result:
        temp = []
        fetched_reels_pks = ele[2]
        if fetched_reels_pks != None:
            fetched_reels_pks = fetched_reels_pks.split(",")
            row_number.append(ele[0])
            retrieved_acc.append(ele[1])

            for ele in fetched_reels_pks:
                if ele != "'":
                    temp.append(ele)
            reels_pk.append(temp)

    print("Accounts Under Scruitiny : ", retrieved_acc)
    print("Row numbers Under Scruitiny : ", row_number)
    print("Number of accs :", len(retrieved_acc))
    print("ACCOUNTS AND ROW NUMBER LENGTHS",len(retrieved_acc), len(row_number))
    print("Press Y To continue or N to exit")
    yes = input()
    if yes == "Y" or yes == "y":
        pass
    else:
        exit(98765)

    existing_threads = []
    itt = 0
    turn_comments = False
    print("Press Y To check for Comments")
    yesx = input()
    if yesx == "Y" or yesx == "y":
        turn_comments = True

    oddie = 0
    num = 0
    row_number_thread = 0
    login_row = 0
    reels_pk_num = 0
    login_reset_now = len(login_accounts_views)

    modd = len(reels_pk) - len(reels_pk) % 50
    reels_pk = reels_pk[:modd]
    print(len(reels_pk))
    for i in range(0, len(reels_pk), 50):
        print("*************************************************************************", itt)
        itt += 5
        if num & 1:  # odd number
            current_proxy = threaded_proxy_list[0]
        else:
            current_proxy = threaded_proxy_list[1]

        if login_row >= login_reset_now:
            login_row = 0

        reels_pk_num += 50
        t1 = threading.Thread(target=check_views, args=(current_proxy, login_accounts_views[login_row], row_number[row_number_thread:row_number_thread+50], reels_pk[reels_pk_num - 50 : reels_pk_num], top, turn_comments, comment_file))
        num += 1
        reels_pk_num += 50
        row_number_thread += 50
        login_row += 1
        t2 = threading.Thread(target=check_views, args=(current_proxy, login_accounts_views[login_row], row_number[row_number_thread:row_number_thread+50], reels_pk[reels_pk_num - 50 : reels_pk_num], top, turn_comments, comment_file))
        num += 1
        reels_pk_num += 50
        login_row += 1
        row_number_thread += 50
        t3 = threading.Thread(target=check_views, args=(current_proxy, login_accounts_views[login_row], row_number[row_number_thread:row_number_thread+50], reels_pk[reels_pk_num - 50 : reels_pk_num], top, turn_comments, comment_file))
        num += 1
        reels_pk_num += 50
        login_row += 1
        row_number_thread += 50
        t4 = threading.Thread(target=check_views, args=(current_proxy, login_accounts_views[login_row], row_number[row_number_thread:row_number_thread+50], reels_pk[reels_pk_num - 50 : reels_pk_num], top, turn_comments, comment_file))
        num += 1
        reels_pk_num += 50
        login_row += 1
        row_number_thread += 50
        t5 = threading.Thread(target=check_views, args=(current_proxy, login_accounts_views[login_row], row_number[row_number_thread:row_number_thread+50], reels_pk[reels_pk_num - 50 : reels_pk_num], top, turn_comments, comment_file))
        num += 1
        login_row += 1
        row_number_thread += 50

        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()

        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()

        reset_proxy_thread_list = []
        for ind, proxy in enumerate(threaded_proxy_list):
            reset_proxy_thread_list.append(threading.Thread(target=reset_proxy, args=(proxy, ind, proxy_code)))
        for r in reset_proxy_thread_list:
            r.start()
        for r in reset_proxy_thread_list:
            r.join()
        time.sleep(20)