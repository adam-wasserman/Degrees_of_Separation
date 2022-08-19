#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 12:43:16 2022

@author: adamwasserman

The purpose of this dataset is to create an database from the IMDb TSV files I downloaded
that I can use to quickly access information remotely.
"""

import sqlite3 as sql
import csv

def createSQLDatabase():
    
    open("data/degrees.db",'w').close()
    con = sql.connect('data/degrees.db')
    
    con.execute('''CREATE TABLE actors
               (id INTEGER, name TEXT, PRIMARY KEY(id))''')
    con.execute('''CREATE TABLE movies
                (id INTEGER, title TEXT, PRIMARY KEY(id))''')
    con.execute('''CREATE TABLE edges
                (movie_id INTEGER, actor_id INTEGER, FOREIGN KEY(movie_id) REFERENCES movies(id), FOREIGN KEY(actor_id) REFERENCES actors(id))''')
    
    with open("data/edges.csv",'r') as read_file:
        reader = csv.reader(read_file)
        cmd = 'INSERT INTO edges (movie_id, actor_id) VALUES (?,?)'
        for row in reader:
            movie = row[0]
            actors = row[1:]
            for actor in actors:
                con.execute(cmd,(int(movie),int(actor)))
    
    with open("data/name_keys.csv",'r') as read_file:
        reader = csv.reader(read_file)
        cmd = 'INSERT INTO actors (id, name) VALUES (?,?)'
        for row in reader:
            con.execute(cmd,(int(row[0]),row[1]))
    
    with open("data/movie_id_titles.csv",'r') as read_file:
        reader = csv.reader(read_file)
        cmd = 'INSERT INTO movies (id, title) VALUES (?,?)'
        for row in reader:
            try:
                int(row[0])
            except ValueError:
                continue
            else:
                con.execute(cmd,(int(row[0]),row[1]))
                
    con.commit()
    con.close()
    