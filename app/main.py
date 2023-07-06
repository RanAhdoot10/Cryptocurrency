from prometheus_client import start_http_server, Gauge
import requests
import random
import time
import vars

def fetch_top_popular_coins(endpoint):
    payload = {}
    headers = {}
    popular_coins_response = requests.request("GET", endpoint, headers=headers, data=payload)
    popular_coins_json_response = popular_coins_response.json()
    popular_coins_data = popular_coins_json_response["coins"]
    
    for coin in popular_coins_data:
        name = coin['i']
        vars.popular_coins_endpoints.update({f'{vars.COINS_DATA_ENDPOINT}{name}': f'{name}'})

fetch_top_popular_coins(vars.POPULAR_COINS_ENDPOINT)

def create_popular_coin_metric(endpoint, label):
    label = label.replace("-", "_")
    metric_name_hour = 'hour_change_trend_' + label
    metric_name_week = 'week_change_trend_' + label
    gauge_metric_hour = Gauge(metric_name_hour, f'an hour change trend {label}', ['endpoint'])
    gauge_metric_week = Gauge(metric_name_week, f'a week change trend {label}', ['endpoint'])
    vars.popular_coins_metrics[endpoint] = gauge_metric_hour, gauge_metric_week

def fetch_cheapest_coins(endpoint):
    payload = {}
    headers = {}
    cheapest_coins_response = requests.request("GET", endpoint, headers=headers, data=payload)
    cheapest_coins_json_response = cheapest_coins_response.json()
    cheapest_coins_data = cheapest_coins_json_response["coins"]
    
    for coin in cheapest_coins_data:
        name = coin['i']
        price = coin['pu']
        price = format(price, '.8f')
        vars.cheapest5.update({name: price})

    sorted_dict = sorted(vars.cheapest5.items(), key=lambda item: item[1], reverse=False)
    cheapest5_items = sorted_dict[:5]
    cheapest5_dict = dict(cheapest5_items)

    for c, p in cheapest5_dict.items():
        vars.cheapest_coins_endpoints.update({f'{vars.COINS_DATA_ENDPOINT}{c}': f'{c}'})

fetch_cheapest_coins(vars.CHEAPEST_COINS_ENDPOINT)

def create_cheapest_coins_metric(endpoint, label):
    label = label.replace("-", "_")
    metric_name = 'price_tag_' + label
    gauge_metric = Gauge(metric_name, 'price tag coin', ['endpoint'])
    vars.cheapest_coins_metrics[endpoint] = gauge_metric

def fetch_data():
    # Fetching data for the popular coins
    for endpoint, label in vars.popular_coins_endpoints.items():
        payload = {}
        headers = {}
        response = requests.request("GET", endpoint, headers=headers, data=payload)
        json_response = response.json()
        hour_trend = json_response['p1']
        week_trend = json_response['p7']
        gauge_metric_hour = vars.popular_coins_metrics.get(endpoint)[0]
        gauge_metric_week = vars.popular_coins_metrics.get(endpoint)[1]
        gauge_metric_hour.labels(endpoint=endpoint).set(hour_trend)
        gauge_metric_week.labels(endpoint=endpoint).set(week_trend)
    
    # Fetching data for the cheapest coins
    for endpoint, label in vars.cheapest_coins_endpoints.items():
        payload = {}
        headers = {}
        response = requests.request("GET", endpoint, headers=headers, data=payload)
        json_response = response.json()
        price = json_response['pu']
        price = format(price, '.8f')
        gauge_metric = vars.cheapest_coins_metrics[endpoint]
        gauge_metric.labels(endpoint=endpoint).set(price)

if __name__ == '__main__':
    start_http_server(8000) 
    # Create metrics for the poupular coins
    for endpoint, label in vars.popular_coins_endpoints.items():
        create_popular_coin_metric(endpoint, label)

    # Create metrics for the 5 cheapest coins
    for endpoint, label in vars.cheapest_coins_endpoints.items():
        create_cheapest_coins_metric(endpoint, label)
    
    # Run the loop to fetch data and update the metrics
    while True:
        fetch_data()
        time.sleep(30)
