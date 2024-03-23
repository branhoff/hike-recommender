import osmnx as ox
import networkx as nx

def calculate_driving_distance(source_lat, source_lon, target_lat, target_lon):
    '''
    Use openstreetmap to get the graph and compute the shortest distance
    '''
    # Get the network graph for the given area
    graph = ox.graph_from_point((source_lat, source_lon), network_type='drive')

    # Get the nearest node in the graph to the target location
    target_node = ox.distance.nearest_nodes(graph, target_lon, target_lat)

    # Get the nearest node in the graph to the source location
    source_node = ox.distance.nearest_nodes(graph, source_lon, source_lat)

    # Calculate the shortest path (in meters) and driving distance (in meters) between the source and target nodes
    shortest_path = nx.shortest_path(graph, source=source_node, target=target_node, weight='length')
    driving_distance = nx.shortest_path_length(graph, source=source_node, target=target_node, weight='length')

    return shortest_path, driving_distance

# Example usage:
if __name__ == "__main__":
    source_lat = 37.4220  # Source latitude
    source_lon = -122.0841  # Source longitude
    target_lat = 37.3317  # Target latitude
    target_lon = -122.0307  # Target longitude

    shortest_path, driving_distance = calculate_driving_distance(source_lat, source_lon, target_lat, target_lon)
    print("Shortest Path:", shortest_path)
    print("Driving Distance (meters):", driving_distance)
