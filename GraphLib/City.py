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