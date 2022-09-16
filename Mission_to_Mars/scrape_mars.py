# add dependencies
from bs4 import BeautifulSoup
import pandas as pd
import time
from splinter import Browser
import requests
from selenium import webdriver
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import html5lib


def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser

def scrape():
    browser = init_browser()

    nasa_mars_data = {}

    #Nasa Mars News
    url = 'https://redplanetscience.com'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find_all('div', class_='content_title')[0].text
    paragraph = soup.find_all('div', class_='article_teaser_body')[0].text

    #mongoDB
    nasa_mars_data['title'] = title
    nasa_mars_data['paragraph'] = paragraph


    #JPL Mars Space Images-Featured Image
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)
    html=browser.html
    soup = BeautifulSoup(html, 'html.parser')
    browser.find_by_css("a.showimg").first.click()
    html=browser.html
    soup=BeautifulSoup(html, 'html.parser')
    image = browser.find_by_css("img.fancybox-image")["src"]
    
    #mongoDB
    nasa_mars_data['featured_image'] = image

    #Mars Facts
    url = 'https://galaxyfacts-mars.com/'
    browser.visit(url)
    mars_facts_df = pd.read_html(url, header=[0])
    mars_facts_df = mars_facts_df[0]
    mars_facts_df.columns = ['Metrics', 'Mars', 'Earth']
    mars_facts_df.drop("Earth",axis=1,inplace=True)
    html_table = mars_facts_df.to_html()
    html_table.replace('\n','')
    
    #mongoDB
    nasa_mars_data['mars_facts'] = html_table

    #Mars Hemispheres
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    results = soup.find_all("div", class_="item")

    images = []

    for result in results:
    
        title = result.find("h3").text
        link = result.find("a", class_="itemLink")["href"]
        title_link = url + link
        browser.visit(title_link)
        html1 = browser.html
        sp = BeautifulSoup(html1, "lxml")
        image = sp.find("img", class_="wide-image")["src"]
        image_url = url + image
    
    
        images.append({"title": title, "image url":image_url})
    
        browser.back()
    
    #mongoDB
    nasa_mars_data["mars_hemisphere"] = images

    browser.quit()

    return nasa_mars_data



