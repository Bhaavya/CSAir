from user_interface.textual_user_interface import UserInterface
from file_mapper import FileMapper
from graph_lib.network import City, Route
import sys
import webbrowser
from datetime import timedelta
import math
DESTINATION_PORT = 1
SOURCE_PORT = 0
LATITUDE = 0
LONGITUDE = 0
NW = '1'
NE = '2'
SW = '3'
SE = '4'


class ServiceManager:
    """Manage user queries. """

    def __init__(self):
        self.json_files = ['../resources/map_data.json', '../resources/cmi_hub.json']
        self.file_mapper = FileMapper(self.json_files)
        self.file_mapper.populate_graph()
        interface = UserInterface()
        self.manage_main_menu(interface)

    def manage_main_menu(self, interface):
        # display main menu
        user_choice = interface.print_menu()
        airline_network = self.file_mapper.airline_network
        # handle queries till user quits
        while user_choice != 'q':
            if user_choice == '1':
                self.display_cities()
            elif user_choice == '2':
                self.manage_city_menu(interface)
            elif user_choice == '3':
                self.manage_stats_menu(interface)
            elif user_choice == '4':
                webbrowser.open(airline_network.visualize())
            elif user_choice == '5':
                self.manage_edit_menu(interface)
            elif user_choice == '6':
                self.get_route_info(airline_network)
            elif user_choice == '7':
                self.get_shortest_route(airline_network)
            else:
                print 'Invalid option.Try again!\n'
            user_choice = interface.print_menu()
        sys.exit(0)

    def manage_city_menu(self, interface):
        # display menu for queries about cities
        user_choice = interface.city_info()
        # handle queries till user quits
        while user_choice != 'q':
            if user_choice == '1':
                self.get_city_code()
            elif user_choice == '2':
                self.get_city_name()
            elif user_choice == '3':
                self.get_city_country()
            elif user_choice == '4':
                self.get_city_continent()
            elif user_choice == '5':
                self.get_city_timezone()
            elif user_choice == '6':
                self.get_city_coordinates()
            elif user_choice == '7':
                self.get_city_population()
            elif user_choice == '8':
                self.get_city_region()
            elif user_choice == '9':
                self.get_connected_cities()
            elif user_choice == '10':
                self.manage_main_menu(interface)
            else:
                print 'Invalid option.Try again!\n'
            user_choice = interface.city_info()
        sys.exit(0)

    def manage_stats_menu(self, interface):
        # display statistical information menu
        user_choice = interface.stats_info()
        airline_network = self.file_mapper.airline_network          # graph of route map
        # process queries till user quits
        while user_choice != 'q':
            if user_choice == '1':
                self.print_longest_flight()
            elif user_choice == '2':
                self.print_shortest_flight()
            elif user_choice == '3':
                print airline_network.get_average_distance()
            elif user_choice == '4':
                print airline_network.get_biggest_city_pop().name
            elif user_choice == '5':
                print airline_network.get_smallest_city_pop().name
            elif user_choice == '6':
                print airline_network.get_average_population()
            elif user_choice == '7':
                self.print_continents()
            elif user_choice == '8':
                hublist = airline_network.get_hub_cities()
                self.print_hubs(hublist)
            elif user_choice == '9':
                self.manage_main_menu(interface)
            else:
                print 'Invalid option.Try again!\n'
            user_choice = interface.stats_info()
        sys.exit(0)

    def manage_edit_menu(self, interface):
        # display editing menu
        user_choice = interface.print_edit_menu()
        airline_network = self.file_mapper.airline_network
        # handle queries till user quits
        while user_choice != 'q':
            if user_choice == '1':
                self.add_city(airline_network)
            elif user_choice == '2':
                self.add_route(airline_network)
            elif user_choice == '3':
                self.remove_city(airline_network)
            elif user_choice == '4':
                self.remove_route(airline_network)
            elif user_choice == '5':
                self.manage_edit_city_menu(airline_network, interface)
            elif user_choice == '6':
                self.manage_main_menu(interface)
            else:
                print 'Invalid option.Try again!\n'
            user_choice = interface.print_edit_menu()
        sys.exit(0)

    def manage_edit_city_menu(self, airline_network, interface):
        """Manage options for editing city information."""
        option = interface.print_edit_city_menu()
        while option != 'q':
            if option == '1':
                self.edit_city_code(airline_network)
            elif option == '2':
                self.edit_city_name(airline_network)
            elif option == '3':
                self.edit_city_country(airline_network)
            elif option == '4':
                self.edit_city_continent(airline_network)
            elif option == '5':
                self.edit_city_coordinates(airline_network)
            elif option == '6':
                self.edit_city_timezone(airline_network)
            elif option == '7':
                self.edit_city_population(airline_network)
            elif option == '8':
                self.edit_city_region(airline_network)
            elif option == '9':
                self.manage_main_menu(interface)
            else:
                print 'Invalid option.Try again!\n'
            option = interface.print_edit_city_menu()
        sys.exit(0)

    def add_city(self, airline_network):
        """Add city to existing network and save changes in json file."""
        print("Enter city details")
        city = {}
        self.enter_code(city, airline_network)
        self.enter_name(city)
        self.enter_country(city)
        self.enter_timezone(city)
        self.enter_coordinates(city)
        self.enter_continent(city)
        self.enter_region(city)
        self.enter_population(city)
        self.file_mapper.add_city(city)
        airline_network.insert_city(City(city))

    @staticmethod
    def enter_code(city, airline_network):
        """Enter code for new city to be added to the network."""
        city['code'] = ''
        # City code must be non empty and not present in network
        while city['code'] == '':
            print 'Please enter city code'
            city['code'] = raw_input('City code:')
            if filter(lambda existing_city: existing_city.code.lower() == city['code'].lower(), airline_network.cities):
                print 'City already exists'
                city['code'] = ''

    @staticmethod
    def enter_name(city):
        """Enter name for new city to be added to the network."""
        city['name'] = raw_input("City name:")
        # City name must be non empty
        while city['name'] == '':
            print 'Please enter city name'
            city['name'] = raw_input('City name:')

    @staticmethod
    def enter_country(city):
        """Enter country for new city to be added to the network"""
        city['country'] = raw_input("City country:")
        # City country must be non empty
        while city['country'] == '':
            print 'Please enter city country'
            city['country'] = raw_input('City country:')

    @staticmethod
    def enter_continent(city):
        """Enter continent for new city to be added to the network."""
        city['continent'] = raw_input("City continent:")
        # City continent must be non empty
        while city['continent'] == '':
            print 'Please enter city continent'
            city['continent'] = raw_input('City continent:')

    @staticmethod
    def enter_timezone(city):
        """Enter timezone for new city to be added to the network."""
        city['timezone'] = ''
        # City timezone must be non empty integer
        while city['timezone'] == '':
            city['timezone'] = raw_input('City timezone:')
            try:
                city['timezone'] = int(city['timezone'])
            except ValueError:
                city['timezone'] = ''
                print 'Please enter valid city timezone'

    @staticmethod
    def enter_region(city):
        """Enter region for new city to be added to the network."""
        city['region'] = ''
        # City region must be non empty integer
        while city['region'] == '':
            city['region'] = raw_input('City region:')
            try:
                city['region'] = int(city['region'])
            except ValueError:
                city['region'] = ''
                print 'Please enter valid city region'

    @staticmethod
    def enter_population(city):
        """Enter population for new city to be added to the network."""
        city['population'] = ''
        # City population must be non negative integer
        while city['population'] == '':
            city['population'] = raw_input('City population:')
            try:
                city['population'] = int(city['population'])
                if city['population'] <= 0:
                    print 'Population must be non-negative. Try again'
                    city['population'] = ''
            except ValueError:
                city['population'] = ''
                print 'Please enter valid city population'

    @staticmethod
    def enter_coordinates(city):
        """Enter coordinates for new city to be added to the network."""
        print("City coordinates:")
        coordinate_entered = False
        while not coordinate_entered:
            hemisphere = raw_input("Enter 1 for NW, 2 for NE, 3 for SW, 4 for SW\n")
            if hemisphere == NW:
                city['coordinates'] = {'N': input("N:"), 'W': input("W:")}
                if 0 <= city['coordinates']['N'] <= 90 and 0 <= city['coordinates']['W'] <= 180:
                    coordinate_entered = True
                else:
                    print 'Invalid coordinates entered. Try again'
            elif hemisphere == NE:
                city['coordinates'] = {'N': input("N:"), 'E': input("E:")}
                if 0 <= city['coordinates']['N'] <= 90 and 0 <= city['coordinates']['E'] <= 180:
                    coordinate_entered = True
                else:
                    print 'Invalid coordinates entered. Try again'
            elif hemisphere == SW:
                city['coordinates'] = {'S': input("S:"), 'W': input("W:")}
                if '0' <= city['coordinates']['S'] <= 90 and 0 <= city['coordinates']['W'] <= 180:
                    coordinate_entered = True
                else:
                    print 'Invalid coordinates entered. Try again'
            elif hemisphere == SE:
                city['coordinates'] = {'S': input("S:"), 'E': input("E:")}
                if 0 <= city['coordinates']['S'] <= 90 and 0 <= city['coordinates']['E'] <= 180:
                    coordinate_entered = True
                else:
                    print 'Invalid coordinates entered. Try again'
            else:
                print 'Invalid option entered. Try again'

    def add_route(self, airline_network):
        """Add a route to network and save changes to json file."""
        print "Enter route details"
        route = {}
        self.enter_ports(route, airline_network)
        route['distance'] = ''
        # Distance must be an integer greater than 0
        while route['distance'] == '':
            route['distance'] = raw_input('Route distance:')
            try:
                route['distance'] = int(route['distance'])
                if route['distance'] <= 0:
                    print 'Distance must be greater than 0. Try again'
                    route['distance']
            except ValueError:
                route['distance']
                print 'Please enter valid route distance'
        # if route is not present in the network then add it, else edit existing route
        if not airline_network.route_exists(route):
            self.file_mapper.add_route(route)
            airline_network.insert_route(Route(route))
        else:
            airline_network.edit_distance(route)

    @staticmethod
    def enter_ports(route, airline_network):
        """Enter ports of route to be added in the network."""
        # Enter source port information
        route['ports'] = ['', '']
        route['ports'][SOURCE_PORT] = raw_input("Enter source port")
        # check if source port is a valid city
        while not (filter(lambda existing_city: existing_city.code.lower() == route['ports'][SOURCE_PORT].lower(),
                          airline_network.cities)):
            print 'Port code must be the code of a city present in the network'
            route['ports'][SOURCE_PORT] = raw_input("Enter source port")
        # Enter destination port information
        route['ports'][DESTINATION_PORT] = raw_input("Enter destination port")
        # check if destination port is a valid city
        while not (filter(lambda existing_city: existing_city.code.lower() == route['ports'][DESTINATION_PORT].lower(),
                          airline_network.cities)):
            print 'Port code must be the code of a city present in the network'
            route['ports'][DESTINATION_PORT] = raw_input("Enter destination port")

    def remove_city(self, airline_network):
        """Remove city from network and edit json file accordingly."""
        city_code = raw_input('Enter city code for removal')
        if airline_network.city_code_exists(city_code):
            self.file_mapper.remove_city(city_code)
            airline_network.remove_city(city_code)
        else:
            print 'City does not exist'

    def remove_route(self, airline_network):
        """Remove route from network and edit json file accordingly."""
        route = {'ports': [raw_input('Enter source port:\n'), raw_input('Enter destination port:\n')]}
        if airline_network.route_exists(route):
            route_to_remove = airline_network.route_exists(route)
            self.file_mapper.remove_route(route)
            airline_network.remove_route(route_to_remove)
        else:
            print 'Route does not exist'

    def get_city_code(self):
        """Print the city code based on city name if city name is valid."""
        city_name = raw_input('Enter city name\n')
        city = self.file_mapper.airline_network.city_name_exists(city_name)     # get city node
        if city is not None:
            print city.code
        else:
            print 'Invalid name entered.Try again!\n'

    def get_city_name(self):
        """Print the city name based on city code if city code is valid."""
        city_code = raw_input('Enter city code\n')
        city = self.file_mapper.airline_network.city_code_exists(city_code)     # get city node
        if city is not None:
            print city.name
        else:
            print 'Invalid code entered.Try again!\n'

    def get_city_country(self):
        """Print the country of city based on city code if city code is valid."""
        city_code = raw_input('Enter city code\n')
        city = self.file_mapper.airline_network.city_code_exists(city_code)     # get city node
        if city is not None:
            print city.country
        else:
            print 'Invalid code entered.Try again!\n'

    def get_city_continent(self):
        """Print the continent of city based on city code if city code is valid."""
        city_code = raw_input('Enter city code\n')
        city = self.file_mapper.airline_network.city_code_exists(city_code)     # get city node
        if city is not None:
            print city.continent
        else:
            print 'Invalid code entered.Try again!\n'

    def get_city_timezone(self):
        """Print the timezone of city based on city code if city code is valid."""
        city_code = raw_input('Enter city code\n')
        city = self.file_mapper.airline_network.city_code_exists(city_code)     # get city node
        if city is not None:
            print city.timezone
        else:
            print 'Invalid code entered.Try again!\n'

    def get_city_coordinates(self):
        """Print the coordinates of city based on city code if city code is valid."""
        city_code = raw_input('Enter city code\n')
        city = self.file_mapper.airline_network.city_code_exists(city_code)     # get city node
        if city is not None:
            for coordinate in city.coordinates:
                print coordinate + ' ' + str(city.coordinates[coordinate])
        else:
            print 'Invalid code entered.Try again!\n'

    def get_city_population(self):
        """Print the city population based on city code if city code is valid."""
        city_code = raw_input('Enter city code\n')
        city = self.file_mapper.airline_network.city_code_exists(city_code)     # get city node
        if city is not None:
            print city.population
        else:
            print 'Invalid code entered.Try again!'

    def get_city_region(self):
        """Print the city region based on city code if city code is valid."""
        city_code = raw_input('Enter city code\n')
        city = self.file_mapper.airline_network.city_code_exists(city_code)     # get city node
        if city is not None:
            print city.region
        else:
            print 'Invalid code entered.Try again!\n'

    def get_connected_cities(self):
        """Print the cities connected via non-stop single flight based on city code if city code is valid."""
        city_code = raw_input('Enter city code\n')
        airline_network = self.file_mapper.airline_network
        city = self.file_mapper.airline_network.city_code_exists(city_code)     # get city node
        if city is not None:
            connected_city_routes = airline_network.routes_connected_to(city_code)      # get routes connecting the city
            for route in connected_city_routes:
                print 'City: ' + route.ports[DESTINATION_PORT] + ' Distance: %d' % route.distance

    def display_cities(self):
        """Print all cities in the network."""
        cities = self.file_mapper.airline_network.cities
        for city in cities:
            print city.name

    def print_longest_flight(self):
        """Print information about longest flight in the network."""
        airline_network = self.file_mapper.airline_network
        longest_route = airline_network.get_longest_flight()
        print "Longest flight is between: " + longest_route .ports[SOURCE_PORT] + " and " + \
              longest_route.ports[DESTINATION_PORT] + " , Distance: %d" % longest_route.distance

    def print_shortest_flight(self):
        """Print information about shortest flight in the network."""
        airline_network = self.file_mapper.airline_network
        shortest_route = airline_network.get_shortest_flight()
        print "Shortest flight is between: " + shortest_route .ports[SOURCE_PORT] + " and " + \
              shortest_route.ports[DESTINATION_PORT] + " , Distance: %d" % shortest_route.distance

    def print_continents(self):
        """Print continents covered by the network along with the cities covered in each continent."""
        airline_network = self.file_mapper.airline_network
        # get dictionary of continents covered with their cities
        continent_list = airline_network.get_continents_covered()

        continent_num = 1
        print 'List of continents covered with cities'
        for continent in continent_list:
            print '%d. \nContinent: ' % continent_num + continent + '\nCities:'
            for city in continent_list[continent]:
                print str(city)
            print '\n'
            continent_num += 1

    @staticmethod
    def print_hubs(hub_list):
        """Print all cities having maximum number of connections."""
        for hub in hub_list:
            print str(hub)

    def edit_city_code(self, airline_network):
        """Edit code of a city in the network.Save changes in json file."""
        prev_city_code = raw_input('Enter code of city which you want to edit')
        if airline_network.city_code_exists(prev_city_code):
            city = airline_network.city_code_exists(prev_city_code)
            print ("Enter new city details")
            # Create a dummy city dictionary for entering city code
            temp_city = {}
            self.enter_code(temp_city, airline_network)
            airline_network.edit_code(prev_city_code, temp_city['code'], city)
            self.file_mapper.edit_city_code(prev_city_code, temp_city['code'])

    def edit_city_name(self, airline_network):
        """Edit name of a city in the network.Save changes in json file."""
        city_code = raw_input('Enter code of city which you want to edit')
        if airline_network.city_code_exists(city_code):
            city = airline_network.city_code_exists(city_code)
            print ("Enter new city details")
            # Create a dummy city dictionary for entering city name
            temp_city = {}
            self.enter_name(temp_city)
            airline_network.edit_name(temp_city['name'], city)
            self.file_mapper.edit_city_name(city_code, temp_city['code'])

    def edit_city_country(self, airline_network):
        """Edit country of a city in the network.Save changes in json file."""
        city_code = raw_input('Enter code of city which you want to edit')
        if airline_network.city_code_exists(city_code):
            city = airline_network.city_code_exists(city_code)
            print ("Enter new city details")
            # Create a dummy city dictionary for entering city name
            temp_city = {}
            self.enter_country(temp_city)
            airline_network.edit_country(temp_city['country'], city)
            self.file_mapper.edit_city_country(city_code, temp_city['country'])

    def edit_city_timezone(self, airline_network):
        """Edit timezone of a city in the network.Save changes in json file."""
        city_code = raw_input('Enter code of city which you want to edit')
        if airline_network.city_code_exists(city_code):
            city = airline_network.city_code_exists(city_code)
            print ("Enter new city details")
            # Create a dummy city dictionary for entering city name
            temp_city = {}
            self.enter_timezone(temp_city)
            airline_network.edit_timezone(temp_city['timezone'], city)
            self.file_mapper.edit_city_timezone(city_code, temp_city['timezone'])

    def edit_city_continent(self, airline_network):
        """Edit timezone of a city in the network.Save changes in json file."""
        city_code = raw_input('Enter code of city which you want to edit')
        if airline_network.city_code_exists(city_code):
            city = airline_network.city_code_exists(city_code)
            print ("Enter new city details")
            # Create a dummy city dictionary for entering city name
            temp_city = {}
            self.enter_continent(temp_city)
            airline_network.edit_continent(temp_city['continent'], city)
            self.file_mapper.edit_city_continent(city_code, temp_city['continent'])

    def edit_city_region(self, airline_network):
        """Edit region of a city in the network.Save changes in json file."""
        city_code = raw_input('Enter code of city which you want to edit')
        if airline_network.city_code_exists(city_code):
            city = airline_network.city_code_exists(city_code)
            print ("Enter new city details")
            # Create a dummy city dictionary for entering city name
            temp_city = {}
            self.enter_region(temp_city)
            airline_network.edit_region(temp_city['region'], city)
            self.file_mapper.edit_city_region(city_code, temp_city['region'])

    def edit_city_population(self, airline_network):
        """Edit population of a city in the network.Save changes in json file."""
        city_code = raw_input('Enter code of city which you want to edit')
        if airline_network.city_code_exists(city_code):
            city = airline_network.city_code_exists(city_code)
            print ("Enter new city details")
            # Create a dummy city dictionary for entering city name
            temp_city = {}
            self.enter_population(temp_city)
            city.population = temp_city['population']
            self.file_mapper.edit_city_population(city_code, city.population)

    def edit_city_coordinates(self, airline_network):
        """Edit coordinates of a city in the network.Save changes in json file."""
        city_code = raw_input('Enter code of city which you want to edit')
        if airline_network.city_code_exists(city_code):
            city = airline_network.city_code_exists(city_code)
            print ("Enter new city details")
            # Create a dummy city dictionary for entering city name
            temp_city = {}
            self.enter_coordinates(temp_city)
            city.coordinates = temp_city['coordinates']
            self.file_mapper.edit_city_coordinates(city_code, city.coordinates)

    def get_route_info(self, airline_network):
        """Print cost,time and distance for a route."""
        # enter route
        ports = self.enter_route()
        if len(ports) < 2:
            print 'Cannot provide route information. At least 2 cities must required'
        else:
            self.print_route_info(airline_network, ports)

    def print_route_info(self, airline_network, ports):
            """Helper to print information about a route."""
            distance = 0
            cost = 0
            current_cost = 0.35
            layover_time = timedelta(minutes=0)
            for port_index in range(0, len(ports)-1):
                # collect information for each leg of flight
                route = {'ports': [ports[port_index], ports[port_index+1]]}
                if airline_network.route_exists(route):
                    leg_distance = airline_network.route_exists(route).distance
                    distance += leg_distance
                    cost += leg_distance * current_cost
                    # cost reduces by 0.05 per kilometer for each leg
                    if current_cost > 0:
                        current_cost -= 0.05
                    # add layover time for ports on route
                    if port_index != len(ports)-2:          # don't add layover time for final destination
                        layover_time += self.find_layover_time(airline_network, ports[port_index+1])
                else:
                    print 'Route does not exist'
                    return
                port_index += 1
            print "Distance : %d km" % distance
            print "Cost : $%f" % cost
            time = self.calculate_time(distance) + layover_time
            self.print_time(time)

    @staticmethod
    def enter_route():
        """Helper to get information about a route.Get ports on route from user."""
        print('Enter city codes on the route')
        choice = 'y'
        ports = []
        while choice == 'y' or choice == 'Y':
            ports.append(raw_input('City code: '))
            choice = raw_input('More cities? (y/n)')
        return ports

    @staticmethod
    def calculate_time(distance):
        """Calculate time taken to travel route.
        :return:time taken
        """
        cruise_speed = 750.0
        acceleration = (cruise_speed * cruise_speed)/(2 * 200.0)
        # for distance greater than 400, accelerate for first 200 km and decelerate for last 200 km
        # acceleration and deceleration at constant acceleration
        # cruise for remaining distance
        if distance >= 400:
            cruise_distance = distance - 400.0
            # acceleration = (final_speed^2 - initial_speed^2)/(2 * distance)
            # time = distance/speed for cruising
            # time = (final speed - initial speed)/acceleration  for acceleration and deceleration
            time = (cruise_distance / cruise_speed) + 2 * (cruise_speed / acceleration)
            time_obj = timedelta(hours=time)
        # for distance less than 400 km, accelerate  at constant acceleration for half distance, then decelerate
        else:
            half_distance = distance/2.0
            # time = sqrt(2*distance/acceleration)
            time = 2 * math.sqrt(2 * half_distance / acceleration)
            time_obj = timedelta(hours=time)
        return time_obj

    @staticmethod
    def find_layover_time(airline_network, port):
        """Find layover time for a port in the route """
        outbound_flights = airline_network.routes_connected_to(port)
        layover_time = timedelta(hours=2, minutes=10)
        subtract_time = 10 * len(outbound_flights)
        # subtract 10 minutes for every outbound flight
        # maximum time that can be subtracted is 2 hrs 10 minutes/ 130 minutes
        # subtract_time 0 means no outbound flights, so no layover time possible
        if 0 < subtract_time <= 130:
            layover_time -= (timedelta(minutes=subtract_time))
        else:
            layover_time = timedelta(minutes=0)
        return layover_time

    @staticmethod
    def print_time(time):
        """print time taken to travel route"""
        print "Time: ",
        if time.days != 0:
            print str(time.days) + ' Day(s)',
        hours, remainder = divmod(time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours != 0:
            print str(hours) + ' Hour(s)',
        if minutes != 0:
            print str(minutes) + ' Minute(s)',
        if seconds != 0:
            print str(seconds) + ' Second(s)'

    def get_shortest_route(self, airline_network):
        """Get information about the shortest route between two cities."""
        start_port = raw_input('Enter starting port')
        if not airline_network.city_code_exists(start_port):
            print 'Invalid port entered'
            return
        destination_port = raw_input('Enter destination port')
        if not airline_network.city_code_exists(destination_port):
            print 'Invalid port entered'
            return
        shortest_route = airline_network.get_shortest_route(start_port, destination_port)
        if shortest_route:
            self.print_route_info(airline_network, shortest_route)
        else:
            print 'No route exists'


def main():
    ServiceManager()

if __name__ == '__main__':
    main()
