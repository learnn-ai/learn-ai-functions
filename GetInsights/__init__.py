import logging

import azure.functions as func
from pprint import pprint
import requests
import json

subscription_key = "bd4280022f694cd4a90e64ee5ebe909b"
endpoint = "https://gene-pool-text-analytics.cognitiveservices.azure.com"

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    keyphrase_url = endpoint + "/text/analytics/v3.0/keyphrases"

    documents = {
        "documents": [
            {"id": "1", "language": "en",
                "text": req.get_json().get("text")}
        ]
    }

    headers = { "Ocp-Apim-Subscription-Key": subscription_key }
    response = requests.post(keyphrase_url, headers=headers, json=documents)
    key_phrases = response.json()
    pprint(key_phrases)

    return func.HttpResponse(body = f'{json.dumps(key_phrases["documents"][0]["keyPhrases"])}', status_code = 200)
