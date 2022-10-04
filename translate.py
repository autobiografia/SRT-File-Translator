#!/usr/bin/python3

# /* Made by @heyo v0.9 */

import re
from googletrans import Translator
import argparse
import pysrt
import os
import glob
import shutil
import sys
import time
from datetime import datetime
import tempfile

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def message(msg):
    cls()
    print(msg)
    
def filebyfile(path):
    srtfiles = []
    for dirpath, dirnames, files in os.walk(os.path.abspath(path)):
        for f in files:
            if os.path.splitext(f)[1] == '.srt':
                fullpath = os.path.join(dirpath, f)
                srtfiles.append(fullpath)
    if not srtfiles:
        print("There is no srt file on this path! Exiting...")
        sys.exit(2)
    return srtfiles

def translate(input, output, languaget):
    translator = Translator()
    message(input + " -- WAIT")
    subs = pysrt.open(input)
    elements = []
    for index, sub in enumerate(subs):
        entry = {'index': sub.index, 'start_time': sub.start, 'end_time': sub.end, 'text': sub.text}
        try:
            translated = translator.translate(sub.text, dest=languaget)
            entry['text'] = translated.text
        except:
            message(input + " -- There are some texts that aren't translated")
        finally:
            elements.append(entry)  
    with open(output, 'w', encoding = "utf8") as fileresp:
        for element in elements:
            try:
                fileresp.write(f"{element['index']}\n{element['start_time']} --> {element['end_time']}\n{element['text']}\n\n")
            except:
                pass
    fileresp.close()
    message(input + " -- OK!!")
def parsefiles(inputFile, languageTo):
    sstr = []
    if languageTo == None:
        languageTo = "pt"
    path = inputFile and inputFile or os.curdir
    srtFiles = filebyfile(path)
    for inputFile in srtFiles:
        outputFile = inputFile.replace(".srt", "") +  "-" + languageTo.upper() + '.srt'
        tempFile = tempfile.NamedTemporaryFile(suffix='.srt',delete=False)
        shutil.copyfile(inputFile,tempFile.name)
        shutil.copyfile(inputFile, outputFile)
        try:
            translate(inputFile, outputFile, languageTo)
            sstr.append(inputFile+' -- OK!!')
        except:
            sstr.append(inputFile+' -- Fail')
    cls()
    print('\n'.join(sstr))
def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-p', '--path', action="store", help="takes the path", metavar="DIR")
    parser.add_argument('-lt', '--language-to', action="store", help="language to translate to")
    args = parser.parse_args()
    parsefiles(args.path, args.language_to)

if __name__ == '__main__':
    main()
    