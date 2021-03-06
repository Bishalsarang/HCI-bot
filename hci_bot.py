# Author: Bishal Sarang
"""
 A bot to automate clicking of links
"""
import re
import requests
import time


def is_valid_login(login_page, login_failed_message):
    """
    :param login_page: requests response object of login page
    :param login_failed_message: message that appears when login is invalid
    :return: boolean value whether login is success
    """
    return not re.search(login_failed_message, login_page.text)


def login(login_url, data):
    """
    :param login_url:  URL of login page
    :param data: credentials in dictionary format
    :return: authorised session and boolean success if login is valid
    """
    # Create Session object
    session = requests.session()

    # Create a new session with given credentials
    login_page = session.post(login_url, data=data)
    return session, is_valid_login(login_page, login_failed_message="Invalid login, please try again")


def print_status(rank, xp, level):
    """
    Prints your rank, xp and levek
    :param rank: Your current rank
    :param xp: Your current xp
    :param level: Your current level
    :return: None
    """
    print("You're now at rank {}".format(rank))
    print("Your current xp is {}".format(xp))
    print("Your current level is {}".format(level))


def get_rank(ladder_html, pattern):
    """
    Returns rank from ladder_html page
    :param ladder_html: requests response object for ladder page
    :param pattern: Regex pattern to get rank
    :return: Your current rank
    """
    return re.search(pattern, ladder_html.text).group(1)


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
    return current_xp, current_level


def click_links(pattern_id, BASE_URL):
    """
    Construct links using pattern ids and base urls and click on links
    :param pattern_id: pattern_ids given BASE_URL
    :param BASE_URL: BASE URL, 2 types of link: view and resource
    :return: None
    """
    for i, id in enumerate(pattern_id):
        print("Clicking Link {}".format(BASE_URL + id))
        session.get(BASE_URL + id)
        print("Waiting {} secs".format(SLEEP_TIME))
        time.sleep(SLEEP_TIME)

        # Load homepage to get xp and level
        home = session.get(COURSE_URL)
        rank = get_rank(session.get(LADDER_URL), pattern_rank)
        xp, level = get_xp_level(pattern_level, pattern_xps, home)
        print_status(rank, xp, level)
        if int(level) >= maximum_level_to_reach:
            print("Congratulations {}. You have reached level {}".format(your_name.title(), level))
            exit(0)
        time.sleep(SLEEP_TIME)

def main():
    """
    Main function to click links
    :return:
    """
    while True:
        click_links(pattern_2_ids, BASE_URL_2)
        click_links(pattern_1_ids, BASE_URL_1)

if __name__ == "__main__":

    # Maximum level you want to reach
    maximum_level_to_reach = 5
    # Time to sleep after every clicks
    SLEEP_TIME = 10

    # Your username and password for ELF
    username = ""
    password = ""

    # ELF Login URL
    LOGIN_URL = "http://elf.ku.edu.np/login/index.php"
    # Login With given credentials
    # Login Parameters
    data = {'username': username,
            'password': password}
    # authorised session after logging in
    session, success = login(LOGIN_URL, data)
    # If success is False i.e login failed
    if not success:
        print("Credentials Wrong. Please Try Again")
        exit(0)

    # HCI Course URL
    COURSE_URL = "http://elf.ku.edu.np/course/view.php?id=14"
    # Ladder URL for HCI
    LADDER_URL = "http://elf.ku.edu.np/blocks/xp/index.php/ladder/14"

    # Regex patterns for username, rank, xps and level
    pattern_username = r'<span class=\"usertext\"(?: id=\"\w+\")?>([\w\s-]+)<.*>'
    pattern_rank = r'<tr class=\"highlight-row\".*?\"\><td class=\".*?>(\d+)</td>'
    pattern_xps = r'<div class=\"pts\">(.+)</div>'
    pattern_level = r'<div class=\".*\"\saria-label=\"Level\s#\d+\">(\d+)</div>'

    # Using the session go to HCI course Page
    home = session.get(COURSE_URL)

    # Get name, rank, xp and level
    your_name = re.search(pattern_username, home.text).group(1)
    rank = get_rank(session.get(LADDER_URL), pattern_rank)
    xp, level = get_xp_level(pattern_level, pattern_xps, home)

    print("Welcome {}".format(your_name.title()))
    print_status(rank, xp, level)

    # Base URL for url types link
    BASE_URL_1 = "http://elf.ku.edu.np/mod/url/view.php?id="
    # Base URL for resource type links
    BASE_URL_2 = "http://elf.ku.edu.np/mod/resource/view.php?id="
    # Pattern for link with url
    regex_pattern_1 = r'href=\"http://elf\.ku\.edu\.np/mod/url/view\.php\?id=(\d+)\"'
    # Pattern for link with resources
    regex_pattern_2 = r'href=\"http://elf\.ku\.edu\.np/mod/resource/view\.php\?id=(\d+)\"'
    # All links of type URL
    pattern_1_ids = re.findall(regex_pattern_1, home.text)
    # All links of type resource
    pattern_2_ids = re.findall(regex_pattern_2, home.text)

    # Main function that calls click_links
    main()

