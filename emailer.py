import pandas as pd
import smtplib,ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#from secrets import mycred
import pandas as pd
from bs4 import BeautifulSoup
import requests
import os.path
from email.mime.application import MIMEApplication

import schedule
import time
from datetime import datetime
import pytz

def mycred():
    username ='sajproject5656@gmail.com'
    password = 'akashjayeshshubham'
    return username,password

file = pd.read_excel('users.xlsx',sheet_name='Sheet1')

contacts = pd.DataFrame(file)
password = mycred()[1]

def job():

    url = "https://www.monster.com/jobs/search/"
    where = "All"
    tech = "Accounting,Java,Python,Web Developer,Django,PHP, Blockchain ,Machine Learning"
    Parameters = {"q": tech , "where": where }
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
    df = pd.DataFrame(data,columns=['Title','Company','Location','Link to Apply'])

    df.index+=1
    directory = os.path.dirname(os.path.realpath(__file__))

    filename = "scrapedfile.csv"
    file_path = os.path.join(directory,'csvfiles/', filename)

    df.to_csv(file_path)

    for i in range(len(contacts)):

            '''
            with open(file_path, 'rb') as f:
                data = f.read()
                f.close()
            '''


            name,email = contacts.iloc[i]
            port = 465
            smtp_server = "smtp.gmail.com"

            msg = MIMEMultipart()
            msg['From'] = mycred()[0]
            msg['To'] = email
            msg['Subject'] = " Congratulations on Email Application."
            body = "Hey {}, How is it Going? I just want to confirm email. Thank you for enrolling ".format(name)
            msg.attach(MIMEText(body, 'plain'))

            with open(file_path, 'rb') as file:
                # Attach the file with filename to the email
                data = file.read()
                msg.attach(MIMEApplication(data,Name=filename))





            text = msg.as_string()
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server,port,context=context) as server:
                server.login(mycred()[0], password)
                server.sendmail(mycred()[0],msg['To'], text)
            print('Sent to:',name)
            print('Done')

schedule.every(1).minutes.do(job)
# schedule.every().hour.do(job)
#schedule.every().day.at('13:58').do(job)
# schedule.every(5).to(10).minutes.do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
# schedule.every().minute.at(":17").do(job)

while True:
    schedule.run_pending()
    time.sleep(1) # wait one minute