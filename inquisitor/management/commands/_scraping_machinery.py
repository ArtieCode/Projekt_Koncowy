from bs4 import BeautifulSoup
import requests
import json
from urllib.parse import urlencode
url_core = "https://archiwumbip.mswia.gov.pl/bip/form/166,Rejestr-przedsiebiorcow-wykonujacych-dzialalnosc-regulowana-w-zakresie-uslug-det.html"



def scrape(starting_counter):
    reached_end = False
    page_counter = starting_counter
    result_list = []


    while not reached_end:

        url_param = f"?page={page_counter}"
        request_url = url_core + url_param

        response = requests.get(request_url)
        page_counter += 1
        if response.status_code != 200:
            return requests.HTTPError

        html = BeautifulSoup(response.content, 'html.parser')
        result_table = html.find(class_='table-listing')
        rows = result_table.find_all('tr')
        if len(rows) == 1:
            reached_end = True
        for row in rows:
            data_list = row.find_all('td')
            row_cleaned = []
            for entry in data_list:
                entry_text = entry.get_text()
                if entry_text == '':
                    entry_text = None
                row_cleaned.append(entry_text)
            result_list.append(row_cleaned)

    result_list.pop(0)
    result_list.pop(len(result_list)-1)

    return result_list



import re
import urllib.parse



def get_single_address(string):
    postcode_pattern = '\d{2}\s*[‒–—―‐-]\s*\d{3}|\d{5}'

    raw_string = string
    if raw_string is None:
        raw_string = ''

    def find_all_postcodes(string):
        return re.findall(postcode_pattern, string)

    postcodes = find_all_postcodes(raw_string)

    number_of_postcodes = len(postcodes)

    if number_of_postcodes == 0:
        return ''
    elif number_of_postcodes == 1:
        address = raw_string
    else:
        return ''

    return address


def scrape_google(string):
    url_core = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?'
    url_settings_and_key = 'inputtype=textquery&fields=formatted_address&key=AIzaSyD-Voj4JLH8i_eQoiV-UhBiMDXsMjM8hfs'

    mydict = {'input': string, 'inputtype': 'textquery',
              'fields': 'formatted_address', 'key': 'AIzaSyD-Voj4JLH8i_eQoiV-UhBiMDXsMjM8hfs'}
    url = url_core + urlencode(mydict)
    print(url)

    response = requests.get(url)
    parsed_response = json.loads(response.content)
    print(parsed_response)
    status = parsed_response['status']
    candidates = parsed_response['candidates']
    if status != "OK":
        print("something went wrong...")
        return None
    result_dict = candidates[0]
    address = result_dict['formatted_address']
    return address





