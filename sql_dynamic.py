#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 14:47:19 2022

@author: adamwasserman
"""

from collections import deque
import sqlite3 as sql


#DI

def dijkstra(act1,act2):
    conn = sql.connect('data/degrees.db')
    
    get_id = "SELECT id FROM actors WHERE name = ?"
    
    get_films = "SELECT movie_id FROM edges WHERE actor_id = ?"
    
    get_cast = "SELECT actor_id FROM edges WHERE movie_id = ?"
    
    p1 = conn.execute(get_id,(act1,)).fetchone()
    film = conn.execute(get_films,p1).fetchall()
    
    p2 = conn.execute(get_id,(act2,)).fetchone()
    
    if not p1 or not p2:
        print("Name INCORRECT!")
        return False
    
    visited = {}
    
    to_visit = deque()
    to_visit.append(p1)
    visited[p1] = None
    
    while to_visit:
        cur = to_visit.popleft()
        if cur == p2:
            path = []
            while visited[cur]:
                prev,movieID = visited[cur]
                path.append((cur,movieID))
                cur = prev
            return act1, path[::-1]
        
        cur_films = conn.execute(get_films,cur).fetchall()
        for film in cur_films:
            for person in conn.execute(get_cast,film):
                if not person in visited:
                    visited[person] = (cur, film)
                    to_visit.append(person)
                    
def translateIDs(start, path):
    conn = sql.connect('data/degrees.db')
    get_name = "SELECT name FROM actors WHERE id = ?"
    get_title = "SELECT title FROM movies WHERE id = ?"
    
    cur = start
    for actor, mov_id in path:
        print(f"""{conn.execute(get_name,cur).fetchone()[0] if cur != start else start} was in {conn.execute(get_title,mov_id).fetchone()[0]} with {conn.execute(get_name,actor).fetchone()[0]}""")
        cur = actor
    
    print(f"The {start}-number is {len(path)}")

if __name__ == '__main__':
    conn = sql.connect('data/degrees.db')
    first_actor = input("Welcome to Degrees of Separation!\nPlease pick a first actor: ")
    first_actor_id = conn.execute(f"SELECT id FROM actors WHERE name = '{first_actor}'").fetchone()
    while not first_actor_id:
        first_actor = input("Invalid name. Try again: ")
        first_actor_id = conn.execute(f"SELECT id FROM actors WHERE name = '{first_actor}'").fetchone()
    
    second_actor = input("Now select a second actor: ")
    second_actor_id = conn.execute(f"SELECT id FROM actors WHERE name = '{second_actor}'").fetchone()
    while not second_actor_id:
        second_actor = input("Invalid name. Try again: ")
        second_actor_id = conn.execute(f"SELECT id FROM actors WHERE name = '{second_actor}'").fetchone()
    
    print("Please wait while the algorithm searches through millions of IMDb actors and shows...")
    translateIDs(*dijkstra(first_actor,second_actor))
        
        