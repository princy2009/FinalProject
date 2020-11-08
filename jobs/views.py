from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

import os
import requests
from bs4 import BeautifulSoup
import sys

def scrapper(city,url1):
    where = city
    url = url1

    Payload = {"q": "Python Developer", "where": where}
    headers = {
        'Accept-Encoding': 'br, gzip, deflate',
        'Accept-Language': 'en-gb',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5)AppleWebKit/605.1.15 (KHTML, like Gecko)Version/12.1.1 Safari/605.1.15',
        'Accept': 'test/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Referer': 'http://www.google.com/',
        'Connection': 'keep-alive',
    }

    r = requests.get(url, headers=headers, params=Payload)
    soup = BeautifulSoup(r.text, 'html.parser')

    Company = []
    Locations = []
    Titles = []
    Links = []

    for x in soup.findAll('section', class_="card-content"):
        for y in x.findAll('div', class_="summary"):
            company = y.find('div', class_="company")
            location = y.find('div', class_="location")
            title = y.find('h2', class_="title")
            links = y.find('a')

            Titles.append(title.text.strip())
            Locations.append(location.text)
            Company.append(company.text.strip())
            Links.append(links["href"])

    data = list(zip(Titles, Company, Locations, Links))
    return data



def index(req):
    url = "https://www.monster.com/jobs/search/"
    where = "New York"
    data = scrapper(where,url)
    return render(req, 'index.html', {'jobs':data})

def search(req):
    url = "https://www.monster.com/jobs/search/"
    print(req)
    where = req.POST.get('myCountry')
    data = scrapper(where,url)
    return render(req, 'index.html', {'jobs':data})



