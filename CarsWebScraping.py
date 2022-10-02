from bs4 import BeautifulSoup
import requests
import csv

url = 'https://www.cars.com/shopping/results/?stock_type=all&makes%5B%5D=bmw&models%5B%5D=&list_price_max=&maximum_distance=20&zip='
req = requests.get(url).text

soup = BeautifulSoup(req, 'lxml')
# print(soup.prettify())

vehicle_cards = soup.find_all('div', {'class':'vehicle-card-main js-gallery-click-card'})
# print(len(vehicle_cards)) 
# for each in vehicle_cards:
# print(vehicle_cards[0].prettify())
# print()
# print('-----'*40)
# vehicle = vehicle_cards[0]
# print(vehicle.prettify())

csv_file = open('Cars Web Scraping22.csv', 'w') 
csv_writer = csv.writer(csv_file, dialect='excel')
csv_writer.writerow(['NAME', 'RATINGS', 'REVIEWS', 'DEALER', 'PRICE'])


count = 0

for i in range(2):
    for vehicle in vehicle_cards:
        count += 1
        print(count)
        try:
            car_name = vehicle.find('a', {'class':'vehicle-card-link js-gallery-click-link'}).h2.text
        except :
            car_name = 'None'
        print('Car Name: ', car_name)
        # print()
        try:
            rating = vehicle.find('div', {'class':'sds-rating'}).span.text
        except :
            rating = 'None'
        print('Ratings: ', rating)
        # print()
        try:
            reviews = (vehicle.find('span', {'class':'sds-rating__link sds-button-link'}).get_text())[1:-9]    # [1:-9] used to remove parathises and reviews from string 
        except:
            reviews = 'None'
        print('Reviews: ', reviews)
        # print()
        try:
            car_dealer = (vehicle.find('div', class_='dealer-name').get_text()).strip()
        except :
            car_dealer = 'None'
        print('Dealer: ', car_dealer)
        # print()
        try:
            car_price = vehicle.find('span', class_='primary-price').get_text()
        except :
            car_price = 'None'
        print('Price: ', car_price)
        # print()
        
        print('-'*30)

        csv_writer.writerow([car_name, rating, reviews, car_dealer, car_price])


    next = soup.find('div', class_='sds-pagination__controls')
    # next_page = (next.find_all('a')[-1])['href']
    next_page = next.find('a', {'id':'next_paginate'})['href']
    next_page_url = 'https://www.cars.com' + next_page
    # print(next_page_url)


    req = requests.get(next_page_url).text
    soup = BeautifulSoup(req, 'lxml')
    vehicle_cards = soup.find_all('div', {'class':'vehicle-card-main js-gallery-click-card'})

csv_file.close()