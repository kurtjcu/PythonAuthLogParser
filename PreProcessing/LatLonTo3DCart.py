import math

class LatLonTo3DCart:
    earth_radis_in_Km  = 1
    lat = 0
    lon = 0
    x = 0
    y = 0
    z = 0

    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

        #self.calc_3DCart()
        self.LLHtoECEF()


    def calc_3DCart(self):
        latRad = math.radians(self.lat)
        lonRad = math.radians(self.lon)

        self.x =  math.sin(lonRad) * math.cos(latRad)
        self.y =  math.sin(lonRad) * math.sin(latRad)
        self.z =  math.cos(lonRad)

    def LLHtoECEF(self):
        # see http://www.mathworks.de/help/toolbox/aeroblks/llatoecefposition.html
        alt = 0 #assume zero altitude
        rad = self.earth_radis_in_Km  # Radius of the Earth (in meters)
        f = 1.0 / 298.257223563  # Flattening factor WGS84 Model
        cosLat = math.cos(self.lat)
        sinLat = math.sin(self.lat)
        FF = (1.0 - f) ** 2
        C = 1 / math.sqrt(cosLat ** 2 + FF * sinLat ** 2)
        S = C * FF

        self.x = (((rad * C + alt) * cosLat * math.cos(self.lon)) + 1)/2
        self.y = (((rad * C + alt) * cosLat * math.sin(self.lon)) + 1)/2
        self.z = (((rad * S + alt) * sinLat) + 1)/2


    def get_cart_Coords(self):
        return ("{}, {}, {}".format(self.x, self.y, self.z))

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_z(self):
        return self.z

    @staticmethod
    def get_coords(lat, long):
        coords = LatLonTo3DCart(lat, long)
        return coords.get_cart_Coords()

if __name__ == "__main__":
    # execute only if run as a script

    print("0,0 >> " + str(LatLonTo3DCart.get_coords(0,0)))
    # print("0,0 >> " + str(LatLonTo3DCart(0, 0).get_cart_Coords()))
    # print("90,0 >> " + str(LatLonTo3DCart(90, 0).get_cart_Coords()))
    # print("-90,0 >> " + str(LatLonTo3DCart(-90, 0).get_cart_Coords()))
    # print("0,180 >> " + str(LatLonTo3DCart(0, 180).get_cart_Coords()))
    # print("0,-180 >> " + str(LatLonTo3DCart(0, -180).get_cart_Coords()))
    #
    # print("90,180 >> " + str(LatLonTo3DCart(180,180).get_cart_Coords()))
    # print("-90,-180 >> " + str(LatLonTo3DCart(-180, -180).get_cart_Coords()))
    # print("90,-180 >>" + str(LatLonTo3DCart(180, -180).get_cart_Coords()))
    # print("-90,180 >>" + str(LatLonTo3DCart(-180, 180).get_cart_Coords()))

