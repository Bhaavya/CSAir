from UserInterface.TextualUserInterface import UserInterface
from LoadGraph import LoadGraph
import sys
import webbrowser

DESTINATION_PORT = 1
SOURCE_PORT = 0
LATITUDE = 0
LONGITUDE = 0


class ServiceManager:
    """Manage user queries. """
    graphLoader = LoadGraph()

    def __init__(self):
        self.graphLoader.populate_graph('../Resources/map_data.json')
        interface = UserInterface()
        self.manage_main_menu(interface)

    def manage_main_menu(self, interface):
        # display main menu
        user_choice = interface.print_menu()
        airline_network = self.graphLoader.airline_network
        # handle queries till user quits
        while user_choice != 'q':
            if user_choice == '1':
                self.display_cities()
            elif user_choice == '2':
                self.manage_city_menu(interface)
            elif user_choice == '3':
                self.manage_stats_menu(interface)
            elif user_choice == '4':
                webbrowser.open(airline_network.visualise())
            else:
                print 'Invalid option.Try again!\n'
            user_choice = interface.print_menu()
        sys.exit(0)

    def manage_city_menu(self,interface):
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

    def manage_stats_menu(self,interface):
        # display statistical information menu
        user_choice = interface.stats_info()
        airline_network = self.graphLoader.airline_network          # graph of route map
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

    def get_city_code(self):
        """Print the city code based on city name if city name is valid."""
        city_name = raw_input('Enter city name\n')
        city = self.graphLoader.airline_network.city_name_exists(city_name)     # get city node
        if city is not None:
            print city.code
        else:
            print 'Invalid name entered.Try again!\n'

    def get_city_name(self):
        """Print the city name based on city code if city code is valid."""
        city_code = raw_input('Enter city code\n')
        city = self.graphLoader.airline_network.city_code_exists(city_code)     # get city node
        if city is not None:
            print city.name
        else:
            print 'Invalid code entered.Try again!\n'

    def get_city_country(self):
        """Print the country of city based on city code if city code is valid."""
        city_code = raw_input('Enter city code\n')
        city = self.graphLoader.airline_network.city_code_exists(city_code)     # get city node
        if city is not None:
            print city.country
        else:
            print 'Invalid code entered.Try again!\n'

    def get_city_continent(self):
        """Print the continent of city based on city code if city code is valid."""
        city_code = raw_input('Enter city code\n')
        city = self.graphLoader.airline_network.city_code_exists(city_code)     # get city node
        if city is not None:
            print city.continent
        else:
            print 'Invalid code entered.Try again!\n'

    def get_city_timezone(self):
        """Print the timezone of city based on city code if city code is valid."""
        city_code = raw_input('Enter city code\n')
        city = self.graphLoader.airline_network.city_code_exists(city_code)     # get city node
        if city is not None:
            print city.timezone
        else:
            print 'Invalid code entered.Try again!\n'

    def get_city_coordinates(self):
        """Print the coordinates of city based on city code if city code is valid."""
        city_code = raw_input('Enter city code\n')
        city = self.graphLoader.airline_network.city_code_exists(city_code)     # get city node
        if city is not None:
            for coordinate in city.coordinates:
                print coordinate + ' ' + str(city.coordinates[coordinate])
        else:
            print 'Invalid code entered.Try again!\n'

    def get_city_population(self):
        """Print the city population based on city code if city code is valid."""
        city_code = raw_input('Enter city code\n')
        city = self.graphLoader.airline_network.city_code_exists(city_code)     # get city node
        if city is not None:
            print city.population
        else:
            print 'Invalid code entered.Try again!'

    def get_city_region(self):
        """Print the city region based on city code if city code is valid."""
        city_code = raw_input('Enter city code\n')
        city = self.graphLoader.airline_network.city_code_exists(city_code)     # get city node
        if city is not None:
            print city.region
        else:
            print 'Invalid code entered.Try again!\n'

    def get_connected_cities(self):
        """Print the cities connected via non-stop single flight based on city code if city code is valid."""
        city_code = raw_input('Enter city code\n')
        airline_network = self.graphLoader.airline_network
        city = self.graphLoader.airline_network.city_code_exists(city_code)     # get city node
        if city is not None:
            connected_city_routes = airline_network.routes_connected_to(city_code)      # get routes connecting the city
            for route in connected_city_routes:
                print 'City: ' + route.ports[DESTINATION_PORT] + ' Distance: %d' % route.distance

    def display_cities(self):
        """Print all cities in the network."""
        cities = self.graphLoader.airline_network.cities
        for city in cities:
            print city.name

    def print_longest_flight(self):
        """Print information about longest flight in the network."""
        airline_network = self.graphLoader.airline_network
        longest_route = airline_network.get_longest_flight()
        print "Longest flight is between: " + longest_route .ports[SOURCE_PORT] + " and " + \
              longest_route.ports[DESTINATION_PORT] + " , Distance: %d" % longest_route.distance

    def print_shortest_flight(self):
        """Print information about shortest flight in the network."""
        airline_network = self.graphLoader.airline_network
        shortest_route = airline_network.get_shortest_flight()
        print "Shortest flight is between: " + shortest_route .ports[SOURCE_PORT] + " and " + \
              shortest_route.ports[DESTINATION_PORT] + " , Distance: %d" % shortest_route.distance

    def print_continents(self):
        """Print continents covered by the network along with the cities covered in each continent."""
        airline_network = self.graphLoader.airline_network
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

    def print_hubs(self, hub_list):
        """Print all cities having maximum number of connections."""
        for hub in hub_list:
            print str(hub)


def main():
    ServiceManager()

if __name__ == '__main__':
    main()




