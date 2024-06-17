import requests
import pandas as pd
from confluent_kafka import Producer
import json
import logging
import time


def main():
    """Main function"""
    # setting logging configuration
    logging.basicConfig(level=logging.INFO)
    # extracting flight ids and data
    flight_ids, live_flights = get_tracked_flights()
    # creating dataframe
    dataframe = pd.DataFrame(live_flights)
    # writing data to file
    dataframe.to_csv('live_flights.csv', index=False)
    # Fetching Data For Flights
    for flight_id in [flight_ids[1]]:
        try:
            while True:
                # Logging flight id
                logging.info(f'Processing flight {flight_id}')
                # fetching data
                data = get_data(flight_id)
                # streaming data
                stream_data(data, flight_id)
                # waiting
                time.sleep(10)
        except Exception as e:
            logging.warning(e)


def get_tracked_flights():
    # creating flights and flight_ids for holding flights data and id respectively
    flights = None
    flight_ids = []
    try:
        # fetching most tracked flights
        tracked_flights = requests.get("https://www.flightradar24.com/flights/most-tracked")
        flights = tracked_flights.json()
        # extracting data component
        flights = flights['data']
        # retrieving ids
        for item in flights:
            flight_ids.append(item['flight_id'])
    except Exception as e:
        print(e)

    return flight_ids, flights


def get_data(flight_id: str) -> dict:
    """Gets Live Flight Data For a given Flight ID"""
    # creating trail for holding results
    trail = None
    try:
        # fetching flight data
        url = f"https://data-live.flightradar24.com/clickhandler/?version=1.5&flight={flight_id}"
        data = requests.get(url).json()
        # converting data to dictionary to allow json dumping
        trail = {"trails": data['trail']}
    except Exception as e:
        print(e)
    return trail


def stream_data(data, flight_id):
    """Stream data from Flight ID to Kafka Topic 'flights'"""
    # setting up configuration for producer
    conf = {
        'bootstrap.servers': 'localhost:19092'
    }
    # instantiating bootstrap-servers
    producer = Producer(**conf)
    # writing flight data to json
    data = json.dumps(data)
    print(data)
    # producing data to servers
    producer.produce("flights", data, key=flight_id)
    # setting timeout for waiting
    producer.poll(0)
    # clearing queue
    producer.flush()


if __name__ == '__main__':
    main()
