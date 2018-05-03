#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Periphery'

from conll09 import *
from random import *
from difflib import SequenceMatcher

def reverse_dict(old_dict):
    new_dict={}
    for k in old_dict:
        v = old_dict[k]
        new_dict[v] = k
    return new_dict

def is_similar(w1, w2):
    r = SequenceMatcher(None, w1, w2).ratio()
    return True if r>0.5 else False

def print_sentence(sent):
    line = []
    for row in sent.rows:
        line.append(row.word)
    linestr = " ".join(line)
    print linestr+"\n"

def get_sent_score(s1, s2):
    # Check 8 random rows
    total = len(s1.rows)
    items = range(0,len(s1.rows))
    rand_ixs = sample(items, total)

    if len(s1.rows)!=len(s2.rows):
        return False

    for x in rand_ixs:
        # check if words match
        word = s1.rows[x].word
        found = False
        for row in s2.rows:
            if word.lower()==row.word.lower():
                found = True
                break
        if not found:
            return False

    return True

def get_sent_score_tolerant(s1, s2):
    # Match the shorter one
    if len(s1.rows)<len(s2.rows):
        shorter = s1
        longer = s2
    else:
        shorter = s2
        longer = s1

    total = len(shorter.rows)
    items = range(0,len(shorter.rows))
    rand_ixs = sample(items, total)

    for x in rand_ixs:
        # check if words match
        word = shorter.rows[x].word
        found = False
        for row in longer.rows:
            if (word.lower()==row.word.lower()):
                found = True
                break
        if not found:
            return False

    return True

def get_sent_score_very_tolerant(s1, s2):
    # Match the shorter one
    if len(s1.rows)<len(s2.rows):
        shorter = s1
        longer = s2
    else:
        shorter = s2
        longer = s1

    total = len(shorter.rows)
    items = range(0,len(shorter.rows))
    rand_ixs = sample(items, total)

    for x in rand_ixs:
        # check if words match
        word = shorter.rows[x].word
        found = False
        for row in longer.rows:
            if is_similar(word.lower(),row.word.lower()):
                found = True
                break
        if not found:
            return False

    return True

def get_matching_sentence(sent, sents09_old, sentence_map):

    for s in sents09_old:
        # if it has been matched before, skip
        if s.idx in sentence_map:
            continue
        if get_sent_score(sent, s):
            return s.idx
    return -1

def get_matching_sentence_tolerant(sent, sents09_old, sentence_map):

    for s in sents09_old:
        # if it has been matched before, skip
        if s.idx in sentence_map:
            continue
        if get_sent_score_tolerant(sent, s):
            return s.idx
    return -1

def get_matching_sentence_very_tolerant(sent, sents09_old, sentence_map):

    for s in sents09_old:
        # if it has been matched before, skip
        if s.idx in sentence_map:
            continue
        #print_sentence(s)
        if get_sent_score_very_tolerant(sent, s):
            return s.idx
    return -1

def transfer_annot(source, target):
    '''
    :param source: old conll09 sentence
    :param target: new conll09 sentence
    :return: new annotated sentence
    '''
    shorter = True if len(target.rows)<len(source.rows) else False
    i = 0
    j = 0
    notFinished = True
    colSize = source.rows[0]
    while(notFinished):
        tr = target.rows[i]
        sr = source.rows[j]
        if tr.word==sr.word:
            #tr.append(sr[12:])
            print "match"
            i+=1
            j+=1
        else:
            if shorter:
                j+=1
            else:
                i+=1
                # annotate with dummy symbols
                #[tr.append('_') for i in range(12,source.colSize+1)]
                print "annotate with dummy symbols"
        if i==len(target.rows):
            notFinished = False

    return None

def get_the_first_matching_row(tword,source,row_map,i):
    matchidx = -1
    for j in range(len(source.rows)):
        if j in row_map:
            continue
        if abs(i-j)>4:
            continue
        if source.rows[j].word==tword:
            matchidx = j
            break
        # Manual
        if tword==u'iste' and source.rows[j].word==u'işte':
            matchidx = j
            break
        if tword==u'Mahkemesi\'ndeki' and source.rows[j].word==u'mahkemesindeki':
            matchidx = j
            break
        if tword==u'Vanlidir' and source.rows[j].word==u'Van\'lıdır':
            matchidx = j
            break
        if tword==u'özenle' and source.rows[j].word==u'özen':
            matchidx = j
            break
        if tword==u'öne' and source.rows[j].word==u'önü':
            matchidx = j
            break
    return matchidx

def get_the_first_matching_row_ud(tword,source,row_map,i):
    matchidx = -1
    for j in range(len(source.rows)):
        if j in row_map:
            continue
        if abs(i-j)>4:
            continue
        if source.rows[j].word==tword or source.rows[j].word.lower()==tword.lower():
            matchidx = j
            break
        # Manual
        if tword==u'örünendir' and source.rows[j].word==u'görünen':
            matchidx = j
            break
        if tword==u'bizle' and source.rows[j].word==u'bizim':
            matchidx = j
            break
        if tword==u'Şarkıcıyı' and source.rows[j].word==u'ŞARKICIYI':
            matchidx = j
            break
        if tword==u'çinse' and source.rows[j].word==u'se':
            matchidx = j
            break
        if tword==u'öne' and source.rows[j].word==u'önü':
            matchidx = j
            break
        if tword==u'ibiydi' and source.rows[j].word==u'ydi':
            matchidx = j
            break
        if tword==u'ibiyim' and source.rows[j].word==u'yim':
            matchidx = j
            break
        if tword==u'adardı' and source.rows[j].word==u'dı':
            matchidx = j
            break
        if tword==u'Şikel' and source.rows[j].word==u'Şıkel':
            matchidx = j
            break
        if tword==u'ce' and source.rows[j].word==u'bilinçsizce':
            matchidx = j
            break
        if tword==u'diyince' and source.rows[j].word==u'deyince':
            matchidx = j
            break
        if tword==u'öneliktir' and source.rows[j].word==u'tir':
            matchidx = j
            break
        if tword==u'itti' and source.rows[j].word==u'ti':
            matchidx = j
            break
        if tword==u'ikibinüç' and source.rows[j].word==u'ikibinuc':
            matchidx = j
            break
        if tword==u'altı' and source.rows[j].word==u'alti':
            matchidx = j
            break
        if tword==u'liralık' and source.rows[j].word==u'lık':
            matchidx = j
            break
        if tword==u'ca' and source.rows[j].word==u'yalnızca':
            matchidx = j
            break
        if tword==u'uğraşıyor' and source.rows[j].word==u'UĞRAŞIYOR':
            matchidx = j
            break
        if tword==u'aradı' and source.rows[j].word==u'ARADI':
            matchidx = j
            break
        if tword==u'landır' and source.rows[j].word==u'dır':
            matchidx = j
            break
        if tword==u'ca' and source.rows[j].word==u'Onca':
            matchidx = j
            break
        if tword==u'Katana' and source.rows[j].word==u'a':
            matchidx = j
            break
        if tword==u'duyumsat�nca' and source.rows[j].word==u'duyumsatınca':
            matchidx = j
            break
        if tword==u'iste' and source.rows[j].word==u'işte':
            matchidx = j
            break
        if tword==u'kilometrelik' and source.rows[j].word==u'lik':
            matchidx = j
            break
        if tword==u'alıveriş' and source.rows[j].word==u'alışveriş':
            matchidx = j
            break
        if tword==u'dür' and source.rows[j].word==u'üdür':
            matchidx = j
            break
        if tword==u'adarız' and source.rows[j].word==u'ız':
            matchidx = j
            break
        if tword==u'9.8\'lik' and source.rows[j].word==u'\'lik':
            matchidx = j
            break
        if tword==u'ce' and source.rows[j].word==u'Delice':
            matchidx = j
            break
        if tword==u'3\'lük' and source.rows[j].word==u'\'lük':
            matchidx = j
            break
        if tword==u'ce' and source.rows[j].word==u'isteksizce':
            matchidx = j
            break
        if tword==u'yüzon' and source.rows[j].word==u'yuzon':
            matchidx = j
            break
        if tword==u'irmibeş\'lik' and source.rows[j].word==u'\'lik':
            matchidx = j
            break
        if tword==u'ibidir' and source.rows[j].word==u'dir':
            matchidx = j
            break
        if tword==u'ça' and source.rows[j].word==u'uzakça':
            matchidx = j
            break
        if tword==u'ca' and source.rows[j].word==u'onca':
            matchidx = j
            break
        if tword==u'trilyonluk' and source.rows[j].word==u'luk':
            matchidx = j
            break
        if tword==u'eneyebiliriz' and source.rows[j].word==u'iz':
            matchidx = j
            break
        if tword==u'akınırım' and source.rows[j].word==u'ım':
            matchidx = j
            break
        if tword==u'ibiydim' and source.rows[j].word==u'ydim':
            matchidx = j
            break
        if tword==u'ca' and source.rows[j].word==u'sonsuzca':
            matchidx = j
            break
        if tword==u'anlışlanabilirlik' and source.rows[j].word==u'lik':
            matchidx = j
            break
        if tword==u'öylenirse' and source.rows[j].word==u'se':
            matchidx = j
            break
        if tword==u'ittir' and source.rows[j].word==u'tir':
            matchidx = j
            break
        if tword==u'çindi' and source.rows[j].word==u'di':
            matchidx = j
            break
        if tword==u'ürkçedeki' and source.rows[j].word==u'ki':
            matchidx = j
            break
        if tword==u'ıkabilirdik' and source.rows[j].word==u'dik':
            matchidx = j
            break
        if tword==u'zereydim' and source.rows[j].word==u'ydim':
            matchidx = j
            break
        if tword==u'yarışım' and source.rows[j].word==u'YARIŞIM':
            matchidx = j
            break
        if tword==u'anlışlanabilirliği' and source.rows[j].word==u'liği':
            matchidx = j
            break
        if tword==u'ki' and source.rows[j].word==u'ürkçedeki':
            matchidx = j
            break
        if tword==u'ce' and source.rows[j].word==u'ilgisizce':
            matchidx = j
            break
        if tword==u'Marks\'ın' and source.rows[j].word==u's\'ın':
            matchidx = j
            break
        if tword==u'kadarıyla' and source.rows[j].word==u'ıyla':
            matchidx = j
            break
        if tword==u'ce' and source.rows[j].word==u'delice':
            matchidx = j
            break
        if tword==u'ca' and source.rows[j].word==u'çılgınca':
            matchidx = j
            break
        if tword==u'özenle' and source.rows[j].word==u'özen':
            matchidx = j
            break
        if tword==u'na' and source.rows[j].word==u'geçersiz':
            matchidx = j
            break
        if tword==u'yirmibeş\'lik' and source.rows[j].word==u'\'lik':
            matchidx = j
            break
        if tword==u'yüzdokuz.' and source.rows[j].word==u'yüzdokuz':
            matchidx = j
            break
        if tword==u'ca' and source.rows[j].word==u'aptalca':
            matchidx = j
            break
    return matchidx

def annotate_sentence(source, target, row_map):
    lines = []
    semLines = []
    for i in range(len(target.rows)):
        line = target.original_lines[i]
        # how many columns will we add ?
        sem_col_size = source.colSize-12
        # get matching row
        si = row_map[i]
        if si==-1:
            sem_cols = [u'_']*sem_col_size
        else:
            sem_cols = source.original_lines[si][12:]
        for j in range(len(sem_cols)):
            line.append(sem_cols[j])
        lines.append(line)
        semLines.append(sem_cols)
    return lines, semLines

def annotate_sentence_ud(source, target, row_map):
    lines = []
    semLines = []
    for i in range(len(target.rows)):
        line = target.original_lines[i]
        # how many columns will we add ?
        sem_col_size = source.colSize-10
        # get matching row
        si = row_map[i]
        if si==-1:
            sem_cols = [u'_']*sem_col_size
        else:
            sem_cols = source.original_lines[si][10:]
        for j in range(len(sem_cols)):
            line.append(sem_cols[j])
        lines.append(line)
        semLines.append(sem_cols)
    return lines, semLines


def annotate_dummy(target):
    lines = []
    semLines = []
    for i in range(len(target.rows)):
        line = target.original_lines[i]
        sem_col_size = 2
        sem_cols = [u'_']*sem_col_size
        for j in range(len(sem_cols)):
            line.append(sem_cols[j])
        lines.append(line)
        semLines.append(sem_cols)
    return lines, semLines

def transfer_annot_simple(source, target):
    row_map = {}
    reverse_row_map = {}

    for i in range(len(target.rows)):
        tword = target.rows[i].word
        sidx = get_the_first_matching_row(tword,source,row_map,i)
        reverse_row_map[i]=sidx
        row_map[sidx]=i

    ann_sent = annotate_sentence(source,target,reverse_row_map)
    return ann_sent


def transfer_annot_simple_ud(source, target):
    row_map = {}
    reverse_row_map = {}

    for i in range(len(target.rows)):
        tword = target.rows[i].word
        sidx = get_the_first_matching_row_ud(tword,source,row_map,i)
        reverse_row_map[i]=sidx
        row_map[sidx]=i

    ann_sent = annotate_sentence_ud(source,target,reverse_row_map)
    return ann_sent