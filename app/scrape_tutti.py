'''
Tutti.ch does not provide functionality to sort your search based on ZIP of the ad, that can be important for heavy things.
This simple script searches through tutti given your parameters + ZIP, and returns links of interesting ad, can be with description
'''

from bs4 import BeautifulSoup
import requests
from pathlib import Path
from time import sleep
import pandas as pd
import argparse
import re
import logging
from tabulate import tabulate
from datetime import datetime
import math
import sys
from selenium import webdriver

#option = webdriver.ChromeOptions()
#option.add_argument(' — incognito')
#driver = webdriver.Chrome(chrome_options=option)

logging.basicConfig(filename='tutti.log', level=logging.INFO)
logging.getLogger().setLevel(logging.INFO)
logging.info('Starting')


def main(zip,kanton=None,price_min=None, price_max=None,searching_for=None, in_app=False):
    '''
    Start point
    :param zip: your zip, mandatory
    :param kanton: your kanton, optional
    :param price_min: optional
    :param price_max: optional
    :param searching_for: optional
    :return: print the list of fitting adds
    '''


    ##--------Creating search link
    link_base='https://www.tutti.ch/de/li/'
    if kanton!=None:
        kanton=kanton.translate(str.maketrans({'ü': 'ue', 'ä': 'ae','ö':'oe'})).lower() #remove umlauts and big letters
        link_base+=kanton+'?'
    else:
        link_base+='ganze-schweiz?'
    if price_max!=None:
        if link_base[-1]!='?':
            link_base +='&pe='+str(price_max)
        else:
            link_base += 'pe=' + str(price_max)
    if price_min!=None:
        if link_base[-1] != '?':
            link_base +='&ps='+str(price_min)
        else:
            link_base += 'ps=' + str(price_min)
    if searching_for!=None:
        if link_base[-1] != '?':
            link_base += '&q='+searching_for
        else:
            link_base += 'q=' + searching_for
    zip=zip.replace('*','.')

    logging.info('The search link was created: ' + link_base)

    # get the whole page
    soup = get_page_content(link_base)

    # get only interesting ads over all pages
    final_links, final_ads = get_all_pages(soup, zip, link_base)

    #Save the results

    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%Y%m%d-%H-%M")
    final_links.to_csv(f'your_search_{timestampStr}.csv')

    #Print or return the results
    if in_app:
        return(final_ads)
    else:
        print('YOUR SEARCH')
        print(tabulate(final_links, headers='keys', tablefmt='psql'))

def get_page_content(url):
    '''
    Load the page into memory
    :param url: url with all search limitations
    :return: json with page
    '''
    pathpp = Path(url)
    #driver.get(pathpp)
    if not pathpp.is_file():
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        logging.info(page.status_code)
    else:
        soup = BeautifulSoup(open(url), "html.parser")
    return soup

def get_all_pages(soup, zip, link_base):
    '''
    runs through all pages, the first page does not have any specific number
    :param soup: first page
    :param zip: to forfard to next page searches
    :param link_base: base link to add page number
    :return: list of fitting ads
    '''

    final_links = pd.DataFrame(columns=['link', 'description', 'price'])
    final_ads = []

    final_links, final_ads = get_ads(soup, zip, final_links, final_ads)
    pages_num= soup.find('div',{'class':'_3N3mg'}).get_text()
    pages_num = int(''.join(re.findall('[0-9]', pages_num)))
    pages_num = math.ceil(pages_num/30) #There are 30 ads per page
    for i in range(2,pages_num):
        sleep(0.7)
        next_page_link= link_base.replace('?','?o='+str(i)+'&')
        logging.info('The new search link was created: ' + next_page_link)
        soup = get_page_content(next_page_link)
        final_links, final_ads = get_ads(soup, zip, final_links, final_ads)

    return(final_links, final_ads)

def get_ads(soup,zip_set, final_links, final_ads):
    '''
    Parses the html and gets out ads with particular zip
    :param soup:
    :return:
    '''

    all_ads = soup.find_all('div', {'class': '_1MojO _1ew6U _391iy _8fEqk'})  # Find all locations+zip

    for ad in all_ads:
        zip = ad.find('span',{'class' : '_3f6Er'})
        zip_txt=zip.get_text()
        zip=''.join(re.findall('[0-9]', zip_txt))

        logging.info('Found zip: ' + zip)

        if bool(re.match(zip_set,zip)) and '!' not in zip_txt:
            link='https://www.tutti.ch'+ad.find('a',{'class':'_16dGT'}).get('href')
            content1=ad.find('h4',{'class':'_2SE_L'}).get_text()
            content2=ad.find('p',{'class':'_2c4Jo'}).get_text()
            price=ad.find('div',{'class':'_6HJe5'}).get_text()
            final_links = final_links.append({'link':link, 'description':content1+'\n'+content2, 'price':price}, ignore_index=True)
            ad=str(ad).replace('href="/de/vi','target="_blank" href="https://www.tutti.ch/de/vi')
            final_ads.append(ad)
            logging.info('Fadded: ' + content1)

    return (final_links, final_ads)




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A tutorial of argparse!')
    parser.add_argument("--zip", help="add your zip, can be not full: 805*/805.")
    parser.add_argument("--kanton", default=None, help="Please write kanton with umlauts or ue, ae, oe")
    parser.add_argument("--price_min", default=None, help="just a number")
    parser.add_argument("--price_max", default=None, help="just a number")
    parser.add_argument("--searching_for", default=None, help="one word")
    args = parser.parse_args()


    if args.zip==None:
        main('8057|8037|8051|8050', kanton='zuerich', price_max='5', searching_for='stuhl')  # uncomment in develop
        sys.exit('!!!PLEASE, PROVIDE YOUR ZIP!!!')
    else:
        main(args.zip, args.kanton, args.price_min, args.price_max, args.searching_for)
