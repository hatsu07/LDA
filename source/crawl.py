#!/usr/bin/env python

import sys
import re
import requests
from bs4 import BeautifulSoup
from collections import deque
from time import sleep
import random


yahoo = 'https://search.yahoo.co.jp/search'


def rmPrint(n):
    '''
    n: n行上の出力を削除
    '''
    sys.stdout.write('\033[' + str(n) + 'F\033[2K\033[G')


def httpGet(url, params={}):
    '''
    url: URL
    params: URLパラメータ
    must: HTTPステータスコードがOKになるまでリクエスト
    return: レスポンス
    '''

    r = requests.get(url, params=params)
    if r.status_code == requests.codes.ok:
        return r
    rmPrint(1)
    print('Error: HTTP status code is', r.status_code)
    return None


def getURLs(params):
    '''
    params: 検索パラメータ
    return: URL: (url, エラー回数)
    Yahooで検索したページのURLを取得
    '''

    while True:
        res = httpGet(yahoo, params=params)
        if res:
            break
        rmPrint(1)
        print('Error: Waiting to request Yahoo')
        sleep(60 * 60)

    soup = BeautifulSoup(res.text, 'lxml')

    web = soup.find('div', id='web')
    urls = deque([(a.get('href'), 0)
                  for a in web.findAll('a') if 'yahoo' not in str(a)])
    print('Num of URLs:', len(urls))
    return urls


def getText(urls, path):
    '''
    urls: Yahoo検索でヒットしたページのURL
    path: WEBテキストの保存ファイル
    ページの本文を取得
    '''

    n = len(urls)
    print('')
    sys.stdout.write('\033[2K\033[G')

    with open(path, 'a') as f:
        while urls:
            url = urls.popleft()
            rmPrint(1)
            print(n - len(urls), '/', n)
            try:
                res = httpGet(url[0])
                if not res:
                    if url[1] > 3:
                        continue
                    rmPrint(1)
                    print('Error: Skipped because of failed Request')
                    urls.append((url[0], url[1] + 1))

                # 本文の抽出
                elif 'html' in res.headers['Content-Type']:
                    res.encoding = res.apparent_encoding
                    soup = BeautifulSoup(res.text, 'lxml')
                    [x.extract() for x in soup.findAll('script')]
                    [x.extract() for x in soup.findAll('style')]
                    text = re.sub(r'[ \t]+', '', soup.getText())
                    text = re.sub(r'[\r\n]+', '/', text)
                    f.write(text + '\n')
            except requests.exceptions.SSLError:
                rmPrint(1)
                print('SSL Error によりスキップ')
            except:
                rmPrint(1)
                print('Error: Exception')
            sleep(random.randint(3, 10))


def crawl(kw):
    '''
    kw: 検索ワード
    クローリング
    '''

    print('Start')

    path = './Corpora/' + kw + '.txt'
    with open(path, 'w') as f:
        f.write('')

    params = {
        'p': kw,
        'ei': 'UTF-8',
        'fl': str(2),
        'b': '01'
    }
    while True:
        print('Page:', int(params['b']) // 10 + 1)
        sys.stdout.write('\033[2K\033[G')

        # Yahoo検索ページのURLを取得
        urls = getURLs(params)
        if not urls:
            break
        sleep(random.randint(5, 50))

        # 本文抽出
        getText(urls, path)

        # 次のページへ
        params['b'] = str(int(params['b']) + 10)
        rmPrint(3)

    print('Finish')


if __name__ == '__main__':
    args = sys.argv
    if len(args) < 2:
        print('Error: 引数が足りません')
        print('ex. python crawl.py 食事')
        exit(0)

    keyword = args[1]

    # 検索ワードでクローリング
    crawl(keyword)
    # 検索ワード+道具でクローリング
    crawl(keyword + '+道具')
    # 検索ワード+方法でクローリング
    crawl(keyword + '+方法')
