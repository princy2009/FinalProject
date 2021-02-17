from django.shortcuts import render
import requests
from bs4 import BeautifulSoup


def scrapper(url1):
    url = url1



    Company = []
    Locations = []
    Titles = []
    Links = []

    # ==================================================================================

    response = requests.get(url)
    #response = requests.get(url, headers=headers, params=Parameters)

    soup = BeautifulSoup(response.text, 'html.parser')
    cards = soup.find_all('div', 'jobsearch-SerpJobCard')

    for card in cards:
        atag = card.h2.a
        job_title = atag['title']
        job_url = 'https://in.indeed.com' + atag.get('href')
        company = card.find('span', 'company')
        job_location = card.find('div', 'recJobLoc').get('data-rc-loc')

        Titles.append(job_title)
        Locations.append(job_location)
        Company.append(company.text.strip())
        Links.append(job_url)

    # ==================================================================================

    data = list(zip(Titles, Company, Locations, Links))
    return data


def index(req):
    url = get_url('python developer', 'mumbai')
    data = scrapper(url)
    return render(req, 'index.html', {'jobs': data})


def search(req):
    where = req.POST.get('myCountry')
    tech = req.POST.get('Tech')
    url = get_url(tech, where)
    data = scrapper(url)
    return render(req, 'index.html', {'jobs': data})


def get_url(position, location):
    template = 'https://in.indeed.com/jobs?q={}&l={}'
    url = template.format(position, location)
    return url



