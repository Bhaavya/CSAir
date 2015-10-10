class UserInterface:
    """Create a text based user interface for handling user queries."""
    def __init__(self):
        print('Welcome to  CSAir')

    @staticmethod
    def print_menu():
        # Prints main menu options and returns user's choice
        print('\nWhat do you want to know about?')
        print('1. Get list of all cities that CSAir Flies to')
        print('2. Get information about a specific city in CSAir route network')
        print('3. Get Statistical information about CSAir\'s route network')
        print('4. Visualise route map')
        print('5. Edit network')
        print('6. Get information about a route')
        print('7. Get shortest route between any two cities')
        print('q. Exit')
        option = raw_input('Enter option\n')
        return option

    @staticmethod
    def city_info():
        # Prints options for queries related to cities and returns user's choice
        print('\nWhat would you like to know about the city?')
        print('1. Code')
        print('2. Name')
        print('3. Country')
        print('4. Continent')
        print('5. Timezone')
        print('6. Coordinates')
        print('7. Population')
        print('8. Region')
        print('9. Connected cities via a nonstop single flight')
        print('10. Go back to main menu')
        print('q. Exit')
        option = raw_input('Enter option\n')
        return option

    @staticmethod
    def stats_info():
        # Prints options related to statistical queries of the network and returns user's choice
        print('\nWhat would you like to know about CSAir\'s route network?')
        print('1. Get Longest Single Flight in the Network')
        print('2. Get the shortest Single Flight in the network')
        print('3. Get the average distance of all the flights in the network')
        print('4. Get the biggest city (by population) served by CSAir')
        print('5. Get the smallest city (by population) served by CSAir')
        print('6. Get the average size (by population) of all the cities served by CSAir')
        print('7. Get a list of all the continents served by CSAir and the cities within that continent')
        print('8. Get the list of CSAir Hub-Cities')
        print('9. Go back to main menu')
        print('q. Exit')
        option = raw_input('Enter option\n')
        return option

    @staticmethod
    def print_edit_menu():
        # Prints options for editing route network
        print('\nWhat would you like to edit?')
        print('1. Add a city')
        print('2. Add a route')
        print('3. Remove a city')
        print('4. Remove a route')
        print('5. Edit an existing city')
        print('6. Go back to main menu')
        print('q. Exit')
        option = raw_input('Enter option\n')
        return option

    @staticmethod
    def print_edit_city_menu():
        print('\nWhat do you want to edit?')
        print('1.City code')
        print('2.City name')
        print('3.City country')
        print('4.City continent')
        print('5.City coordinates')
        print('6.City timezone')
        print('7.City population')
        print('8. City region')
        print('9. Go back to main menu')
        print('q. Exit')
        option = raw_input('Enter option\n')
        return option
