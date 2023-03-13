import json
from urllib.request import urlopen, HTTPError
import time

results_list = []
url_aisles_list = []
aisles_list = []
url_list = []
department_name = 'Frutas_Verduras'
sec = 0

store_dic = {'4273':'32553','1327':'8978','3101':'47859','8782':'34078','11239':'48167','12814':'40050','9969':'33986'}

# store_dic = {'4273':'32553','1327':'8978'}
department_id = 'C_538'

def json_next_list(url):
    try:
        time.sleep(sec)
        response = urlopen(url)
    except HTTPError as e:
        retry_after = e.headers.get('Retry-After')
        print(f'need to wait:{retry_after}s')
        time.sleep(int(retry_after))
        response = urlopen(url)
        
    data_json = json.loads(response.read())
    results_list.extend(data_json["results"])
    return data_json["next"]

def json_aisles_list(url):
    try:
        time.sleep(sec)
        response = urlopen(url)
    except HTTPError as e:
        retry_after = e.headers.get('Retry-After')
        print(f'need to wait:{retry_after}s')
        time.sleep(int(retry_after))
        response = urlopen(url)
    data_json = json.loads(response.read())
    aisles_list.clear()
    aisles_list.extend(data_json["aisles"])
    return 

for branches in store_dic.values():
    url = f'https://cornershopapp.com/api/v3/branches/{branches}/departments/{department_id}?products_sort_asc=0&products_sort_by=popularity'
    json_aisles_list(url)
    for aisle in aisles_list:
        url_aisle = f'https://cornershopapp.com/api/v3/branches/{branches}/aisles/{aisle["id"]}/products?sort_asc=0&sort_by=popularity'
        url_aisles_list.append(url_aisle)

print(f'urls to scrape:{len(url_aisles_list)}')

# this for loop scrape all the products of a given aisle

for url in url_aisles_list:
    next_url = json_next_list(url)
    while next_url != None:
        next_url = json_next_list(next_url)

# print(json.dumps(results_list, indent=4)) 

fileName = f'department_{department_id}_{department_name}'
with open(f'{fileName}.json', 'w') as fp:
    json.dump(results_list, fp, indent=4)
results_list.clear()




