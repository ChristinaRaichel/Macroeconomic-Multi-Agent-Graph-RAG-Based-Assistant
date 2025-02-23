
import requests
import pandas as pd
import logging

logging.basicConfig(level = logging.DEBUG)


def create_df(indicator, url):
    page = 1
    all_data = []

    while True:
        response = requests.get(f"{url}&page={page}")
        
        if response.status_code != 200:
            logging.error(f"Failed to fetch data for {indicator}: {response.status_code}")
            break
    
        data = response.json()
        if not data or len(data) < 2:
            logging.info(f"No more data found for {indicator} on page {page}.")
            break

        all_data.extend(data[1])

        if page >= data[0]['pages']:
            break
        page += 1

    countries = []
    values = []
    years = []

    for entry in all_data:
        country = entry["country"]["value"]
        year = entry["date"]
        value = entry["value"]

        countries.append(country)
        years.append(year)
        values.append(value)

    df = pd.DataFrame({"Country": countries, "Year": years, f"{indicator}": values})
    return df


urls = ["http://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.CD?format=json",\
        "http://api.worldbank.org/v2/country/all/indicator/FP.CPI.TOTL.ZG?format=json",\
        "http://api.worldbank.org/v2/country/all/indicator/SL.UEM.TOTL.ZS?format=json",\
        "http://api.worldbank.org/v2/country/all/indicator/NE.TRD.GNFS.ZS?format=json",\
        "http://api.worldbank.org/v2/country/all/indicator/DT.DOD.DECT.CD?format=json",\
        "http://api.worldbank.org/v2/country/all/indicator/SP.POP.TOTL?format=json"
    ]
indicators = ["gdp", "inflation (Consumer Prices, Annual %)", "unemployment (Total, % of Total Labor Force)", "trade (Trade as % of GDP)", \
    "debt (Total External Debt Stocks, USD)", "population (total)"]


indicator_url_dict = dict(zip(indicators,urls))

for indicator, url in indicator_url_dict.items():
    logging.info(f"Fetching data for {indicator}")
    df_name = f"{indicator}_df"
    df = create_df(indicator, url)
    globals()[df_name] = df
    print(f"Data for {indicator}:\n", df.head(), "\n")


