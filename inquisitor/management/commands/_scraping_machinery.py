from bs4 import BeautifulSoup
import requests

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



