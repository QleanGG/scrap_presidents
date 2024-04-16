import requests
from bs4 import BeautifulSoup
import csv

def read_countries_from_csv(file_path):
    countries = []
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            countries.append(row[1])  
    return countries

csv_file_path = 'country.csv'  
countries_list = read_countries_from_csv(csv_file_path)



def find_president(country):
    url = f'https://en.wikipedia.org/wiki/{country}'
    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Look for the anchor tag with title 'President of Iran'
        president_link = soup.find('a', title=f'President of {country}')
        if president_link:
            # Navigate to the parent and find the nearest td sibling
            th = president_link.find_parent('th')
            try:
                president = th.find_next_sibling('td').findChild('a').text
            except Exception as e:
                return e
        else:
            president = "Information not found"  # If the specific format is not found
        
        return president
    else:
        return f"Failed to retrieve data. Status code: {response.status_code}"
    
def find_all_pres(countries):
    for country in countries:
        print(find_president(country))

if __name__ == '__main__':
    find_all_pres(countries_list)