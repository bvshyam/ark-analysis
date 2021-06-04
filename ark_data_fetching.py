import os
from utils.ark_utils import csv_write
from utils.ark_utils import download_csv, process_csv_file
from utils.credentials import CSV_FOLDERNAME, ARK_WEBSITE

# Setup Logging
import logutil
import logging
from logutil import LOGGER_NAME
logger = logging.getLogger(LOGGER_NAME)

def main():
    logger.info('Ark Analysis Starting')

    if not os.path.exists(CSV_FOLDERNAME):
        os.mkdir(CSV_FOLDERNAME)
    
    url_list = [
        ('arkq', 'https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_AUTONOMOUS_TECHNOLOGY_&_ROBOTICS_ETF_ARKQ_HOLDINGS.csv'),
        ('arkk', 'https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_INNOVATION_ETF_ARKK_HOLDINGS.csv'),
        ('arkw', 'https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_NEXT_GENERATION_INTERNET_ETF_ARKW_HOLDINGS.csv'),
        ('arkg', 'https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_GENOMIC_REVOLUTION_MULTISECTOR_ETF_ARKG_HOLDINGS.csv'),
        ('fintech-etf', 'https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_FINTECH_INNOVATION_ETF_ARKF_HOLDINGS.csv'),
        ('3d-printing-etf', 'https://ark-funds.com/wp-content/fundsiteliterature/csv/THE_3D_PRINTING_ETF_PRNT_HOLDINGS.csv'),
        ('israel-etf', 'https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_ISRAEL_INNOVATIVE_TECHNOLOGY_ETF_IZRL_HOLDINGS.csv'),
        ('arkk','https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_SPACE_EXPLORATION_&_INNOVATION_ETF_ARKX_HOLDINGS.csv')
    ]

    csv_filename = os.path.join(CSV_FOLDERNAME,  ARK_WEBSITE + '.csv')

    csv_data = []
    header_row = ['Stock_Ticker', 'Stock_name', 'Location', 'Weight', 'Website']
    csv_data.insert(0, header_row)

    for fund_name, url in url_list:
        logger.debug('Extracting Data for Fund ' + fund_name)
        fund_csv_filename = os.path.join(CSV_FOLDERNAME, fund_name + '.csv')
        download_csv(url, fund_csv_filename)
        if fund_csv_filename:
            data = process_csv_file(fund_csv_filename, ARK_WEBSITE)
            if data:
                csv_data = csv_data + data
                
    if len(csv_data) > 1:
        csv_write(csv_filename, csv_data, 'w') 
        
if __name__ == '__main__':
    main()