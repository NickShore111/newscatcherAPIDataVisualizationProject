from django.shortcuts import render, HttpResponse, redirect
# from django.http import HttpResponse
from datetime import datetime
from django.contrib import messages
from newscatcher_api.models import *

# Global variables
topics_list = [
    "Pollution",
    "Climate Change",
    "Education",
    "Unemployment",
    "Violence",
    "Terrorism",
    "Substance Abuse",
    "Food Insecurity",
]
countries = [
    {"name": "China", "id": "CN", "lang": "en"},
    {"name": "India", "id": "IN", "lang": "hi"},
    {"name": "United States", "id": "US", "lang": "en"},
    {"name": "Brazil", "id": "BR", "lang": "pt"},
    {"name": "Russia", "id": "RU", "lang": "ru"},
    {"name": "Mexico", "id": "MX", "lang": "es"},
    {"name": "Japan", "id": "JP", "lang": "ja"},
    {"name": "Philippines", "id": "PH", "lang": "tl"},
    {"name": "Germany", "id": "DE", "lang": "de"},
    {"name": "France", "id": "FR", "lang": "fr"},
    {"name": "United Kingdom", "id": "GB", "lang": "en"},
    {"name": "Italy", "id": "IT", "lang": "", "lang": "it"},
]


def index(request):
    request.session.flush()
    list_options = {"topics_list": topics_list, "countries": countries}
    return render(request, 'newscatcher_api/form.html', {"list_options": list_options})


def results(request):
    request.session.flush()
    query = dict()
    inquiry_input = dict()
    query["agg_by"] = "day"
    query["country"] = request.POST['country_id']
    query["media"] = False
    # Input validation
    errors = Inquiry.objects.query_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect("/newscatcher")
    for country in countries:
        if country['id'] == request.POST['country_id']:
            inquiry_input['country_name'] = country['name']
            query['lang'] = country['lang']
    query["from"] = datetime.strptime(
        request.POST['from'], '%Y-%m-%d').strftime('%m/%d/%Y')
    query["to"] = datetime.strptime(
        request.POST['to'], '%Y-%m-%d').strftime('%m/%d/%Y')
    # Log Inquiry and get primary key
    inquiry_object = Inquiry.objects.create(
        country_id=request.POST['country_id'], country=inquiry_input['country_name'], ref_date_start=query["from"], ref_date_end=query["to"])
    inquiry_id = int(inquiry_object.id)
    request.session['inquiry_id'] = inquiry_id
    request.session['country_name'] = inquiry_input['country_name']
    request.session['from'] = query['from']
    request.session['to'] = query['to']
    print("inquiry_id: ", inquiry_id)
    # Process queries
    print("PROCESSING TOPIC QUERIES TO NEWSCATCHER API")
    final_results = Result.objects.process_topics(
        request.POST, query, inquiry_id)
    # final_results => [percent_data, combined_errors, doc_counts]
    print("*"*10, "Return from result.objects.process_topics", "*"*10)
    print("Percent_results: ", final_results[0])
    print("Error_results: ", final_results[1])
    request.session['final_results'] = final_results[0]
    request.session['status_errors'] = final_results[1]
    request.session['doc_counts'] = final_results[2]
    return redirect('/newscatcher/display')


def display(request):
    list_options = {"topics_list": topics_list, "countries": countries}
    return render(request, 'newscatcher_api/form.html', {"list_options": list_options})


def technologies(request):
    img_gallery = [
        {"id": "0", "img": "CodeSnippet1", "title": "Django Template Engine",
            "desc": "Block tags for template rendering and sources used."},
        {"id": "1", "img": "CodeSnippet7", "title": "One-to-Many Relational Database",
            "desc": "Database model creation using Django's built-in SQLite3 backend."},
        {"id": "2", "img": "CodeSnippet9", "title": "Input Validation",
            "desc": "Converting and reformatting datetime inputs, using timedelta, performing validations, returning errors."},
        {"id": "3", "img": "CodeSnippet10", "title": "Interactive Data Visualization",
            "desc": "Display variable data using conditionals with Highcharts interactive Javascript."},
        {"id": "4", "img": "CodeSnippet5", "title": "JQueryUI Datepicker",
            "desc": "Utilizing JQuery library for interactice elements."},
        {"id": "5", "img": "CodeSnippet0", "title": "Bootstrap v5.0",
            "desc": "Bootstrap image carousel."},
    ]
    return render(request, 'newscatcher_api/technologies.html', {"img_gallery": img_gallery})


def methods(request):
    img_gallery = [
        {"id": "0", "img": "MethodSnippet0", "title": "Country Info Used for Query",
            "desc": "Working list of dictionaries stores name, ISO 3166-1 alpha-2 country codes, and 2 letter language codes."},
        {"id": "1", "img": "MethodSnippet1", "title": "Sample Code Snippet for Requests",
            "desc": "RapidAPI's Newscatcher /v1/aggregation url, querystring, and request method."},
        {"id": "2", "img": "MethodSnippet2", "title": "Sample Code Snippet API Response",
            "desc": "status: 'ok' returns aggregation of articles doc_counts for each day requested."},
        {"id": "3", "img": "MethodSnippet3", "title": "Sample Code Snippet User Inputs",
            "desc": "Listing all possible user inputs allowed for Newscatcher /v1/aggregation API."},
        {"id": "4", "img": "MethodSnippet5", "title": "Sample Code Snippet No Matches",
            "desc": "Whether through lack of results or bad search terms status can return 'No matches'."},
        {"id": "5", "img": "ProcessSnippet0", "title": "Django Models.py Used to Build Search Queries",
            "desc": "Each topic is sent through requests.request method using stored query headers and parameters."},
        {"id": "6", "img": "ProcessSnippet1", "title": "Conditional Statements",
            "desc": "Loop through topic responses and for each query status = 'ok' calculate total doc_count and store in variable, else doc_count = 0."},
        {"id": "7", "img": "ProcessSnippet2", "title": "Calculate Total",
            "desc": "First, find total of all doc_counts stored"},
        {"id": "8", "img": "ProcessSnippet3", "title": "Calculate Percentage",
            "desc": "Use Try to divide each topic doc_count by total, then mutliply by 100. If results don't yield responses we won't run into ZeroDivisionError."},
    ]
    return render(request, 'newscatcher_api/methods.html', {"img_gallery": img_gallery})
