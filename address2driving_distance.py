import osmnx as ox
import networkx as nx

def calculate_driving_distance(source_address, target_address):
    '''
    Use openstreetmap to get the graph and compute the shortest distance
    '''
    # Get the network graph for the given addresses
    graph = ox.graph_from_address(source_address, network_type='drive')

    # Geocode the target address to get its latitude and longitude
    target_location = ox.geocode(target_address)

    # Get the nearest node in the graph to the target location
    target_node = ox.distance.nearest_nodes(graph, target_location[1], target_location[0])

    # Get the nearest node in the graph to the source address
    source_node = ox.distance.nearest_nodes(graph, graph.nodes[target_node]['y'], graph.nodes[target_node]['x'])

    # Calculate the shortest path (in meters) and driving distance (in meters) between the source and target nodes
    shortest_path = nx.shortest_path(graph, source=source_node, target=target_node, weight='length')
    driving_distance = nx.shortest_path_length(graph, source=source_node, target=target_node, weight='length')

    return shortest_path, driving_distance

# Example usage:
if __name__ =="__main__":
    source_address = "1600 Amphitheatre Parkway, Mountain View, CA"
    target_address = "1 Infinite Loop, Cupertino, CA"
    shortest_path, driving_distance = calculate_driving_distance(source_address, target_address)
    print("Shortest Path:", shortest_path)
    print("Driving Distance (meters):", driving_distance)
