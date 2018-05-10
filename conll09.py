#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Periphery'

from conv import *
notMatched = 0

# sesli dusmesi special cases
specialStuff = {}
specialStuff[u'çağrıl'] = u'çağır'
specialStuff[u'savrul'] = u'savur'
specialStuff[u'kavrul'] = u'kavur'
specialStuff[u'ayrıl'] = u'ayır'
specialStuff[u'onul'] = u'ona'
specialStuff[u'ediver'] = u'et' # ud is wrong
specialStuff[u'kon'] = u'koy'

#conll09 structure
class conll09Row:
    id = 0
    def __init__(self, id):
        self.id = id
        self.word = ''
        self.lemma = ''
        self.plemma = ''
        self.pos = ''
        self.ppos = ''
        self.feats = ''
        self.pfeats = ''
        self.head = ''
        self.phead = ''
        self.deprel = ''
        self.pdeprel = ''
        self.isPredicate = False
        self.predicateSense = ''
        self.predIx = 0
        # idx: predicate
        # label: argLabel
        # argDict[1]='A0'
        self.argDict = {}
        self.isArg = False

class conll09Sent:
    # sentence id
    idx = 0
    def __init__(self, idx):
        # sentence id
        self.idx = idx
        # predicates in form of conll09 row
        self.predicates = []
        # conll09rows
        self.rows = []
        self.args = []
        self.colSize = 0
        self.original_lines = []

    def printSent(self):
        text = ''
        for r in self.rows:
            text += (r.word+' ')
        print text

#CONLLUD Rows
class conllUDRow:
    id = 0
    def __init__(self, id):
        self.id = id
        self.word = ''
        self.lemma = ''
        self.pos = ''
        self.ppos = ''
        self.feats = ''
        self.head = ''
        self.phead = ''
        self.deprel = ''
        self.pdeprel = ''
        # they will be empty in the first pass
        self.isPredicate = False
        self.predicateSense = ''
        self.predIx = 0
        self.misc =  ''
        # idx: predicate
        # label: argLabel
        # argDict[1]='A0'
        self.argDict = {}
        self.numberOfFields = 0

class conllUDSent:
    # sentence id
    idx = 0
    def __init__(self, idx):
        # sentence id
        self.idx = idx
        # predicates in form of conllud row
        self.predicates = []
        self.args = []
        # conlludrows
        self.rows = []
        # multiple span rows
        self.multirows = []
        self.lastDerivIds = []
        self.firstDerivIds = []
        # maps conll09 predicate indexes(1,2,3) to conllud predicate indexes
        self.predIndxMap = {}

    def printSent(self):
        text = ''
        for r in self.rows:
            text += (r.word+' ')
        print text

def getConll09Sents(fIn):
    data = getContent(fIn).split("\n")
    allSent = []
    ix = 1
    pixCnt = 1
    # sentence number 1
    sent = conll09Sent(ix)
    for row in data:
        if len(row)==0:
            allSent.append(sent)
            # new sentence
            ix += 1
            # predicate index counter for the new sentence
            # starts from 1
            pixCnt = 1
            sent = conll09Sent(ix)
        else:
            # resolve data
            cols = row.split("\t")
            sent.colSize = len(cols)
            sent.original_lines.append(cols)
            # new row in a sentence
            row = conll09Row(cols[0])
            row.word = cols[1]
            row.lemma = cols[2]
            row.plemma = cols[3]
            row.pos = cols[4]
            row.ppos = cols[5]
            row.feats = cols[6]
            row.pfeats = cols[7]
            row.head = cols[8]
            row.phead = cols[9]
            row.deprel = cols[10]
            row.pdeprel = cols[11]
            # 12: Y if it is a predicate
            row.isPredicate = (cols[12]=='Y')
            row.predicateSense = cols[13]
            for i in range(14,len(cols)):
                offset = 13
                rix = i-offset
                if(not (cols[i].startswith('_'))):
                    # then it is an argument of some predicate of index rix
                    row.argDict[rix]= cols[i]
                    row.isArg = True
                    if not sent.args.__contains__(row):
                        sent.args.append(row)
            if row.isPredicate:
                row.predIx = pixCnt
                pixCnt += 1
                # store in predicates
                sent.predicates.append(row)
            sent.rows.append(row)
    return allSent

def getConll09SentNoAnnot(fIn):
    data = getContent(fIn).split("\r\n")
    if len(data)<=1:
        data = getContent(fIn).split("\n")
    allSent = []
    ix = 1
    pixCnt = 1
    # sentence number 1
    sent = conll09Sent(ix)
    for row in data:
        if len(row)==0:
            allSent.append(sent)
            # new sentence
            ix += 1
            # predicate index counter for the new sentence
            # starts from 1
            pixCnt = 1
            sent = conll09Sent(ix)
        else:
            # resolve data
            cols = row.split("\t")
            sent.original_lines.append(cols)
            # new row in a sentence
            row = conll09Row(cols[0])
            row.word = cols[1]
            row.lemma = cols[2]
            row.plemma = cols[2]
            row.pos = cols[3]
            row.ppos = cols[4]
            row.feats = cols[5]
            row.pfeats = cols[5]
            row.head = cols[6]
            row.phead = cols[6]
            row.deprel = cols[7]
            row.pdeprel = cols[7]
            sent.rows.append(row)
    return allSent

def getUDSentAnnot(fIn):
    data = getContent(fIn).split("\n")
    allSent = []
    ix = 1
    pixCnt = 1
    # sentence number 1
    sent = conll09Sent(ix)
    for row in data:
        if len(row)==0:
            allSent.append(sent)
            # new sentence
            ix += 1
            # predicate index counter for the new sentence
            # starts from 1
            pixCnt = 1
            sent = conll09Sent(ix)
        else:
            # resolve data
            cols = row.split("\t")
            sent.original_lines.append(cols)
            # new row in a sentence
            row = conll09Row(cols[0])
            row.word = cols[1]
            row.lemma = cols[2]
            row.plemma = cols[2]
            row.pos = cols[3]
            row.ppos = cols[4]
            row.feats = cols[5]
            row.pfeats = cols[5]
            row.head = cols[6]
            row.phead = cols[6]
            row.deprel = cols[7]
            row.pdeprel = cols[7]
            sent.rows.append(row)
    return allSent

def getUDSentNoAnnot(fIn):
    data = getContent(fIn).split("\n")
    allSent = []
    ix = 1
    pixCnt = 1
    # sentence number 1
    sent = conll09Sent(ix)
    for row in data:
        if len(row)==0:
            allSent.append(sent)
            # new sentence
            ix += 1
            # predicate index counter for the new sentence
            # starts from 1
            pixCnt = 1
            sent = conll09Sent(ix)
        else:
            # resolve data
            cols = row.split("\t")
            sent.original_lines.append(cols)
            # new row in a sentence
            row = conll09Row(cols[0])
            row.word = cols[1]
            row.lemma = cols[2]
            row.plemma = cols[2]
            row.pos = cols[3]
            row.ppos = cols[4]
            row.feats = cols[5]
            row.pfeats = cols[5]
            row.head = cols[6]
            row.phead = cols[6]
            row.deprel = cols[7]
            row.pdeprel = cols[7]
            sent.rows.append(row)
    return allSent

def getConllUDSents(fIn):
    data = getContent(fIn).split("\n")
    allSent = []
    ix = 1
    pixCnt = 1
    # sentence number 1
    sent = conllUDSent(ix)
    for row in data:
        if len(row)==0:
            allSent.append(sent)
            # new sentence
            ix += 1
            pixCnt = 1
            sent = conllUDSent(ix)
        else:
            # resolve data
            cols = row.split("\t")
            # new row in a sentence
            if(not cols[0].__contains__('-')):
                row = conllUDRow(cols[0])
                row.word = cols[1]
                row.lemma = cols[2]
                row.pos = cols[3]
                row.ppos = cols[4]
                row.feats = cols[5]
                row.head = cols[6]
                row.deprel = cols[7]
                sent.rows.append(row)
            else:
                row = conllUDRow(cols[0])
                row.word = cols[1]
                row.lemma = cols[2]
                row.pos = cols[3]
                row.ppos = cols[4]
                row.feats = cols[5]
                row.head = cols[6]
                row.deprel = cols[7]
                sent.multirows.append(row)
                # add ids to multirowIds
                allInd = cols[0].split("-")
                findx = int(allInd[0])
                lastx = int(allInd[-1])
                sent.firstDerivIds.append(findx)
                sent.lastDerivIds.append(lastx)
            row.numberOfFields = len(cols)
            if(len(cols)>10):
                # include predicate information
                row.isPredicate = (cols[10]=='Y')
                row.predicateSense = cols[11]
                for i in range(12,len(cols)):
                    offset = 11
                    rix = i-offset
                    if(not (cols[i].startswith('_'))):
                        # then it is an argument of some predicate of index rix
                        row.argDict[rix]= cols[i]
                        row.isArg = True
                        if not sent.args.__contains__(row):
                            sent.args.append(row)
                if row.isPredicate:
                    row.predIx = pixCnt
                    pixCnt += 1
                    # store in predicates
                    sent.predicates.append(row)
    return allSent

def writeConllUDSents(fOut, sentsUD):
    content = []
    for sent in sentsUD:
        for row in sent.rows:
            cols = []
            cols.append(row.id)
            cols.append(row.word)
            cols.append(row.lemma)
            cols.append(row.pos)
            cols.append(row.ppos)
            cols.append(row.feats)
            cols.append(row.head)
            cols.append(row.deprel)
            #lis of secondary dependencies (empty)
            cols.append('_')
            if(len(row.misc)>0):
                cols.append(row.misc)
            else:
                cols.append('_')
            if(row.isPredicate):
                cols.append('Y')
                cols.append(row.predicateSense)
            else:
                cols.append('_')
                cols.append('_')
            for i in range(1, len(sent.predicates)+1):
                if(i in row.argDict):
                    label = row.argDict[i]
                    cols.append(label)
                else:
                    cols.append('_')
            rowStr = '\t'.join(cols)
            content.append(rowStr)
        content.append('')
    writeContent(fOut, content)
