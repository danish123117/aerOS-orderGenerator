import requests
import json
def ngsi_create_entity(d,orion,orion_port,context,context_port):#updates latest values
    url = f'http://{orion}:{orion_port}/ngsi-ld/v1/entities/'
    #url = 'http://localhost:1026/ngsi-ld/v1/entityOperations/create'
    headers = {
  'Link': f'<http://{context}:{context_port}/ngsi-context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"',
  'Content-Type': 'application/json'
}
    payload = json.dumps(d)
    response = requests.request("POST", url, headers=headers, data=payload)
    return response

def ngsi_setup_DOG(orion,orion_port,context,context_port):
    data = {
    "id": "urn:ngsi-ld:extOrder:order001",
    "type": "extOrder",
    "timestamp": "2024-01-16T17:50:07.5870Z",
    "orderId": "test",
    "orderQuantity":0 } 

    payload = data
    resp= ngsi_create_entity(payload,orion,orion_port,context,context_port)
    return resp

def ngsi_subscribe_DOG(orion, orion_port, context, context_port, notify_endpoint):
    url = f'http://{orion}:{orion_port}/ngsi-ld/v1/subscriptions/'

    headers = {
          'Content-Type': 'application/ld+json'  }

    subscription = {
        "description": "Notify me of all changes to extOrder",
        "type": "Subscription",
        "entities": [
            {
                "id": "urn:ngsi-ld:extOrder:order001",
                "type": "extOrder"
            }
        ],
          "watchedAttributes": ["orderId", "orderQuantity", "timestamp" ],
        "notification": {
            "attributes": ["orderId", "orderQuantity", "timestamp"],  # Ensures all attributes are included
            "format": "normalized",
            "endpoint": {
                "uri": notify_endpoint,
                "accept": "application/json"
            }
        },
        "@context": f"http://{context}:{context_port}/ngsi-context.jsonld"
    }

    response = requests.post(url, headers=headers, data=json.dumps(subscription))
    return response


#Done
payload = json.dumps({
  "description": "Notify me of all product price changes",
  "type": "Subscription",
  "entities": [
    {
      "type": "Product"
    }
  ],
  "watchedAttributes": [
    "price"
  ],
  "notification": {
    "format": "keyValues",
    "endpoint": {
      "uri": "http://tutorial:3000/subscription/price-change",
      "accept": "application/json"
    }
  },
  "@context": "http://context-provider:3000/data-models/ngsi-context.jsonld"
})
headers = {
  'content-type': 'application/ld+json'
}