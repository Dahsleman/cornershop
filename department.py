import json
from urllib.request import urlopen
import time

results_list = []
sec = 0.5
store = '4273'

#parse the url api of the aisle and return the url api of the next pages of the products (lazyload)
def json_next(url):
    try:
        time.sleep(sec)
        response = urlopen(url)
    except:
        time.sleep(sec)
        response = urlopen(url)
    data_json = json.loads(response.read())
    return data_json["next"]

#append the products of the aisle in the results_list
def json_list(url):
    try:
        time.sleep(sec)
        response = urlopen(url)
    except:
        time.sleep(sec)
        response = urlopen(url)
    data_json = json.loads(response.read())
    results_list.extend(data_json["results"])
    return results_list

json_view_list=[]
aisles_list=[]
url_list=[]

#return the aisles_id of all departments of the store. I use this to create the url api thats gona be scraped. 
def aisles(url):
    try:
        response = urlopen(url)
    except:
        time.sleep(sec)
        response = urlopen(url)
    data_json = json.loads(response.read())
    json_view_list.extend(data_json['departments'])
    for r in json_view_list:
        aisle = r['aisles']
        for a in aisle:
            id = a['id']
            aisles_list.append(id)
    return aisles_list

branche = '32553'
url_store = f'https://cornershopapp.com/api/v3/branches/{branche}?with_suspended_slots&app_capabilities=DATA_REQUEST_BASIC_FORM,CUSTOMER_WITH_SENDBIRD_CHAT,DATA_REQUEST_PRESCRIPTION,LOYALTY_PROVIDERS_WITH_2FA,IMAGE_SUPPORT_CHAT,TC_BLOCKER,CUSTOMER_SMART_SERVICE_FEE,STORE_WITHOUT_PRICING_NOTES'
aisles_list = aisles(url_store)

for aisle in aisles_list:
    #url api thats gone be scraped
    url_aisle = f'https://cornershopapp.com/api/v3/branches/{branche}/aisles/{aisle}/products?sort_asc=0&sort_by=popularity'
    url_list.append(url_aisle)

# this for loop scrape all the products of a given aisle 
for url in url_list:
    while json_next(url) != None:
        json_list(url)
        url = json_next(url)

# in the end the program create the file.
fileName = f'store_{store}'
with open(f'{fileName}.json', 'w') as fp:
    json.dump(results_list, fp, indent=4)


