import json
from urllib.request import urlopen, HTTPError
import time

results_list = []
url_list = []
aisle_name = 'Frutas_frescas'
sec = 0

store_dic = {'4273':'32553','1327':'8978','3101':'47859','8782':'34078','11239':'48167','12814':'40050','9969':'33986'}
aisle_id = 'C_134'

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
    #check if "results" is empty, and if its not append in results_list
    x=list(data_json.values())
    if(x.count([])!=len(x)):
        results_list.extend(data_json["results"])
    return data_json["next"]

for branches in store_dic.values():
    url = f'https://cornershopapp.com/api/v3/branches/{branches}/aisles/{aisle_id}/products?sort_asc=0&sort_by=popularity'
    url_list.append(url)

for url in url_list:

    next_url = json_next_list(url)
    while next_url != None:
        next_url = json_next_list(next_url)

fileName = f'aisle_{aisle_id}_{aisle_name}'
with open(f'{fileName}.json', 'w') as fp:
    json.dump(results_list, fp, indent=4)
results_list.clear()


