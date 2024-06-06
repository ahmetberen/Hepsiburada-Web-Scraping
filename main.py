# Importing necessary libraries
import requests  # Library for making HTTP requests
from bs4 import BeautifulSoup  # Library for parsing HTML content
import pandas as pd  # Library for data manipulation

# Lists to store the extracted data
product_names = []  # To store product names
product_prices = []  # To store product prices
product_link = []   # To store product links

header = {"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0"}
# URL of the Hepsiburada website to scrape
url = 'https://www.hepsiburada.com/bellek-ramler-c-47?filtreler=ramkapasitesi:16€20GB;ramhizi:3200€20MHz;kullanimtipi:DDR4;uyumlusistemler:PC'

x = int(input("Type in how many pages you want to scrap: (In this case it can't be over 6 since the max amount of pages in there is 6)"))

# Making sure the program won't overhead
if x > 6:
    print("Cannot print more than six, assigning the max page.")
    x = 6

for i in range(x):
    if i != 0:
        # Sending a request to the Hepsiburada website
        response = requests.get(url + '&sayfa=' + str(i+1), headers=header)
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

# Saving the extracted data to a CSV file
df.to_csv('hepsiburada_data.csv',index = True)

