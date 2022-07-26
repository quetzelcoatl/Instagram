import mysql.connector

def save_excel(sheet_path_FINAL):
    connection = mysql.connector.connect(host='localhost', user="root", password="Nikzzkr19@",
                                         database=sheet_path_FINAL,
                                         auth_plugin='mysql_native_password')
    c = connection.cursor()

    file = open("tempfile.txt", "r")
    read_from_file = file.readlines()
    read_from_file = [x[:-1] if x[-1] == "\n" else x for x in read_from_file]

    reels_fetcher = "select id, reels_pk, number_of_reels, reels_views, reels_likes from reels"
    relogin_fetcher = "select id, reels_pk, number_of_reels, reels_views, reels_likes from reels"
    story_fetcher = "select id, highlights_pk, highlights_link, story_status, funnel_link from story"
    directmessage_fetcher = "select id, targetted_users from dm"
    mentions_fetcher = "select id, mentions from mentions"
    posts_fetcher = "select id, post_pk from posts"

    for ele in read_from_file:
        try:
            initial = True
            splitted = ele.split("::")
            print(splitted)
            last_activity, status, followers, following, posts, last_login_time, proxy,profile_pic, biograpy, external_url = "", "", "", "", "", "","","","",""
            if splitted[4] == "Initial Login" or "Initial Login" in splitted[4]:  # FOR INITIAL LOGIN INSERTING ROWS
                initial = False
                if "Error" not in splitted[4]:
                    splitted = [x if x != "_pass_" else "" for x in splitted]
                    last_activity, status, proxy, last_login_time = splitted[4], "Working", splitted[6], splitted[13]
                    followers, following = splitted[7], splitted[8]
                    insert = ''' INSERT INTO Accounts (email, password, group_id, last_activity, status, proxy, username, followers, following, posts, profile_pic, bio, bio_link, last_login_time)
                             VALUES
                             ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')
                             '''.format(splitted[1], splitted[2], splitted[3], splitted[4], splitted[5], splitted[6],
                                        splitted[7], splitted[8], splitted[9], splitted[10], splitted[11], splitted[12],
                                        "None", splitted[13])
                    print(insert)
                    c.execute(insert)


            elif splitted[4] == "Reels Working" or "Reels" in splitted[4]:  # FOR UPDATING/INSERTING ROWS IN REELS
                if reels_fetcher:
                    c.execute(reels_fetcher)
                    reels_fetcher = False
                    rows = c.fetchall()
                    reels_dict = {}
                    rows = [list(x) for x in rows]
                    for row in rows:
                        reels_dict[row[0]] = row[1:]
                    print("UID Present in reels table : ", reels_dict)

                if "Challenge" in splitted[4]:
                    last_activity, status, proxy, last_login_time = splitted[4], "Not Working", splitted[5], splitted[12]
                else:
                    last_activity, status, proxy, last_login_time = splitted[4], "Working", splitted[5], splitted[12]
                followers, following = splitted[13], splitted[14]

                if "Error" not in splitted[4] and "Challenge" not in splitted[4]:
                    if int(splitted[0]) in reels_dict.keys():
                        # CHECKS IF ID ALREADY EXISTS IN REELS TABLE TO PREVENT DUPLICATES
                        print(len(splitted))

                        print("{} exists in reels table ".format(splitted[0]))
                        reels_link = splitted[10]
                        reels_name = splitted[11]
                        reels_time = splitted[12]

                        existing_pk = reels_dict[int(splitted[0])][0]
                        existing_pk += "," + splitted[7]

                        existing_number = reels_dict[int(splitted[0])][1]
                        posts = reels_dict[int(splitted[0])][1]
                        #existing_number = int(existing_number) + 1

                        existing_views = reels_dict[int(splitted[0])][2]
                        existing_views =  splitted[8]

                        existing_likes = reels_dict[int(splitted[0])][3]
                        existing_likes =  splitted[9]

                        update_reels = """
                                        UPDATE reels
                                        SET email='{}', password='{}',group_id='{}',status='{}',proxy='{}',number_of_reels='{}',reels_pk='{}',
                                        reels_views='{}',reels_likes='{}',reels_link='{}',reel_name='{}',reels_time='{}'
                                        WHERE id = {};
                                       """.format(splitted[1], splitted[2], splitted[3], splitted[4], splitted[5],
                                                  existing_number, existing_pk, existing_views,
                                                  existing_likes, reels_link, reels_name, reels_time, splitted[0])
                        print(update_reels)
                        # exit(4524)
                        c.execute(update_reels)
                        connection.commit()
                    else:
                        print("{} does not exist in reels table ".format(splitted[0]))
                        splitted = [x if x != "_pass_" else "" for x in splitted]
                        posts = splitted[6]

                        insert_reels = ''' INSERT INTO reels (id, email, password, group_id, status, proxy, number_of_reels, reels_pk, reels_views, reels_likes,
                                                        reels_link, reel_name, reels_time)
                                     VALUES
                                     ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')
                                     '''.format(splitted[0], splitted[1], splitted[2], splitted[3], splitted[4],
                                                splitted[5],splitted[6], splitted[7], splitted[8], splitted[9], splitted[10],
                                                splitted[11], splitted[12])
                        print(insert_reels)
                        # exit(4524)
                        c.execute(insert_reels)
                        connection.commit()

            elif splitted[4] == "Posted Story" or "Story" in splitted[4]:  # FOR UPDATING/INSERTING ROWS IN REELS:
                if story_fetcher:
                    c.execute(story_fetcher)
                    story_fetcher = False
                    rows = c.fetchall()
                    story_dict = {}
                    rows = [list(x) for x in rows]
                    for row in rows:
                        story_dict[row[0]] = row[1:]
                    print("UID Present in story table : ", story_dict)
                followers, following = splitted[11], splitted[12]

                if "Challenge" in splitted[4]:
                    last_activity, status, proxy, last_login_time = splitted[4], "Not Working", splitted[5], splitted[10]
                else:
                    last_activity, status, proxy, last_login_time = splitted[4], "Working", splitted[5], splitted[10]

                if "Error" not in splitted[4] and "Challenge" not in splitted[4]:
                    if int(int(splitted[0])) in story_dict.keys():
                        print("{} exists in story table ".format(splitted[0]))
                        followers, following = splitted[11], splitted[12]
                        highlights_pk = story_dict[int(splitted[0])][0]
                        highlights_pk += "," + splitted[6]

                        highlights_link = story_dict[int(splitted[0])][1]
                        highlights_link += "," + splitted[7]

                        story_status = story_dict[int(splitted[0])][2]
                        story_status += "," + splitted[8]

                        funnel_link = story_dict[int(splitted[0])][3]
                        funnel_link += "," + splitted[9]
                        story_time = splitted[10]
                        # story_fetcher = "select id, highlights_pk, highlights_link, story_status, funnel_link from reels"
                        update_reels = """
                                        UPDATE story
                                        SET email='{}', password='{}',group_id='{}',status='{}',proxy='{}',highlights_pk='{}',highlights_link='{}',
                                        story_status='{}',funnel_link='{}',story_time='{}'
                                        WHERE id = {};
                                       """.format(splitted[1], splitted[2], splitted[3], splitted[4],
                                                  splitted[5], highlights_pk, highlights_link, story_status,
                                                  funnel_link, story_time,
                                                  splitted[0])
                        print(update_reels)
                        c.execute(update_reels)
                        connection.commit()
                    else:
                        print("{} does not exist in story table ".format(splitted[0]))
                        splitted = [x if x != "_pass_" else "" for x in splitted]

                        insert_story = ''' INSERT INTO story (id, email, password, group_id, status, proxy, highlights_pk, highlights_link,
                                                            story_status, funnel_link, story_time)
                                             VALUES
                                             ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')
                                             '''.format(splitted[0], splitted[1], splitted[2], splitted[3], splitted[4],
                                                        splitted[5], splitted[6], splitted[7], splitted[8], splitted[9],
                                                        splitted[10])
                        print(insert_story)
                        c.execute(insert_story)
                        connection.commit()

            elif splitted[1] == "Warmup Done" or "Warmup" in splitted[1]:  # JUST UPDATING VALUES NO INSERT
                if "Challenge" in splitted[2]:
                    last_activity, status, proxy, last_login_time = splitted[1], splitted[2], splitted[6], splitted[7]
                else:
                    last_activity, status, proxy, last_login_time = splitted[1], splitted[2], splitted[6], splitted[7]

                biograpy = splitted[4]
                external_url = splitted[5]
                profile_pic = splitted[3]
                followers, following = splitted[8], splitted[9]

                if "Error" not in splitted[1]:
                    followers, following = splitted[8], splitted[9]
                    update_warmup = """
                                    UPDATE accounts
                                    SET last_activity='{}',status='{}',profile_pic='{}',bio='{}',bio_link='{}'
                                    WHERE id = {};
                                   """.format(splitted[1], splitted[2], splitted[3], splitted[4], splitted[5], splitted[0])
                    #print(update_warmup)
                    #c.execute(update_warmup)

            elif splitted[1] == "Follow Done" or "Follow" in splitted[1]:  # JUST UPDATING VALUES NO INSERT
                last_activity, status, last_login_time, proxy, followers, following, = splitted[1], splitted[2], splitted[4], splitted[3], splitted[5], splitted[6]

            elif splitted[4] == "DirectMessage Done" or "DirectMessage" in splitted[4]:
                if "Challenge" in splitted[4]:
                    last_activity, status, proxy, last_login_time = splitted[4], "Not Working", splitted[6], splitted[8]
                else:
                    last_activity, status, proxy, last_login_time = splitted[4], "Working", splitted[6], splitted[8]
                if directmessage_fetcher:
                    c.execute(directmessage_fetcher)
                    directmessage_fetcher = False
                    rows = c.fetchall()
                    story_dict = {}
                    rows = [list(x) for x in rows]
                    for row in rows:
                        story_dict[row[0]] = row[1:]
                    print("UID Present in DM table : ", story_dict)

                followers, following = splitted[9], splitted[10]

                if "Error" not in splitted[4] and "Challenge" not in splitted[4]:
                    if int(splitted[0]) in story_dict.keys():
                        print("{} exists in dm table, updating table ".format(splitted[0]))
                        targetted_users = story_dict[int(splitted[0])][0]
                        targetted_users = targetted_users[:-1]
                        #targetted_users += "," + splitted[7]

                        update_directmessage = """
                                        UPDATE dm
                                        SET email='{}', password='{}',group_id='{}',status='{}',proxy='{}',targetted_users='{}',dm_time='{}'
                                        WHERE id = {}
                                       """.format(splitted[1], splitted[2], splitted[3], splitted[4],
                                                  splitted[5], targetted_users, splitted[8], splitted[0])
                        print(update_directmessage)
                        c.execute(update_directmessage)
                        connection.commit()
                    else:
                        print("{} does not exist in dm table, inserting into table ".format(splitted[0]))
                        splitted = [x if x != "_pass_" else "" for x in splitted]
                        insert_directmessage = ''' INSERT INTO dm (id, email, password, group_id, status, proxy,
                                                                    targetted_users, dm_time)
                                             VALUES
                                             ('{}','{}','{}','{}','{}','{}','{}','{}')
                                             '''.format(splitted[0], splitted[1], splitted[2], splitted[3], splitted[4],
                                                        splitted[5], splitted[7], splitted[8])
                        print(insert_directmessage)
                        c.execute(insert_directmessage)
                        connection.commit()

            elif splitted[4] == "Mentions Done" or "Mentions" in splitted[4]:
                if "Challenge" in splitted[5]:
                    last_activity, status, proxy, last_login_time = splitted[4], "Not Working", splitted[6], splitted[8]
                else:
                    last_activity, status, proxy, last_login_time = splitted[4], "Working", splitted[6], splitted[8]
                if mentions_fetcher:
                    c.execute(mentions_fetcher)
                    mentions_fetcher = False
                    rows = c.fetchall()
                    story_dict = {}
                    rows = [list(x) for x in rows]
                    for row in rows:
                        story_dict[row[0]] = row[1:]
                    print("UID Present in mentions table : ", story_dict)
                followers, following = splitted[9], splitted[10]
                if "Error" not in splitted[4] and "Challenge" not in splitted[4]:
                    if int(splitted[0]) in story_dict.keys():
                        print("{} exists in mentions table, updating table ".format(splitted[0]))
                        targetted_users = story_dict[int(splitted[0])][0]
                        targetted_users += splitted[7]
                        update_mentions = """
                                                UPDATE mentions
                                                SET email='{}', password='{}',group_id='{}',status='{}',proxy='{}',mentions='{}',mention_time='{}'
                                                WHERE id = {}
                                                """.format(splitted[1], splitted[2], splitted[3], splitted[4],
                                                           splitted[6], targetted_users, splitted[8], splitted[0])
                        print(update_mentions)
                        print("why not update")
                        c.execute(update_mentions)
                        connection.commit()
                    else:
                        print("{} does not exist in mentions table, inserting into table ".format(splitted[0]))
                        splitted = [x if x != "_pass_" else "" for x in splitted]
                        insert_directmessage = ''' INSERT INTO mentions (id, email, password, group_id, status, proxy,
                                                                                mentions, mention_time)
                                                         VALUES
                                                         ('{}','{}','{}','{}','{}','{}','{}','{}')
                                                         '''.format(splitted[0], splitted[1], splitted[2], splitted[3],
                                                                    splitted[4], splitted[6],
                                                                    splitted[7], splitted[8])
                        print(insert_directmessage)
                        c.execute(insert_directmessage)
                        connection.commit()

            elif splitted[4] == "Relogin Working" or "Relogin" in splitted[4]:  # FOR UPDATING/INSERTING ROWS IN REELS
                if relogin_fetcher:
                    print("Executing SAVE RELOGIN Function")
                    c.execute(relogin_fetcher)
                    relogin_fetcher = False
                    rows = c.fetchall()
                    relogin_dict = {}
                    rows = [list(x) for x in rows]
                    for row in rows:
                        relogin_dict[row[0]] = row[1:]
                    print("UID Present in reels table : ", relogin_dict)

                if "Challenge" in splitted[4]:
                    last_activity, status, proxy, last_login_time = splitted[4], "Not Working", splitted[5], splitted[11]
                else:
                    last_activity, status, proxy, last_login_time = splitted[4], "Working", splitted[5], splitted[11]
                followers, following = splitted[12], splitted[13]

                biograpy = splitted[9]
                external_url = splitted[10]

                if "Error" not in splitted[4] and "Challenge" not in splitted[4]:
                    if int(splitted[0]) in relogin_dict.keys():
                        print(len(splitted))

                        print("{} exists in reels table ".format(splitted[0]))
                        reels_time = splitted[11]

                        existing_number = splitted[6]
                        posts = splitted[6]

                        existing_views =  splitted[7]

                        existing_likes =  splitted[8]

                        update_reels = """
                                        UPDATE reels
                                        SET email='{}', password='{}',group_id='{}',status='{}',proxy='{}',number_of_reels='{}',
                                        reels_views='{}',reels_likes='{}',reels_time='{}'
                                        WHERE id = {};
                                       """.format(splitted[1], splitted[2], splitted[3], splitted[4], splitted[5],
                                                  existing_number, existing_views,
                                                  existing_likes, reels_time, splitted[0])
                        print(update_reels)
                        c.execute(update_reels)
                        connection.commit()

            elif splitted[4] == "Posts Done" or "Posts" in splitted[4]:
                if "Challenge" in splitted[5]:
                    last_activity, status, proxy, last_login_time = splitted[4], "Not Working", splitted[6], splitted[9]
                else:
                    last_activity, status, proxy, last_login_time = splitted[4], "Working", splitted[6], splitted[9]
                if posts_fetcher:
                    c.execute(posts_fetcher)
                    posts_fetcher = False
                    rows = c.fetchall()
                    story_dict = {}
                    rows = [list(x) for x in rows]
                    for row in rows:
                        story_dict[row[0]] = row[1:]
                    print("UID Present in posts table : ", story_dict)
                followers, following = splitted[10], splitted[11]
                if "Error" not in splitted[4] and "Challenge" not in splitted[4]:
                    if int(splitted[0]) in story_dict.keys():
                        print("{} exists in posts table, updating table ".format(splitted[0]))
                        post_pk = story_dict[int(splitted[0])][0]
                        post_pk += "," + splitted[7]
                        update_posts = """
                                                UPDATE posts
                                                SET email='{}', password='{}',group_id='{}',status='{}',proxy='{}',post_pk='{}',post_link='{}',post_time='{}'
                                                WHERE id = {}
                                                """.format(splitted[1], splitted[2], splitted[3], splitted[4],
                                                           splitted[6], post_pk, splitted[8], splitted[9], splitted[0])
                        print(update_posts)
                        c.execute(update_posts)
                        connection.commit()
                    else:
                        print("{} does not exist in posts table, inserting into table ".format(splitted[0]))
                        splitted = [x if x != "_pass_" else "" for x in splitted]
                        insert_posts = ''' INSERT INTO posts (id, email, password, group_id, status, proxy,
                                                                                post_pk, post_link, post_time)
                                                         VALUES
                                                         ('{}','{}','{}','{}','{}','{}','{}','{}','{}')
                                                         '''.format(splitted[0], splitted[1], splitted[2], splitted[3],
                                                                    splitted[4], splitted[6],
                                                                    splitted[7], splitted[8], splitted[9])
                        print(insert_posts)
                        c.execute(insert_posts)
                        connection.commit()

            update_accounts = """
                                UPDATE accounts
                                SET
                                """

            following, followers = followers, following
            skip_account_update = True
            if initial:
                if last_activity != "_pass_" and last_activity != "":
                    update_accounts += "last_activity='{}'".format(last_activity) + ", "
                    skip_account_update = False

                if status != "_pass_" and status != "":
                    update_accounts += "status='{}'".format(status) + ", "
                    skip_account_update = False

                if proxy != "_pass_" and proxy != "":
                    update_accounts += "proxy='{}'".format(proxy) + ", "
                    skip_account_update = False

                if followers != "_pass_" and followers != "":
                    update_accounts += "followers='{}'".format(followers) + ", "
                    skip_account_update = False

                if following != "_pass_" and following != "":
                    update_accounts += "following='{}'".format(following) + ", "
                    skip_account_update = False

                if posts != "_pass_" and posts != "":
                    update_accounts += "posts='{}'".format(posts) + ", "
                    skip_account_update = False

                if biograpy != "_pass_" and biograpy != "":
                    update_accounts += "bio='{}'".format(biograpy) + ", "
                    skip_account_update = False

                if external_url != "_pass_" and external_url != "":
                    update_accounts += "bio_link='{}'".format(external_url) + ", "
                    skip_account_update = False

                if last_login_time != "_pass_" and last_login_time != "":
                    update_accounts += "last_login_time='{}'".format(last_login_time) + ", "
                    skip_account_update = False

                if profile_pic != "_pass_" and profile_pic != "":
                    update_accounts += "profile_pic='{}'".format(profile_pic) + ", "
                    skip_account_update = False

                if skip_account_update:
                    continue
                update_accounts = update_accounts[:-2]
                update_accounts += "WHERE id = {}".format(splitted[0])
                print("Updating Account Table : ", update_accounts)
                c.execute(update_accounts)
            connection.commit()
        except Exception as e:
            print(e)
            continue
    connection.close()

#save_excel("vps3")
