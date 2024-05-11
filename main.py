from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

URL = "https://appbrewery.github.io/Zillow-Clone/"
GOOGLE_FORM = "https://forms.gle/qvE9kPNKjgTtAeHN6"

response = requests.get(URL)
response_data = response.text
soup = BeautifulSoup(response_data, "html.parser")
# Get the prices of the houses below $3000
house_price = soup.find_all(name="span", class_="PropertyCardWrapper__StyledPriceLine")
price_list = [prices.text.split("+")[0].split("/")[0] for prices in house_price]
# Get the addresses of the houses
house_address = soup.find_all(name="a" ,class_="StyledPropertyCardDataArea-anchor" )
address_list  = [address.text.strip() for address in house_address]
# Get the links 
house_links = soup.find_all(name="a" ,class_="StyledPropertyCardDataArea-anchor" )
link_list =  [link.get("href") for link in house_links]

### Using selenium to fill in a google form with the above details

#Get selenium to open the google form
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get(GOOGLE_FORM)
driver.maximize_window()

# Loop through the lists and fill each item on the list to the google form
length  = 0
for n in range(len(price_list)):
    length += 1
    address_field = driver.find_elements(By.XPATH, value='//input[@class="whsOnd zHQkBf"]')[0]
    address_field.send_keys(address_list[n])
    price_field = driver.find_elements(By.XPATH, value='//input[@class="whsOnd zHQkBf"]')[1]
    price_field.send_keys(price_list[n])
    link_field = driver.find_elements(By.XPATH, value='//input[@class="whsOnd zHQkBf"]')[2]
    link_field.send_keys(link_list[n])
    submit_button = driver.find_element(By.XPATH , value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div').click()
    if length < len(price_list):
        another_response_button = driver.find_element(By.XPATH, value='/html/body/div[1]/div[2]/div[1]/div/div[4]/a').click() 