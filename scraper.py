import time
import csv
from selenium import webdriver
from bs4 import BeautifulSoup
import requests

start_url = "https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"
browser = webdriver.Chrome("\chromedriver")
browser.get(start_url)
time.sleep(10)
headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date", "hyperlink", "planet_type", "mass", "planet_radius", "orbital_radius", "eccentricity", "orbital_period", "discover_date", "detection_method"]
planet_data = []
new_planet_data = []

def scrape():
    for i in range(0,201):
        while True:
            time.sleep(2)
            soup = BeautifulSoup(browser.page_source, "html.parser")
            current_page_num = int(soup.find_all("input", attrs = {"class", "page_num"})[0].get("value"))
            if current_page_num < i:
                browser.find_element_by_xpath('//*[@id="primary_column"]/div[1]/div[2]/div[1]/div/nav/span[2]/a').click()
            elif current_page_num>i:
                browser.find_element_by_xpath('//*[@id="primary_column"]/div[1]/div[2]/div[1]/div/nav/span[1]/a').click()
            else:
                break
        for ul_tag in soup.find_all("ul", attrs = {"class", "exoplanet"}):
            li_tags = ul_tag.find_all("li")
            temp_list = []
            for index, li_tags in enumerate(li_tags):
                if index == 0:
                    temp_list.append(li_tags.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tags.contents[0])
                    except:
                        temp_list.append("")
            hyperlink_li_tags = li_tags[0]
            temp_list.append("https://expoplanets.nasa.gov"+ hyperlink_li_tags.find_all("a", href = True)[0]["href"]) 
            planet_data.append(temp_list)
        browser.find_element_by_xpath('//*[@id="primary_column"]/div[1]/div[2]/div[1]/div/nav/span[2]/a').click()
        print(f"{i}page 1 done")

def scrapemoredata(hyperlink):
    try:
        
    with open("scraper_2.csv", "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(planet_data)

scrape()