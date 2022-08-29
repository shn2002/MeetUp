import googlemaps


class User:
    def __init__(self, name='', password='', occupation='', address='', age=-1):
        self.name = name
        self.password = password
        self.occupation = occupation
        self.address = address
        self.age = age
        self.lat = 0
        self.lng = 0
        self.id = -1
        self.messages = []
        self.get_coordinates()


    def add_message(self, messages):
        self.messages = messages

    # convert the address to lag and lng.
    def get_coordinates(self):
        API_KEY = ''
        gmaps = googlemaps.Client(key=API_KEY)
        coordinates = gmaps.geocode(self.address)[0].get("geometry").get("location")
        self.lat, self.lng = coordinates['lat'], coordinates['lng']

    def get_user(self):
        return self.name, self.password, self.occupation, self.address, self.age, self.lat, self.lng
