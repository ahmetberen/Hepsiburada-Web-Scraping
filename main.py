# Importing necessary libraries
import unicodedata
import re
from urllib.parse import unquote
import requests  # Library for making HTTP requests
from bs4 import BeautifulSoup  # Library for parsing HTML content
import pandas as pd  # Library for data manipulation

# Lists to store the extracted data
product_names = []  # To store product names
product_prices = []  # To store product prices
product_link = []   # To store product links

header = {"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0"}
# URL of the Hepsiburada website to scrape
url = 'https://www.hepsiburada.com/ara?q=rtx%204080'

x = int(input("Type in how many pages you want to scrap: "))

# Making sure the program won't overhead

for i in range(x):
    if i != 0:
        # Sending a request to the Hepsiburada website
        response = requests.get(url + '&sayfa=' + str(i+1), headers=header)
        if len(response.history) != 0:
            print("There are no pages after " + str(i-1) + ".")
            print("Scraping " + str(i-1) + " pages.")
            break
    else:
        response = requests.get(url, headers=header)

    # Parsing the HTML content of the webpage
    soup = BeautifulSoup(response.content, 'html.parser')


    # Finding all the containers that hold product information
    product_containers = soup.findAll('li', attrs={'class': 'productListContent-zAP0Y5msy8OHn5z7T_K_'})

    # Extracting data from each product container
    for product in product_containers:
        # Extracting the name of the product
        name = product.find('h3', attrs={'data-test-id': 'product-card-name'}).text.strip()
        product_names.append(name)

        # Extracting the price of the product
        price = product.find('div', attrs={'data-test-id': 'price-current-price'}).text.strip()
        product_prices.append(price)

        # Extracting the link of the product
        link = product.find('a').get('href')
        product_link.append('https://www.hepsiburada.com' + link)

for element in product_prices:
    elementIndex = product_prices.index(element)
    element = element.replace(".", "")
    element = element.replace(",", "")
    element = element.replace(" TL", "")
    product_prices[elementIndex] = element


# Creating a DataFrame to organize the extracted data
data = {
    'Product Name': product_names,
    'Link': product_link,
    'Price': product_prices,
}
df = pd.DataFrame(data)
df.Price = df.Price.astype('float')
df = df.sort_values(by=['Price'], ascending=False)

def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


# Saving the extracted data to a CSV file
clean_url = slugify(url.split("m/")[1])
df.to_csv('hepsiburada_data' + clean_url + '.csv',index = True)

