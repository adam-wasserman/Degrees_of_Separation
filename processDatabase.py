#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 19:56:07 2022

@author: adamwasserman

The purpose of this file is to process the IMDb tsv files I downloaded into
smaller files that better fit my needs
"""

import csv

def processNames():
    with open("data/name.basics.tsv",'r') as read_file, open("data/name_keys.csv",'w') as write_file:
        reader = csv.reader(read_file, delimiter ='\t')
        writer = csv.writer(write_file)
        for row in reader:
            if "actor" in row[4] or "actress" in row[4]:
                _id = row[0][2:]
                name = row[1]
                writer.writerow([_id,name])
                
                
def processMovies():
    with open("data/title.basics.tsv",'r') as read_file, open("data/movie_id_titles.csv",'w') as write_file:
        reader = csv.reader(read_file, delimiter ='\t')
        writer = csv.writer(write_file)
        for row in reader:
            _id = row[0][2:]
            name = row[3]
            writer.writerow([_id,name])

def processVectors():
    with open("data/title.principals.tsv",'r') as read_file, open("data/edges.csv",'w') as write_file:
        reader = csv.reader(read_file, delimiter ='\t')
        writer = csv.writer(write_file)
        
        for row in reader:#finds the first actor/actress
            if row[3] == 'actor' or row[3] == 'actress':
                break
        
        movie = row[0][2:]
        actors = []
        actors.append(row[2][2:])
        for row in reader:
            if row[3] == "actress" or row[3] == 'actor':
                if movie != row[0][2:]:
                    writer.writerow([movie] + actors)
                    movie = row[0][2:]
                    actors.clear()
                actors.append(row[2][2:])
        writer.writerow([movie] + actors)
        
# =============================================================================
#                 movie = row[0][2:]
#                 name = row[2][2:]
#                 writer.writerow([movie,name])
#                 
# =============================================================================
    