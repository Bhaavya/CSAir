import unittest
from GraphLib.Network import Network
from GraphLib.City import City
from GraphLib.Route import Route

city1 = {
            "code": "MNL",
            "name": "Manila",
            "country": "PH",
            "continent": "Asia",
            "timezone": 8,
            "coordinates": {"N": 15, "E": 121},
            "population": 19600000,
            "region": 4
}
city2 = {
            "code": "SGN",
            "name": "Ho Chi Minh City",
            "country": "VN",
            "continent": "Asia",
            "timezone": 7,
            "coordinates": {"N": 11, "E": 107},
            "population": 6100000,
            "region": 4
}
city3 = {
            "code": "MOW",
            "name": "Moscow",
            "country": "RU",
            "continent": "Europe",
            "timezone": 3,
            "coordinates": {"N": 56, "E": 38},
            "population": 13600000,
            "region": 2
}
route1 = {
            "ports": ["MNL", "SGN"],
            "distance": 1374
}
route2 = {
            "ports": ["MOW", "MNL"],
            "distance": 88200
}
route3 = {
            "ports": ["MOW", "SGN"],
            "distance": 86200
}
route4 = {
            "ports": ["SGN", "MNL"],
            "distance": 1374
}
route5 = {
            "ports": ["MNL", "MOW"],
            "distance": 88200
}
route6 = {
            "ports": ["SGN", "MOW"],
            "distance": 86200
}

SOURCE_PORT = 0
DESTINATION_PORT = 1


class NetworkTest(unittest.TestCase):
    # tests functions for graph query
    network = Network()
    city1 = City(city1)
    city2 = City(city2)
    city3 = City(city3)
    route1 = Route(route1)
    route2 = Route(route2)
    route3 = Route(route3)
    route4 = Route(route4)
    route5 = Route(route5)
    route6 = Route(route6)
    routes = [route1, route2, route3, route4, route5, route6]
    cities = [city1, city2, city3]
    network.insert_city(city1)
    network.insert_city(city2)
    network.insert_city(city3)
    network.insert_route(route1)
    network.insert_route(route2)
    network.insert_route(route3)
    network.insert_route(route4)
    network.insert_route(route5)
    network.insert_route(route6)

    def test_insert(self):
        self.assertItemsEqual([self.city1, self.city2, self.city3], self.network.cities)
        self.assertItemsEqual(self.routes, self.network.routes)

    def test_city_code_exists(self):
        self.assertFalse(self.network.city_name_exists("Champaign"))
        self.assertEqual(self.network.city_name_exists("Moscow").code, 'MOW')

    def test_city_name_exists(self):
        self.assertFalse(self.network.city_code_exists("Cmn"))
        self.assertEqual(self.network.city_code_exists("mnl").name, 'Manila')

    def test_routes_connected_to(self):
        self.assertItemsEqual(self.network.routes_connected_to('mnl'), [self.route1, self.route5])

    def test_get_longest_flight(self):
        self.assertItemsEqual(self.network.get_longest_flight().ports, ["MOW", "MNL"])

    def test_get_shortest_flight(self):
        self.assertItemsEqual(self.network.get_shortest_flight().ports, ["MNL", "SGN"])

    def test_get_average_distance(self):
        sum_distance = 0
        for route in self.routes:
            sum_distance += route.distance

        self.assertEqual(self.network.get_average_distance(),sum_distance/6)

    def test_get_biggest_city_pop(self):
        self.assertEqual(self.network.get_biggest_city_pop().name, 'Manila')

    def test_get_smallest_city_pop(self):
        self.assertEqual(self.network.get_smallest_city_pop().name, 'Ho Chi Minh City')

    def test_get_average_population(self):
        sum_population = 0
        for city in self.cities:
            sum_population += city.population
        self.assertEqual(self.network.get_average_population(), sum_population/3)

    def test_get_continents_covered(self):
        continents = {"Asia": ['Manila', 'Ho Chi Minh City'], "Europe": ['Moscow']}
        self.assertItemsEqual(self.network.get_continents_covered(), continents)

    def test_get_hub_cities(self):
        self.assertItemsEqual(self.network.get_hub_cities(), ['MNL', 'SGN', 'MOW'])

    def test_visualise(self):
        self.assertEqual(self.network.visualise(),'http://www.gcmap.com/mapui?P=MNL-SGN,MOW-MNL,MOW-SGN,SGN-MNL,MNL-MOW,SGN-MOW&MS=bm&DU=mi')
