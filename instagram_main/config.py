from instagram_main.modules import config_json
from io import StringIO
import pandas as pd
from random import randint, choice


georgia_cities_path = r"C:\Users\Nastracha\Instagram\instagram_main\Locations\georgia_cities.json"
config_file_path = r"C:\Users\Nastracha\Instagram\instagram_main\config.json"
config = config_json(config_file_path)
georgia_cities = config_json(georgia_cities_path)


# URL
instagram_login_page = config["URL"]["instagram"]
my_profile_page = config["URL"]["my_profile"]
tag_url = config["URL"]["url_tags"]

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
unlike_button = config["IG_elements"]["Unlike_button"]
next_button = config["IG_elements"]["next_button"]

# hash_tags
fitness = config["Hash_tags"]["fitness"]
# instagram_main/Hashtags/fitness_hash_list.txt


# SQL Scripts
get_followed_users = config["Sql_scripts"]["get_followed_users"]
if_following = config["Sql_scripts"]["if_following"]
update_unfollowed = config["Sql_scripts"]["update_unfollowed"]



# comment list
comments_list = ["nice!", "sweet!", ":-)", "Cool", "👍🏿"]

# georgia cities

# atlanta_search = georgia_cities["georgia"]["Atlanta"]
# norcross_search = georgia_cities["georgia"]["norcross"]
# marietta_search = georgia_cities["georgia"]["marietta"]
# buckhead_search = georgia_cities["georgia"]["buckhead"]
# alpharetta_search = georgia_cities["georgia"]["alpharetta"]
# tucker_search = georgia_cities["georgia"]["tucker"]
# doraville_search = georgia_cities["georgia"]["doraville"]
# mcdonough_search = georgia_cities["georgia"]["mcdonough"]


# cities_list = [georgia_cities['georgia'][x] for x in georgia_cities['georgia']]
# print(cities_list)
# # print(georgia_cities["georgia"])




# list_a = ['mike', 'james', 'tommas']
# list_df = pd.DataFrame(list_a)
# list_t = tuple(list_a)
# # print(list_df)
# io_list = StringIO()
# list_df.to_csv(io_list, sep=",", header=False, index=False)
# io_list.seek(0)
# print('abs is a monster', io_list.getvalue())
# print(io_list.getvalue())
