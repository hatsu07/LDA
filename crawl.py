import sys
import re
import requests
from bs4 import BeautifulSoup
from collections import deque
from time import sleep


yahoo = 'https://search.yahoo.co.jp/search'


def rmPrint(n):
    '''
    n: n行上の出力を削除
    '''
    sys.stdout.write('\033[' + str(n) + 'F\033[2K\033[G')


def checkResponse(r):
    '''
    r: レスポンス
    HTTPステータスコードのチェック
    '''
    if r.status_code == requests.codes.ok:
        return True
    else:
        rmPrint(1)
        print('Error: HTTP status code is', r.status_code)
        if r.status_code == 999:
            sleep(60 * 60)
        else:
            sleep(60)
    return False


def httpGet(url, params={}, must=False):
    '''
    url: URL
    params: URLパラメータ
    must: HTTPステータスコードがOKになるまでリクエスト
    return: レスポンス
    '''

    i = 0
    while must or i < 5:
        r = requests.get(url, params=params)
        if checkResponse(r):
            return r
        i += 1
    rmPrint(1)
    print('Error: Skipped because of failed 5 times')
    return None


def getURLs(params):
    '''
    params: 検索パラメータ
    return: URL
    Yahooで検索したページのURLを取得
    '''

    res = httpGet(yahoo, params=params, must=True)
    soup = BeautifulSoup(res.text, 'lxml')

    web = soup.find('div', id='web')
    urls = deque([a.get('href') for a in web.findAll('a')])
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
    with open(path, 'a') as f:
        while urls:
            url = urls.popleft()
            rmPrint(1)
            print(n - len(urls), '/', n)
            try:
                res = httpGet(url)
                if not res:
                    continue

                # 本文の抽出
                if 'html' in res.headers['Content-Type']:
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
            sleep(10)


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
        'dups': str(1),
        'b': '01'
    }
    while True:
        print('Page:', int(params['b']) // 10 + 1)

        # Yahoo検索ページのURLを取得
        urls = getURLs(params)
        if not urls:
            break
        sleep(10)

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
