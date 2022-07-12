from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time


yt_trending_url = 'https://www.youtube.com/feed/trending/'


def get_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_driver = webdriver.Chrome('chromedriver', options=chrome_options)
    return chrome_driver


def get_videos(driver, url):
    # Fetching page
    driver.get(url)
    time.sleep(5)
    # Get video div tags
    video_div_tag = 'ytd-video-renderer'
    videos = driver.find_elements(By.TAG_NAME, video_div_tag)

    return videos


def parse_video(video):
    # Find the line of html that contains the information we want
    title_tag = video.find_element(By.ID, 'video-title')
    channel_div = video.find_element(By.CLASS_NAME, 'ytd-channel-name')
    views_and_time = video.find_element(By.ID, 'metadata-line').text.split('\n')
    description = video.find_element(By.ID, 'description-text')

    # Get the exact information from the html
    title = title_tag.text
    url = title_tag.get_attribute('href')
    views = views_and_time[0]
    upload_time = views_and_time[1]
    channel_name = channel_div.text
    description_text = description.text

    return {'Title': title,
            'Channel': channel_name,
            'Description': description_text,
            'Views': views,
            'Time': upload_time,
            'URL': url,
            }


def get_trending_videos(url):
    driver = get_driver()
    videos = get_videos(driver, url)

    return [parse_video(video) for video in videos]


if __name__ == "__main__":

    list_of_videos = get_trending_videos(yt_trending_url)
    videos_df = pd.DataFrame(list_of_videos)
    videos_df.to_csv('youtube trending videos.csv', sep='|')