from requests.models import Response
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
        beeline.add_context({'hex_color': hex_color})
        try:
            res = requests.get(url, timeout=5)
            res.raise_for_status()
            print('res non-error', res.status_code)

            body = res.json()
            if res.status_code == 200:
                beeline.add_context({'num_results': len(body['records'])})
                return {
                    'statusCode': res.status_code,
                    'body': json.dumps({'records': body['records']})
                }

            return {'statusCode': res.status_code}

        except requests.exceptions.RequestException as e:
            print('res error', res.status_code, e)

            if res.status_code < 500:
                return {
                    'statusCode': res.status_code,
                    'body': e.args[0] # Need to return body to avoid throwing a function output error (automatic 502)
                }
            raise
