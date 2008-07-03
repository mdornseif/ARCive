#!/usr/bin/env python
# encoding: utf-8
"""
tools.py

Created by Maximillian Dornseif on 2008-06-05.
Copyright (c) 2008 HUDORA. All rights reserved.
"""

import sys
import re
import unittest


def build_ngramms(l, n=3):
    ret = []
    for terms in l:
        terms = terms.split()
        while len(terms) >= n:
            ret.append(terms[:n])
            terms = terms[1:]
    return ret
    

def read_list(filename):
    fd = open(filename)
    ret = []
    for line in fd:
        if not line.startswith('#'):
            ret.append(line.strip())
    return ret


def normalize_list(l):
    split_re = re.compile(r'[^\w@\.-]', re.UNICODE)
    ret = []
    for line in l:
        # clean up lines
        line = line.strip().lower()
        ret.append(' '.join(' '.join([x for x in split_re.split(line)if len(x) > 2]).split()))
    return ret


def terms_from_file(filename):
    terms = []
    termdata = normalize_list(read_list(filename))
    # use the terms as they are found in the original file
    terms.extend(termdata)
    # add Ngramms
    terms.extend([' '.join(x) for x in build_ngramms(termdata,5)])
    terms.extend([' '.join(x) for x in build_ngramms(termdata,4)])
    terms.extend([' '.join(x) for x in build_ngramms(termdata,3)])
    terms.extend([' '.join(x) for x in build_ngramms(termdata,2)])
    # add variations
    terms.extend([x.replace('-', ' ').replace('@', ' ').replace('.', ' ') for x in termdata])
    return sorted(set(terms))
    