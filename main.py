import os
import sqlite3

import mysql.connector
from openpyxl import load_workbook
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
from Instagram_FINAL.analytics import analytics
from Instagram_FINAL.first_login import first_login
from Instagram_FINAL.reel_posting import reel_posting
from Instagram_FINAL.reset_proxy import reset_proxy
from Instagram_FINAL.save_excel import save_excel
from Instagram_FINAL.threaded_check_views import threaded_check_views
from Instagram_FINAL.threaded_dm import dm
from Instagram_FINAL.threaded_follow_only import threaded_follow_only
from Instagram_FINAL.threaded_mentions import mentions
from Instagram_FINAL.threaded_relogin import threaded_relogin
from Instagram_FINAL.threaded_story import threaded_story
from Instagram_FINAL.warmup import warmup

number_of_accounts = 3  # THE NUMBER OF ACCOUNTS ACTIONS PER PROXY
threaded_proxy_list = ["Rjenkins313:Audit313@173.92.252.25:2001","Rjenkins313:Audit313@173.92.252.25:2002", "Rjenkins313:Audit313@173.92.252.25:2003",
                       "Rjenkins313:Audit313@173.92.252.25:2004", "Rjenkins313:Audit313@173.92.252.25:2005"]
proxy_code = ["1", "2", "3", "4", "5"]
threaded_proxy_list = ["Rjenkins313:Audit313@173.92.252.25:2001"]
proxy_code = ["1"]
sheet_path_FINAL = "vps3"  # CHANGE THE PATH OF THE EXCEL FILE HERE
reel_folder_path = r"C:\Users\Administrator\PycharmProjects\contentcombinationbot\FileStructure\output\dogsreels"  # CHANGE THE DIRECTORY HERE TO CHANGE THE REELS PATH
spintax_reels = '{Look at| Checkout|See|Check|Go Check|Find} the {Highlights|Story Highlights} on my profile {to} learn more about {#Nfts|#NFT|#NFTs}'
# SPINTAX FOR REELS
list_of_links = ["https://discord.gg/VUAW3yqhZu", "https://discord.gg/nHDYmwSKxx", "https://discord.gg/8TJwxuqAY9",
                 "https://discord.gg/Fb2mjXXCQG", "https://discord.gg/Bf22sEKPkx", "https://discord.gg/4AcckBvGN4",
                 "https://discord.gg/67fh9cjSXQ", "https://discord.gg/yNekrGvBUT", "https://discord.gg/auVNqSbvp9",
                 "https://discord.gg/eDtgDy3tk3", "https://discord.gg/tbZkRYrJek", "https://discord.gg/88S5MBnntE",
                 "https://discord.gg/aexkTdYhfr", "https://discord.gg/dJMaKacmKP", "https://discord.gg/UMc69BNz6w",
                 "https://discord.gg/Ey2cZwgbtq", "https://discord.gg/3aQtEXGTWj", "https://discord.gg/wncPdbceF8",
                 "https://discord.gg/jrhpTRCs7j", "https://discord.gg/KqE5jgPHDD", "https://discord.gg/cAN2FxmXBZ",
                 "https://discord.gg/rbaQnetTZw", "https://discord.gg/CdsDMCH36G", "https://discord.gg/QvnwQAfTmu",
                 "https://discord.gg/gXA9tER7u3", "https://discord.gg/fGawGAXWTC", "https://discord.gg/afa9y5meXr",
                 "https://discord.gg/zc2XSv4xJx", "https://discord.gg/nrEr7K6C4V", "https://discord.gg/CFwgNw6AvJ",
                 "https://discord.gg/tnKGS3XQvr", "https://discord.gg/RjHeXVBHqW", "https://discord.gg/tmwwWnaUDT",
                 "https://discord.gg/KgKfV7A5vS", "https://discord.gg/JVBCdkB7wb", "https://discord.gg/pcp4MjEMZT",
                 "https://discord.gg/tnKGS3XQvr", "https://discord.gg/MSf5rScPsk", "https://discord.gg/96yMcw8AZr",
                 "https://discord.gg/pkjcamf2jr", "https://discord.gg/n6Wh3hRKak", "https://discord.gg/txMbXbZ9Aj",
                 "https://discord.gg/6Nudts6ay9", "https://discord.gg/aTG8YaXZ56", "https://discord.gg/2sz53qScKx",
                 "https://discord.gg/ZpXuZh6W7a", "https://discord.gg/ZAFPhbycxy", "https://discord.gg/g8dDsXaTJW",
                 "https://discord.gg/HgnpRWTtZS", "https://discord.gg/7jfcunSq6e", "https://discord.gg/WF4QGPMqAg",
                 "https://discord.gg/VNGvVMqPWb", "https://discord.gg/F49pRv3Dak", "https://discord.gg/VDJDQbC8CE",
                 "https://discord.gg/9r4TjUKM2S", "https://discord.gg/rfb2jpDkhY", "https://discord.gg/s4576N2YCP",
                 "https://discord.gg/HgnpRWTtZS", "https://discord.gg/25Pd7g3GmC", "https://discord.gg/Gvqe7EW4yk",
                 "https://discord.gg/DtGurU9Psj", "https://discord.gg/aR8QdEmqms", "https://discord.gg/Tv7BwUDDtP",
                 "https://discord.gg/jAuavrMS2b", "https://discord.gg/cM95ysCgEQ", "https://discord.gg/RW464kCMMU",
                 "https://discord.gg/vXtSsjt3D2", "https://discord.gg/5YBReRk9kg", "https://discord.gg/Hszk6rUmNC",
                 "https://discord.gg/bj5hEyXCmt", "https://discord.gg/hyhnEfjrGk", "https://discord.gg/4Nzk3Dmfnt",
                 "https://discord.gg/6c6SDEDDp8", "https://discord.gg/JbP2QMvYr5", "https://discord.gg/vjPFQm6PGT",
                 "https://discord.gg/jmrmftH7J8", "https://discord.gg/BUHmhgdhAB", "https://discord.gg/JcCfC6ZDVu",
                 "https://discord.gg/tz6r4W2Up9", "https://discord.gg/gRBJWcmaR4", "https://discord.gg/M4T98sWGnx",
                 "https://discord.gg/wdSyXRYqdx", "https://discord.gg/DJf3XGF9yq", "https://discord.gg/hybqNpGGWD",
                 "https://discord.gg/GJu6ktqpGV", "https://discord.gg/9PEpQ2S2kG", "https://discord.gg/7AvvMxaZK2",
                 "https://discord.gg/bV5aQe8Sp3", "https://discord.gg/EAbzQ6vQuA", "https://discord.gg/pWh47kChAx",
                 "https://discord.gg/xpJQBRDEVp", "https://discord.gg/cVubydH9vQ", "https://discord.gg/mGaymqQM4F",
                 "https://discord.gg/WCWKQBawvp", "https://discord.gg/PYze2QkF", "https://discord.gg/xquDnsFxKB",
                 "https://discord.gg/2Fphg6RjnP", "https://discord.gg/etXaK9pCHm", "https://discord.gg/D5YaMHtjgy",
                 "https://discord.gg/RVKUKkqnwy", "https://discord.gg/nJjATvYkGZ", "https://discord.gg/Mw8S6UMcWw",
                 "https://discord.gg/zkCuPX7TVR", "https://discord.gg/36ab9Cj9SR", "https://discord.gg/w54DKgBpGv",
                 "https://discord.gg/xfJSbchGUz", "https://discord.gg/p5aXj8jnQu", "https://discord.gg/xgRcZn49GX",
                 "https://discord.gg/adYdzh6yCt", "https://discord.gg/HdYS7Kvtq2", "https://discord.gg/F9NwuawDS3",
                 "https://discord.gg/MG9HvWmUv4", "https://discord.gg/cYEHGBNuwt", "https://discord.gg/SwMXcd3dhH",
                 "https://discord.gg/GHj3mHbFPM", "https://discord.gg/CKaGRNsvAB", "https://discord.gg/eEWCPDD69p",
                 "https://discord.gg/MpRK4uW2bK", "https://discord.gg/39qdBFWKX3", "https://discord.gg/Vv7NgKw7JG",
                 "https://discord.gg/CW5VNdGbZv", "https://discord.gg/Jgpg2TAw3z", "https://discord.gg/T7XPhw2veW",
                 "https://discord.gg/XFXZvmYVNM", "https://discord.gg/Ff6Gmkw67Y", "https://discord.gg/HzyGJKsQPj",
                 "https://discord.gg/hvSMwWrMWY", "https://discord.gg/eNaY9sWV3M", "https://discord.gg/jzZxjzKkTm",
                 "https://discord.gg/hZr5AHUR9Q", "https://discord.gg/sn4gpxJjF4", "https://discord.gg/TQ4vU9BC3W",
                 "https://discord.gg/fcMnR9ZT3u", "https://discord.gg/GPX7xgMAS7", "https://discord.gg/rzHZZaUmDV",
                 "https://discord.gg/zfdW2e29Ge", "https://discord.gg/eSQmwRj8qc", "https://discord.gg/ujfuRGF6gS",
                 "https://discord.gg/k9CrmFTUBZ", "https://discord.gg/dFG2mEUrP7", "https://discord.gg/cXuQ4CW2VN",
                 "https://discord.gg/prAHfv623M", "https://discord.gg/Ucyj6h6wT4", "https://discord.gg/4FAhupJNBu",
                 "https://discord.gg/jRkVrHJA38", "https://discord.gg/Wg2xGq4nTT", "https://discord.gg/Re5ZqEnCaX",
                 "https://discord.gg/PBXZt5KWcU", "https://discord.gg/JjRmtkeNrA", "https://discord.gg/DVMWf9gcP9",
                 "https://discord.gg/e3YtqJbhVx", "https://discord.gg/CNtE4Y7PNQ", "https://discord.gg/U6JNNyZr45",
                 "https://discord.gg/JXGYFg98zg", "https://discord.gg/MyETRjAxvW", "https://discord.gg/f5mCSZtPeT",
                 "https://discord.gg/pQHEZnAytY", "https://discord.gg/wJCds3VQeP", "https://discord.gg/pKFPgbzv6x",
                 "https://discord.gg/9BnpyVyqsW", "https://discord.gg/fhheDphN7h", "https://discord.gg/nQAcMqGBYS",
                 "https://discord.gg/cdZexbxzT7", "https://discord.gg/yStCSSeatV", "https://discord.gg/fBWfFEcxWp",
                 "https://discord.gg/FKZFjsmVkA", "https://discord.gg/PBAhP8YHSR", "https://discord.gg/9B7TvefcJM",
                 "https://discord.gg/7zYQ3puz5K", "https://discord.gg/v4aFRfz5ec", "https://discord.gg/Qfv7SZAd6M",
                 "https://discord.gg/T4nsC2Wdw5", "https://discord.gg/BreGuH5zYS", "https://discord.gg/uDxVvzRy",
                 "https://discord.gg/7KH356BYT3", "https://discord.gg/BsYDwQ7PFs", "https://discord.gg/Uf87bUKJNU",
                 "https://discord.gg/9qDGMdF3Gk", "https://discord.gg/mtesV3rWke", "https://discord.gg/k4rw5fPXgz",
                 "https://discord.gg/Zbs8Z5WAA7", "https://discord.gg/qGqxDwCkkR", "https://discord.gg/cdQuQUMQZP",
                 "https://discord.gg/Ejt5TAawc2", "https://discord.gg/qmdeYUh4pC", "https://discord.gg/hQYpunve4c",
                 "https://discord.gg/5gdNdZ98Cz", "https://discord.gg/rBtmRWwNfR", "https://discord.gg/4kya9RBzBP",
                 "https://discord.gg/Z3mqdSFH9m", "https://discord.gg/JbZJmWDfsu", "https://discord.gg/qvUQwu63dV",
                 "https://discord.gg/YRfbu53SHw", "https://discord.gg/FSENgcrSKN", "https://discord.gg/J7VxydcMV4",
                 "https://discord.gg/CfyAdMv3Zm", "https://discord.gg/DpGSYVyPuF", "https://discord.gg/nKyVjTEvCg",
                 "https://discord.gg/xXzcjgDq4R", "https://discord.gg/nPhepdJQeW", "https://discord.gg/SdRpsmjUq6"]
media_path = "src/imgs"  # CHANGE THE DIRECTORY HERE TO CHANGE THE STORY_IMAGES
profile_pics_path = "src/pics"  # CHANGE THE DIRECTORY HERE TO CHANGE THE PROFILE_PICS
comment_file = "src/comments.txt"  # CHANGE THE DIRECTORY HERE TO CHANGE THE COMMENTS FILE
mentions_user_names = "src/mentions.txt"  # CHANGE THE DIRECTORY HERE TO CHANGE THE MENTIONS FILE
mentions_post_url = "https://www.instagram.com/p/CaHJ5rWl4s3/"  # URL OF THE MENTIONS POST
dm_user_names = "src/dm.txt"
target_number_dm_per_cycle = 2  # NUMBER OF DMs PER ACCOUNT
# CHANGE THE DIRECTORY HERE TO CHANGE THE DM FILE
dm_message = '{Look at| Checkout|See|Check|Go Check|Find} the {Highlights|Story Highlights} on my profile {to} learn more about {#Nfts|#NFT|#NFTs}'  # MESSAGE CONTENTS FOR DM
account_list_path = "src/accounts.txt"  # PATH OF THE ACCOUNTS TO BE ADDED FOR FIRST LOGIN
warmup_spintax = "{Posting|Uploading|Promoting|Sharing} {Crypto|NFT|Metaverse} related {content|videos|posts|reels} \n {#nft|#nfts} {#crypto|#reels} {#metaverse|#meta}"  # SPINTAX FOR ACCOUNT BIO
follow_path = "src/finalfollowing.txt"  # FOLLOW PATH FOR ACCOUNTS TO FOLLOW
view_checker_accounts_code = "view_checker"  # CODE FOR ACCOUNTS IN DB
# CHANGE THIS FOR RESETTING PROXY ONCE EVERY N NUMBER OF ACCOUNTS

mention_file = open(mentions_user_names, "r")
read_from_mentions = mention_file.readlines()
read_from_mentions = [x[:-1] if x[-1] == "\n" else x for x in read_from_mentions]

dm_file = open(dm_user_names, "r")
read_from_dm_file = dm_file.readlines()
read_from_dm_file = [x[:-1] if x[-1] == "\n" else x for x in read_from_dm_file]

connection = mysql.connector.connect(host='localhost', user="root", password="Nikzzkr19@", database=sheet_path_FINAL,
                                     auth_plugin='mysql_native_password');
cursor = connection.cursor()


def name_pop():
    temp = ""
    for i in range(9):
        temp += "@" + read_from_mentions.pop(0) + " "
    return temp


def dm_pop():
    temp = ""
    for i in range(target_number_dm_per_cycle):
        temp += read_from_dm_file.pop(0) + "::"
    return temp


pics = []
for ele in os.listdir(profile_pics_path):
    pics.append(ele)

clear_text = input("Input Y to Clear Text file N for No\n")
if clear_text == "Y" or clear_text == "y":
    f = open('tempfile.txt', 'r+')
    f.truncate(0)

input_ = int(input(
    "Enter 1) For initial Login \n"
    "2) For Warmup - Profile Pic/Bio Only \n"
    "3) For Reels Posting \n"
    "4) For Checking Views \n"
    "5) For Warmup - Threaded Follow Only \n"
    "6) To Save Settings\n"
    "7) For Posting Story\n"
    "8) To Reset Proxy\n"
    "9) For Detailed Analytics\n"
    "10) To Relogin and update JSON Files\n"
    "11) For Mentions\n"
    "12) For Direct Messaging (DMs)\n"))

id_arr = []
accounts_arr = []
if input_ != 1 and input_ != 8 and input_ != 6:
    print("Select by using GROUP ID or ID RANGE")
    choice = int(input("Enter 1 for selection using GROUP ID and 2 For ID RANGE\n"))
    if choice == 1:
        code = input("Enter the GROUP ID\n")
        query = "SELECT id, email, password FROM Accounts WHERE group_id = '{}';".format(code)
        cursor.execute(query)
        rows = cursor.fetchall()
        id_arr = []
        accounts_arr = []
        rows = [list(x) for x in rows]
        for row in rows:
            id_arr.append(str(row[0]))
            accounts_arr.append(row[1] + ":" + row[2])

    elif choice == 2:
        start_range = int(input("Enter the start of ID RANGE\n"))
        stop_range = int(input("Enter the end of ID RANGE\n"))
        range_query = """SELECT id, email, password, group_id FROM accounts WHERE id BETWEEN {} AND {}""".format(
            start_range, stop_range)
        cursor.execute(range_query)
        rows = cursor.fetchall()
        id_arr = []
        accounts_arr = []
        rows = [list(x) for x in rows]
        for row in rows:
            id_arr.append(str(row[0]))
            accounts_arr.append(row[1] + ":" + row[2])
        code = rows[0][3]
        print("Code being used is : ", code)

print("Total Accounts Selected : ", len(id_arr))
print(accounts_arr)
stop = input("Enter Y to Continue or N to terminate\n")
if stop == "N" or stop == "n":
    exit(999999)

if input_ == 11:  # MENTIONS
    mentions(sheet_path_FINAL, code, id_arr, accounts_arr, number_of_accounts, threaded_proxy_list, proxy_code,
             read_from_mentions, mentions_post_url)
    save_excel(sheet_path_FINAL)

elif input_ == 12:  # DIRECT MESSAGING
    dm(sheet_path_FINAL, code, id_arr, accounts_arr, number_of_accounts, threaded_proxy_list, proxy_code,
       read_from_dm_file, dm_message)
    save_excel(sheet_path_FINAL)

elif input_ == 5:  # WARMUP THREADED FOLLOW ONLY
    threaded_follow_only(sheet_path_FINAL, code, id_arr, accounts_arr, number_of_accounts, threaded_proxy_list,
                         proxy_code, follow_path)
    save_excel(sheet_path_FINAL)

elif input_ == 6:  # SAVE EXCEL
    save_excel(sheet_path_FINAL)

elif input_ == 10:  # RELOGIN
    threaded_relogin(sheet_path_FINAL, code, id_arr, accounts_arr, number_of_accounts, threaded_proxy_list, proxy_code)
    save_excel(sheet_path_FINAL)

elif input_ == 9:  # ANALYTICS
    analytics(sheet_path_FINAL)

elif input_ == 8:  # RESET PROXY
    for ind, ele in enumerate(threaded_proxy_list):
        reset_proxy(ele, ind, proxy_code)

elif input_ == 7:  # STORY
    story_images = []
    for ele in os.listdir(media_path):
        story_images.append(media_path + "/" + str(ele))
    threaded_story(sheet_path_FINAL, code, id_arr, accounts_arr, number_of_accounts, threaded_proxy_list, proxy_code,
                   story_images, list_of_links)
    save_excel(sheet_path_FINAL)

elif input_ == 2:  # WARMUP PROFILE PIC/BIO ONLY
    pics = []
    for ele in os.listdir(profile_pics_path):
        pics.append(ele)
    warmup(sheet_path_FINAL, code, id_arr, accounts_arr, number_of_accounts, threaded_proxy_list, proxy_code, pics,
           profile_pics_path, warmup_spintax)
    save_excel(sheet_path_FINAL)

elif input_ == 4:  # CHECKING VIEWS
    login_accounts_views = []
    conn = sqlite3.connect(sheet_path_FINAL)
    c = conn.cursor()
    fetcher = '''
              SELECT account_uid, account FROM Accounts WHERE group_id = '{}';
              '''.format(view_checker_accounts_code)
    c.execute(fetcher)
    result = c.fetchall()
    for ele in result:
        login_accounts_views.append(ele[1])

    threaded_check_views(sheet_path_FINAL, threaded_proxy_list, proxy_code, login_accounts_views, comment_file)
    save_excel(sheet_path_FINAL)

elif input_ == 3:  # POSTING REELS
    reel_posting(sheet_path_FINAL, code, id_arr, accounts_arr, number_of_accounts, threaded_proxy_list, proxy_code,
                 reel_folder_path, spintax_reels)
    save_excel(sheet_path_FINAL)

elif input_ == 1:  # INITIAL LOGIN
    first_login(account_list_path, number_of_accounts, threaded_proxy_list, proxy_code)
    save_excel(sheet_path_FINAL)
