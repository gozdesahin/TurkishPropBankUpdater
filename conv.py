__author__ = 'Periphery'
# encoding: utf-8

import codecs

# file related stuff
def getContent(file_path):
    fin = codecs.open(file_path, encoding='utf-8')
    strIn = fin.read()
    fin.close()
    return strIn

def writeContent(file_path, content):
    fout = codecs.open(file_path, "w", "utf-8")
    for n in content:
        fout.write(n+'\n')
    fout.close()

def writeToFile(file_path, sentences):
    fout = codecs.open(file_path, "w", "utf-8")
    i = 0
    for sentence in sentences:
        for line in sentence:
            linestr=u"\t".join(line)
            fout.write(linestr+u'\n')
        i+=1
        if i!=len(sentences):
            fout.write(u'\n')
    fout.close()