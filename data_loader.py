
import requests
import pandas as pd
import logging

gdp_url = "http://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.CD?format=json"

gdp_response = requests.get(gdp_url)
gdp_data = gdp_response.json()

countries = []
gdp_values = []
years = []

for entry in gdp_data[1]:  # API response structure
    country = entry["country"]["value"]
    year = entry["date"]
    gdp = entry["value"]
    
    countries.append(country)
    years.append(year)
    gdp_values.append(gdp)

gdp_df = pd.DataFrame({"Country": countries, "Year": years, "GDP": gdp_values})
print(gdp_df.head())


