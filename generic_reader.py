#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Periphery'

from conv import *


def getGenericSents(fIn):
    data = getContent(fIn).split("\r\n")
    if len(data)<=1:
        data = getContent(fIn).split("\n")

    allSent = {}
    ix = 1
    # Read row by row starting from sentence number 1
    sent = []
    for row in data:
        if len(row)==0:
            allSent[ix] = sent
            ix += 1
            sent = []
        else:
            sent.append(row)
    return allSent


def writeGenericSents(file_path, sentences):
    fout = codecs.open(file_path, "w", "utf-8")
    i = 0
    for sentence in sentences:
        for line in sentence:
            fout.write(line+u'\n')
        i+=1
        if i!=len(sentences):
            fout.write(u'\n')
    fout.close()