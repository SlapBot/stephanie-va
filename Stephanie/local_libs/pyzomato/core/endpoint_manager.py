class EndpointManager:
    def __init__(self):
        self.base_url = "https://developers.zomato.com/api/v2.1"
        self.endpoints = self.get_endpoints()

    def get_endpoints(self):
        endpoints = {
            'categories': self.base_url + '/categories',
            'locations': self.base_url + '/locations',
            'location_details': self.base_url + '/location_details',
        }
        return endpoints

    def get_endpoint(self, name):
        return self.endpoints[name]
