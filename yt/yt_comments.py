def scroll_to_bottom(driver, prev_height):
    driver.execute_script(f"window.scrollTo({prev_height}, {prev_height + 400});")


def get_height(driver):
    height = driver.execute_script("""
        function get_height() {
            return Math.max(
                Math.max(document.documentElement.scrollHeight, document.body.scrollHeight),
                Math.max(document.documentElement.offsetHeight, document.body.offsetHeight),
                Math.max(document.documentElement.clientHeight, document.body.clientHeight)
            );
        }
        return get_height()
    """)
    return height


def select_new_first(driver, sort_comments_btn_xpath):
    # selecting top comments or newest first
    driver.find_element("xpath", sort_comments_btn_xpath).click()
    time.sleep(1)
    driver.find_element("xpath", '//*[contains(text(), "Newest first")]').click()


import time
from collections import defaultdict

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup as bs

url = 'https://www.youtube.com/watch?v=jO6qQDNa2UY'
# select if you want newest comments first + other options
new_first = True
no_of_comments = 100

# initializing the selenium browser
options = Options()
# options.add_argument('--headless')
options.add_argument("--start-maximized")

service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=options)
driver.get(url)

sort_comments_btn_xpath = '//div[@class="style-scope tp-yt-paper-menu-button"][@id="trigger"]/tp-yt-paper-button/div[@id="icon-label"][normalize-space(text())="Sort by"]'
description_box = "//div[@class='item style-scope ytd-watch-metadata'][@id='description']"

WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located(("xpath", description_box))
)

prev_height = 0
time.sleep(1)
scroll_to_bottom(driver, prev_height)

WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located(("xpath", sort_comments_btn_xpath))
)

title = driver.find_element("xpath", '//div[@id="above-the-fold"]//h1').text.strip()
channel_name = driver.find_element("xpath",
                                   '//div[@id="upload-info"]//ytd-channel-name[@id="channel-name"]').text.strip()
# format the description
description = driver.find_element("xpath",
                                  '//div[@id="description-inner"]//ytd-text-inline-expander[@id="description-inline-expander"]//yt-attributed-string').text.strip()
total_comments = driver.find_element("xpath", '//h2[@id="count"]').text.strip()

print(title, channel_name, description, total_comments)

if new_first:
    select_new_first(driver, sort_comments_btn_xpath)

# dictionary with usernames as keys and the rest of the data stored as a list of that key
comments = defaultdict(list)

# scrolling to end of comments
height = get_height(driver)

while (prev_height != height) and (len(comments) < no_of_comments):
    scroll_to_bottom(driver, height)
    time.sleep(2)
    prev_height = height
    height = get_height(driver)

    # finding the comment boxes in selenium
    comment_boxes_list = driver.find_elements("xpath", "//ytd-comment-thread-renderer")

    for comment_box in comment_boxes_list:
        # checking if some part of comment is hidden if yes then click read more

        # converting each comment box separately to beautiful soap
        source = bs(comment_box.get_attribute("innerHTML"), "lxml")
        comment_data = source.select_one("#main")
        reply_data = source.find_all(id="more-replies")
        username = comment_data.select_one("#author-text").text.strip()

        # comments are seperated on the basis of emojis, links and text so add each separately
        all_comment_parts = comment_data.select_one("#content-text").contents
        comment = ""
        for comment_part in all_comment_parts:
            if comment_part.name == "img":
                comment = comment + comment_part["alt"] + " "
            elif comment_part.name == "a" or comment_part.name == "span":
                comment = comment + comment_part.text.strip()

        published_time = comment_data.select_one(".published-time-text").text.strip()
        likes = comment_data.select_one("#vote-count-middle").text.strip()

        if (len(reply_data) > 0):
            replies = reply_data[0].select_one("span",
                                               class_="yt-core-attributed-string--white-space-no-wrap").text.strip()
        else:
            replies = "0 replies"

        # [0]->comment, [1]->published time, [2]->total replies, [3]->likes
        data = []
        data.append(comment)
        data.append(published_time)
        data.append(replies)
        data.append(f'{likes} likes')

        comments[username].append(data)

    driver.execute_script("""
        var element = document.querySelector("ytd-comment-thread-renderer");
        element.parentNode.removeChild(element);
    """)

    time.sleep(2)

print(len(comments))
print(comments)

driver.quit
