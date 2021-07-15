import beeline
import json
import os
import requests
import urllib.parse

from beeline.middleware.awslambda import beeline_wrapper

FOGG_API_KEY = os.getenv('FOGG_API_KEY')
BASE_URL = 'https://api.harvardartmuseums.org'

beeline.init(writekey=os.getenv('HONEYCOMB_API_KEY'), dataset='color-app', service_name='color-lambda', debug=True)

@beeline_wrapper
def get_artwork_by_color(event, context):
    print('event', event)

    url_encoded_color = event['queryStringParameters']['color']
    hex_color = urllib.parse.unquote(url_encoded_color)
    print('url color', url_encoded_color)

    # only retrieve objects with image urls, get first 10 at random
    url = f'{BASE_URL}/object?apikey={FOGG_API_KEY}&color={url_encoded_color}&sort=random&hasimage=1&q=imagepermissionlevel:0'
    print('url', url)

    with beeline.tracer('fogg_api_call'):
        res = requests.get(url)

        print('res', res.status_code)
        body = res.json()
        print(body)

        num_results = (len(body['records']))
        beeline.add_context({'hex_color': hex_color, 'num_results': num_results})
        return {
            'statusCode': 200,
            'body': json.dumps({'records': body['records']})
        }
