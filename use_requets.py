import requests
from bs4 import BeautifulSoup

url = 'https://boston.craigslist.org/search/sof'
try:
    response = requests.get(url)
    print('Sussess', response.status_code)
    #print(f'datanya {response.text}')
    soup = BeautifulSoup(response.text, features="html.parser")
    #mendapatkan semua tag href
    # tags = soup.find_all('a')
    # for tag in tags:
    #     print(tag.get('href'))
    #mendapatkan semua title
    # titles = soup.find_all('a',{'class':'result-title'})
    # for title in titles:
    #     print(title.text)

    #body
    # addresses = soup.find_all("span",{'class':'result-hood'})
    # for address in addresses:
    #     print(address.text)

    #mengambil semuanya dalam satu kali scrap

    jobs = soup.find_all('p',{'class':'result-info'})
    for job in jobs:
        title = job.find('a',{'class':'result-title'}).text
        location_tag = job.find('span',{'class':'result-hood'})
        location = location_tag.text if location_tag else "Tidak ada info"
        time = job.find('time',{'class':'result-date'}).text
        link = job.find('a',{'class':'result-title'}).get('href')
        print(f"Judul pekerjaan {title} : lokasi {location} \n Batas Akhir {time} \n daftar sekarang {link}")
except Exception as e:
    print('And error', e)