from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/webdrivers/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False, incognito = True)


def scrape():

    mars_latest = {}
    browser = init_browser()

    #NASA Mars News

    #define url and browse
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    #parsing with BeautifulSoup and the html.parser
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #retrieve the first list item
    results = soup.find('li', class_="slide")
    # retrieve the title, new, and  date  of the first list element
    news_title= results.find('div', class_='content_title').text
    news_p= results.find('div', class_='article_teaser_body').text
    news_date= results.find('div', class_='list_date').text
    print(news_date)
    #close browser
    browser.quit()
    
    
#--------------------------------------------------------------------------
    #JPL Mars Space Images - Featured Image

    browser = init_browser()
    #define url and browse
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    #parsing with BeautifulSoup and the html.parser
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #automatic clicks
    medium_image_button = browser.click_link_by_partial_text('FULL IMAGE')
    more_info_button= browser.click_link_by_partial_text('more info')

    #parsing with BeautifulSoup and the html.parser
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #retrieve href link image
    featured_image = soup.find("figure", class_="lede")
    featured_image_href = featured_image.a['href']
    featured_image_clik= browser.click_link_by_href(featured_image_href)

    #parsing with BeautifulSoup and the html.parser in the new page
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #retrieving the full size image url
    full_image_url= soup.img["src"]

    #close browser
    browser.quit()

    return print(full_image_url)

scrape()












