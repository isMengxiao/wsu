# -*- coding: utf-8 -*-

import urllib3
from bs4 import BeautifulSoup

def get_html(url):
    http = urllib3.PoolManager(timeout=2)
    response = http.request('get', url)
    html = response.data
    return html

def get_soup(url):
    if not url:
        return None
    soup = BeautifulSoup(get_html(url), features="html.parser")
    return soup

def get_ele(soup, selector):
    ele = soup.select(selector)
    return ele

def main():
    url = 'https://www.eecs.wsu.edu/~cs460/samples/'
    print("Which LAB do you want to download?(Number):")
    num = input()
    ss = num
    url = url + ss
    print(url)
    soup = get_soup(url)
    link = soup.body.pre.select('a')
    t = 0
    file = './'+ss+'/wget'
    print(file)
    f = open(file, 'w')
    for x in link:
        if t>=5:
            s = "wget "+url+'/'+x.next
            print(s)
            f.write(s)
            f.write('\n')
        t+=1
    f.write('wget https://www.eecs.wsu.edu/~cs460/'+num+'.html')
    f.write('\n')
    f.close()
    #print(link)


if __name__ == '__main__':
    main()
