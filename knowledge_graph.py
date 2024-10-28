import networkx as nx
import matplotlib.pyplot as plt

# Define movie ratings to color them based on the criteria
movie_ratings = {
    # Cluster 1 - Christopher Nolan Movies
    "Inception": 8.8, "The Dark Knight": 9.0, "Interstellar": 8.6, "Dunkirk": 7.9, "Tenet": 5.3,
    # Cluster 2 - Quentin Tarantino Movies
    "Pulp Fiction": 8.9, "Kill Bill": 8.1, "Django Unchained": 8.4, "Death Proof": 4.9,
    # Cluster 3 - Steven Spielberg Movies
    "Jurassic Park": 8.1, "E.T.": 7.8, "Schindler's List": 8.9, "1941": 4.6,
    # Cluster 4 - James Cameron Movies
    "Titanic": 7.8, "Avatar": 7.8, "Terminator": 8.0, "Piranha II: The Spawning": 3.7
}

# Create a directed graph for the extended knowledge graph example
G_knowledge_extended = nx.DiGraph()

# Add nodes for multiple clusters
G_knowledge_extended.add_nodes_from([
    # Cluster 1 - Christopher Nolan Movies
    "Inception", "The Dark Knight", "Interstellar", "Dunkirk", "Tenet", "Christopher Nolan",
    "Leonardo DiCaprio", "Christian Bale", "Matthew McConaughey", "Tom Hardy", "Sci-Fi", "Action", "Drama",
    "Oscar", "BAFTA",

    # Cluster 2 - Quentin Tarantino Movies
    "Pulp Fiction", "Kill Bill", "Django Unchained", "Death Proof", "Quentin Tarantino", 
    "Uma Thurman", "Samuel L. Jackson", "Jamie Foxx", "Crime", "Western", "Golden Globe",

    # Cluster 3 - Steven Spielberg Movies
    "Jurassic Park", "E.T.", "Schindler's List", "1941", "Steven Spielberg", 
    "Jeff Goldblum", "Liam Neeson", "Adventure", "Historical", "Comedy", "Academy Award",

    # Cluster 4 - James Cameron Movies
    "Titanic", "Avatar", "Terminator", "Piranha II: The Spawning", "James Cameron", 
    "Kate Winslet", "Arnold Schwarzenegger", "Zoe Saldana", "Romance", "Thriller", "Fantasy", "Horror"
])

# Add edges with relationships
G_knowledge_extended.add_edges_from([
    # Cluster 1 - Christopher Nolan
    ("Inception", "Christopher Nolan", {"relationship": "directed by"}),
    ("The Dark Knight", "Christopher Nolan", {"relationship": "directed by"}),
    ("Interstellar", "Christopher Nolan", {"relationship": "directed by"}),
    ("Dunkirk", "Christopher Nolan", {"relationship": "directed by"}),
    ("Tenet", "Christopher Nolan", {"relationship": "directed by"}),
    ("Inception", "Leonardo DiCaprio", {"relationship": "stars"}),
    ("The Dark Knight", "Christian Bale", {"relationship": "stars"}),
    ("Interstellar", "Matthew McConaughey", {"relationship": "stars"}),
    ("Dunkirk", "Tom Hardy", {"relationship": "stars"}),
    ("Inception", "Sci-Fi", {"relationship": "genre"}),
    ("The Dark Knight", "Action", {"relationship": "genre"}),
    ("Dunkirk", "Drama", {"relationship": "genre"}),
    ("Tenet", "Sci-Fi", {"relationship": "genre"}),

    # Cluster 2 - Quentin Tarantino
    ("Pulp Fiction", "Quentin Tarantino", {"relationship": "directed by"}),
    ("Kill Bill", "Quentin Tarantino", {"relationship": "directed by"}),
    ("Django Unchained", "Quentin Tarantino", {"relationship": "directed by"}),
    ("Death Proof", "Quentin Tarantino", {"relationship": "directed by"}),
    ("Pulp Fiction", "Uma Thurman", {"relationship": "stars"}),
    ("Pulp Fiction", "Samuel L. Jackson", {"relationship": "stars"}),
    ("Django Unchained", "Jamie Foxx", {"relationship": "stars"}),

    # Cluster 3 - Steven Spielberg
    ("Jurassic Park", "Steven Spielberg", {"relationship": "directed by"}),
    ("E.T.", "Steven Spielberg", {"relationship": "directed by"}),
    ("Schindler's List", "Steven Spielberg", {"relationship": "directed by"}),
    ("1941", "Steven Spielberg", {"relationship": "directed by"}),
    ("Jurassic Park", "Jeff Goldblum", {"relationship": "stars"}),

    # Cluster 4 - James Cameron
    ("Titanic", "James Cameron", {"relationship": "directed by"}),
    ("Avatar", "James Cameron", {"relationship": "directed by"}),
    ("Terminator", "James Cameron", {"relationship": "directed by"}),
    ("Piranha II: The Spawning", "James Cameron", {"relationship": "directed by"}),
    ("Titanic", "Kate Winslet", {"relationship": "stars"}),
    ("Terminator", "Arnold Schwarzenegger", {"relationship": "stars"}),
    ("Avatar", "Zoe Saldana", {"relationship": "stars"})
])

# Define a function to determine color based on movie ratings or director average rating
def get_director_color(director):
    directed_movies = [movie for movie, data in G_knowledge_extended.edges(director, data=True) if data.get("relationship") == "directed by"]
    if not directed_movies:
        return 'gray'
    avg_rating = sum(movie_ratings.get(movie, 0) for movie in directed_movies) / len(directed_movies)
    if avg_rating > 8:
        return 'green'
    elif avg_rating > 5:
        return 'yellow'
    else:
        return 'red'

def get_node_color(node):
    if node in movie_ratings:
        rating = movie_ratings.get(node)
        if rating > 8:
            return 'green'
        elif rating > 5:
            return 'yellow'
        else:
            return 'red'
    if any("directed by" in data.get("relationship", "") for _, _, data in G_knowledge_extended.edges(node, data=True)):
        return get_director_color(node)
    return 'gray'

# Color each node based on the updated rules
node_colors = [get_node_color(node) for node in G_knowledge_extended.nodes()]

# Draw the final graph
plt.figure(figsize=(15, 12))
pos = nx.spring_layout(G_knowledge_extended)
nx.draw(G_knowledge_extended, pos, with_labels=True, node_color=node_colors, node_size=3000, font_size=9, font_weight='bold', arrows=True)
edge_labels = nx.get_edge_attributes(G_knowledge_extended, 'relationship')
nx.draw_networkx_edge_labels(G_knowledge_extended, pos, edge_labels=edge_labels, font_color='green')
plt.title("Knowledge Graph with Color-Coded Movies and Directors by Rating")
plt.show()
