from selenium import webdriver
from selenium.webdriver.support.color import Color
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from instagram_main.credentials import get_cred_from_lasspass
from time import sleep
from random import randint, choice
import pandas as pd
from io import StringIO
from instagram_main.config import *
from instagram_main.modules import (
    check_if_element_by_css,
    read_hash_tag,
    add_comment,
    read_sql_file,
)
from instagram_main.DB_connection.db_modules import (
    get_records,
    connect_db,
    disconnect_db,
)
from tqdm import tqdm


# current_date_time = "nothing"
connection = connect_db("")

# login info
username, password = get_cred_from_lasspass("Instagram")


# selenium page controller or webdriver
def browser():
    # Chrome driver
    chrome_driver_path = chrome_driver
    # initiate Chrome browser
    driver = webdriver.Chrome(executable_path=chrome_driver_path)
    driver.maximize_window()
    driver.implicitly_wait(2)
    return driver


# selenium page controller or webdriver
browser = browser()


# explicit wait call
wait = WebDriverWait(browser, 4)


# navigate to instagram.com
def navigate_to_url(url):
    browser.get(url)
    browser.implicitly_wait(4)


# login to instagram.com
def login_to_instagram(username, password):
    navigate_to_url(instagram_login_page)
    username_field = browser.find_element_by_name("username")
    password_field = browser.find_element_by_name("password")
    button_login = browser.find_element_by_xpath(
        '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]'
    )
    username_field.send_keys(username)
    password_field.send_keys(password)
    button_login.click()
    browser.implicitly_wait(5)
    pop_up_notification = check_if_element_by_css(browser, login_popup_not_now_element)
    if pop_up_notification:
        not_now = browser.find_element_by_css_selector(login_popup_not_now_element)
        not_now.click()
        print("not now clicked")


login_to_instagram(username, password)


def search_user_by_hash(hash_by_category):
    """
    :param hash_by_category: pass a list of hash-tags or pass one one the following
     categories to use item from config.json
    :return:
    """
    hash_tag_list = read_hash_tag(hash_by_category)
    tag = choice(hash_tag_list)
    navigate_to_url(tag_url + tag)
    browser.implicitly_wait(5)
    first_thumbnail = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, thumbnail))
    )
    first_thumbnail.click()


def follow_user(follow_list):
    try:
        followed = 0
        instagram_user = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, users_name))
        ).text
        is_follow_sql = read_sql_file(if_following)
        query_with_param = is_follow_sql.replace("textToReplace", instagram_user)
        already_following_df = get_records(connection, query_with_param)
        if (
            already_following_df.bool() is False
            and browser.find_element_by_css_selector(follow_button).text == "Follow"
        ):

            if browser.find_element_by_css_selector(follow_button).text == "Follow":
                browser.find_element_by_css_selector(follow_button).click()
                # add followed to new_followed_list
                follow_list.append(instagram_user)
                followed += 1
    except Exception:
        followed = None
    return followed


def like_pic():
    likes = 0
    try:
        if wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, like_button))
        ).is_displayed():
            wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, like_button))
            ).click()
            likes += 1
    except Exception as es:
        wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, unlike_button))
        ).is_displayed()
        print("picture already liked")
    except:
        print("like button not found")
    return likes


def send_comment(comment_here):
    """
    :param comment_here: Variable name of a list containing comments eg: comment = ['nice','awesome','cool']
    :return: this adds a comment to the comment section of the user
    """
    while 1 == 1:
        determine_to_comment = randint(1, 5)
        try:

            print(determine_to_comment)
            if determine_to_comment >= 3:
                comment_section = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea.Ypffh"))
                )
                comment_section.send_keys(comment_here[randint(0, len(comment_here))])
                sleep(1)
                # hit Enter to send comment
                comment_section.send_keys(Keys.ENTER)
                sleep(randint(2, 4))
                break
            else:
                break
        except Exception:
            sleep(randint(5, 8))


# next picture
def click_next_pic():
    next_pic = browser.find_element_by_css_selector(next_button)
    next_pic.click()
    sleep(randint(2, 4))


def get_following_count():
    following = browser.find_element_by_css_selector(
        my_following + f"{username}/following/']"
    )
    following_count = int(following.text.replace(" following", ""))
    return following_count


# new code starts here --------------------------------------------------------------------------
# login_to_instagram(username, password)
# search_user_by_hash(fitness)
# follow_user()
# # like_pic()
# send_comment(comments_list)
# click_next_pic()


def follow_by_hash_tag(amount):
    navigate_to_url(my_profile_page + f"/{username}")
    following_count = get_following_count()
    new_followed = []
    account_uid_sql = read_sql_file(get_followed_users)
    query_with_param = account_uid_sql.replace("textToReplace", username)
    account_uid_df = get_records(connection, query_with_param)
    account_uid_df = account_uid_df.at[0, "ig_id"]
    while len(new_followed) < amount - 1:
        search_user_by_hash(fitness)
        for i in range(6):
            follow_user(new_followed)
            click_next_pic()
    navigate_to_url(my_profile_page + f"/{username}")
    new_following_count = get_following_count()
    updated_user_df = pd.DataFrame(new_followed, index=None, columns=["Followed_users"])
    current_date_time = pd.Timestamp.now()
    updated_user_df.insert(1, "date", current_date_time, True)
    updated_user_df.insert(0, "userID", account_uid_df, False)
    following_details = {
        "current_F": new_following_count,
        "previous_F": following_count,
        "today_date": current_date_time,
        "userID": account_uid_df,
    }
    following_details_df = pd.DataFrame(following_details, index=[0])
    print(following_details_df)
    print(updated_user_df)
    follow_details_table_name = 'public."follow_details"'
    iamfollowing_table_name = 'public."IG_iamfollowing"'
    output_fd = StringIO()
    output = StringIO()
    following_details_df.to_csv(output_fd, sep="\t", header=False, index=False)
    updated_user_df.to_csv(output, sep="\t", header=False, index=False)
    output_fd.seek(0)
    output.seek(0)
    cur = connection.cursor()
    cur.copy_from(
        output_fd,
        follow_details_table_name,
        columns=(
            "current_following_count",
            "previous_following_count",
            "date_last_updated",
            "ig_id",
        ),
    )
    cur.copy_from(
        output,
        iamfollowing_table_name,
        columns=("ig_id", "followed_username", "date_followed"),
    )
    connection.commit()
    cur.close()


def like_by_hash_tag(amount):
    new_liked = 0
    pbar = tqdm(total=new_liked, desc="total liked", leave=True)
    while new_liked <= amount:
        search_user_by_hash(fitness)
        for i in range(20):
            new_liked += like_pic()
            click_next_pic()
    return new_liked


def like_comment_follow_user():
    hash_tag_list = read_hash_tag(fitness)
    # prev_user_list = []
    sql = read_sql_file(get_followed_users)
    query_with_param = sql.replace("textToReplace", username)
    followed_from_db = get_records(connection, query_with_param)
    ig_id = [i for i in followed_from_db["ig_id"]]
    ig_id = ig_id[0]
    prev_user_list = [
        users for users in followed_from_db["followed_username"]
    ]  # list of followed from DB

    new_followed = []
    tag = -1
    followed = 0
    likes = 0
    comments = 0

    for hash_tag in hash_tag_list:
        tag += 1
        navigate_to_url(
            "https://www.instagram.com/explore/tags/" + hash_tag_list[tag] + "/"
        )

        first_thumbnail = browser.find_element_by_css_selector(thumbnail)
        first_thumbnail.click()
        sleep(randint(1, 2))
        try:
            for x in range(0, 3):
                instagram_user = browser.find_element_by_css_selector(users_name).text

                if (
                    instagram_user not in prev_user_list
                    and browser.find_element_by_css_selector(follow_button).text
                    == "Follow"
                ):
                    # if user already followed, do not follow
                    if (
                        browser.find_element_by_css_selector(follow_button).text
                        == "Follow"
                    ):
                        browser.find_element_by_css_selector(follow_button).click()
                        # add followed to new_followed_list
                        new_followed.append(instagram_user)
                        followed += 1
                        # liking the picture
                        button_like = wait.until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, like_button))
                        )
                        # browser.find_element_by_css_selector(like_button)
                        button_like.click()
                        likes += 1
                        # sleep(1)

                        # adds comment from the comment list
                        # adds random comments
                        add_comment(comments_list, wait, instagram_user)
                        comments += 1

                    # next picture
                    next_pic = browser.find_element_by_css_selector(next_button)
                    next_pic.click()
                    sleep(randint(2, 4))
                else:
                    next_pic = browser.find_element_by_css_selector(next_button)
                    next_pic.click()
        except:
            continue
    updated_user_df = pd.DataFrame(new_followed, index=None, columns=["Followed_users"])
    current_date_time = pd.Timestamp.now()
    updated_user_df.insert(1, "date", current_date_time, True)
    updated_user_df.insert(0, "userID", ig_id, False)
    print(updated_user_df)
    table_name = 'public."IG_iamfollowing"'
    output = StringIO()
    updated_user_df.to_csv(output, sep="\t", header=False, index=False)
    output.seek(0)
    cur = connection.cursor()
    cur.copy_from(
        output, table_name, columns=("ig_id", "followed_username", "date_followed")
    )
    connection.commit()
    cur.close()


# follow_by_hash_tag(2)
# like_by_hash_tag(5)
# like_comment_follow_user()
# browser.quit()
# disconnect_db(connection)


# browser.get(my_profile_page + f"/{username}")
# followers = browser.find_element_by_css_selector(
#     my_followers + f"{username}/followers/']"
# )

def unfollow_IG_user():
    unfollowed_list = []
    account_uid_sql = read_sql_file(get_followed_users)
    query_with_param = account_uid_sql.replace("textToReplace", username)
    account_uid_df = get_records(connection, query_with_param)
    account_uid_df = account_uid_df["followed_username"]
    print(account_uid_df)
    # acc = account_uid_df.at[0, "followed_username"]
    for user_id in account_uid_df:
        navigate_to_url(my_profile_page + f"/{user_id}")
        browser.implicitly_wait(2)
        follow_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.vBF20 button')))
        if follow_button.text == 'Following':
            follow_button.click()
            unfollowed_list.append(user_id)
            unfollowing_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.piCib button.-Cab_')))
            unfollowing_button.click()
        else:
            print(user_id, 'already unfollowed')
    unfollowed_list_t = tuple(unfollowed_list)
    print(unfollowed_list_t)
    cur = connection.cursor()
    cur.execute(f'update public."IG_iamfollowing" set unfollowed_username = True where followed_username in  {unfollowed_list_t}')
    connection.commit()
    cur.close()

# unfollowing_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.piCib button.-Cab_')))
# unfollowing_button.click()
unfollow_IG_user()
sleep(5)
exit()
# followers_count = followers.text
# following_count = following.text
# print(int(followers_count.replace("followers", "")))
# print(int(following_count.replace(" following", "")))
# int(following_count.replace(' following', '')) and nt(following_count.replace(' following', ''))


