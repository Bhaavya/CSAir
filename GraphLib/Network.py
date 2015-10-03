SOURCE_PORT = 0
DESTINATION_PORT = 1


class Network:
    """ Represent airline network as a graph with nodes as cities and routes as edges."""
    def __init__(self):
        self.routes = []
        self.cities = []

    def insert_city(self, city):
        """Insert a city node."""
        self.cities.append(city)

    def insert_route(self, route):
        """Insert a route edge."""
        self.routes.append(route)

    def city_name_exists(self, name):
        """Return city node with the given name.
        :return: city node if name is valid, else None
        """
        for city in self.cities:
            if (city.name.lower()).strip() == name.lower():
                return city
        return None

    def city_code_exists(self, code):
        """Return city node with the given code.
        :return: city node if code is valid, else None
        """
        for city in self.cities:
            if (city.code.lower()).strip() == code.lower():
                return city
        return None

    def routes_connected_to(self, code):
        """Return routes with the given city as source port."""
        connected_city_routes = []
        for route in self.routes:
            if route.ports[SOURCE_PORT].lower() == code.lower():
                connected_city_routes.append(route)
        return connected_city_routes

    def get_longest_flight(self):
        """Return route with maximum distance between ports.
        If there are multiple routes with this maximum distance,return only first such route.
        """
        max_distance = 0
        longest_route = None
        for route in self.routes:
            if route.distance > max_distance:
                max_distance = route.distance
                longest_route = route
        return longest_route

    def get_shortest_flight(self):
        """Return route with least distance between ports.
        If there are multiple routes with this minimum distance,return only first such route.
        """
        min_distance = self.routes[0].distance
        shortest_route = self.routes[0]
        for route in self.routes:
            if route.distance < min_distance:
                min_distance = route.distance
                shortest_route = route
        return shortest_route

    def get_average_distance(self):
        """Return average of distance of all flights."""
        sum_distance = 0
        num_flights = 0
        for route in self.routes:
            sum_distance += route.distance
            num_flights += 1
        return sum_distance/num_flights

    def get_biggest_city_pop(self):
        """Return biggest city by population.
         If there are multiple cities with this maximum population,return only first such city.
         """
        max_population = 0
        biggest_city = None
        for city in self.cities:
            if max_population < city.population:
                max_population = city.population
                biggest_city = city
        return biggest_city

    def get_smallest_city_pop(self):
        """Return smallest city by population.
         If there are multiple cities with this minimum population,return only first such city.
         """
        min_population = self.cities[0].population
        smallest_city = None
        for city in self.cities:
            if min_population > city.population:
                min_population = city.population
                smallest_city = city
        return smallest_city

    def get_average_population(self):
        """Return average population of all cities in the network."""
        sum_population = 0
        num_cities = 0
        for city in self.cities:
            sum_population += city.population
            num_cities += 1
        return sum_population/num_cities

    def get_continents_covered(self):
        """Return dictionary of continents covered with their cities."""
        continents = {}
        for city in self.cities:
            if city.continent not in continents:        # unseen continents
                continents[city.continent] = []
            continents[city.continent].append(city.name)
        return continents

    def get_hub_cities(self):
        """Return city with maximum number of connections.
        If multiple cities have this maximum number of connections, return all such cities.
        """
        # finds number of connections for each source port
        cities = {}
        for route in self.routes:
            if route.ports[SOURCE_PORT] not in cities:      # unseen route source port
                cities[route.ports[SOURCE_PORT]] = 0
            cities[route.ports[SOURCE_PORT]] += 1           # increment connections of the source port
        # finds cities with maximum number of connections
        max_connections = 0
        hub_cities = []
        for city in cities:
            if max_connections < cities[city]:
                max_connections = cities[city]
                hub_cities = []
            if cities[city] == max_connections:
                hub_cities.append(city)

        return hub_cities

    def visualise(self):
        # returns url for visualisation of network using the website Great Circle Mapper
        routes_url_mid = ''
        # add all routes to the url
        for route in self.routes:
            ports = route.ports
            routes_url_mid = routes_url_mid + str(ports[SOURCE_PORT]) + '-' + str(ports[DESTINATION_PORT]) + ','

        length = len(routes_url_mid)
        routes_url = 'http://www.gcmap.com/mapui?P=' + routes_url_mid[:length-1] + '&MS=bm&DU=mi'
        return routes_url
