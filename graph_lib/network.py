import heapq
import sys
SOURCE_PORT = 0
DESTINATION_PORT = 1
CITY_CODE = 1


class City:
    """For a city node from dictionary."""
    def __init__(self, city):
        self.code = city['code']
        self.name = city['name']
        self.country = city['country']
        self.continent = city['continent']
        self.timezone = city['timezone']
        self.coordinates = city['coordinates']
        self.population = city['population']
        self.region = city['region']


class Route:
    """Form a route edge from dictionary."""
    def __init__(self, route):
        self.distance = route['distance']
        self.ports = route['ports']


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

    def route_exists(self, route):
        """Return route with the given route ports.
        :return: route object if ports are valid, else None
        """
        route_to_remove = filter(
            lambda existing_route: existing_route.ports[SOURCE_PORT].lower() == route['ports'][SOURCE_PORT].lower() and
            existing_route.ports[DESTINATION_PORT].lower() == route['ports'][DESTINATION_PORT].lower(),
            self.routes)
        if route_to_remove:
            return route_to_remove[0]
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

    def visualize(self):
        # returns url for visualization of network using the website Great Circle Mapper
        routes_url_mid = ''
        # add all routes to the url
        for route in self.routes:
            ports = route.ports
            routes_url_mid = routes_url_mid + str(ports[SOURCE_PORT]) + '-' + str(ports[DESTINATION_PORT]) + ','

        length = len(routes_url_mid)
        routes_url = 'http://www.gcmap.com/mapui?P=' + routes_url_mid[:length-1] + '&MS=bm&DU=mi'
        return routes_url

    def remove_city(self, city_code):
        """Remove city from network.Also remove all routes to and from city."""
        city = self.city_code_exists(city_code)
        self.cities.remove(city)
        # remove routes to and from city
        related_routes = filter(lambda route: (route.ports[SOURCE_PORT].lower() == city_code.lower() or
                                               route.ports[DESTINATION_PORT].lower() == city_code.lower()), self.routes)
        for route in related_routes:
            self.remove_route(route)

    def remove_route(self, route):
        """Remove route from network."""
        self.routes.remove(route)

    def edit_distance(self, route):
        """Edit distance of a route."""
        if self.route_exists(route):
            edit_route = self.route_exists(route)
            edit_route.distance = route['distance']

    def edit_code(self, city_code, new_code, city):
        """Edit code in city and all routes to and from the city whose code is to be edited.
        Code must be valid."""
        city.code = new_code
        related_routes = filter(lambda route: (route.ports[SOURCE_PORT].lower() == city_code.lower() or
                                               route.ports[DESTINATION_PORT].lower() == city_code.lower()), self.routes)
        for route in related_routes:
                if route.ports[SOURCE_PORT].lower() == city_code.lower():
                    route.ports[SOURCE_PORT] = new_code
                else:
                    route.ports[DESTINATION_PORT] = new_code

    @staticmethod
    def edit_name(new_name, city):
        """Edit city name.
        Code must be valid."""
        city.name = new_name

    @staticmethod
    def edit_country(new_country, city):
        """Edit country.
        Code must be valid."""
        city.country = new_country

    @staticmethod
    def edit_timezone(new_timezone, city):
        """Edit timezone.
        Code must be valid."""
        city.timezone = new_timezone

    @staticmethod
    def edit_continent(new_continent, city):
        """Edit continent.
        Code must be valid."""
        city.continent = new_continent

    @staticmethod
    def edit_region(new_region, city):
        """Edit region.
        Code must be valid."""
        city.region = new_region

    def get_shortest_route(self, start_port, destination_port):
        """Implement Dijkstra's algorithm to find shortest route between two ports
        ports must in the network
        :return: shortest route
        """
        # list of cities with additional keys
        # tent_dist is tentative shortest distance
        # visited for marking city as visited
        cities = []
        for city in self.cities:
            cities.append({'city_code': city.code, 'visited': False, 'tent_dist': sys.maxint, 'route': []})
        source_city = filter(lambda city: city['city_code'].lower() == start_port.lower(), cities)
        source_city[0]['tent_dist'] = 0
        destination_city_list = filter(lambda city: city['city_code'].lower() == destination_port.lower(), cities)
        destination_city = destination_city_list[0]
        unvisited_cities = self.build_unvisited_city_heap(cities)

        while len(unvisited_cities):
            current_city_heap = heapq.heappop(unvisited_cities)
            current_city_list = filter(lambda city: city['city_code'].lower() == current_city_heap[CITY_CODE].lower(), cities)
            current_city = current_city_list[0]
            if current_city['tent_dist'] == sys.maxint:         # no route exists between source and destination
                return None
            cities = self.update_connected_cities(cities, current_city)
            current_city['visited'] = True
            if destination_city['visited']:
                destination_city['route'].append(destination_city['city_code'])
                return destination_city['route']
            # Rebuild heap
            unvisited_cities = self.build_unvisited_city_heap(cities)

    def update_connected_cities(self, cities, current_city):
        # Update tentative shortest routes for connected cities
        for connected_route in self.routes_connected_to(current_city['city_code']):
            connected_cities = filter(
                lambda city: city['city_code'].lower() == connected_route.ports[DESTINATION_PORT].lower(), cities)
            connected_city = connected_cities[0]
            if not connected_city['visited']:
                updated_distance = current_city['tent_dist'] + connected_route.distance
                if connected_city['tent_dist'] > updated_distance:
                    connected_city['tent_dist'] = updated_distance
                    connected_city['route'] = []
                    for prev_port in current_city['route']:
                        connected_city['route'].append(prev_port)
                    connected_city['route'].append(current_city['city_code'])
        return cities

    @staticmethod
    def build_unvisited_city_heap(cities):
        unvisited_cities = []
        for city in cities:
            if not city['visited']:
                unvisited_cities.append((city['tent_dist'], city['city_code']))
        heapq.heapify(unvisited_cities)
        return unvisited_cities
