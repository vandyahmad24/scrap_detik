import requests
import pandas as pd
from bs4 import BeautifulSoup

url = 'https://boston.craigslist.org/search/sof'
#buat dictionry
job_dic = {}
try:
    job_no = 0
    while True:
        response = requests.get(url)
        print('Sussess', response.status_code)
        # print(f'datanya {response.text}')
        soup = BeautifulSoup(response.text, features="html.parser")
        # mendapatkan semua tag href
        # tags = soup.find_all('a')
        # for tag in tags:
        #     print(tag.get('href'))
        # mendapatkan semua title
        # titles = soup.find_all('a',{'class':'result-title'})
        # for title in titles:
        #     print(title.text)

        # body
        # addresses = soup.find_all("span",{'class':'result-hood'})
        # for address in addresses:
        #     print(address.text)

        # mengambil semuanya dalam satu kali scrap

        jobs = soup.find_all('p', {'class': 'result-info'})
        for job in jobs:
            title = job.find('a', {'class': 'result-title'}).text
            location_tag = job.find('span', {'class': 'result-hood'})
            location = location_tag.text if location_tag else "Tidak ada info"
            time = job.find('time', {'class': 'result-date'}).text
            link = job.find('a', {'class': 'result-title'}).get('href')
            # mengambil detail dari perkerjaan
            job_response = requests.get(link)
            job_data = job_response.text
            job_soup = BeautifulSoup(job_data, features="html.parser")
            job_description = job_soup.find('section', {'id': 'postingbody'}).text
            job_attributes_tag = job_soup.find('p', {'class': 'attrgroup'})
            job_attributes = job_attributes_tag.text if job_attributes_tag else "N/A"
            job_no+=1
            # print(job)
            job_dic[job_no] = [title,location,time,job_description,job_attributes]

            # job_soup
            # print(
            #     f"Judul pekerjaan {title} : lokasi {location} \n Batas Akhir {time} \n Deskripsi Perkerjaan {job_description} Info lain {job_attributes}")
        url_tag = soup.find('a',{'title':'next page'})
        if url_tag.get('href'):
            url = 'https://boston.craigslist.org'+url_tag.get('href')
            print(url)
        else:
            break
    print(f'total job : {job_no}')
    data = pd.DataFrame.from_dict(job_dic, orient='index', columns=['Judul Perkerjaan','lokasi','Batas Akhir','Deskripsi Perkerjaan','Info Lain'])
    data.head()
    #rubah csv
    data.to_csv('data_pekerjaan.csv')

except Exception as e:
    print('And error', e)
