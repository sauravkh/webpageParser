import requests
from bs4 import BeautifulSoup
import image_scraper
import os
import xlsxwriter
from requests.exceptions import RequestException
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time



''' 
author : Saurav Kharb

'''


def setupSelenium(url):

    title= name= num= text= time_ = averageRating = "N/A"

    times = content=numset=names = [];


    # set the default path to chromedriver and start the browser
    path_to_chromedriver = '/Users/TheSauravKharb/Downloads/chromedriver';
    browser = webdriver.Chrome(executable_path = path_to_chromedriver);
    browser.get(url)
    print('Please wait....')
    time.sleep(5)

    # scrapes the text that tells the total number of reviews --> "(20 reviews)"
    try:
        number_of_ratings_string = browser.find_element_by_css_selector(".rpro-avg-rating");
    except NoSuchElementException:
        print("No matching elements found for the css selector")

    # scrapes and counts the stars for average rating by using appropriate css selectors
    try:
        full_stars = browser.find_elements_by_css_selector(".rpro-avg-rating .fa-star");
        half_stars = browser.find_elements_by_css_selector(".rpro-avg-rating .fa-star-half-o");
        if(len(half_stars) > 0): 
            num = 0.5;
        else:
            num = 0
        averageRating = len(full_stars) + num;
    except NoSuchElementException:
        print("No matching elements found for the css selector")

    # scrapes names of each reviewer by using appropriate css selector
    try:
        name_list = browser.find_elements_by_css_selector(".each-review .rpro-head .rpro-poster");
        names = [x.text for x in name_list]
    except NoSuchElementException:
        print("No matching elements found for the css selector")

    # scrapes number of stars for each reviewer using appropriate css selectors
    try:
        size = len(names);
        numSet = []
        for i in range(0,size):
            char_index = i + 3;
            selector = "div.mod.rpro-container.Light > div:nth-child(" + str(char_index) + ") > div.rpro-rating > i";
            num_stars = browser.find_elements_by_css_selector(selector);
            numSet.append(len(num_stars))
    except NoSuchElementException:
        print("No matching elements found for the css selector")

    
    # scrapes the review text for each reviewer
    try:
        review_text = browser.find_elements_by_css_selector(".each-review .rpro-content");
        content = [x.text for x in review_text]
    except NoSuchElementException:
        print("No matching elements found for the css selector")

    # scrapes the title of the product from the webpage
    try:
        title = browser.find_element_by_css_selector(".product-title");
        title = title.text;
    except NoSuchElementException:
        print("No matching elements found for the css selector")

    # scrapes the time when the reviews were posted
    try:
        time_list = browser.find_elements_by_css_selector(".each-review .rpro-head .rpro-posted");
        times = [x.text for x in time_list]
    except NoSuchElementException:
        print("No matching elements found for the css selector")

    # scrapes the url's of all images in file
    try:      
        img_list = browser.find_elements_by_css_selector("img");
        urls = [x.get_attribute('src') for x in img_list]
        hidden_list = browser.find_elements_by_css_selector(".image-1");
        for element in hidden_list:
                urls.append(element.value_of_css_property("background-image"))
    except NoSuchElementException:
        print("No matching elements found for the css selector")
    

    # setup and write data in a spreadsheet
    workbook = xlsxwriter.Workbook('downloads/reviewData.xlsx')
    worksheet = workbook.add_worksheet()

    # set a style for headings
    bold = workbook.add_format({'bold': True})

    # write the heading names
    worksheet.write(0,0, "Product Name",bold);
    worksheet.write(0,1, "Number of reviews",bold);
    worksheet.write(0,2, "Average Rating", bold);
    worksheet.write(0,3, "Average Rating", bold);

    # write associated data points
    worksheet.write(1,0, title);
    worksheet.write(1,1, num);
    worksheet.write(1,2, averageRating);

    rowCount = 1;
    for url in urls:
        worksheet.write(rowCount,3, url);
        rowCount += 1;

    num_of_urls = rowCount;

    worksheet.write(num_of_urls,0, "Reviewer Name", bold);
    worksheet.write(num_of_urls,1, "Individual Rating", bold);
    worksheet.write(num_of_urls,2, "Review", bold);
    worksheet.write(num_of_urls,3, "Time stamp", bold);

    num_of_urls += 1;
    rowCount = num_of_urls;
    for name in names:
        worksheet.write(rowCount,0, name);
        rowCount += 1;

    rowCount = num_of_urls;
    for num in numSet:
        worksheet.write(rowCount,1, num);
        rowCount += 1;
    
    rowCount = num_of_urls;
    for text in content:
        worksheet.write(rowCount,2, text);
        rowCount += 1;

    rowCount = num_of_urls;
    for time_ in times:
        worksheet.write(rowCount,3, time_);
        rowCount += 1;

    print("Scraping the website");
    print("=====================")
    print("All retrievable data written successfully!")


def scrape_webpage(URL):
    html  = request_url(URL)
    if(html != ""):
        setupSelenium(URL)
        get_iamges(URL)    


def request_url(URL):
    try:
        response = requests.get(URL)
        html = response.text
        return html  
    except ValueError:
        print("Could not request website")
        quit()
    return ""


def get_iamges(URL):
    # runs a command line 
    os.system("image-scraper %s" %URL)


def main():
    URL = input("Enter the URL to scrape:  ")
    scrape_webpage(URL)


main()