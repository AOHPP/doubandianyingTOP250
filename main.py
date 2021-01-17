import requests
import codecs
from bs4 import BeautifulSoup

Download_Url = 'https://movie.douban.com/top250'

def download_page(url):
    headers = { 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
    data = requests.get(url,headers=headers).content.decode('utf-8')
    return data

def parse_html(html):
    soup = BeautifulSoup(html,'html.parser')
    movie_list_soup = soup.find('ol', attrs={'class':'grid_view'})

    movie_name_list = []

    for movie_li in movie_list_soup.find_all('li'):
        detail = movie_li.find('div',attrs={'class':'hd'})
        movie_name = detail.find('span',attrs={'class':'title'}).getText()
        movie_name_list.append(movie_name)

    next_page = soup.find('span',attrs={'class':'next'}).find('a')
    #print(next_page)
    if next_page:
        return movie_name_list,Download_Url + next_page['href']
    return movie_name_list,None

def main():
    url = Download_Url

    with codecs.open('movies','wb',encoding='utf-8') as fp:
        while url:
            html = download_page(url)
            movies,url = parse_html(html)
            fp.write(u'{movies}\n'.format(movies='\n'.join(movies)))

if __name__ == '__main__':
    main()

