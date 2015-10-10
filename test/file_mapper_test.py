import unittest
from airline_system.file_mapper import FileMapper
from graph_lib.network import Network, City, Route
import json

SOURCE_PORT = 0
DESTINATION_PORT = 1
city1 = {
      "code": "SCL",
      "name": "Santiago",
      "country": "CL",
      "continent": "South America",
      "timezone": -4,
      "coordinates": {"S": 33, "W": 71},
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

city3 = {
      "code": "MEX",
      "continent": "North America",
      "coordinates": {
        "N": 19,
        "W": 99
      },
      "country": "MX",
      "name": "Mexico City",
      "population": 23400000,
      "region": 1,
      "timezone": -6
}
city4 = {
            "code": "MIA",
            "continent": "North America",
            "coordinates": {
                "N": 26,
                "W": 80
            },
            "country": "US",
            "name": "Miami",
            "population": 5400000,
            "region": 1,
            "timezone": -5
}

route1 = {
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
route3 = {
      "distance": 4231,
      "ports": [
        "LIM",
        "MEX"
      ]
}

route4 = {
            "distance": 2053,
            "ports": [
                "MEX",
                "MIA"
            ]
}


class FileMapperTest(unittest.TestCase):
    # Tests json parser and loader
    def setUp(self):
        self.file_mapper = FileMapper(['../resources/test.json', '../resources/additional_test_data.json'])
        self.primary_file = '../resources/test.json'
        self.network = Network()
        self.city1 = City(city1)
        self.city2 = City(city2)
        self.city3 = City(city3)
        self.route1 = Route(route1)
        self.route2 = Route(route2)
        self.route3 = Route(route3)

    def test_populate_graph(self):
        """Test if cities and routes from both files are added to graph."""
        self.file_mapper.populate_graph()
        self.assertEquals(self.file_mapper.airline_network.cities[0].name, self.city1.name)
        self.assertEquals(self.file_mapper.airline_network.cities[1].name, self.city2.name)
        self.assertEquals(self.file_mapper.airline_network.cities[2].name, self.city3.name)
        self.assertEquals(self.file_mapper.airline_network.routes[0].ports, self.route1.ports)
        self.assertEquals(self.file_mapper.airline_network.routes[1].ports, self.route2.ports)
        self.assertEquals(self.file_mapper.airline_network.routes[2].ports, self.route3.ports)

    def test_add_city(self):
        """Test if city is added to primary file."""
        self.file_mapper.add_city(city4)
        primary_json_data = open(self.primary_file, 'r')
        primary_data = json.load(primary_json_data)
        self.assertTrue(city4 in primary_data['metros'])
        primary_json_data.close()

    def test_add_route(self):
        """Test if route is added to primary file."""
        self.file_mapper.add_route(route4)
        primary_json_data = open(self.primary_file, 'r')
        primary_data = json.load(primary_json_data)
        self.assertTrue(route4 in primary_data['routes'])
        primary_json_data.close()

    def test_remove_route(self):
        """Test if route is removed from primary file."""
        self.file_mapper.remove_route(route1)
        primary_json_data = open(self.primary_file, 'r')
        primary_data = json.load(primary_json_data)
        self.assertFalse(route1 in primary_data['routes'])
        primary_json_data.close()

    def test_remove_city(self):
        """Test if city and its routes are removed from primary file."""
        self.file_mapper.remove_city(city2['code'])
        primary_json_data = open(self.primary_file, 'r')
        primary_data = json.load(primary_json_data)
        self.assertFalse(city2 in primary_data['metros'])
        self.assertFalse(route1 in primary_data['routes'])
        self.assertFalse(route2 in primary_data['routes'])
        primary_json_data.close()

    def test_edit_city_code(self):
        """Test if city code is edited in metros and routes."""
        self.file_mapper.edit_city_code(city2['code'], 'NLIM')
        primary_json_data = open(self.primary_file, 'r')
        primary_data = json.load(primary_json_data)
        self.assertEquals(primary_data['metros'][1]['code'], 'NLIM')
        self.assertEquals(primary_data['routes'][0]['ports'][DESTINATION_PORT], 'NLIM')
        self.assertEquals(primary_data['routes'][1]['ports'][SOURCE_PORT], 'NLIM')
        primary_json_data.close()

    def test_edit_city_name(self):
        """Test if city name is edited in primary file."""
        self.file_mapper.edit_city_name(city2['code'], 'New Lima')
        primary_json_data = open(self.primary_file, 'r')
        primary_data = json.load(primary_json_data)
        self.assertEquals(primary_data['metros'][1]['name'], 'New Lima')
        primary_json_data.close()

    def test_edit_city_country(self):
        """Test if city country is edited in primary file."""
        self.file_mapper.edit_city_country(city2['code'], 'New PE')
        primary_json_data = open(self.primary_file, 'r')
        primary_data = json.load(primary_json_data)
        self.assertEquals(primary_data['metros'][1]['country'], 'New PE')
        primary_json_data.close()

    def test_edit_city_continent(self):
        """Test if city continent is edited in primary file."""
        self.file_mapper.edit_city_continent(city2['code'], 'New South America')
        primary_json_data = open(self.primary_file, 'r')
        primary_data = json.load(primary_json_data)
        self.assertEquals(primary_data['metros'][1]['continent'], 'New South America')
        primary_json_data.close()

    def test_edit_city_timezone(self):
        """Test if city timezone is edited in primary file."""
        self.file_mapper.edit_city_timezone(city2['code'], '5')
        primary_json_data = open(self.primary_file, 'r')
        primary_data = json.load(primary_json_data)
        self.assertEquals(primary_data['metros'][1]['timezone'], '5')
        primary_json_data.close()

    def test_edit_city_region(self):
        """Test if city region is edited in primary file."""
        self.file_mapper.edit_city_region(city2['code'], '2')
        primary_json_data = open(self.primary_file, 'r')
        primary_data = json.load(primary_json_data)
        self.assertEquals(primary_data['metros'][1]['region'], '2')
        primary_json_data.close()

    def test_edit_city_population(self):
        """Test if city population is edited in primary file."""
        self.file_mapper.edit_city_population(city2['code'], '800000')
        primary_json_data = open(self.primary_file, 'r')
        primary_data = json.load(primary_json_data)
        self.assertEquals(primary_data['metros'][1]['population'], '800000')
        primary_json_data.close()

    def test_edit_city_coordinates(self):
        """Test if city coordinates is edited in primary file."""
        self.file_mapper.edit_city_coordinates(city2['code'], {"S": 15, "W": 80})
        primary_json_data = open(self.primary_file, 'r')
        primary_data = json.load(primary_json_data)
        self.assertEquals(primary_data['metros'][1]['coordinates'], {"S": 15, "W": 80})
        primary_json_data.close()


    def tearDown(self):
        with open("../resources/original_test.json") as f:
            lines = f.readlines()
            with open("../resources/test.json", "w") as f1:
                f1.writelines(lines)
