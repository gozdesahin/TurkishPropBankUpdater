#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gözde Gül Şahin'

from merger import *
import pickle
import os
import argparse
import os.path
import sys

def main():
    parser = argparse.ArgumentParser(description='updateUDSemantics.py')

    ## Data options
    parser.add_argument('-oldPBUDFile', type=str,
                        default='/media/isguderg/Work/Doktora/Data Sets/Yeni_IMST/pb/ud/trpb_ud_v1.1.conllu',
                        help='Türkçe anlamsal etiketlemelerin olduğu UD dosyası')

    parser.add_argument('-newIMSTUDFile', type=str,
                        default='/media/isguderg/Work/Doktora/Data Sets/Yeni_IMST/imst_son/ud/imst141.single.conllu.trimmed',
                        help='Yeni UD dosyası (header olmaması lazım)')

    parser.add_argument('-mappingFile', type=str,
                        default='final_sent_map.pkl',
                        help='Cümle eşleştirmeleri')

    parser.add_argument('-save_dir', type=str,
                        default='/home/isguderg/Documents/mapping_output',
                        help='Kaydedilecek yer')

    opt = parser.parse_args()
    mapSemanticsToIMSTUD(opt)

def mapSemanticsToIMSTUD(opt):

    sentsud_old = getUDSentAnnot(opt.oldPBUDFile)
    sentsud_new = getUDSentNoAnnot(opt.newIMSTUDFile)

    # sentence_map[old_sentence_index]=new_sentence_index
    if(os.path.exists(opt.mappingFile)):
        sentence_map = pickle.load(open(opt.mappingFile, "rb"))
    else:
        sys.exit("First Run update09Semantics to find sentence matches")

    # sentence_map[new_sentence_index]=old_sentence_index
    reverse_sentence_map = reverse_dict(sentence_map)

    annotated_sents = []
    semantic_fields = []

    for i in range(len(sentsud_new)):
        #print i
        nidx = (i+1)
        sent_new = sentsud_new[nidx - 1]
        if nidx in reverse_sentence_map:
            oidx = reverse_sentence_map[nidx]
            sent_old = sentsud_old[oidx-1]
            #print_sentence(sent_old)
            #print_sentence(sent_new)
            annot_sent, ann = transfer_annot_simple_ud(sent_old, sent_new)
            annotated_sents.append(annot_sent)
            semantic_fields.append(ann)
        # No annotation exists for the sentence, just add two columns then
        else:
            annot_sent, ann = annotate_dummy(sent_new)
            annotated_sents.append(annot_sent)
            semantic_fields.append(ann)

    assert len(annotated_sents)==len(sentsud_new)
    assert len(semantic_fields)==len(sentsud_new)

    # Now transfering annotation
    save_dir = opt.save_dir
    try:
        os.stat(save_dir)
    except:
        os.mkdir(save_dir)

    fInud_wsemantic = os.path.join(save_dir, "merged.conllu")
    fInud_osemantic = os.path.join(save_dir, "semantic_layer.conllu")

    # write merged file
    writeToFile(fInud_wsemantic, annotated_sents)

    # write semantic fields only
    writeToFile(fInud_osemantic, semantic_fields)
    print "Done mapping, check output folder"

if __name__ == "__main__":
    main()