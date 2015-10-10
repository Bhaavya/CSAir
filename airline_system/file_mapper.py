import json
from graph_lib.network import Network, City, Route
SOURCE_PORT = 0
DESTINATION_PORT = 1


class FileMapper:
    """Load from and save to json file."""
    def __init__(self, json_files):
        """Combine json_files and store in the primary file."""
        self.airline_network = Network()        # graph representing route map
        primary_file = json_files[0]
        if len(json_files) > 1:
            primary_json_data = open(primary_file, 'r+')
            primary_data = json.load(primary_json_data)
            for addon_file in json_files[1:]:
                addon_json_data = open(addon_file, 'r')
                addon_data = json.load(addon_json_data)
                for city in addon_data['metros']:
                    primary_data['metros'].append(city)
                for route in addon_data['routes']:
                    primary_data['routes'].append(route)
                addon_json_data.close()
            primary_json_data.seek(0)
            json.dump(primary_data, primary_json_data, sort_keys=True, indent=4, separators=(',', ': '))
            primary_json_data.close()
        self.json_file = primary_file

    def populate_graph(self):
        """Load graph nodes and edges from JSON file."""
        data = open(self.json_file, 'r')
        parsed_json = json.load(data)
        # insert city as nodes
        for city in parsed_json['metros']:
            city_node = City(city)
            self.airline_network.insert_city(city_node)
        # insert route as edges
        for route in parsed_json['routes']:
            route_edge = Route(route)
            self.airline_network.insert_route(route_edge)
        data.close()

    def add_city(self, city):
        """Add city in primary json file."""
        file_ptr = open(self.json_file, 'r+')
        json_data = json.load(file_ptr)
        json_data['metros'].append(city)
        file_ptr.seek(0)
        json.dump(json_data, file_ptr, sort_keys=True, indent=4, separators=(',', ': '))
        file_ptr.close()

    def add_route(self, route):
        """Add route in primary json file."""
        file_ptr = open(self.json_file, 'r+')
        json_data = json.load(file_ptr)
        json_data['routes'].append(route)
        file_ptr.seek(0)
        json.dump(json_data, file_ptr, sort_keys=True, indent=4, separators=(',', ': '))
        file_ptr.close()

    def remove_city(self, city_code):
        """Remove city from primary json file."""
        file_ptr = open(self.json_file, 'r')
        json_data = json.load(file_ptr)
        remove_city = filter(lambda city: city['code'].lower() == city_code.lower(), json_data['metros'])
        json_data['metros'].remove(remove_city[0])
        # remove all routes from and to the city
        related_routes = filter(lambda route: (route['ports'][SOURCE_PORT].lower() == city_code.lower() or
                                               route['ports'][DESTINATION_PORT].lower() == city_code.lower()),
                                json_data['routes'])
        for route in related_routes:
            json_data['routes'].remove(route)
        file_ptr.close()
        file_ptr = open(self.json_file, 'w')
        json.dump(json_data, file_ptr, sort_keys=True, indent=4, separators=(',', ': '))
        file_ptr.close()

    def remove_route(self, route):
        """Remove route from primary json file."""
        file_ptr = open(self.json_file, 'r')
        json_data = json.load(file_ptr)
        remove_route = filter(lambda existing_route: (existing_route['ports'][SOURCE_PORT].lower() ==
                                                      route['ports'][SOURCE_PORT].lower()) and
                                                     (existing_route['ports'][DESTINATION_PORT].lower() ==
                                                      route['ports'][DESTINATION_PORT].lower()),
                              json_data['routes'])
        json_data['routes'].remove(remove_route[0])
        file_ptr.close()
        file_ptr = open(self.json_file, 'w')
        json.dump(json_data, file_ptr, sort_keys=True, indent=4, separators=(',', ': '))
        file_ptr.close()

    def edit_city_code(self, city_code, new_code):
        """Edit city code in primary json file.Edit codes in all routes to and from the city."""
        file_ptr = open(self.json_file, 'r+')
        json_data = json.load(file_ptr)
        edit_city = filter(lambda city: city['code'].lower() == city_code.lower(), json_data['metros'])
        edit_city[0]['code'] = new_code
        related_routes = filter(lambda route: (route['ports'][SOURCE_PORT].lower() == city_code.lower() or
                                               route['ports'][DESTINATION_PORT].lower() == city_code.lower()),
                                json_data['routes'])
        for route in related_routes:
            if route['ports'][SOURCE_PORT].lower() == city_code.lower():
                    route['ports'][SOURCE_PORT] = new_code
            else:
                    route['ports'][DESTINATION_PORT] = new_code
        file_ptr.seek(0)
        json.dump(json_data, file_ptr, sort_keys=True, indent=4, separators=(',', ': '))
        file_ptr.close()

    def edit_city_name(self, city_code, new_name):
        """Edit city name in primary json file."""
        file_ptr = open(self.json_file, 'r+')
        json_data = json.load(file_ptr)
        edit_city = filter(lambda city: city['code'].lower() == city_code.lower(), json_data['metros'])
        edit_city[0]['name'] = new_name
        file_ptr.seek(0)
        json.dump(json_data, file_ptr, sort_keys=True, indent=4, separators=(',', ': '))
        file_ptr.close()

    def edit_city_country(self, city_code, new_country):
        """Edit city country in primary json file."""
        file_ptr = open(self.json_file, 'r+')
        json_data = json.load(file_ptr)
        edit_city = filter(lambda city: city['code'].lower() == city_code.lower(), json_data['metros'])
        edit_city[0]['country'] = new_country
        file_ptr.seek(0)
        json.dump(json_data, file_ptr, sort_keys=True, indent=4, separators=(',', ': '))
        file_ptr.close()

    def edit_city_continent(self, city_code, new_continent):
        """Edit city continent in primary json file."""
        file_ptr = open(self.json_file, 'r+')
        json_data = json.load(file_ptr)
        edit_city = filter(lambda city: city['code'].lower() == city_code.lower(), json_data['metros'])
        edit_city[0]['continent'] = new_continent
        file_ptr.seek(0)
        json.dump(json_data, file_ptr, sort_keys=True, indent=4, separators=(',', ': '))
        file_ptr.close()

    def edit_city_timezone(self, city_code, new_timezone):
        """Edit city timezone in primary json file."""
        file_ptr = open(self.json_file, 'r+')
        json_data = json.load(file_ptr)
        edit_city = filter(lambda city: city['code'].lower() == city_code.lower(), json_data['metros'])
        edit_city[0]['timezone'] = new_timezone
        file_ptr.seek(0)
        json.dump(json_data, file_ptr, sort_keys=True, indent=4, separators=(',', ': '))
        file_ptr.close()

    def edit_city_region(self, city_code, new_region):
        """"Edit city region in primary json file."""
        file_ptr = open(self.json_file, 'r+')
        json_data = json.load(file_ptr)
        edit_city = filter(lambda city: city['code'].lower() == city_code.lower(), json_data['metros'])
        edit_city[0]['region'] = new_region
        file_ptr.seek(0)
        json.dump(json_data, file_ptr, sort_keys=True, indent=4, separators=(',', ': '))
        file_ptr.close()

    def edit_city_population(self, city_code, new_population):
        """Edit city population in primary json file."""
        file_ptr = open(self.json_file, 'r+')
        json_data = json.load(file_ptr)
        edit_city = filter(lambda city: city['code'].lower() == city_code.lower(), json_data['metros'])
        edit_city[0]['population'] = new_population
        file_ptr.seek(0)
        json.dump(json_data, file_ptr, sort_keys=True, indent=4, separators=(',', ': '))
        file_ptr.close()

    def edit_city_coordinates(self, city_code, new_coordinates):
        """Edit city coordinates in primary json file."""
        file_ptr = open(self.json_file, 'r+')
        json_data = json.load(file_ptr)
        edit_city = filter(lambda city: city['code'].lower() == city_code.lower(), json_data['metros'])
        edit_city[0]['coordinates'] = new_coordinates
        file_ptr.seek(0)
        json.dump(json_data, file_ptr, sort_keys=True, indent=4, separators=(',', ': '))
        file_ptr.close()
