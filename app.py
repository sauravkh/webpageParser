import requests
from bs4 import BeautifulSoup
import image_scraper
import os
import xlsxwriter
from requests.exceptions import RequestException



''' 
author : Saurav Kharb
Last Modified : 2/4/18

Code to scrape web page 
reads a url 
downloads text, numbers 
downloads images
write to excel

make an array of all the text or div's with text
loop through the array 

add error handling
'''



def scrape_webpage(URL):
    html  = request_url(URL)
    if(html != ""):
        text_list = parse_image_urls(html)
        write_to_file(text_list)
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

def parse_image_urls(html):
    soup = BeautifulSoup(html, 'html.parser')
    text = []
    for link in soup.find_all('img'):
        text.append(link.get('src'))
    return text

def write_to_file(text):
    workbook = xlsxwriter.Workbook('downloads/image_urls.xlsx')
    worksheet = workbook.add_worksheet()
    row = 0
    for url in text:
        worksheet.write_string(row,1, url)
        row += 1
    workbook.close()
    print("=========================")
    print('Text and image links written')
    print("=========================")



def main():
    URL = input("Enter the URL to scrape:  ")
    scrape_webpage(URL)

main()