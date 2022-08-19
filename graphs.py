#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 12:24:41 2022

@author: adamwasserman
"""

from collections import defaultdict
from collections import deque
from collections import namedtuple
import math
import imdb
import random
import csv
import matplotlib.pyplot as plt
import pylab


class Static_Graph:
    def __init__(self): # all graphs are undirected
        '''
        Initializes an undirected graph where edges are movies and nodes are actors
        '''
        self.adj_list = defaultdict(lambda: set())
        self.edge_const = namedtuple("Edge", ("actor", "movie"))
        self.actor_dict = {}
        self.movie_dict = {}
        
    
    def addVertex(self,actor):
        '''Adds a vertex in O(1) time as a set'''
        self.adj_list[actor] = set()
        
    def addEdge(self, act1, act2, movie):#edges are tuples (actor, movie)
        '''
        Adds an edge between two vertices in O(1) time
        Edges are named tuples constructed by the self.edge_const object
        '''
        self.adj_list[act1].add(self.edge_const(act2,movie))
        self.adj_list[act2].add(self.edge_const(act1,movie))
    
    def getVertices(self):
        '''Returns all the vertices in the graph in O(1)'''
        return self.adj_list.keys()
    
    def get_person_IMDb(self,name):
        '''
        Returns a the IMDb id of a given person
            
            Parameters:
                name: a string that is the given person's name
            
            Returns:
                a string that is the person's IMDb id taken from the self.actor_dict object
        '''
        for key,value in self.actor_dict.items():
            if value == name:
                return key
        print("Person not found!")
        return False
    
    def get_movie_IMDb(self,title):
        '''
        Returns a the IMDb id of a given movie
            
            Parameters:
                title: a string that is the given movie's name
            
            Returns:
                a string that is the movie's IMDb id taken from the self.movie_dict object
        '''
        for key,value in self.movie_dict.items():
            if value == title:
                return key
        print("Title not found")
        return False
    
    def get_name(self,imdb_id):
        '''
        Returns the name of an actor given their IMDb title
        
            Paramters:
                imdb_id: a string consisting of an IMDb id
                
            Returns:
                a string consisting of the name corresponding to the given IMDb id in the self.actor_dict object
        '''
        return self.actor_dict[imdb_id]
    
    def get_title(self,imdb_id):
        '''
        Returns the title of a movie given its IMDb title
        
            Paramters:
                imdb_id: a string consisting of an IMDb id
                
            Returns:
                a string consisting of the title corresponding to the given IMDb id in the self.movie_dict object
        '''
        return self.movie_dict[imdb_id]
    
    def containsVertex(self,v):
        '''
        Checks whether a given vertex exists in the graph in O(1) time
        
            Parameters:
                v: the vertex whose existence will be checked
            
            Returns:
                in_graph (boolean): boolean as to whether the vertex is in the graph
        '''
        return v in self.adj_list.keys()
    
    
    def addNRandomMovies(self,n=5,start_date=2000,end_date=2022):
        """
        Adds random movies to the graph from the ONLINE IMDb database through http requests
        
            Parameters:
                n (int): the number of movies too add
                start_date (int): the earliest release date for an added movie; default is 2000
                end_date (int): the latest release date for an added moovie; default is 2022
        
        """
        ia = imdb.Cinemagoer()
        max_imdb_id = 1000000 #I discovered this through some trial and error
        added = 0
        while added < n:
            imdb_id = str(random.randint(1,max_imdb_id))
            try:
                movie = ia.get_movie(imdb_id)
            except:
                print("An exception occurred: invalid generated imdb_id")
                continue
            if movie['year'] > end_date or movie['year'] < start_date:
                print("Did NOT add: ",movie['title'], movie['year'])
                continue
            print("Added: ", movie['title'],movie['year'])
            self.addIMDBMov(movie)
            added += 1
            
    def addUserSpecMovie(self):
        '''
        Prompts the user for a movie then adds it from the ONLINE IMDb database through http requests
        When the user no longer wishes to add movies, they should hit enter without typing any characters
        '''
        ia = imdb.Cinemagoer()
        
        usr_input = input("Movie to add (hit enter to stop): ")
        
        while usr_input:
            m_lst = ia.search_movie(usr_input)
            if not m_lst:
                print("Movie typed incorrectly!")
            else:
                m = m_lst[0]
                ia.update(m)
                print(m)
                self.addIMDBMov(m)
            usr_input = input("Movie to add (hit enter to stop): ")
    
    def addIMDBMov(self,m):   
        '''
        Stores the given IMDb movie obect in the graph.
        Adds or updates each actor in the movie
        
            Parameters:
                m (imdb.Movie): the IMDb movie object to add
        '''
        
        if m.movieID in self.movie_dict:
            return
        
        self.movie_dict[m.movieID] = m['title']
        for i in range(len(m['cast'])):
            if not m['cast'][i].personID in self.actor_dict:
                self.actor_dict[m['cast'][i].personID] = m['cast'][i]['name']
            for j in range(i,len(m['cast'])):
                self.addEdge(m['cast'][i].personID,m['cast'][j].personID,m.movieID)
        
    def addActor(self,a,existing_actors_only = True):
        '''
        Adds an actor to the graph along with their connections from every movie in the IMDb ONLINE database
        
            Parameters:
                a (imdb.Person): the person to add
                existing_actors_only (bool): boolean which tells whether new actors should be added; default is no
        
        '''
        ia = imdb.Cinemagoer()
        ia.update(a,['filmography'])
        self.actor_dict[a.personID] = a['name']
        films = a['filmography']
        films = films.get('actor',False) or films.get('actress',False)
        for film in films:
            ia.update(film)
            for actor in film['cast']:
                if not existing_actors_only or actor.personID in self.adj_list:
                    self.addEdge(a.personID,actor.personID,film.movieID)
                    self.movie_dict[film.movieID] = film['title']
                    self.actor_dict[actor.personID] = actor['name']
    
    def processData(self,connections="data/topmoviesNshows.csv",actor_ids="data/actor_keys.csv",movie_ids="data/movie_keys.csv"):
        '''
        Loads data from local files into the graph
        
            Parameters:
                connections (str): the file containing the foreign keys of the movies and actors, related
                actor_ids (str): file containing the primary keys for each actor and their name
                movie_ids (str): file contaiining the primary keys for each movie and their name
        '''
        
        with open(connections, 'r') as connections_file:
            csv_reader = csv.reader(connections_file, delimiter=",")
            for row in csv_reader:
                
                mov = row[0]
                actors = row[1:]
                
                for i in range(len(actors)):
                    for j in range(i+1,len(actors)):
                        self.addEdge(actors[i], actors[j], mov)
        connections_file.close()
        
        with open(actor_ids,'r') as actor_file:
            csv_reader = csv.reader(actor_file)
            for _id,name in csv_reader:
                self.actor_dict[_id] = name
        actor_file.close()
        
        with open(movie_ids,'r') as movie_file:
            csv_reader = csv.reader(movie_file)
            for _id,title in csv_reader:
                self.movie_dict[_id] = title
        movie_file.close()
    
    def neighbors(self, v):
        '''
        Returns the neighbors of a given vertex in O(1) time
        
            Parameter:
                v (str): the vertex whose neighbors are desired
            
            Returns:
                neighbors_set (set): the set of the neighbors of v
        '''
        return self.adj_list.get(v,False)
    
    def check_connected(self, v1, v2):
        '''
        Implements are BFS to check whether two vertices are connected in the graph in O(n) time 
        where n is the number of vertices
        
        
            Parameters:
                v1 (str): the first vertex
                v2 (str): the second vertex
            
            Returns:
                connected (bool): whether the vertices are connected
        '''
        to_visit = set([v1])
        visited = set() #how we will keep track of the visisted nodes
        
        while to_visit:
            cur = to_visit.pop()
            visited.add(cur)
            for neighbor,_movie in self.neighbors(cur):
                if neighbor == v2:
                    return True
                if not neighbor in visited:
                    to_visit.add(neighbor)
        return False
    
    def shortest_path(self, v1, v2):
        '''
        Uses are BFS to find the shortest path between two vertices
        Operates in O(n) time where n is the number of vertices in the graph
        If no path exists, it returns math.inf
        
            Parameters:
                v1 (str): the first vertex
                v2 (str): the second vertex
                
            Returns:
                path (list or float): the path of their connection
        '''
        #we will use a dictionary to represent the visited nodes and their previous nodes
        visited = {}
        #we will use a queue to represent the nodes we need to search
        to_visit = deque()
        to_visit.append(v1)
        visited[v1] = None
        
        
        while to_visit:
            v = to_visit.popleft()
            if v == v2:
                path = []
                while visited[v]:
                    prev,movie = visited[v]
                    path.append((v,movie))
                    v = prev
                return path[::-1]
            
            for edge in self.neighbors(v):
                if not edge.actor in visited:
                    visited[edge.actor] = self.edge_const(v,edge.movie)
                    to_visit.append(edge.actor)
        
        return math.inf

            
    def print_path(self,start, path):
        """
        Prints a given path to the console
        
            Parameters:
                start (str): the first actor in the path
                path (list): the path
        """
        
        cur = start
        for actor, mov_id in path:
            print(f"{self.get_name(cur) if cur != start else start} was in {self.get_title(mov_id)} with {self.get_name(actor)}")
            cur = actor
        
        print(f"The {start}-number is {len(path)}")
        
        
    def path_from_source(self, v1): #O(N)
        """
        Calculates the distance of each vertex from a source vertex using BFS algorithm
        Operates in O(N) time (each vertex visited just once)
        Operates in O(N) space — a dictionary is created containing each connected vertex
        
            Parameters:
                v1 (str): the source vertex
                
            Returns:
                totals (dict): a dictionary where the keys are distances from v1 and the values are lists of vertices
                of the corresponding distance
        """
        
        to_visit = deque()
        visited = {v1:0}
        
        to_visit.append(v1)
        dist = 1
        to_visit.append(False)
        
        while to_visit:
            cur = to_visit.popleft()
            if not cur:
                if to_visit:
                    dist += 1
                    to_visit.append(False)
            else:
                for actor,movie in self.neighbors(cur):
                    if not actor in visited:
                        visited[actor] = dist
                        to_visit.append(actor)
        
        totals = defaultdict(list)
        for key,value in visited.items():
            totals[value].append(key)
        return totals
        
        
    def count_components(self, return_components = False):
        '''
        A BFS algorithm to calculate the number of components in the graph
        O(n) time since each vertex is visited just once
        O(n) space since we must create a set of every vertex
        
            Parameters:
                return_components (boolean): whether to return the components are just the count; default is just count
            
            Returns:
                res (int or list): If return_components is set to True, returns a list of sets of components
                If return_compoonents is set to False, returns a integer representing the number of components
            
        '''
        
        not_visited = set(key for key in self.adj_list)
        to_visit = deque()
        
        if return_components:
            components = []
        
        res = 0
        while not_visited:
            cur = not_visited.pop()
            to_visit.append(cur)
            visited = set([cur]) # added list cur
            res += 1
            
            #execute BFS
            while to_visit:                
                cur = to_visit.popleft()
#                visited.add(cur)
                for edge in self.neighbors(cur):
                    if not edge.actor in visited:
                        to_visit.append(edge.actor)
                        visited.add(edge.actor) # added — ensures O(N) time because we visit every vertex once
                
            if return_components:
                components.append(visited)
            not_visited = not_visited.difference(visited)
        
        return res if not return_components else components

if __name__ == '__main__':
    graph = Static_Graph()
    print("By default, we will load in information from the top 250 movies and top 250 TV shows.")
    graph.processData()
    mode = usr_inp = input("""Please select a mode using the following numbers:
        1. Path between 2 actors
        2. Centrality of a single actor (computationally expensive)
        3. Count the number of components in the graph (computationally expensive)
        4. Add movies/shows from IMDb (needs WiFi)
        
        Type 'q' at any time to quit
        
        Your input: """)
    while usr_inp != 'q':
        if usr_inp == 'c':
            usr_inp = mode = input("""Please select a mode using the following numbers:
                1. Path between 2 actors
                2. Centrality of a single actor (computationally expensive)
                3. Count the number of components in the graph (computationally expensive)
                4. Add movies/shows from IMDb (needs WiFi)
                Type 'q' at any time to quit
                
                Your input: """)
            continue
        elif mode == '1':
            actor_1_name = input("Pick your first actor: ")
            while not graph.get_person_IMDb(actor_1_name):
                actor_1_name = input("Invalid! Pick your first actor: ")
            actor_2_name = input("Pick your second actor: ")
            while not graph.get_person_IMDb(actor_2_name):
                actor_2_name = input("Invalid! Pick your second actor: ")
            print("\n Calculating... \n")
            graph.print_path(actor_1_name, graph.shortest_path(graph.get_person_IMDb(actor_1_name),graph.get_person_IMDb(actor_2_name)))
        
        elif mode == '2':
            actor_name = input("Pick your actor: ")
            while not graph.get_person_IMDb(actor_name):
                actor_name = input("Invalid! Pick your actor: ")
            print("\n Calculating... This might take awhile... \n")
            
            d = graph.path_from_source(graph.get_person_IMDb(actor_name))
            total_connected = 0
            for key,val in d.items():
                print(f"There {'is' if len(val) == 1 else 'are'} {len(val)} actor{'s' if len(val) > 1 else ''} that {'is' if len(val) == 1 else 'are'} a distance of {key} from {actor_name}")
                total_connected += len(val)
            
            disc = len(graph.getVertices()) - total_connected
            print(f"There are {disc} actors disconnected from {actor_name}")
            
            ans = input('Would you like to see a log graph? (y/n): ')
            
            if ans == 'y':
                fig,ax = plt.subplots(1,2)
                ax[0].set_xlabel(f"Dist from {actor_name}")
                ax[0].set_ylabel(f"Number of Actors")
                ax[0].set_title(f"Centrality of {actor_name}")
                ax[0].set_yscale('log')
                
                x = list(range(max(d.keys())))
                y = [len(d.get(i,[])) for i in range(len(x))]

                ax[0].plot(x,y)
                my_labels = ("Conn","Disconn")
                ax[1].pie([total_connected,disc],explode=(0.05,0.05),autopct = lambda x: round(x,1))
                ax[1].legend(labels = my_labels, loc="best")
                pylab.show()
        elif mode == '3':
            print("\n Calculating... This might take awhile... \n")
            print(f"There are {graph.count_components()} many components")
            usr_inp = 'c'
            continue
        elif mode == '4':
            graph.addUserSpecMovie()
        else:
            print("Invalid mode.")
        
                
            
        
        usr_inp = input("Hit enter to continue with the same mode. Type 'q' to quit and 'c' to change modes: ")
        
        
            
        