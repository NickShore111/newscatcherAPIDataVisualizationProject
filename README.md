# API Front-End Demo

## Project Goals:
- Make use of RapidAPI's Newscatcher /v1/aggregation endpoint to pull data on article counts from around the world
- Utilize Javascript to provide an interactive interface for viewing data, taking advantage of [Highcharts](https://www.highcharts.com/demo/pie-drilldown) template resources
- Perform data validation on user request and endpoint response
- Deploy project to Ubuntu server on AWS

### Landing Page
![Landing page for site](/newscatcher_api/static/img/Landing%20page.png)

## Perform Data Validation:
- Date range limited to range of 5 or less, before present day
- Optional extra Topic supplied by user limited to string length 5-20
- Check return response status for errors and display with output list
- Check for ZeroDivision error during percent calculation

### Results Output Example Display
![Results from search](/newscatcher_api/static/img/Output%20example.png)
