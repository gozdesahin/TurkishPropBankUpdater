#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gözde Gül Şahin'

from generic_reader import *
from merger import *
import pickle
import argparse

def main():
    parser = argparse.ArgumentParser(description='add_cols.py')

    ## Data options
    parser.add_argument('-annImstFile', type=str,
                        default='/media/isguderg/Work/Doktora/Data Sets/Yeni_IMST/imst_son/09/imst141.single.conll.merged',
                        help='Türkçe anlamsal etiketlemelerin olduğu dosya')

    opt = parser.parse_args()
    addCols(opt)

def addCols(opt):
    sents = getGenericSents(opt.annImstFile)
    file_path = opt.annImstFile+".aug"
    fout = codecs.open(file_path, "w", "utf-8")
    i = 0
    for sentence in sents.values():
        for line in sentence:
            cols = line.split(u"\t")
            newcols = []
            for i in range(len(cols)):
                if i in [2,5,6,7]:
                    newcols.append(cols[i])
                    newcols.append(cols[i])
                elif i in [8,9]:
                    continue
                else:
                    newcols.append(cols[i])
            line = u"\t".join(newcols)
            fout.write(line+u'\n')
        i+=1
        if i!=len(sents):
            fout.write(u'\n')
    fout.close()

if __name__ == "__main__":
    main()

