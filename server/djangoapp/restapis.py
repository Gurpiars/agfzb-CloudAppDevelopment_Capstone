import requests
import json
import pdb
from .models import CarDealer
from requests.auth import HTTPBasicAuth

def get_request(url, **kwargs):
    print(kwargs)
    print('GET from  {}'.format(url))
    try:
        response= requests.get(url , headers={'Content-Type':'application/json'},
                                    params=kwargs)
    except Exception as e:
        print(f'Network exception occurred: {e}')
    status_code = response.status_code
    print('with status {}'.format(status_code))
    json_data=json.loads(response.text)
    print (json_data)
    return json_data


def get_dealers_from_cf(url, **kwargs):
    results=[]
    json_result = get_request(url)
    if json_result:
        dealers= json_result[1:10]
        for dealer in dealers:
            dealer_doc = dealer
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],short_name=dealer_doc["short_name"], st= dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results
# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function

# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



