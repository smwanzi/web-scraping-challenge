#!/usr/bin/env python
# coding: utf-8

# Mission to Mars
# Jupyter Notebook Conversion to Python Script

# Import dependencies
from bs4 import BeautifulSoup
from splinter import Browser
from selenium import webdriver
import pandas as pd
import time
import datetime as dt
#import re
################################################
# Windows
# Set Executable Path & Initialize Chrome Browser
################################################
# executable_path = {"executable_path": "./chromedriver.exe"}
# browser = Browser("chrome", **executable_path)

#################################################
# Latest Mars News
################################################# 
def scrape():
        mars_dict={}
        # set chrome driver path
        executable_path = {'executable_path': 'chromedriver.exe'}
        browser = Browser('chrome', **executable_path, headless=False)
        import time
        # visit NASA Mars News url
        url='https://mars.nasa.gov/news/'
        browser.visit(url)
        time.sleep(3)

        # use html to create beautiful soup object
        html = browser.html
        soup = BeautifulSoup(html,'html.parser')

        # Extract news article title and paragraph text
        article = soup.find("div", class_='list_text')
     
        # extract news title
        news_title = article.find("div", class_="content_title").text
        mars_dict['title']= news_title
        
        # extract the paragraph text
        news_p =soup.find ('div', class_='article_teaser_body').text
        mars_dict["paragraph"] = news_p
#################################################
# JPL Mars Space Images - Featured Mars Image
#################################################
        import time
        image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
        browser.visit(image_url)
        time.sleep(3)
        # Click to go to 'FULL IMAGE'
        browser.links.find_by_partial_text('FULL IMAGE')[0].click()
        time.sleep(3)
        # Click to go to 'more info' 
        browser.links.find_by_partial_text('more info').click()
        time.sleep(3)
        # Parse HTML with Beautiful Soup
        html = browser.html
        image_soup = BeautifulSoup(html, 'html.parser')

        # Scrape the URL and extract the Featured image URL
        feat_img_url = image_soup.find('figure', class_='lede').a['href']
        featured_image_url = f'https://www.jpl.nasa.gov{feat_img_url}'
       
        mars_dict['featured_image_url'] = featured_image_url
        
#################################################
# Mars Weather
#################################################      
        # Visit Mars Weather twitter page for latest tweet on Mars Weather
        import time
        url ='https://twitter.com/marswxreport?lang=en'
        browser.visit(url)
        time.sleep(3)

        # use html to create beautiful soup object
        html = browser.html
        soup = BeautifulSoup(html,'html.parser')
        
        # extract the latest Mars Weather Tweet
        mars_weather = soup.find('div', class_='css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0').text
        mars_dict['mars_weather'] = mars_weather
        
#################################################
# Mars Facts
#################################################
        # Visit Mars facts Url
        url = 'https://space-facts.com/mars/'
        browser.visit(url)
        html = browser.html

        # Use Pandas to scrape the table containing facts about Mars and clean it up
        table = pd.read_html(url)
        mars_facts = table[2]
        # Rename columns
        mars_facts.columns = ['Description','Value']
        # Reset Index 
        mars_facts.set_index('Description', inplace=True)
        # Converting table data to Html string
        mars_facts = mars_facts.to_html()
        mars_facts = mars_facts.replace("\n", "")
              
        mars_dict['mars_facts']= mars_facts
        
#################################################
# Mars Hemispheres
#################################################
        import time
        # Visit the USGS Astrogeology site to obtain high resolution images for each of Mar's hemispheres.
        url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        browser.visit(url)
        time.sleep(5)
        html = browser.html

        # Create BeautifulSoup object; parse with 'html.parser'
        soup = BeautifulSoup(html, 'html.parser')

        products = soup.find('div', class_='result-list')
        hemispheres=products.find_all('div', class_='item')
       
        # Loop through returned results and 
        # create a list of links for the hemispheres img urls

        hemisphere_image_urls=[]

        for hemisphere in hemispheres:
            title = hemisphere.find("h3").text
            title = title.replace("Enhanced", "")
            end_link = hemisphere.find("a")["href"]
            image_link = "https://astrogeology.usgs.gov/" + end_link    
            browser.visit(image_link)
            import time
            time.sleep(5)
            html = browser.html
            soup = BeautifulSoup(html, "html.parser")
            downloads = soup.find("div", class_="downloads")
            image_url = downloads.find("a")["href"]
            hemisphere_image_urls.append({"title": title, "image_url": image_url})
            import datetime as dt 
            
        mars_dict['hemisphere_urls'] = hemisphere_image_urls
        mars_dict["TimeStamp"]=dt.datetime.now()
                                 
        # Close the browser after scraping
        browser.quit()   
        return mars_dict
                                 
# if __name__ == '__main__':
#     scrape()
