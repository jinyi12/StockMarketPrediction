import numpy as np
import time 
import datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen

def get_soup_with_repeat(url, repeat_times=3, verbose=True):
    for i in range(repeat_times):
        try:
            time.sleep(np.random.poisson(3))
            response = urlopen(url)
            data = response.read().decode('utf-8')
            return(BeautifulSoup(data, "lxml"))
        except Exception as e:
            if i == 0:
                print(e)
            if verbose:
                print("retrying...")
            continue

def generate_past_n_days_date(numdays):
    """Generate the date for the past N days in YYYY/MM/DD format"""

    # Get the base day (today)
    base = datetime.datetime.today()
    # Get date range, create an array of dates
    date_range = [base - datetime.timedelta(days=x) for x in range(0, numdays)]
    return [x.strftime("%Y%m%d") for x in date_range]        