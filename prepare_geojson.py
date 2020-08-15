#!/usr/bin/env python

from datetime import date, timedelta
import json
import pandas as pd
import requests

def filter_counties(geojson, state="18"):
    return {
        "type": "FeatureCollection",
        "features": list(filter(lambda f: f["properties"]["STATE"] == state, geojson["features"]))
    }

def load_county_populations(population_csv, column="POPESTIMATE2019"):
    pop = pd.read_csv(population_csv, encoding="iso-8859-1")
    pop["FIPS"] = pop["STATE"] * 1000 + pop["COUNTY"]
    pop = pop[pop["STATE"] == 18]
    pop = pop[["STATE", "COUNTY", "CTYNAME", "FIPS", column]]
    pop["POP"] = pop[column]
    pop = pop.set_index('FIPS')
    return pop.to_dict('index')

def load_covid_19_data(covid_data_excel):
    covid = pd.read_excel(covid_data_excel)
    past_14_days = [(date.today() - timedelta(days=x)).isoformat() for x in range(14)]
    covid = covid[covid["DATE"].isin(past_14_days)]
    covid_count = covid.pivot(index="LOCATION_ID", columns="DATE", values="COVID_COUNT").to_dict('index')
    covid_deaths = covid.pivot(index="LOCATION_ID", columns="DATE", values="COVID_DEATHS").to_dict('index')
    covid_test = covid.pivot(index="LOCATION_ID", columns="DATE", values="COVID_TEST").to_dict('index')
    return covid_count, covid_deaths, covid_test


if __name__ == "__main__":
    counties_geojson = "./gz_2010_us_050_00_20m.json"
    output_file = "./counties.geojson"
    with open(counties_geojson, 'r', encoding="iso-8859-1") as c:
        counties_data = filter_counties(json.load(c), state="18")
    pop_data = load_county_populations("./co-est2019-alldata.csv")
    # download the latest covid_report_county_date.xlsx
    covid_data_response = requests.get("https://hub.mph.in.gov/dataset/bd08cdd3-9ab1-4d70-b933-41f9ef7b809d/resource/afaa225d-ac4e-4e80-9190-f6800c366b58/download/covid_report_county_date.xlsx")
    covid_count, covid_deaths, covid_test = load_covid_19_data(covid_data_response.content)
    for feature in counties_data["features"]:
        fips = int(feature["properties"]["STATE"]) * 1000 + int(feature["properties"]["COUNTY"])
        feature["properties"]["POP"] = pop_data[fips]["POP"]
        feature["properties"]["COVID_DEATHS"] = covid_deaths[fips]
        feature["properties"]["COVID_COUNT"] = covid_count[fips]
        feature["properties"]["COVID_TEST"] = covid_test[fips]
    with open(output_file, "w") as o:
        o.write("const counties = ")
        json.dump(counties_data, o)
