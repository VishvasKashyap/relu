from selenium import webdriver
from selenium.webdriver.common.by import By
from collections import Counter
import re

driver = webdriver.Chrome()

driver.get("https://www.dailymotion.com/user/tseries/1")


def extract_video_ids(url_list):
    video_ids = []
    for url in url_list:
        match = re.search(r'/video/([^/]+)', url)
        if match:
            video_ids.append(match.group(1))
    return video_ids


video_urls = []
while len(video_urls) < 500:
    urls_on_page = driver.find_elements_by_xpath('//a[@class="dmp_VideoCard__thumbnailContainer"]')
    for url_element in urls_on_page:
        video_urls.append(url_element.get_attribute('href'))
        if len(video_urls) >= 500:
            break
    if len(video_urls) < 500:
        next_page_button = driver.find_element_by_xpath('//button[@class="dmp_Pagination__next"]')
        next_page_button.click()

video_ids = extract_video_ids(video_urls)

char_count = Counter(''.join(video_ids))

most_common_char = min(char_count.items(), key=lambda x: (-x[1], x[0]))

print(f"{most_common_char[0]}:{most_common_char[1]}")

driver.quit()