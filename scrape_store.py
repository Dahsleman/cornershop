import json
from urllib.request import urlopen, HTTPError
import time
import urllib

results_list = []
json_view_list=[]
aisles_list=[]
url_list=[]
sec = 0

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

#return the aisles_id of all departments of the store. I use this to create the url api thats gona be scraped. 
def aisles(url):
    response = urlopen(url)
    data_json = json.loads(response.read())
    json_view_list.extend(data_json['departments'])
    for r in json_view_list:
        aisle = r['aisles']
        for a in aisle:
            id = a['id']
            aisles_list.append(id)
    return aisles_list

"""START"""
store = '1327'
branche = '8978'
url_branche = f'https://cornershopapp.com/api/v3/branches/{branche}?with_suspended_slots&app_capabilities=DATA_REQUEST_BASIC_FORM,CUSTOMER_WITH_SENDBIRD_CHAT,DATA_REQUEST_PRESCRIPTION,LOYALTY_PROVIDERS_WITH_2FA,IMAGE_SUPPORT_CHAT,TC_BLOCKER,CUSTOMER_SMART_SERVICE_FEE,STORE_WITHOUT_PRICING_NOTES'
aisles_list = aisles(url_branche)


for aisle in aisles_list:
    #url api thats gone be scraped
    url_aisle = f'https://cornershopapp.com/api/v3/branches/{branche}/aisles/{aisle}/products?sort_asc=0&sort_by=popularity'
    url_list.append(url_aisle)

print(f'urls to scrape:{len(url_list)}')

# this for loop scrape all the products of a given aisle
i = 0 
for url in url_list:
    print(f'starting:{i+1}-aisle:{aisles_list[i]}')
    next_url = json_next_list(url)
    while next_url != None:
        next_url = json_next_list(next_url)
    print(f'{i+1}:done')
    i +=1

# in the end the program create the file.
fileName = f'store_{store}'
with open(f'{fileName}.json', 'w') as fp:
    json.dump(results_list, fp, indent=4)