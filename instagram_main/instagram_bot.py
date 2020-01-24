from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from instagram_main.credentials import get_cred_from_lasspass
from time import sleep, strftime
from random import randint
import pandas as pd
from instagram_main.config import *
from instagram_main.modules import check_if_element_by_css, read_hash_tag, add_comment

current_date_time = "nothing"

# login info
username = get_cred_from_lasspass("Instagram")["user"]
password = get_cred_from_lasspass("Instagram")["pass"]


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
wait = WebDriverWait(browser, 100)


# navigate to instagram.com
def navigate_to_url():
    browser.get(instagram_login_page)
    browser.implicitly_wait(3)


navigate_to_url()


# login to instagram.com
def login_to_instagram(username, password):

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


def like_comment_follow_user():
    # "gymrat", "fitness","atl", "cardio", "travel"
    hash_tag_list = read_hash_tag(fitness)
    comments_list = ["nice!", "sweet!", ":-)", "Cool", "👍🏿"]
    prev_user_list = []
    # prev_user_list = pd.read_csv(
    #     "20200117-020548_users_followed_list.csv", delimiter=","
    # ).iloc[:,0:]
    # prev_user_list = list(prev_user_list)
    # print(prev_user_list)

    new_followed = []
    tag = -1
    followed = 0
    likes = 0
    comments = 0

    for hash_tag in hash_tag_list:
        tag += 1
        browser.get(
            "https://www.instagram.com/explore/tags/" + hash_tag_list[tag] + "/"
        )
        browser.implicitly_wait(3)
        first_thumbnail = browser.find_element_by_css_selector(thumbnail)
        first_thumbnail.click()
        sleep(randint(1, 2))
        try:
            for x in range(1, 3):
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
                        add_comment(comments_list, wait)
                        comments += 1
                        print("comment added for user: ", instagram_user)

                    # next picture
                    next_pic = browser.find_element_by_css_selector(next_button)
                    next_pic.click()
                    sleep(randint(2, 4))
                else:
                    next_pic = browser.find_element_by_css_selector(next_button)
                    next_pic.click()
        except:
            continue
    for n in range(0, len(new_followed)):
        prev_user_list.append(new_followed[n])

    updated_user_df = pd.DataFrame(
        prev_user_list, index=None, columns=["Followed_users"]
    )
    updated_user_df.to_csv(
        "{}_users_followed_list.csv".format(strftime("%Y%m%d-%H%M%S"))
    )
    print(updated_user_df)


# get current followers count
# test navigate to my profile
browser.get(my_profile_page)
followers = browser.find_element_by_css_selector(my_followers)
following = browser.find_element_by_css_selector(my_following)
followers_count = followers.text
following_count = following.text
print(followers_count)
print(int(following_count.replace(" following", "")))
# int(following_count.replace(' following', '')) and nt(following_count.replace(' following', ''))


like_comment_follow_user()

browser.quit()
