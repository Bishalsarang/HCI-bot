# Author: Bishal Sarang
import re
import requests
import time

def get_xp_level(pattern_level, pattern_xps, home):
    """
    :param pattern_level:  regex pattern to extract level from homepage
    :param pattern_xps: regex pattern to extract xps from home page
    :param home: home request object
    :return:
    current_xp and current_level
    """
    current_level = re.search(pattern_level, home.text).group(1)
    current_xp = re.search(pattern_xps, home.text).group(1)
    current_xp = re.search(r'([\d,]+)', current_xp).group(1)
    return  current_xp, current_level


# Your username and password for ELF
username = ""
password = ""

# ELF Login URL
LOGIN_URL = "http://elf.ku.edu.np/login/index.php"

# HCI Course URL
COURSE_URL = "http://elf.ku.edu.np/course/view.php?id=14"

postfix = "&redirect=1"

# Regex patterns
pattern_xps = r'<div class=\"pts\">(.+)</div>'
pattern_level = r'<div class=\".*\"\saria-label=\"Level\s#\d+\">(\d+)</div>'
# Pattern for link with url
regex_pattern_1 = r'href=\"http://elf\.ku\.edu\.np/mod/url/view\.php\?id=(\d+)\"'
# Pattern for link with resources
regex_pattern_2 = r'href=\"http://elf\.ku\.edu\.np/mod/resource/view\.php\?id=(\d+)\"'

# Base URL for url types link
BASE_URL_1 = "http://elf.ku.edu.np/mod/url/view.php?id="
# Base URL for resource type links
BASE_URL_2 = "http://elf.ku.edu.np/mod/resource/view.php?id="

# Create Session object
session = requests.session()
# Login Parameters
data = {'username': username, 'password': password}
# Create a new session with given credentials
sess = session.post(LOGIN_URL, data=data)

# Using the session go to HCI course Page
home = session.get(COURSE_URL)

xp, level = get_xp_level(pattern_level, pattern_xps, home)
print("Your initial xp is {}".format(xp))
print("Your initial level is {}".format(level))


pattern_1_ids = re.findall(regex_pattern_1, home.text)
pattern_2_ids = re.findall(regex_pattern_2, home.text)



num_of_times = 20

# Simulate link clicking num_of_times
for j in range(20):

    for i, id in enumerate(pattern_2_ids):
        print("Clicking Link {}".format(BASE_URL_2 + id))
        session.get(BASE_URL_2 + id)
        print("Waiting {} secs".format(10))
        time.sleep(10)

        # Load homepage to get xp and level
        home = session.get(COURSE_URL)
        xp, level = get_xp_level(pattern_level, pattern_xps, home)
        print("Your current  xp is {}".format(xp))
        print("Your current level is {}".format(level))
        time.sleep(10)

    for i, id in enumerate(pattern_1_ids):
        print("Clicking Link {}".format(BASE_URL_1 + id))
        session.get(BASE_URL_1 + id)
        print("Waiting {} secs".format(10))
        time.sleep(10)

        # Load homepage to get xp and level
        home = session.get(COURSE_URL)
        xp, level = get_xp_level(pattern_level, pattern_xps, home)
        print("Your current  xp is {}".format(xp))
        print("Your current level is {}".format(level))
        time.sleep(10)

