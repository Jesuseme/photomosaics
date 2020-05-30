# This code scrapes images from the website Unsplash.com

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import urllib.request
import os


def create_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--incognito")
    return webdriver.Chrome('chromedriver.exe', options=chrome_options)


def scrapeImageURLs(driverArgument, pages):
    print("Scraping image URLs...")
    totalImages = set()
    for counter in range(pages):
        images = driverArgument.find_elements_by_tag_name('img')
        for image in images:
            try:
                src = image.get_attribute('src')
                if 'photo' in src and 'profile' not in src:
                    totalImages.add(src)
            except StaleElementReferenceException:
                continue
        driverArgument.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN, Keys.PAGE_DOWN, Keys.PAGE_DOWN)
    driverArgument.quit()

    return totalImages


def downloadImages(srcList, arg):
    print(f"Downloading {arg} images...")
    previous_path = os.getcwd()
    folder = f'{arg.capitalize()} Images'
    if not os.path.exists(folder):
        os.mkdir(folder)
    os.chdir(folder)
    amtOfImages = len(srcList)
    counter = 0
    for index, src in enumerate(srcList):
        imageName = f'{arg}-{counter}.jpg'
        if os.path.exists(imageName):
            while os.path.exists(imageName):
                counter += 1
                imageName = f'{arg}-{counter}.jpg'
        urllib.request.urlretrieve(src, imageName)
        print(f"Downloaded {index + 1}/{amtOfImages} images.")

    os.chdir(previous_path)


def main():
    arg = 'car'
    url = f'https://unsplash.com/s/photos/{arg}'

    driver = create_driver()
    driver.get(url)
    imgSources = scrapeImageURLs(driver, pages=7)
    downloadImages(imgSources, arg)


if __name__ == '__main__':
    main()