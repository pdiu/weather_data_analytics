import pandas as pd
import sqlite3
import requests
import pdb
import logging
import json
import datetime

API_HOST = "weatherbit-v1-mashape.p.rapidapi.com"
API_KEY = "790823c4c7mshc1dc6e51242a198p13f69ejsn818199a22f39"

def init_logging():
    FORMAT = "[%(asctime)s %(levelname)s %(filename)s:%(lineno)s] %(funcName)s - %(message)s"
    today = datetime.date.today()
    logging.basicConfig(filename=f"app{today}.log", format=FORMAT, datefmt="%d-%b-%y %H:%M:%S", level=logging.INFO)

def main():
    try:
        logging.info("Starting script...")
        create_connection("pythonsqlite.db")
        # Auckland lat/lon co-ordinates
        get_current_weather("-36.85", "174.76")
    except Exception as e:
        logging.error(e)

def get_current_weather(lat, lon):
    logging.info(f"Running")
    url = "https://weatherbit-v1-mashape.p.rapidapi.com/current"
    querystring = {"lat":lat,"lon":lon}
    headers = {"X-RapidAPI-Key": API_KEY, "X-RapidAPI-Host":API_HOST}
    response = requests.request("GET", url, headers=headers, params=querystring)
    response_dict = json.loads(response.text)
    df = pd.DataFrame.from_dict(response_dict["data"][0])
    df.to_csv(f"AKL.csv", header=True)
    logging.info(f"Closing")

def create_connection(db_file):
    logging.info(f"Running")
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except sqlite3.Error as e:
        logging.error(f"{create_connection.__name__} {e}")
    finally:
        if conn:
            conn.close()
            logging.info(f"Closing")

if __name__ == "__main__":
    main()