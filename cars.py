import requests
from bs4 import BeautifulSoup
import csv
import time

def scrape_otomoto(brand, page_url):
    try:
        # Send a GET request to the page
        response = requests.get(page_url)
        # Check if the response was successful
        if response.status_code != 200:
            print(f"Failed to retrieve data from {page_url}")
            return []

        # Parse the content of the page with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the listings on the page using the article tag and class name provided
        listings = soup.find_all('article', class_='ooa-1t80gpj ev7e6t818')

        # Create a list to hold our data
        cars_data = []

        for listing in listings:
            try:
                # Extract the necessary information
                name = listing.find('h1', class_='ev7e6t89 ooa-1xvnx1e er34gjf0').get_text(strip=True)
                price = listing.find('h3', class_='ev7e6t82 ooa-bz4efo er34gjf0').get_text(strip=True).replace(' ', '') + ' PLN'
                km = listing.find('dd', {"data-parameter": "mileage"}).get_text(strip=True).replace(' km', '').replace(' ', '')
                fuel_type = listing.find('dd', {"data-parameter": "fuel_type"}).get_text(strip=True)
                gear_type = listing.find('dd', {"data-parameter": "gearbox"}).get_text(strip=True)
                year = listing.find('dd', {"data-parameter": "year"}).get_text(strip=True).strip()

                # Add the car data to our list
                cars_data.append([brand, name, price, km, fuel_type, gear_type, year])
            except AttributeError:
                # If one of the fields is missing, skip this listing or handle it accordingly
                continue

        return cars_data
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return []

# List of car brands to scrape
car_brands = [
    'bmw', 'toyota', 'skoda', 'peugeot', 'renault',
    'ford', 'mercedes-benz', 'volkswagen', 'hyundai',
    'mini', 'volvo', 'seat', 'mazda'
]

# The CSV file we will write to
csv_file = 'otomoto_all_brands_cars.csv'

# Open the CSV file
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the header to the CSV file
    writer.writerow(['Brand', 'Name', 'Price', 'Km', 'Fuel Type', 'Gear Type', 'Year of Production'])

    # Loop through each car brand
    for brand in car_brands:
        # Loop through the specified range of pages for each brand
        for page in range(2, 551):
            print(f"Scraping page {page} for {brand}")
            page_url = f'https://www.otomoto.pl/osobowe/{brand}?page={page}'
            # Call the scrape function
            data = scrape_otomoto(brand, page_url)
          
            if(len(data) == 0):
                break   # Break the loop if no data was returned
            # Write the data to the CSV file
            writer.writerows(data)
            # Delay to prevent overloading the server
            time.sleep(1)

print(f'Data scraped and saved to {csv_file}')



###