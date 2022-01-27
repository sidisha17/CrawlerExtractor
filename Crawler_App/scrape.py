from selenium import webdriver
from shutil import which
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from django.contrib import messages
from webdriver_manager.chrome import ChromeDriverManager

def scrape(sku):
    """Scrapes Amazon and gets the details of entered product"""
    chrome_options=Options()
    chrome_options.add_argument("--headless")
    chrome_path=which('chromedriver')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.get(f"https://www.amazon.in/dp/{sku}/")
    
    try:
        title = driver.find_element_by_xpath('//*[@id="productTitle"]').text
    except:
        title = 'No Title Available'

    try:
        price = driver.find_element_by_xpath('//*[@id="priceblock_ourprice"]').text
    except:
        try:
            price = driver.find_element_by_xpath('//*[@id="priceblock_dealprice"]').text
        except:
            try:
                price = driver.find_element_by_xpath('//*[@id="priceblock_saleprice"]').text
            except:                    
                try:
                    price = driver.find_element_by_xpath('//*[@id="soldByThirdParty"]/span').text
                except:
                    try:
                        price = driver.find_element_by_xpath('//*[@id="kindle-price"]').text
                    except:
                        price = 'No Price Available'
                        
    try:
        description = driver.find_element_by_xpath('//*[@id="productDescription"]/p[1]').text
    except:
        description = 'No Description Available'

    try:
        overall = driver.find_element_by_xpath('//*[@id="reviewsMedley"]/div/div[1]/div[2]/div[2]/span').text
    except:
        overall = 'No Ratings'

    try:
        five=driver.find_element_by_xpath('//*[@id="histogramTable"]/tbody/tr[1]/td[3]/span[2]/a').text    
    except:
        five = '0%'
        
    try:
        four=driver.find_element_by_xpath('//*[@id="histogramTable"]/tbody/tr[2]/td[3]/span[2]/a').text
    except:
        four = '0%'
        
    try:
        three=driver.find_element_by_xpath('//*[@id="histogramTable"]/tbody/tr[3]/td[3]/span[2]/a').text
    except:
        three = '0%'
        
    try:
        two=driver.find_element_by_xpath('//*[@id="histogramTable"]/tbody/tr[4]/td[3]/span[2]/a').text
    except:
        two = '0%'
        
    try:
        one = driver.find_element_by_xpath('//*[@id="histogramTable"]/tbody/tr[5]/td[3]/span[2]/a').text
    except:
        one = '0%'
  
    ratings_map = {'overall': overall, '5star': five, '4star': four, '3star': three, '2star':two, '1star':one}
    output = {'title': title,'price':price, 'desc':description, 'ratings_map':ratings_map}
    driver.close()
    return output

