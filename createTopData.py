#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 23:02:36 2022

@author: adamwasserman

The purpose of this file is to create a data set from the top 250 TV shows and Movies that I
download from the internet using the IMDb Python API
"""

import imdb
import csv

def createDataSet():
    ia = imdb.Cinemagoer()
    
    with open("data/topmoviesNshows.csv",'w') as open_file:
        writer = csv.writer(open_file)
        mov_list = ia.get_top250_movies()
        counter = 0
        for movie in mov_list:
            ia.update(movie)
            actors = [person.personID for person in movie['cast']]
            writer.writerow([movie.movieID] + actors)
            counter +=1
            print(f"Processed {counter} movie")
        
        mov_list = ia.get_top250_tv()
        for movie in mov_list:
            ia.update(movie)
            actors = [person.personID for person in movie['cast']]
            writer.writerow([movie.movieID] + actors)
            counter +=1
            print(f"Processed {counter} movie")
    open_file.close()
    
def createIMDBkeys():
    ia = imdb.Cinemagoer()
    movie_ids = []
    
    with open("data/actor_keys.csv",'w') as open_file:
        writer = csv.writer(open_file)
        mov_list = ia.get_top250_movies()
        counter = 0
        for movie in mov_list:
            ia.update(movie)
            movie_ids.append([movie.movieID,movie['title']])
            for actor in movie['cast']:
                writer.writerow([actor.personID,actor['name']])
            counter += 1
            if counter % 5 == 0:
                print(counter)
        mov_list = ia.get_top250_tv()
        for movie in mov_list:
            ia.update(movie)
            movie_ids.append([movie.movieID,movie['title']])
            for actor in movie['cast']:
                writer.writerow([actor.personID,actor['name']])
            counter += 1
            if counter % 5 == 0:
                print(counter)
                
    open_file.close()
    
    with open("data/movie_keys.csv", 'w') as open_file:
        writer = csv.writer(open_file)
        for movie in movie_ids:
            writer.writerow(movie)
    open_file.close()
    
def purgeRepeats():
    with open("data/actor_keys.csv","r") as read_file, open('data/_actor_keys.csv', 'w') as write_file:
        reader = csv.reader(read_file)
        writer = csv.writer(write_file)
        seen_actors = set()
        for _id, name in reader:
            if _id in seen_actors:
                continue
            seen_actors.add(_id)
            writer.writerow([_id,name])
    read_file.close()
    write_file.close()
        
            