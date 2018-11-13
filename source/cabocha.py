#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import mecab
import CaboCha


class Cabocha:

    def __init__(self):
        self.c = CaboCha.Parser(
            '-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')

    def parse(self, sent):
        # 係り受け解析

        def spawnSyntax(chunk):
            own = chunk['info'][1]
            post = re.match(r'-*\d+', chunk['info'][2]).group(0)
            morphemes = []
            for morpheme in chunk['morphemes']:
                morphemes.append(mecab.Morpheme(morpheme))
            return Syntax(own, post, morphemes)

        result = self.c.parse(sent).toString(
            CaboCha.FORMAT_LATTICE).split('\n')

        chunk = {'info': [], 'morphemes': []}
        chunks = []
        for line in result:
            l = re.split('[\t, ]', line)
            if l[0] in {'*', 'EOS'}:
                if chunk['morphemes']:
                    chunks.append(spawnSyntax(chunk))

                chunk['info'] = l
                chunk['morphemes'] = []
            else:
                chunk['morphemes'].append(l)
        return chunks


class Syntax:

    def __init__(self, own, post, morphemes):
        self.morphemes = morphemes
        self.own = int(own)
        self.post = int(post)

    def print(self, key=''):
        print('from', self.own, 'to', self.post)
        for morpheme in self.morphemes:
            morpheme.print(key=key)
