#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import unicodedata
import mojimoji as moji


def normalizeChar(text):
    # 全角カナ，半角数字，半角記号に変換
    zen = moji.han_to_zen(text, digit=False, ascii=False)
    return moji.zen_to_han(zen, kana=False)


def normalizeNum(text):
    # 数字を０に変換
    return re.sub(r'\d+\.*\d*', '0', text)


def isSymbol(c):
    # 記号かどうか
    return c not in {
        'Lu',
        'Ll',
        'Lt',
        'Lm',
        'Lo',
        'Nd',
        'Nl',
        'No',
        'So'
    }
    # return c in {'Ps', 'Po', 'Pe', 'Zs', 'So', 'Sm', 'Cc'}


def removeSymbol(text):
    # 記号を/に変換
    result = ''
    prev = ''
    for c in text:
        code = unicodedata.category(c)
        if isSymbol(code):
            if not isSymbol(prev):
                result += '/'
        else:
            result += c
        prev = code
    return result
