# Dependencies and Setup
# import dependencies
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup as bs
from selenium import webdriver

import pandas as pd
import time

# Initialize the browser
def init_browser():
    # load the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)

# Create Mission to Mars dictionary that can be imported into Mongo
mars_info = {}

# Scrape function for Mars news
def scrape_mars_news():
    browser = init_browser()

    # Visit the website
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    
    # Create HTML object
    html = browser.html
    
    # Parse HTML with beautiful soup
    soup = bs(html, 'html.parser')
    
    # find the first element in the tree
    # use ul and li
    results = soup.select_one('ul.item_list li.slide')
    
    # get the title and paragraphs
    news_title = results.find('div', class_="content_title").find('a').text
    news_p = results.find('div', class_="article_teaser_body").text
    
    # enter information into the dictionary
    mars_info['news_title'] = news_title
    mars_info['news_paragraph'] = news_p

    return mars_info
    
    browser.quit()
    
    
# Scrap the featured image
def scrape_mars_image():
    browser = init_browser()

    # Visit the website
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    
    # Making a beautiful soup
    html = browser.html
    image_soup = bs(html, 'html.parser')
    
    # find the image in the gallery website
    image_element = image_soup.find('div', class_='carousel_items')
    image_element
    
    # Grab the featured image url
    featured_image_url  = image_element.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
    
    url_text = 'https://www.jpl.nasa.gov'

    img_url = f'{url_text}{featured_image_url}'
    
    # Make the full url
    featured_image_url = url_text + img_url
    
    # Display full link to featured image
    featured_image_url 

    # Dictionary entry from FEATURED IMAGE
    mars_info['featured_image_url'] = featured_image_url 
        
    return mars_info

    browser.quit()
    
# Scrape function for Mars hemisphere images
def scrape_mars_hemispheres():
    browser = init_browser()
    
    # Visit the website
    # Making the url
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Making a beautiful soup
    html = browser.html
    hemisphere_soup = bs(html, 'html.parser')
    
    # Retreive all items that contain mars hemispheres information.
    html_items = hemisphere_soup.find_all('div', class_='item')

    # Create empty list for hemisphere urls 
    hemisphere_image_urls = []

    # Save the main url, so that you can loop through each website
    hemispheres_main_url = 'https://astrogeology.usgs.gov'

    # loop through all of the elements to find the html and visit each site
    # Use beautiful soup and parse through each website to grab the necessary information
    for item in html_items:

        # Store title
        title = item.find('h3').text

        # Store link that leads to full image website
        img_url = item.find('a', class_='itemLink product-item')['href']

        # Combine the main website link to the link with the other page 
        # This will allow us to visit individual websites
        browser.visit(hemispheres_main_url + img_url)

        # HTML Object of individual hemisphere information website 
        img_url = browser.html

        # Parse HTML with Beautiful Soup for each hemisphere website
        hemi_soup = bs(img_url, 'html.parser')

        # Retrieve full image source 
        img_url = hemispheres_main_url + hemi_soup.find('img', class_='wide-image')['src']

        # Append the retreived information into a list of dictionaries 
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
        
    mars_info['hemisphere_image_urls'] = hemisphere_image_urls
        
    return mars_info

    browser.quit()
    
# Find Mars Facts
def scrape_mars_facts():

    # Visit Mars facts url 
    url_facts = 'http://space-facts.com/mars/'

    # Use Panda's `read_html` to parse the url
    tables = pd.read_html(url_facts)

    # Find the mars facts DataFrame
    df = tables[0]
    df.columns = ['Characteristics', 'Value']
    df1 = df.set_index("Characteristics")
    
    mars_facts = df1.to_html(header=True, index=True)

    # Dictionary entry from MARS FACTS
    mars_info['mars_facts'] = mars_facts    

    return mars_info
  
    browser.quit()    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

