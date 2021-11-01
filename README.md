# API Data Visualization Demo
- Click [here](http://13.229.123.107/newscatcher/) to visit my live demo.

With so much news being repetitive and monotonous, I wanted to create a way to easily visualize and compare topics being reported on in different countries. 

I utilize [RapidAPI's Newscatcher](https://rapidapi.com/newscatcher-api-newscatcher-api-default/api/newscatcher/) /v1/aggregation 
endpoint to pull totals based on Topic from different countries around the world.

![Landing page for site](/newscatcher_api/static/img/Landing%20page.png)

After the user selects date range, country and topics, we output the results, along with a [Highcharts](https://www.highcharts.com/demo/pie-drilldown) interactive javascript piechart:

![Results from search](/newscatcher_api/static/img/Output%20example.png)
