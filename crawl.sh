#!/bin/bash

merge() {
	cat ./Corpora/*.txt > ./Corpora/ADL/$1
	rm ./Corpora/*.txt
}

echo 'Start'

python ./source/crawl.py 食事
merge eating.txt

python ./source/crawl.py 整容
python ./source/crawl.py 手洗い
python ./source/crawl.py 洗顔
python ./source/crawl.py 歯磨き
merge grooming.txt

python ./source/crawl.py 清拭
python ./source/crawl.py 入浴
merge bathing.txt

python ./source/crawl.py 更衣
python ./source/crawl.py 着替え
merge dressing.txt

python ./source/crawl.py トイレ動作
python ./source/crawl.py 排泄
merge excreting.txt

echo 'Finish'
