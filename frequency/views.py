from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import urllib.request, urllib.error, urllib.parse
from . import obo
import json
from .models import Webdata

# Create your views here.
visited_url = []

def webScrap(url):
    response = urllib.request.urlopen(url)
    html = response.read()
    text = obo.stripTags(html).lower()
    fullwordlist = obo.stripNonAlphaNum(text)
    wordlist = obo.removeStopwords(fullwordlist, obo.stopwords)
    dictionary = obo.wordListToFreqDict(wordlist)
    sorteddict = obo.sortFreqDict(dictionary)
    sorteddict = sorteddict[:10]
    
    Web = Webdata()
    if(url in visited_url):
        return True, sorteddict
    Web.webdata_name = url
    visited_url.append(url)
    Web.webdata_list = json.dumps(sorteddict)
    Web.save()
    return False, sorteddict

def form(request):
    return render(request, 'index.html')

@csrf_exempt
def result(request):
    url = request.POST['enteredUrl']
    db_from_data, sorteddict = webScrap(url)
    

    text = "Fetched form Database: " + str(db_from_data) + "<br>"
    for s in sorteddict:
        text = text + "<br>"+ str(s)
    return HttpResponse(text)

