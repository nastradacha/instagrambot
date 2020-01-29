import json
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from random import randint
from time import sleep


def last_login(path_to_lastpass_login):
    """
    :param path_to_lastpass_login: json file containing lasspass login credentials
    :return: a dictionary object containing the username and password
    """
    with open(path_to_lastpass_login) as cred_file:
        credential = json.load(cred_file)
    return credential


def config_json(file_path):
    with open(file_path) as config_file:
        c_config = json.load(config_file)
        config_file.close()
    return c_config


def add_comment(comment_here, wait, instagram_user):
    """
    :param comment_here: Variable name of a list containing comments eg: comment = ['nice','awesome','cool']
    :param wait: This is a browser explicit wait function, wait function is added to a variable in the instagram_bot.py
    :param instagram_user: instagram_user  that is being followed or liked
    :return: this adds a comment to the comment section of the user
    """
    while 1 == 1:
        determine_to_comment = randint(1, 5)
        try:

            print(determine_to_comment)
            if determine_to_comment >= 3:
                comment_section = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'textarea.Ypffh')))
                comment_section.send_keys(comment_here[randint(0, len(comment_here))])
                sleep(1)
                # hit Enter to send comment
                comment_section.send_keys(Keys.ENTER)
                print("comment added for user: ", instagram_user)
                sleep(randint(2, 4))
                break
            else:
                break
        except Exception:
            sleep(randint(5, 8))


def read_hash_tag(filename):
    with open(filename, 'r') as file:
        file_list = file.read().split()
        file_list = [i.replace('#', '') for i in file_list]
        file.close()
        return file_list


def check_if_element_by_css(webdriver, selector):
    try:
        webdriver.find_element_by_css_selector(selector)
    except NoSuchElementException:
        return False
    return True


def read_sql_file(sql_file):
    file = open(sql_file)
    sql_file = file.read().replace('\n', ' ')
    file.close()
    return sql_file
#
# current_date_time = pd.Timestamp.now()
# print(current_date_time)
# strftime("%Y%m%d-%H%M%S")
