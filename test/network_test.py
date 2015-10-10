import unittest
from graph_lib.network import Network, City, Route

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
    def setUp(self):
        self.network = Network()
        self.city1 = City(city1)
        self.city2 = City(city2)
        self.city3 = City(city3)
        self.route1 = Route(route1)
        self.route2 = Route(route2)
        self.route3 = Route(route3)
        self.route4 = Route(route4)
        self.route5 = Route(route5)
        self.route6 = Route(route6)
        self.routes = [self.route1, self.route2, self.route3, self.route4, self.route5, self.route6]
        self.cities = [self.city1, self.city2, self.city3]
        self.network.insert_city(self.city1)
        self.network.insert_city(self.city2)
        self.network.insert_city(self.city3)
        self.network.insert_route(self.route1)
        self.network.insert_route(self.route2)
        self.network.insert_route(self.route3)
        self.network.insert_route(self.route4)
        self.network.insert_route(self.route5)
        self.network.insert_route(self.route6)

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

    def test_visualize(self):
        self.assertEqual(self.network.visualize(), 'http://www.gcmap.com/mapui?P=MNL-SGN,MOW-MNL,MOW-SGN,SGN-MNL,MNL-MOW,SGN-MOW&MS=bm&DU=mi')

    def test_get_shortest_route(self):
        self.assertEqual(self.network.get_shortest_route('MNL', 'MOW'), ['MNL', 'SGN', 'MOW'])

    def test_edit_code(self):
        self.network.edit_code('MNL', 'NMNL', self.network.cities[0])
        self.assertEquals(self.network.cities[0].code, 'NMNL')
        # check if code is edited in its routes
        self.assertEquals(self.network.routes[0].ports[SOURCE_PORT], 'NMNL')
        self.assertEquals(self.network.routes[1].ports[DESTINATION_PORT], 'NMNL')
        self.assertEquals(self.network.routes[3].ports[DESTINATION_PORT], 'NMNL')
        self.assertEquals(self.network.routes[4].ports[SOURCE_PORT], 'NMNL')
        self.network.edit_code('NMNL', 'MNL', self.network.cities[0])

    def test_edit_name(self):
        self.network.edit_name('New Manila', self.network.cities[0])
        self.assertEquals(self.network.cities[0].name, 'New Manila')

    def test_edit_country(self):
        self.network.edit_country('NPH', self.network.cities[0])
        self.assertEquals(self.network.cities[0].country, 'NPH')

    def test_edit_continent(self):
        self.network.edit_continent('New Asia', self.network.cities[0])
        self.assertEquals(self.network.cities[0].continent, 'New Asia')

    def test_edit_timezone(self):
        self.network.edit_timezone(1, self.network.cities[0])
        self.assertEquals(self.network.cities[0].timezone, 1)

    def test_edit_region(self):
        self.network.edit_region(1, self.network.cities[0])
        self.assertEquals(self.network.cities[0].region, 1)
