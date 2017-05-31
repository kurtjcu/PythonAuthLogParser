from datetime import datetime
import pygeoip


class Host:
    ip = "none"
    port = 0
    username = ""
    date_time = ''
    ip_location_info = ''
    did_not_find_count = 0

    def __init__(self, ip, port, username, date):
        self.ip = ip
        self.port = port
        self.username = username
        self.date_time = datetime.strptime("2017 " + date, "%Y %b %d %H:%M:%S")

        gi = pygeoip.GeoIP('../Databases/GeoLiteCity.dat')

        # self.country = gi.country_code_by_addr(ip)
        self.ip_location_info = gi.record_by_addr(ip)

        # {
        #     'city': u'Mountain View',
        #     'region_code': u'CA',
        #     'area_code': 650,
        #     'time_zone': 'America/Los_Angeles',
        #     'dma_code': 807,
        #     'metro_code': 'San Francisco, CA',
        #     'country_code3': 'USA',
        #     'latitude': 37.41919999999999,
        #     'postal_code': u'94043',
        #     'longitude': -122.0574,
        #     'country_code': 'US',
        #     'country_name': 'United States',
        #     'continent': 'NA'
        # }
        if self.ip_location_info is None:
            self.ip_location_info = {
                'city': u'none',
                'region_code': u'none',
                'area_code': 0,
                'time_zone': 'none',
                'dma_code': 0,
                'metro_code': 'none, none',
                'country_code3': 'None',
                'latitude': -100000,
                'postal_code': u'none',
                'longitude': -100000,
                'country_code': 'none',
                'country_name': 'none',
                'continent': 'NA'
            }
            Host.did_not_find_count = Host.did_not_find_count + 1


    def get_ip(self):
        return self.ip

    def get_port(self):
        return self.port

    def get_username(self):
        return self.username

    def get_date_time(self):
        return self.date_time

    def get_date(self):
        return self.date_time.date()

    def get_day(self):
        return self.date_time.weekday()

    def get_time(self):
        return self.date_time.time()

    def get_hour(self):
        return self.date_time.hour

    def get_country(self):
        country = self.ip_location_info['country_name']
        if country is None:
            country = "None"
        return country

    def get_latitude(self):
        lat = self.ip_location_info['latitude']
        #lat.strip(',')
        return str(lat)

    def get_longitude(self):
        return str(self.ip_location_info['longitude'])

    def get_city(self):
        city = self.ip_location_info['city']
        if city is None:
            city = "None"
        return city

    def get_csv(self):
        return self.get_ip() + ',' \
               + self.get_port() + ',' \
               + self.get_username() + ',' \
               + self.get_date_time().__str__() + ',' \
               + self.get_country() + ',' \
               + self.get_city() + ',' \
               + self.get_longitude() + ',' \
               + self.get_latitude()


if __name__ == "__main__":
    # execute only if run as a script
    testHost = Host("189.36.240.195", "8080", "test_username", "Apr 19 15:56:30")

    print ("ip = " + testHost.get_ip())
    print ("port = " + testHost.get_port())
    print ("username = " + testHost.get_username())
    print ("date and time = " + testHost.get_date_time().__str__())
    print ("country = " + testHost.get_country())
    print ("city = " + testHost.get_city())
    print ("longitude = " + str(testHost.get_longitude()))
    print ("latitude = " + str(testHost.get_latitude()))
