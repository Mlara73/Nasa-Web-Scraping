from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():

    # initializing browser
    browser = init_browser()
    mars_latest = {}

    #NASA Mars News

    # a while loop to refresh the page when it gets stuck
    counter = 0
    while (not counter>5):
    
        html_news = browser.html
        soup = BeautifulSoup(html_news, 'html.parser')
    
        url_news = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
        browser.visit(url_news)
    
        if soup.find_all('div', class_='list_text'):
            results_news= soup.find_all('div', class_='list_text')      
            break    
        else:
            counter= counter+1
            time.sleep(3);

    # data scraping and storing
    titles_list = []
    p_list= []
    date= []

    for result in results_news:
        content_title= result.find('div', class_= 'content_title').text
        paragraphs= result.find('div', class_='article_teaser_body').text
        dates= result.find('div', class_='list_date').text
        titles_list.append(content_title)
        p_list.append(paragraphs)
        date.append(dates)
    
    news_title= titles_list[0]
    news_p= p_list[0]
    date_info= date[0]

    
#--------------------------------------------------------------------------
    #JPL Mars Space Images - Featured Image
    #define url and browse
    url_images = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_images)

    #parsing with BeautifulSoup and the html.parser
    html_images = browser.html
    soup = BeautifulSoup(html_images, 'html.parser')

    #automatic clicks
    medium_image_button = browser.click_link_by_partial_text('FULL IMAGE')
    more_info_button= browser.click_link_by_partial_text('more info')

    #parsing with BeautifulSoup and the html.parser
    html_more_info = browser.html
    soup = BeautifulSoup(html_more_info, 'html.parser')

    #retrieve href link image
    featured_image = soup.find("figure", class_="lede")
    featured_image_href = featured_image.a['href']
    featured_image_clik= browser.click_link_by_href(featured_image_href)

    #parsing with BeautifulSoup and the html.parser in the new page
    html_href = browser.html
    soup = BeautifulSoup(html_href, 'html.parser')

    #retrieving the full size image url
    full_image_url= soup.img["src"]

#------------------------------------------------------------------------------
    #Mars Weather

    # a while loop to refresh the page when it gets stuck
    counter_weather = 0
    while (not counter_weather>5):
    
        #parsing with BeautifulSoup and the html.parser
        html_tweeter = browser.html
        soup = BeautifulSoup(html_tweeter, 'html.parser')
    
        #define url and browse
        url_tweeter = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(url_tweeter)
    
        if soup.find_all("div",class_='css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0'):
            weather_tweets= soup.find_all("div",class_='css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0')
            break
        else:
            counter_weather = counter_weather + 1
            time.sleep(3);
    #data scraping and storing

    tweets_list=[]
    for tweet in weather_tweets:
        tweet_text= tweet.find('span', class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0').text

        if 'InSight' in tweet_text:
            tweets_list.append(tweet_text)
            break
        else:
            pass
    mars_weather= tweets_list[0]
#------------------------------------------------------------------------------
    #Mars Fcats
    url_facts = 'https://space-facts.com/mars/'
    browser.visit(url_facts)

    #reading htm
    mars_table = pd.read_html(url_facts)

    #converting html table into df
    df = mars_table[0]
    mars_df= df.rename(columns={0:"", 1:"value"})
    mars_facts_df= mars_df.set_index("")

    #saving table to html
    mars_html_table = mars_facts_df.to_html(header=False, justify= "left")

#------------------------------------------------------------------------------
    #Mars Hemispheres

    #define url and browse
    url_hemispheres = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hemispheres)

    #parsing with BeautifulSoup and the html.parser
    html_hemispheres = browser.html
    soup = BeautifulSoup(html_hemispheres, 'html.parser')

    #retrieve all descriptions
    descriptions_text= soup.find_all("div",class_="description")

    hemisphere_image_urls = []
    for description in descriptions_text:
        try:
            title = description.h3.text
            link_title= browser.click_link_by_partial_text(title)
            html_title = browser.html
            soup = BeautifulSoup(html_title, 'html.parser')
            img_results= soup.find('div',class_="downloads")
            img_url= img_results.a['href']
        
            browser.visit(url_hemispheres)
        
             
            if title and img_url:
                hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
            
        except AttributeError as e:
            print(e)

    browser.quit()
#---------------------------------------------------------------------------------
#Generating database dictionary
    mars_latest["news_title"] = news_title
    mars_latest["news_paragraph"] = news_p
    mars_latest["news_date"] = date_info
    mars_latest["image_url"] = full_image_url
    mars_latest["mars_weather"] = mars_weather
    mars_latest['mars_table']= mars_html_table
    mars_latest['hemisphere_list']= hemisphere_image_urls

    return mars_latest   















