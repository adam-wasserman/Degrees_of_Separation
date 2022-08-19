#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 17:37:40 2022

@author: adamwasserman

Run a dynamic graph through the IMDb database. VERY SLOW!
"""

import imdb
from collections import deque
import copy


#DI
def dijkstra(act1, act2):
    ia = imdb.Cinemagoer()
    
    p1 = ia.search_person(act1)[0]
    ia.update(p1,['filmography'])
    film = p1['filmography'].get('actor')
    film = film if film else p1['filmography']['actress']
    
    p2 = ia.search_person(act2)[0]
    p2_id = p2.personID
    
    visited = {}
    # ONLY FIND A SINGLE SHORTEST PATH (MORE MIGHT EXIST)^^
    to_visit = deque()
    to_visit.append(p1['imdbID'])
    visited[p1['imdbID']] = None
    
    num = 0
    actors = 0
    
    while to_visit:
        cur = to_visit.popleft()
        actors += 1
        if cur == p2_id:
            path = []
            while visited[cur]:
                prev,movieID = visited[cur]
                path.append((cur,movieID))
                cur = prev
            return path[::-1]
        
        cur_films = ia.get_person(cur)['filmography']
        cur_films = cur_films['actor'] if cur_films.get('actor', False) else cur_films['actress']
        for film in cur_films:
            ia.update(film)
            for person in film['cast']:
                if not person.personID in visited:
                    visited[person.personID] = film.movieID
                    to_visit.append(person.personID)
            num += 1
            print(f"Processed {num} films: {film['title']}")
        print(f"Actors seen: {actors}")

def neighborIntersection(act1, act2):
    ia = imdb.Cinemagoer()
    
    p1 = ia.search_person(act1)[0]
    p2 = ia.search_person(act2)[0]
    
    focus_d = d1 = {p1.personID:None}
    d2 = {p2.personID: None}
    dist = 0
    
    while not set(d1.keys()).intersection(set(d2.keys())):
        for prev_person in list(focus_d.keys()):
            films = ia.get_person(prev_person)['filmography']
            films = films.get('actor') or films.get('actress')
            for film in films:
                ia.update(film)
                for person in film['cast']:
                    if not person.personID in focus_d:
                        focus_d[person.personID] = (prev_person, film.movieID)
                print(f"Film processed: {film}")
        dist += 1
        focus_d = d2 if focus_d is d1 else d1
    
    repeated_elem = cur = set(d1.keys()).intersection(set(d2.keys())).pop()
    path1 = []
    path2 = []
    while d1[cur]:
        prev,movie = d1[cur]
        path1.append((cur,movie))
        cur = prev
    
    cur = repeated_elem
    while d2[cur]:
        prev, movie = d2[cur]
        path2.append(d2[cur])
        cur = prev
    
    return dist, convertPath(path1[::-1] + path2)


def convertPath(lst):
    ia = imdb.Cinemagoer()
        
    return list(map(lambda tup: (ia.get_movie(tup[1])['title'],ia.get_person(tup[0])['name']),lst))

def neighborNoPath(act1, act2):
    ia = imdb.Cinemagoer()
    
    p1 = ia.search_person(act1)[0]
    p2 = ia.search_person(act2)[0]
    
    focus_set = set1 = set([p1.personID])
    set2 = set([p2.personID])
    dist = 0
    
    while not set1.intersection(set2):
        for prev_person in copy.copy(focus_set):
            films = ia.get_person(prev_person)['filmography']
            films = films.get('actor') or films.get('actress')
            for film in films:
                ia.update(film)
                for person in film['cast']:
                    focus_set.add(person.personID)
                print(f"Film processed: {film}")
        dist += 1
        focus_set = set2 if focus_set is set1 else set1
    
    return dist
                
        
    
    
