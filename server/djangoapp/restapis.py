import requests
import json
import pdb
from .models import CarDealer ,DealerReview
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
def get_dealer_reviews_from_cf(url, dealerid):
    results=[]
    json_result=get_request(url, id=dealerid)
    if json_result:
        try:
            reviews = json_result  # Or adjust based on your actual JSON structure
            for review in reviews:
                review_doc= review
                review_obj = DealerReview(
                    dealership=review_doc['dealership'],
                    name=review_doc['name'],
                    review=review_doc['review'],
                    car_model=review_doc['car_model'],
                    car_make=review_doc['car_make'],
                    car_year=review_doc['car_year'],
                    purchase=review_doc['purchase'],
                    id=review_doc['id'],
                    purchase_date=review_doc['purchase_date'],
                )
                results.append(review_obj)
        except Exception as e:
            print('something went wrong in restapis try block:', e)
    else:
        print('something went wrong in restapis')

    return results
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



