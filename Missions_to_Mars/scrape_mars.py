from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


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

    #retrieve all news
    results= soup.find_all('div', class_='list_text')
    # retrieve the title, new, and  date  of the first list element
    titles_list = []
    p_list= []
    date= []

    for result in results:
        content_title= result.find('div', class_= 'content_title').text
        paragraphs= result.find('div', class_='article_teaser_body').text
        dates= result.find('div', class_='list_date').text
        titles_list.append(content_title)
        p_list.append(paragraphs)
        date.append(dates)
    
    news_title= titles_list[0]
    news_p= p_list[0]
    date_info= date[0]
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

#------------------------------------------------------------------------------
    #Mars Weather

    browser = init_browser()

    #define url and browse
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
  
    #parsing with BeautifulSoup and the html.parser
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

    #find all tweets
    weather_tweets= soup.find_all("div",class_='css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0')

    #retrieve only the first weather tweet
    tweets_list=[]
    for tweet in weather_tweets:
        tweet_text= tweet.find('span', class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0').text
        if 'InSight' in tweet_text:
            tweets_list.append(tweet_text)
            break
        else:
            pass
    mars_weather= tweets_list[0]
    print(mars_weather)
    # browser.quit()

#------------------------------------------------------------------------------
    #Mars Fcats
    url = 'https://space-facts.com/mars/'

    #reading htm
    mars_table = pd.read_html(url)

    #converting html table into df
    df = mars_table[0]
    mars_df= df.rename(columns={0:"", 1:"value"})
    mars_facts_df= mars_df.set_index("")

    #saving table to html
    mars_html_table = mars_facts_df.to_html(header=False, justify= "left")

#------------------------------------------------------------------------------
    #Mars Hemispheres

    #define url and browse
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    #parsing with BeautifulSoup and the html.parser
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #retrieve all descriptions
    descriptions_text= soup.find_all("div",class_="description")

    hemisphere_image_urls = []
    for description in descriptions_text:
        try:
            title = description.h3.text
            link_title= browser.click_link_by_partial_text(title)
            html = browser.html
            soup = BeautifulSoup(html, 'html.parser')
            img_results= soup.find('div',class_="downloads")
            img_url= img_results.a['href']
        
            browser.visit(url)
        
             
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

    print(mars_latest)
    return mars_latest   















