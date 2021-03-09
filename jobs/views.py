
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import pandas as pd





def scrapper(city,url1,tech):
    where = city
    url = url1
    tech1 = tech

    Parameters = {"q": tech1 , "where": where }
    headers = {
        'Accept-Encoding': 'br, gzip, deflate',
        'Accept-Language': 'en-gb',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5)AppleWebKit/605.1.15 (KHTML, like Gecko)Version/12.1.1 Safari/605.1.15',
        'Accept': 'test/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Referer': 'http://www.google.com/',
        'Connection': 'keep-alive',
    }

    r = requests.get(url, headers=headers, params=Parameters)
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
    df = pd.DataFrame(data)
    df.to_csv('jobs.csv')
    print(df)
    
    

    return data



def index(req):
    url = "https://www.monster.com/jobs/search/"
    where = "All"
    tech = "Accounting,Java,Python,Web Developer,Django,PHP, Blockchain ,Machine Learning"
    data = scrapper(where,url,tech)
    return render(req, 'index.html', {'jobs':data})

def search(req):
    url = "https://www.monster.com/jobs/search/"
    print(req)
    where = req.POST.get('myCountry')
    tech = req.POST.get('Tech')
    data = scrapper(where,url,tech)
    return render(req, 'index.html', {'jobs':data})
    

'''

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrapper(params):
    #url = url1



    Company = []
    Locations = []
    Titles = []
    Links = []
    Salary=[]
    Date=[]

    # ==================================================================================

    #url = get_url('python developer', 'mumbai')
    headers = {
        'Accept-Encoding': 'br, gzip, deflate',
        'Accept-Language': 'en-gb',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5)AppleWebKit/605.1.15 (KHTML, like Gecko)Version/12.1.1 Safari/605.1.15',
        'Accept': 'test/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Referer': 'http://www.google.com/',
        'Connection': 'keep-alive',
    }
    url = 'https://in.indeed.com/jobs/'

    response = requests.get(url,headers=headers,params=params)

    soup = BeautifulSoup(response.text, 'html.parser')
    cards = soup.find_all('div', 'jobsearch-SerpJobCard')

    for card in cards:
        atag = card.h2.a
        job_title = atag['title']
        job_url = 'https://in.indeed.com' + atag.get('href')
        company = card.find('span', 'company')
        job_location = card.find('div', 'recJobLoc').get('data-rc-loc')
        try:
            salary = card.find('span',class_='salaryText').text.strip()
        except:
            salary = None
        date = card.find('span',class_='date')



        Titles.append(job_title)
        Locations.append(job_location)
        Company.append(company.text.strip())
        Links.append(job_url)
        Salary.append(salary)
        Date.append(date.text.strip())





    # ==================================================================================

    data = list(zip(Titles, Company, Locations,Salary,Date, Links))
    #df = pd.DataFrame(data)
    return data

@login_required(login_url='login')
def index(req):
    params = {
        'q': 'python developer',
        'l': 'mumbai',
        'sort': 'date',

    }
    url = get_url(params)
    data = scrapper(params)
    return render(req, 'index.html', {'jobs': data})


def search(req):

    where = req.POST.get('myCountry')
    tech = req.POST.get('Tech')
    jtype = req.POST.get('jt')
    print(where,tech,jtype)
    try:
        params = {
            'q':tech,
            'l':where,
            'jt':jtype,
            'sort':'date',

        }
    except:
        params = {
            'q': tech,
            'l': where,
            'sort':'date',

        }

    url = get_url(params)
    data = scrapper(params)
    return render(req, 'index.html', {'jobs': data})


def get_url(params):
    #template = 'https://in.indeed.com/jobs?q={}&l={}&sort=date'
    headers = {
        'Accept-Encoding': 'br, gzip, deflate',
        'Accept-Language': 'en-gb',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5)AppleWebKit/605.1.15 (KHTML, like Gecko)Version/12.1.1 Safari/605.1.15',
        'Accept': 'test/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Referer': 'http://www.google.com/',
        'Connection': 'keep-alive',
    }

    url = 'https://in.indeed.com/jobs/'
    response = requests.get(url,headers=headers,params=params)



    #url = template.format(position, location)
    return response.url
'''












