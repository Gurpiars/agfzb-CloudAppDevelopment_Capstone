import requests
import json
import pdb
from .models import CarDealer ,DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 \
    import Features, SentimentOptions

API="2xlX9h82snRK9uMcCFCKzEEZXpjXzFJHzS4Bep7Q_8G8"
URL="https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/5f57816d-c113-4e84-9397-1193f87336c8"

def get_request(url, **kwargs):
    print(kwargs)
    print('GET from  {}'.format(url))
    try:
        response= requests.get(url , params=kwargs, headers={'Content-Type':'application/json'},
                                auth=HTTPBasicAuth('apikey', API))
    except Exception as e:
        print(f'Network exception occurred: {e}')
    status_code = response.status_code
    print('with status {}'.format(status_code))
    json_data=json.loads(response.text)
    return json_data


def get_dealers_from_cf(url, **kwargs):
    results=[]
    json_result = get_request(url)
    if json_result:
        dealers= json_result[0:10]
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
        # Get all review data from the response
        reviews = json_result
        # For every review in the response
        for review in reviews:
            # Create a DealerReview object from the data
            # These values must be present
            review_content = review["review"]
            id = review["_id"]
            name = review["name"]
            purchase = review["purchase"]
            dealership = review["dealership"]
            sentiment=analyze_review_sentiments(review['review'])

            try:
                # These values may be missing
                car_make = review["car_make"]
                car_model = review["car_model"]
                car_year = review["car_year"]
                purchase_date = review["purchase_date"]

                # Creating a review object
                review_obj = DealerReview(dealership=dealership, id=id, name=name, 
                                          purchase=purchase, review=review_content, car_make=car_make, 
                                          car_model=car_model, car_year=car_year, purchase_date=purchase_date,
                                          sentiment=sentiment
                                          )

            except KeyError:
                print("Something is missing from this review. Using default values.")
                # Creating a review object with some default values
                review_obj = DealerReview(
                    dealership=dealership, id=id, name=name, purchase=purchase, review=review_content,
                    sentiment="Unknown", purchase_date="Unknown", car_make="Unknown", car_model="Unknown", car_year="Unknown")
            # Saving the review object to the list of results
            results.append(review_obj)

    return results
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(review):
    authenticator = IAMAuthenticator(API)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2023-12-02',
    authenticator=authenticator)
    try:
        response = natural_language_understanding.analyze(
        text=review,
        features=Features(sentiment=SentimentOptions(targets=[review]))
        ).get_result()
        label=json.dumps(response, indent=2) 
        label = response['sentiment']['document']['label'] 
        print (label)
        return (label)
    except Exception as e:
        print(f"An error occurred in sentiment analysis: {e}")
        return None

        
def post_request(url, json_payload, **kwargs):
    try:
        response= requests.post(url, params=kwargs, json=json_payload)
        response.raise_for_status()
        return response.json
    except requests.RequestException as e:
        print(f"Error making POST request: {e}")
        return None
        






