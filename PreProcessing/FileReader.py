from Host import Host


class FileReader:
    hosts = []

    def __init__(self, file_path):
        with open(file_path, 'rt') as log:
            text = log.read()

        # COLLECTING HOSTS AND IPS
        for line in text.split("\n"):

            if len(line) > 5:
                # PARSE LINE AND ADJUST FIELD LENGTH
                check_1 = line.find("cron:session")
                check_2 = line.find("Disconnecting")
                check_3 = line.find("Address")
                check_4 = line.find("repeated")
                if check_1 == -1 and check_2 == -1 and check_3 == -1 and check_4 == -1:
                    break_in = line.find("Failed password")
                    if break_in != -1:
                        words = line.split(" from ")
                        words2 = (words[1]).split(" port ")

                        ip = words2[0]
                        port = self.get_ports(line)  # GET PORT USED
                        datetime = self.get_date(line)  # GET DATE
                        username = self.get_username(line)



                        host = Host(ip, port, username, datetime)
                        self.hosts.append(host)
        i = 0
        for host in self.hosts:
            i = i + 1
            print (str(i))
            print (host.get_csv())

        print("Number of IP Addresses not found = " + str(Host.did_not_find_count))

    def get_hosts(self):
        return self.hosts

    @staticmethod
    def get_date(my_line):
        date_words = my_line.split(":")
        date = date_words[0] + ":" + date_words[1] + ":" + ((date_words[2]).split(" "))[0]
        return date

    @staticmethod
    def get_ports(my_line):
        port_words = my_line.split(" port ")
        port = (port_words[1]).split(" ")
        return port[0]

    @staticmethod
    def get_username(my_line):

        if my_line.find("Failed password for invalid user ") == -1:
            username_words = my_line.split("Failed password for ")
        else:
            username_words = my_line.split("Failed password for invalid user ")

        username = (username_words[1]).split(" ")
        return username[0]

    @staticmethod
    def get_field_names():
        return ["DayOfWeek", "TimeOfDay", "HourSinceStart", "DaySinceStart" "ScaledTime", "IP_Address", "IP_AsRank", "IP_AsAttackCount", "IP_AsRandomInt", "Port", "PortNormalised", "Uname", "UName_AsRank", "UName_AsCount", "UName_AsRandomInt",  "Country", "City", "Loc_X", "Loc_Y", "Loc_Z"]


if __name__ == "__main__":
    # execute only if run as a script
    testFile_reader = FileReader("../Source_files/smallUnauthOnly.log") #Source_files/smallUnauthOnly.log
