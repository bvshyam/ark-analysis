import time
import random
import os
import json
import csv
import string

import requests
from bs4 import BeautifulSoup
import html5lib


# Setup Logging
import logging
from logutil import LOGGER_NAME
logger = logging.getLogger(LOGGER_NAME)

def csv_write(file_name, data, open_type='w'):
    try:
        if not data:
            logger.error(['No Data Found','CSV Write'])
            return None
        f=open(file_name, open_type, newline='')
        csvWriter = csv.writer(f)
        if isinstance(data[0], list):
            csvWriter.writerows(data)
        else:
            csvWriter.writerow(data)
        f.close()
    except Exception as e:
        logger.error(['CSV Write', file_name, data, open_type, e], exc_info=True)
    else:
        return 'OK'


def download_csv(url, fund_csv_filename):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        response = requests.get(url, headers =headers)
        response.raise_for_status()
        with open(fund_csv_filename, 'w') as f:
            f.write(response.text)
    except Exception as e:
        logger.exception('Unable to download CSV')


def csv_read(file_name):
    try:
        data = []
        with open(file_name,'r') as f:
            reader = csv.reader(f)
            for row in reader:
                data.append(row)
    except Exception as e:
        logger.error(['CSV Read', file_name, e], exc_info=True)
    else:
        return data


def process_csv_file(fund_csv_filename, website_name):
    try:
        result = []
        csv_data = csv_read(fund_csv_filename)
        for row in csv_data[1:]:
            if len(row) < 7:
                continue
            
            if not row[3]:
                continue

            temp = [
                row[3],
                row[2].replace('"', '').strip(),
                row[1],
                row[7],
                website_name
            ]
            result.append(temp)
    except Exception as e:
        logger.exception('Unable to processes CSV')
        result = []
    
    return result
