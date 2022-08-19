# Degrees of Separation
Relate actors to each other through common movies and TV shows! Use graph theory to calculate the shortest path between two actors and more!

### Motivation
This project attempts to implement the Degrees of Kevin Bacon game. Its was the discrete math course I took during the summer of 2022. Most of the algorithms and concepts implemented here come directly from that course.

### Usage
Run the graph.py file to work with data from the top 250 movies and top 250 TV shows. To work with the entire IMDb database, you must download the file linked [here](https://drive.google.com/drive/folders/1ZJ-OMo0_KYH3gODvKqrtALVfaEoQWved?usp=sharing) (the file was too large for GitHub).

### Iterations
Initially, I tried to use IMDbPY, the IMBd's Python API, to run Dijkstra's algorithm for calculating the shortest distance between two nodes. The algorithm is located in the [http_dynamic.py](https://github.com/adam-wasserman/Degrees_of_Separation/blob/main/http_dynamic.py) file. This method, however, required thousands upon thousands of pull requests, so runtime was unacceptably slow. So, instead, I sought to store information locally. I downloaded information from the top 250 movies and top 250 TV shows, storing it in CSV files. I then uploaded these data to a graph object that I implemented in [graphs.py](https://github.com/adam-wasserman/Degrees_of_Separation/blob/main/graphs.py). While dramatically improving run time, this method only allowed me to work with a small subset of movies and TV shows. Although possible, loading the entire IMDb database into this graph object was time consuming. Ultimately, I created a simple relational database that I queried using the sqlite3 library in Python. That code can be found [here]((https://github.com/adam-wasserman/Degrees_of_Separation/blob/main/sql_dynamic.py)
