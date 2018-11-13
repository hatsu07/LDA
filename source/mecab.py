#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import MeCab


class Mecab:

    def __init__(self, option=''):
        self.tagger = MeCab.Tagger(
            '-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd ' + option)

    def wakati(self, sentence):
        # 分かち書き
        return self.tagger.parse(sentence)

    def parse(self, sent):
        result = []
        for line in self.tagger.parse(sent).split('\n'):
            vals = re.split(r'[\t,]', line)
            if len(vals) > 7:
                morpheme = Morpheme(vals)
                result.append(morpheme)
        return result

    # def parseWord(self, word):
    #     # 単語のパース
    #     res = self.tagger.parse(word).split('\n')[0]
    #     res = re.split(r'[\t,]', res)
    #     return Morpheme(res)
    #     # return None

    # def parseSent(self, sentence):
    #     # 文章のパース
    #     result = []
    #     words = self.wakati(sentence).split(' ')[:-1]
    #     for word in words:
    #         item = self.parseWord(word)
    #         if item:
    #             result.append(item)
    #     return result


class Morpheme:
    # 表層形   品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用型,活用形,原形,読み,発音

    def __init__(self, result):
        self.surface = result[0]
        self.part = result[1]
        self.subpart1 = result[2]
        self.subpart2 = result[3]
        self.subpart3 = result[4]
        self.type = result[5]
        self.form = result[6]
        self.stem = result[7]

    def print(self, key=''):
        if key == 'surface':
            print(self.surface)
        elif key == 'stem':
            print(self.stem)
        elif key == 'part':
            print(self.part)
        elif key == 'subpart1':
            print(self.subpart1)
        elif key == 'form':
            print(self.form)
        else:
            print(
                self.surface,
                self.part,
                self.subpart1,
                self.subpart2,
                self.subpart3,
                self.type,
                self.form,
                self.stem,
            )
