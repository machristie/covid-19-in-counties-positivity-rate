# Choropleth map of COVID-19 trends in Indiana counties

Color code each county in Indiana based on the 14 day trend of positivity rate.

See the live site at
https://machristie.github.io/covid-19-in-counties-positivity-rate/

## Getting Started

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python prepare_geojson.py
```

## Resources

- https://leafletjs.com/examples/choropleth/
- https://hub.mph.in.gov/dataset/covid-19-county-wide-test-case-and-death-trends/resource/afaa225d-ac4e-4e80-9190-f6800c366b58
  - https://hub.mph.in.gov/api/3/action/datastore_search?q={%22COUNTY_NAME%22:%22monroe%22,%20%22DATE%22:%222020-07-31%22}&resource_id=afaa225d-ac4e-4e80-9190-f6800c366b58
  - https://hub.mph.in.gov/api/3/action/datastore_search?q={%22DATE%22:%222020-07-31%22}&resource_id=afaa225d-ac4e-4e80-9190-f6800c366b58
  - https://hub.mph.in.gov/api/3/action/datastore_search_sql?sql=SELECT%20*%20from%20%22afaa225d-ac4e-4e80-9190-f6800c366b58%22%20WHERE%20%22COUNTY_NAME%22%20LIKE%20%27Monroe%27
  - `q` parameter in the API is too fuzzy, not exact enough. Use `filters` or
    SQL instead.
  - https://hub.mph.in.gov/api/3/action/datastore_search_sql?sql=SELECT%20*%20from%20%22afaa225d-ac4e-4e80-9190-f6800c366b58%22%20WHERE%20%22DATE%22%20%3E=%20current_date%20-%2014
- https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/totals/co-est2019-alldata.csv
- county shape data: https://eric.clst.org/tech/usgeojson/

## TODO

- [x] Python script to get just Indiana counties from US counties geojson
- [x] add 2019 estimated population per county to properties of each county in
      geojson
- [x] remove fetch
- [x] change script to download covid xlsx data
- [x] publish index.html to gh-pages
- [x] add display of date range
- [x] add hover with county details
- [x] add legend for the colors
- [x] seem to not have past two days worth of data reliably
- [ ] add toggle between past 7 and past 14 days?
- [ ] more buckets for positivity rates (0-2, 2-4, 4-6, 6-8, 8-10, 10+)?
- [ ] make more mobile friendly
