


class AuthenticatedUserRemoval:
    auth_users = []
    source_file = ''
    destination_file_path = ''

    def __init__(self, source_file_path, destination_file_path):
        self.destination_file_path = destination_file_path
        with open(source_file_path, 'rt') as log:
            self.source_file = log.read()
            log.close()
            self.collect_usernames()

            if len(self.auth_users) > 0:
                self.write_new_file()
                print("new file without authorised users has been written")
            else:
                destination_file = open(self.destination_file_path, 'w')
                destination_file.write(self.source_file)
                print("source written directly to destination as no auth users found")
                destination_file.close()




    def collect_usernames(self):
        # COLLECTING HOSTS AND IPS
        for line in self.source_file.split("\n"):

            if len(line) > 5:
                # PARSE LINE AND ADJUST FIELD LENGTH
                check_1 = line.find("Accepted password for ")
                # check_2 = line.find("Disconnecting")
                # check_3 = line.find("Address")
                # check_4 = line.find("repeated")
                if check_1 > -1:
                    words = line.split("Accepted password for ")
                    words2 = (words[1]).split(" from ")
                    username = words2[0]

                    if not (username in self.auth_users):
                        self.auth_users.append(username)

        i = 0
        for user in self.auth_users:
            i = i + 1
            print str(i)
            print user

    def write_new_file(self):
        destination_file = open(self.destination_file_path, 'w')
        for line in self.source_file.split("\n"):
            if len(line) > 5:
                line_has_auth_user = False
                for user in self.auth_users:
                    if not line_has_auth_user and user in line:
                        line_has_auth_user = True
                    else:
                        destination_file.write(line + '\n')

        print(destination_file)
        destination_file.close()



if __name__ == "__main__":
    # execute only if run as a script
    testAuthUserRemoval = AuthenticatedUserRemoval("Source_files/auth.log", "Source_files/UnAuthorisedOnly.log")
