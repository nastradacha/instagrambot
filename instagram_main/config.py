from instagram_main.modules import config_json


config_file_path = r"C:\Users\Nastracha\Instagram\instagram_main\config.json"
config = config_json(config_file_path)


# URL
instagram_login_page = config["URL"]["instagram"]
my_profile_page = config["URL"]["my_profile"]

# Chrome browser driver
chrome_driver = config["configs"]["Chrome_driver"]

# Elements for my profile page
my_followers = config["Elements"]["my_followers_selector"]
my_following = config["Elements"]["my_following_selector"]

# other elements
login_popup_not_now_element = config["IG_elements"]["login_popup_not_now_element"]
thumbnail = config["IG_elements"]["thumbnail"]
users_name = config["IG_elements"]["usersname"]
follow_button = config["IG_elements"]["follow_button"]
like_button = config["IG_elements"]["like_button"]
next_button = config["IG_elements"]["next_button"]

# hash_tags
fitness = config["Hash_tags"]["fitness"]
# instagram_main/Hashtags/fitness_hash_list
