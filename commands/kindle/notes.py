#!/usr/bin/env python2.7
import os

def readFileLines(f, strip=True):
    lines = []
    try:
        with open(f) as fi:
            lines = fi.readlines()
            if strip: lines = [l.decode("utf-8-sig").strip() for l in lines];
    except:
        pass
    return lines

def splitAtEquals(lines):
    l = []
    found = []
    for line in lines:
        if set(line[:]) == set("="):
            l.append(found)
            found = []
        else: found.append(line)
    return l

def typeAndLocationForClip(clip):
    info = clip.split("|")[0]
    t = info.split(" ")[2]
    l = " ".join(info.split(" ")[4:6])
    return t,l

def clippingList(d=os.environ['KINDLE_DIR']):
    clips = readFileLines(d+"/My Clippings.txt")
    clips = splitAtEquals(clips)
    books = {}
    for clip in clips:
        b = clip[0]
        t,l = typeAndLocationForClip(clip[1])
        q = "\n".join(clip[2:])[1:]
        c = {"book":b, "type": t, "location": l, "text":q}
        if b not in books: books[b] = []
        books[b].append(c)
    return books

def printClippingList(l):
    for book in l:
        print "# "+book
        print ""
        for q in l[book]:
            s = "\""+q["text"]+"\""+ " ("+q["type"]+", "+q["location"]+")"
            print s.encode('utf-8')
            print ""
        print ""

def clippings():
    clips = clippingList()
    printClippingList(clips)

if __name__ == '__main__':
    clippings()
