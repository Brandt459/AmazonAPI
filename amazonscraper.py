import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import operator

driver = webdriver.Chrome()


def get_data(keywords):
    driver.get('https://www.amazon.com')
    search = driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]')
    search.send_keys(keywords)
    search.send_keys(Keys.RETURN)

    try:
        results = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 's-main-slot')))
        print(results)
        listings = results.find_elements_by_css_selector(
            'div[data-component-type=s-search-result]')
        print(listings)
        data = []
        for listing in listings:
            try:
                url = listing.find_element_by_class_name(
                    'a-link-normal').get_attribute('href')
            except:
                continue
            try:
                image = listing.find_element_by_tag_name(
                    'img').get_attribute('src')
            except:
                continue
            try:
                title = listing.find_element_by_class_name(
                    'a-size-medium').text.strip()
            except:
                continue
            a = 0
            for word in search_list:
                if word.lower() not in title.lower():
                    a = 1
            if a == 1:
                continue
            try:
                dollars = listing.find_element_by_class_name(
                    'a-price-whole').text.strip()
                dollars = dollars.replace(',', '')
            except:
                continue
            try:
                cents = listing.find_element_by_class_name(
                    'a-price-fraction').text.strip()
            except:
                continue
            price = [dollars, cents]
            price = '.'.join(price)
            current_data = {'title': title,
                            'price': price,
                            'image': image,
                            'url': url
                            }
            data.append(current_data)
    except:
        return ''
    return data


def write_csv(data):
    with open('amazon.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        row = [data['title'], data['price'],
               data['image'], data['url']]
        writer.writerow(row)


def scraper(keywords):
    with open('amazon.csv', 'w', encoding='utf-8') as csv1:
        csv1.truncate()
    global search_list
    search_list = keywords.split(' ')
    if len(search_list) > 1:
        search_list = [word for word in search_list]
    if type(search_list) == str:
        search_list = [search_list]
    data = get_data(keywords)
    for line in data:
        write_csv(line)
    sort = None
    with open('amazon.csv', 'r', encoding='utf-8') as csv1:
        reader = csv.reader(csv1)
        unsorted = []
        for row in reader:
            unsorted.append(row)
        for row in unsorted:
            row[1] = float(row[1])
        sort = sorted(unsorted, key=operator.itemgetter(1))
    with open('amazon.csv', 'w', newline='', encoding='utf-8') as csv1:
        writer = csv.writer(csv1)
        for row in sort:
            writer.writerow(row)
    new_data = []
    with open('amazon.csv', 'r', encoding='utf-8') as csv1:
        reader = csv.reader(csv1)
        reader = list(reader)
        new_data.append(reader[:5])
    new_data_dict = []
    for data in new_data:
        for line in data:
            new_data_dict.append(
                {'title': line[0], 'price': line[1], 'image': line[2], 'url': line[3]})
    return new_data_dict
