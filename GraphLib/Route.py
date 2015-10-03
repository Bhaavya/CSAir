class Route:
    """Form a route edge from dictionary."""
    def __init__(self,route):
        self.distance = route['distance']
        self.ports = route['ports']