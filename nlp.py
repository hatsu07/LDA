#!/usr/bin/env python
# -*- coding: utf-8 -*-
import preprocessing as pre
import mecab
import cabocha


tagger = mecab.Mecab()
parser = cabocha.Cabocha()


def normalize(text):
    # 前処理
    text = pre.normalizeChar(text)
    text = pre.normalizeNum(text)
    text = pre.removeSymbol(text)
    if text:
        return text
    return ''


def parseMorphemes(sent):
    # 形態素解析
    result = tagger.parse(sent)
    return result


def parseSyntax(sent):
    # 係り受け解析
    return parser.parse(sent)


def printMorphemes(morphemes, key=''):
    # 形態素解析の結果表示
    for morpheme in morphemes:
        morpheme.print(key=key)


def printSyntax(syntax, key=''):
    # 係り受け解析の結果表示
    for item in syntax:
        item.print(key=key)


def getWakati(sent, key='surface'):
    lSent = sent.split('/')
    result = []
    for s in lSent:
        if not s:
            continue
        morphemes = parseMorphemes(s)
        wakati = ''
        for morpheme in morphemes:
            if key == 'surface':
                wakati += morpheme.surface + ' '
            elif key == 'stem':
                wakati += morpheme.stem + ' '
            elif key == 'part':
                wakati += morpheme.part + ' '
            elif key == 'subpart1':
                wakati += morpheme.subpart1 + ' '
            elif key == 'form':
                wakati += morpheme.form + ' '
        result.append(wakati[:-1])

    return result
