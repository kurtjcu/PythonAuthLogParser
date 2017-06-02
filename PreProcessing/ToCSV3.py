import datetime
import math
from operator import itemgetter
import numpy as np

from PreProcessing import Host, FileReader, LatLonTo3DCart
from collections import Counter, OrderedDict
from random import shuffle


class ToCSV:
    destination_file_path = ''
    source = []
    source_field_names = []
    date_time_max = 0
    date_time_min = 0
    ip_rank_max = 0
    ip_rank_min = 0
    ip_count_max = 0
    ip_count_min = 0
    ip_int_max = 0
    ip_int_min = 0
    uname_rank_max = 0
    uname_rank_min = 0
    uname_count_max = 0
    uname_count_min = 0
    uname_int_max = 0
    uname_int_min = 0
    port_max = 0
    port_min = 0

    def __init__(self, source, source_field_names, destination_file_path):
        self.destination_file_path = destination_file_path
        self.source = source
        self.source_field_names = source_field_names

    def write_new_file(self):
        destination_file = open(self.destination_file_path, encoding='utf-8', mode='w+')  # encoding='utf-8', mode='w+'

        # write the names of the fields
        field_names_as_string = ''

        for name in self.source_field_names:
            field_names_as_string = field_names_as_string + name
            if self.source_field_names.index(name) != len(self.source_field_names) - 1:
                field_names_as_string = field_names_as_string + ","

        destination_file.write(field_names_as_string + '\n')

        # write each row

        # first remove any entries if lat or long = -100000
        for host in source:
            if host.get_latitude() == "-100000" or host.get_longitude() == "-100000":
                source.remove(host)
                print("removed = " + host.get_longitude())

        # collect lists of data to be normalised

        # create list if items we want to process further
        ip_addresses_all = []
        uname_all = []
        date_time_all = []
        port_all = []
        for host in source:
            ip_addresses_all.append(host.get_ip())
            uname_all.append(host.get_username())
            date_time_all.append(self.get_seconds_since_epoc(host))
            port_all.append(host.get_port())

        # count and create dict
        ip_address_dict_with_count = Counter(ip_addresses_all)
        uname_dict_with_count = Counter(uname_all)

        # ipAddressAsRank
        ip_address_as_dict_ordered_by_rank = OrderedDict(
            sorted(ip_address_dict_with_count.items(), reverse=True, key=itemgetter(1)))
        print("backwards ip Dict = " + str(ip_address_as_dict_ordered_by_rank))

        uname_as_dict_ordered_by_rank = OrderedDict(
            sorted(uname_dict_with_count.items(), reverse=True, key=itemgetter(1)))
        print("backwards uname Dict = " + str(uname_as_dict_ordered_by_rank))

        # IPAddressesAsRandomInt
        ip_addresses_as_random = set(ip_addresses_all)
        ip_addresses_as_random = list(ip_addresses_as_random)
        shuffle(ip_addresses_as_random)
        ip_addresses_as_random_int = {}
        for index in range(len(ip_addresses_as_random)):
            ip_addresses_as_random_int[ip_addresses_as_random[index]] = index

        # unameAsRandomInt
        uname_as_random = set(uname_all)
        uname_as_random = list(uname_as_random)
        shuffle(uname_as_random)
        uname_as_random_int = {}
        for index in range(len(uname_as_random)):
            uname_as_random_int[uname_as_random[index]] = index

        # set max and min for all
        self.date_time_max = max(date_time_all)
        self.date_time_min = min(date_time_all)
        self.ip_rank_max = len(ip_address_as_dict_ordered_by_rank)
        self.ip_rank_min = 0
        self.ip_count_max = max(ip_address_dict_with_count.values())
        self.ip_count_min = min(ip_address_dict_with_count.values())
        self.ip_int_max = max(ip_addresses_as_random_int.values())
        self.ip_int_min = min(ip_addresses_as_random_int.values())
        self.uname_rank_max = len(uname_as_dict_ordered_by_rank)
        self.uname_rank_min = 0
        self.uname_count_max = max(uname_dict_with_count.values())
        self.uname_count_min = min(uname_dict_with_count.values())
        self.uname_int_max = max(uname_as_random_int.values())
        self.uname_int_min = min(uname_as_random_int.values())
        self.port_max = max(port_all)
        self.port_min = min(port_all)

        print(self.date_time_max)
        print(self.date_time_min)

        # write each row
        for attack in self.source:
            position = LatLonTo3DCart.LatLonTo3DCart.get_coords(float(attack.get_latitude()),
                                                                float(attack.get_longitude()))
            seconds_since_start = self.get_seconds_since_epoc(attack) - self.date_time_min

            host_as_string = attack.get_day().__str__() + "," \
                             + attack.get_hour().__str__() + "," \
                             + str(int(seconds_since_start / (60 * 60))) + ',' \
                             + str(int(seconds_since_start / (60 * 60 * 24))) + ',' \
                             + str(
                self.normalise(self.date_time_max, self.date_time_min, self.get_seconds_since_epoc(attack))) + ',' \
                             + '\"\"\"' + str(attack.get_ip()) + '\"\"\"' + "," \
                             + str(self.normalise(self.ip_rank_max, self.ip_rank_min,
                                                  list(ip_address_as_dict_ordered_by_rank.keys()).index(
                                                      attack.get_ip()))) + ',' \
                             + str(self.normalise(math.log(self.ip_rank_max), math.log(0.0000000001),
                                                  self.log_scaling(list(ip_address_as_dict_ordered_by_rank.keys()).index(
                                                      attack.get_ip())))) + ',' \
                             + str(self.normalise(self.ip_count_max, self.ip_count_min,
                                                  ip_address_dict_with_count.get(attack.get_ip()))) + ',' \
                             + str(self.normalise(self.ip_int_max, self.ip_int_min,
                                                  ip_addresses_as_random_int.get(attack.get_ip()))) + ',' \
                             + str(attack.get_port()) + "," \
                             + str(self.normalise(self.port_max, self.port_min, attack.get_port())) + "," \
                             + '\"\"\"' + str(attack.get_username()) + '\"\"\"' + "," \
                             + str(self.normalise(self.uname_rank_max, self.uname_rank_min,
                                                  list(uname_as_dict_ordered_by_rank.keys()).index(
                                                      attack.get_username()))) + ',' \
                             + str(self.normalise(math.log(self.uname_rank_max), math.log(0.0000000001),
                                                  self.log_scaling(list(uname_as_dict_ordered_by_rank.keys()).index(
                                                      attack.get_username())))) + ',' \
                             + str(self.normalise(self.uname_count_max, self.uname_count_min,
                                                  uname_dict_with_count.get(attack.get_username()))) + ',' \
                             + str(self.normalise(self.uname_int_max, self.uname_int_min,
                                                  uname_as_random_int.get(attack.get_username()))) + ',' \
                             + '\"\"\"' + str(attack.get_country().replace(',', '')).replace(' ', '_') + '\"\"\"' + "," \
                             + '\"\"\"' + str(attack.get_city().replace(',', '')).replace(' ', '_') + '\"\"\"' + "," \
                             + position + '\n'

            destination_file.write(host_as_string)

        destination_file.close()

    def normalise_array(self, array):
        array_min = min(array)
        array_max = max(array)
        temp_array = []

        for number in array:
            temp_array.append((number - array_min) / (array_max - array_min))

        return temp_array

    def normalise(self, max, min, value):
        return (value - min) / (max - min)

    def get_seconds_since_epoc(self, host):
        date_time = host.get_date_time()
        epoc = datetime.datetime.utcfromtimestamp(0)
        return (date_time - epoc).total_seconds()

    def log_scaling(self, dataset):
        dataset = np.array(dataset)
        return self.safe_ln(dataset)

    def safe_ln(self, x, minval=0.0000000001):
        return np.log(x.clip(min=minval))


if __name__ == "__main__":
    # execute only if run as a script
    source_field_names = FileReader.FileReader.get_field_names()
    source_file_reader = FileReader.FileReader("../Source_files/UnAuthorisedOnly.log")
    source = source_file_reader.get_hosts()

    my_csv = ToCSV(source, source_field_names, "../Source_files/fullCSV.csv")
    my_csv.write_new_file()
