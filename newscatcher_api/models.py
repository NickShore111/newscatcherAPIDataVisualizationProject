from django.db import models
from datetime import datetime, timedelta
import requests
# Newscatcher API parameters
url = "https://newscatcher.p.rapidapi.com/v1/aggregation"
headers = {'x-rapidapi-host': "newscatcher.p.rapidapi.com",
           'x-rapidapi-key': "86d80c43d4msh8b45d3c483a4ba4p1e1bdejsna4edf1a13baf"}


class InquiryManager(models.Manager):
    def query_validator(self, postData):
        errors = {}
        today_date = datetime.today().strftime("%Y-%m-%d")
        today = datetime.strptime(today_date, "%Y-%m-%d")
        if not postData['to'] or not postData['from']:
            errors['date'] = "Please select valid dates."
        else:
            date_to = datetime.strptime(postData['to'], "%Y-%m-%d")
            date_from = datetime.strptime(postData['from'], "%Y-%m-%d")
            delta = timedelta(days=5)
            if date_to >= today or date_from >= today:
                errors['date'] = "Please select dates in the past."
            elif date_from > date_to:
                errors['date'] = "Date To and From conflict."
            elif date_to - date_from > delta:
                errors['date'] = "Date range cannot exceed 5 days."
        if "topic" not in postData:
            errors['topics'] = "Please select some topics."
        if len(postData['keyword']) > 0 and len(postData['keyword']) < 4 or len(postData['keyword']) > 20:
            errors['keyword'] = "Keyword range is 4-20 characters."
        return errors
class ResultManager(models.Manager):
    def process_topics(self, postData, query, inquiry_id):
        postData = dict(postData)
        if len(postData['keyword']) > 3:
            keyword = str(postData['keyword'][0])
            postData['topic'].append(keyword.capitalize())
        topicCountResults = Result.objects.topic_request(
            postData['topic'], query, inquiry_id)
        final_results = Result.objects.calc_percentage(topicCountResults)
        return final_results

    def topic_request(self, postData, query, inquiry_id):
        docs_count = dict()
        status = dict()
        for topic in postData:
            query["q"] = topic
            response = requests.request(
                "GET", url, headers=headers, params=query)
            data = response.json()
            if data['status'] == "ok":
                total_count = 0
                for day in data['aggregation']:
                    total_count += int(day['doc_count'])
                docs_count[topic] = total_count
                status[topic] = data['status']
                """Saving results to DB if results return valid"""
                Result.objects.create(
                    topic=query["q"], doc_count=docs_count[query["q"]], inquiry=Inquiry.objects.get(id=inquiry_id))
            else:
                docs_count[topic] = 0
                status[topic] = data['status']
        results = [docs_count, status]
        return results

    def calc_percentage(self, results):
        percent_data = {}
        total = 0
        doc_counts = dict(results[0])
        for count in doc_counts.values():
            total += count
        print("total doc_count: ", total)
        for key, value in doc_counts.items():
            try:
                percent = (value/total) * 100
            except ZeroDivisionError:
                print("ZeroDivisionError")
                results[1]['DivisionError'] = "Not enough results for output"
            else:
                percent_data[key] = round(percent, 1)
        status_errors = results[1]
        final_results = [percent_data, status_errors, doc_counts]
        return final_results


""" Results saved to SQLLite3 Database for posterity and potential future processing"""
class Inquiry(models.Model):
    country = models.CharField(max_length=20)
    country_id = models.CharField(max_length=2)
    ref_date_start = models.CharField(max_length=15)
    ref_date_end = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = InquiryManager()


class Result(models.Model):
    topic = models.CharField(max_length=20)
    doc_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    inquiry = models.ForeignKey(Inquiry, on_delete=models.CASCADE)
    objects = ResultManager()
