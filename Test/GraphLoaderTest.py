import unittest
from AirlineSystem.LoadGraph import LoadGraph
from GraphLib.Network import Network
from GraphLib.City import City
from GraphLib.Route import Route

city1 = {
      "code": "SCL",
      "name": "Santiago",
      "country": "CL",
      "continent": "South America",
      "timezone": -4,
      "coordinates": {"S": 33,"W": 71},
      "population": 6000000,
      "region": 1
    }
city2 = {
      "code": "LIM",
      "name": "Lima",
      "country": "PE",
      "continent": "South America",
      "timezone": -5,
      "coordinates": {
        "S": 12,
        "W": 77
      },
      "population": 9050000,
      "region": 1
    }

route1 ={
      "ports": [
        "SCL",
        "LIM"
      ],
      "distance": 2453
    }
route2 = {
      "ports": [
        "LIM",
        "SCL"
      ],
      "distance": 2453
    }

class GraphLoaderTest(unittest.TestCase):

    # Tests json parser and loader
    graphLoader = LoadGraph()
    network = Network()
    city1 = City(city1)
    city2 = City(city2)
    route1 = Route(route1)
    route2 = Route(route2)
    routes = [route1, route2]
    cities = [city1, city2]

    def test_populate_graph(self):
        self.graphLoader.populate_graph('../Resources/test_data.json')
        self.assertEquals(self.graphLoader.airline_network.cities[0].name, self.city1.name)
        self.assertEquals(self.graphLoader.airline_network.cities[1].name, self.city2.name)
        self.assertEquals(self.graphLoader.airline_network.routes[0].ports, self.route1.ports)
        self.assertEquals(self.graphLoader.airline_network.routes[1].ports, self.route2.ports)




