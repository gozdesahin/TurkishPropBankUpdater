#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gözde Gül Şahin'

from generic_reader import *
from merger import *
import pickle
import argparse

def main():
    parser = argparse.ArgumentParser(description='split.py')

    ## Data options
    parser.add_argument('-pbfile', type=str,
                        default='/media/isguderg/Work/Doktora/Data Sets/Yeni_IMST/deneme/imst141.single.conll',
                        help='Türkçe anlamsal etiketlemelerin olduğu dosya')

    opt = parser.parse_args()
    splitFile(opt)

def splitFile(opt):
    sents = getGenericSents(opt.pbfile)

    # Data splits
    trainSents = []
    devSents = []
    testSents = []

    trainMap = reverse_dict(pickle.load(open("sent_map_train.pkl", "rb")))
    devMap = reverse_dict(pickle.load(open("sent_map_dev.pkl", "rb")))
    testMap = reverse_dict(pickle.load(open("sent_map_test.pkl", "rb")))

    # Get training sentences
    for k in trainMap:
        sent_ix = trainMap[k]
        trainSents.append(sents[sent_ix])

    # Get dev sentences
    for k in devMap:
        sent_ix = devMap[k]
        devSents.append(sents[sent_ix])

    # Get test sentences
    for k in testMap:
        sent_ix = testMap[k]
        testSents.append(sents[sent_ix])

    writeGenericSents(opt.pbfile+".train", trainSents)
    writeGenericSents(opt.pbfile+".dev", devSents)
    writeGenericSents(opt.pbfile+".test", testSents)

if __name__ == "__main__":
    main()

