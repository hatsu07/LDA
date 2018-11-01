import sys
import re
import requests
from bs4 import BeautifulSoup
from collections import deque
from time import sleep


def makePayload(p):
    """
    p: dict
    return: クエリストリング
    クエリストリング作成
    """

    res = '?'
    for item in p:
        res += item + '=' + p[item] + '&'
    return res


def getURLs(word, save=False):
    """
    word: 検索単語
    save: URLを保存するかどうか
    return: URL
    Yahooで検索したページのURLを取得
    """

    print('Start getURLs')
    param = {
        'p': word,
        'b': '01'
    }
    r = requests.get('https://search.yahoo.co.jp/search' + makePayload(param))
    soup = BeautifulSoup(r.text, 'html.parser')

    urls = deque([])
    flag = True
    if save:
        f = open('./urls.txt', 'w')
    while flag:
        flag = False
        for a in soup.findAll('a'):
            url = a.get('href')
            if 'http' in url and 'yahoo' not in url:
                urls.append(url)
                if save:
                    f.write(url + '\n')
                flag = True

        print('Num of URLs:', len(urls))
        sleep(3)
        param['b'] = str(int(param['b']) + 10)
        r = requests.get(
            'https://search.yahoo.co.jp/search' + makePayload(param))
        soup = BeautifulSoup(r.text, 'html.parser')
    if save:
        f.close()
    print('Finish getURLs')
    return urls


def loadURLs():
    """
    return: URL
    URL読み込み
    """

    urls = deque([])
    with open('./urls.txt', 'r') as f:
        for url in f.readlines():
            urls.append(re.sub(r'\n', '', url))
    return urls


def getText(urls, path):
    """
    urls: Yahoo検索でヒットしたページのURL
    path: WEBテキストの保存ファイル
    """

    print('Start getText')
    with open(path, 'w') as f:
        while urls:
            url = urls.popleft()
            print(len(urls))
            try:
                r = requests.get(url)
                if 'html' in r.headers['Content-Type']:
                    r.encoding = r.apparent_encoding
                    soup = BeautifulSoup(r.text, 'lxml')
                    [x.extract() for x in soup.findAll('script')]
                    [x.extract() for x in soup.findAll('style')]
                    text = re.sub(r'(\n)\1{2,}', '\n', soup.getText())
                    f.write(text)
            except requests.exceptions.SSLError as e:
                print('SSL Error によりスキップ')
                continue
            sleep(1)
    print('Finish getText')

if __name__ == '__main__':
    args = sys.argv
    if len(args) < 2:
        print('Error: 引数が足りません')
        print('ex. python crawl.py 食事 ./Eating_Crawl.txt')
        exit(0)

    if len(args) < 4:
        urls = getURLs(args[1])
        getText(urls, args[2])
    else:
        urls = getURLs(args[1], True)
        urls = loadURLs()
        getText(urls, args[2])
