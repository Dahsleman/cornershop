import json
from urllib.request import urlopen, HTTPError
import time

results_list = []
url_list = []
product_name = 'Banana_Prata'
sec = 0

store_dic = {'4273':'32553','1327':'8978','3101':'47859','8782':'34078','11239':'48167','12814':'40050','9969':'33986'}
product_id = '1258169'

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
    results_list.extend(data_json)
    return data_json

for branches in store_dic.values():
    url = f'https://cornershopapp.com/api/v2/branches/{branches}/products/{product_id}'
    url_list.append(url)

for url in url_list:
    json_next_list(url)


# print(json.dumps(results_list, indent=4))

fileName = f'product_{product_id}_{product_name}'
with open(f'{fileName}.json', 'w') as fp:
    json.dump(results_list, fp, indent=4)
results_list.clear()


