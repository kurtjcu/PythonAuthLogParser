import math
from operator import itemgetter

from PreProcessing import Host, FileReader
from collections import Counter, OrderedDict
from random import shuffle


class ToCSV:
    destination_file_path = ''
    source = []
    source_field_names = []

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
        for host in source:
            ip_addresses_all.append(host.get_ip())
            uname_all.append(host.get_username())

        # count and create dict
        ip_address_dict_with_count = Counter(ip_addresses_all)
        uname_dict_with_count = Counter(uname_all)

        # ipAddressAsRank
        ip_address_as_dict_ordered_by_rank = OrderedDict(
            sorted(ip_address_dict_with_count.items(), reverse=False, key=itemgetter(1)))
        print("backwards ip Dict = " + str(ip_address_as_dict_ordered_by_rank))

        uname_as_dict_ordered_by_rank = OrderedDict(
            sorted(uname_dict_with_count.items(), reverse=False, key=itemgetter(1)))
        print("backwards uname Dict = " + str(uname_as_dict_ordered_by_rank))

        # IPAddressesAsRandomInt
        ip_addresses_as_random_int = set(ip_addresses_all)
        ip_addresses_as_random_int = shuffle(list(ip_addresses_as_random_int))

        uname_as_random_int = set(uname_all)
        uname_as_random_int = shuffle(list(uname_as_random_int))




        # write each row
        for attack in self.source:
            host_as_string = attack.get_day().__str__() + "," \
                             + attack.get_hour().__str__() + "," \
                             + '\"\"\"' + str(attack.get_ip()) + '\"\"\"' + "," \
                             + str(attack.get_port()) + "," \
                             + '\"\"\"' + str(attack.get_username()) + '\"\"\"' + "," \
                             + '\"\"\"' + str(attack.get_country().replace(',', '')).replace(' ', '_') + '\"\"\"' + "," \
                             + '\"\"\"' + str(attack.get_city().replace(',', '')).replace(' ', '_') + '\"\"\"' + "," \
                             + str(attack.get_longitude()) + "," \
                             + str(attack.get_latitude()) + '\n'

            destination_file.write(host_as_string)

        destination_file.close()

        def normalise(self, array):
            array_min = min(array)
            array_max = max(array)
            temp_array = []

            for number in array:
                temp_array.append(number - array_min) / (array_max - array_min)

            return temp_array


if __name__ == "__main__":
    # execute only if run as a script
    source_field_names = FileReader.FileReader.get_field_names()
    source_file_reader = FileReader.FileReader("../Source_files/smallUnauthOnly.log")
    source = source_file_reader.get_hosts()

    my_csv = ToCSV(source, source_field_names, "../Source_files/smallCSV.csv")
    my_csv.write_new_file()
