from PreProcessing import Host, FileReader


class ToCSV:
    destination_file_path = ''
    source = []
    source_field_names = []

    def __init__(self, source, source_field_names, destination_file_path):
        self.destination_file_path = destination_file_path
        self.source = source
        self.source_field_names = source_field_names

    def write_new_file(self):
        destination_file = open(self.destination_file_path, encoding='utf-8', mode='w+') #encoding='utf-8', mode='w+'

        # write the names of the fields
        field_names_as_string = ''

        for name in self.source_field_names:
            field_names_as_string = field_names_as_string + name
            if self.source_field_names.index(name) != len(self.source_field_names) - 1:
                field_names_as_string = field_names_as_string + ","

        destination_file.write(field_names_as_string + '\n')

        # write each row


        for attack in self.source:

            host_as_string = attack.get_day().__str__() + ","\
                            + attack.get_hour().__str__() + ","\
                            + str(attack.get_ip()) + ","\
                            + str(attack.get_port()) + ","\
                            + str(attack.get_username()) + ","\
                            + str(attack.get_country().replace(',', '')).replace(' ', '_') + ","\
                            + str(attack.get_city().replace(',', '')).replace(' ', '_')  + ","\
                            + str(attack.get_longitude()) + ","\
                            + str(attack.get_latitude()) + '\n'\


            destination_file.write(host_as_string)

        destination_file.close()


if __name__ == "__main__":
    # execute only if run as a script
    source_field_names = FileReader.FileReader.get_field_names()
    source_file_reader = FileReader.FileReader("../Source_files/UnAuthorisedOnly.log")
    source = source_file_reader.get_hosts()

    my_csv = ToCSV(source, source_field_names, "../Source_files/someshit.csv")
    my_csv.write_new_file()
