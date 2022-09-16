#Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymongo
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
  
  executable_path = {'executable_path': ChromeDriverManager().install()}
  return Browser("chrome", **executable_path, headless=False)


def scrape_all():

  browser = init_browser()

  mars_data = {}

  #Nasa Mars News
  url = 'https://redplanetscience.com'
  browser.visit(url)
  response = requests.get(url)
  html = browser.html
  soup = BeautifulSoup(html, 'html.parser')

  mars_news=soup.find("div", class_="list_text")
  title = mars_news.find('div', class_='content_title').text
  paragraph = mars_news.find('div', class_='article_teaser_body').text

  #mongoDB
  mars_data['title'] = title
  mars_data['paragraph'] = paragraph


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
  mars_data['featured_image'] = image

  #Mars Facts
  url = 'https://galaxyfacts-mars.com/'
  browser.visit(url)
  mars_facts_df = pd.read_html(url, header=[0])
  mars_facts_df = mars_facts_df[0]
  mars_facts_df.columns = ['Metrics', 'Mars', 'Earth']
  mars_facts_df.drop("Earth",axis=1,inplace=True)
  html_table = mars_facts_df.to_html()
  html_table.replace('\n','')
  mars_facts_df.to_html('table.html')
    
  #mongoDB
  mars_data['mars_facts'] = html_table

  #Mars Hemispheres
  url = 'https://marshemispheres.com/'
  browser.visit(url)
  html = browser.html
  hemisphere_soup = BeautifulSoup(html, "html.parser")
  soup1 = BeautifulSoup(html, "html.parser")
  results = soup1.find_all("div", class_="item")

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
    mars_hemisphere={}
    
    
    images.append({"title": title, "image url":image_url})
    
    browser.back()
    
  #mongoDB
  mars_data['mars_hemispheres'] = images

  browser.quit()

  return mars_data
mars_data = scrape_all()

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

db = client.mars
collection = db.mars

collection.update_one({}, {"$set": mars_data}, upsert=True)



  




