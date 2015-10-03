import json
from GraphLib.City import City
from GraphLib.Route import Route
from GraphLib.Network import Network


class LoadGraph:
    """Load graph nodes and edges from JSON file. """
    def __init__(self):
        self.airline_network = Network()        # graph representing route map

    def populate_graph(self, json_file):
        data = open(json_file)
        parsed_json = json.load(data)
        # insert city as nodes
        for city in parsed_json['metros']:
            city_node = City(city)
            self.airline_network.insert_city(city_node)
        # insert route as edges
        for route in parsed_json['routes']:
            route_edge1 = Route(route)
            route_edge2 = Route({'distance': route['distance'], 'ports': [route['ports'][1], route['ports'][0]]})
            self.airline_network.insert_route(route_edge1)
            self.airline_network.insert_route(route_edge2)