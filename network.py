"""
File:    network.py
Author:  Toni Olafunmiloye
Date:    12/4/20
Section: 41
E-mail:  oolafun1@umbc.edu
Description: This file is the network class
"""

"""
network.py is both the definition file for the Network class as well as the driver for the program.

In network you need to implement the functions which the driver will call for the all the different commands.
"""

from phone import Phone
from switchboard import Switchboard
import csv


"""                                                                                                                                                                                                                                                           
import json                                                                                                                                                                                                                                                   
import csv (you can do either if you choose, or just use the regular file io)                                                                                                                                                                                 

Some constants below are for the driver, don't remove them unless you mean to.                                                                                                                                                                                
"""

HYPHEN = "-"
QUIT = 'quit'
SWITCH_CONNECT = 'switch-connect'
SWITCH_ADD = 'switch-add'
PHONE_ADD = 'phone-add'
NETWORK_SAVE = 'network-save'
NETWORK_LOAD = 'network-load'
START_CALL = 'start-call'
END_CALL = 'end-call'
DISPLAY = 'display'


# switch-add 443
# Enter command: switch-add 410
# Enter command: switch-add 656
# Enter command: switch-connect 443 410
# Enter command: phone-add 656-112-3412
# Enter command: phone-add 443-132-1332
# Enter command: phone-add 410-111-2222
# Enter command: switch-connect 656 410
# Enter command: start-call 656-112-3412 443-132-1332

class Network:
    def __init__(self):
        """
            Construct a network by creating the switchboard container object

            You are free to create any additional data/members necessary to maintain this class.
        """
        self.switchboard_list = []

    def load_network(self, filename):
        """
        :param filename: the name of the file to be loaded.  Assume it exists and is in the right format.
                If not, it's ok if your program fails.
        :return: success?
        """
        self.switchboard_list = []

        with open(filename, "r") as read_csv_file:

            for line in read_csv_file:
                if "Switchboard:" in line:
                    line = line.split(" ")
                    switchboard = Switchboard(line[1])
                    self.switchboard_list.append(switchboard)


    def save_network(self, filename):
        """
        :param filename: the name of your file to save the network.  Remember that you need to save all the
            connections, but not the active phone calls (they can be forgotten between save and load).
            You must invent the format of the file, but if you wish you can use either json or csv libraries.
        :return: success?
        """
        # file should be 'file.csv'
        with open(filename, "w", newline='') as save_file:
            for i in range(len(self.switchboard_list)):
                save_file.write("Switchboard: " + str(self.switchboard_list[i].area_code) + "\n" + "\t" +
                                "Phone Numbers: " + str(self.switchboard_list[i].switchboard_phone_number_list) + "\n" + "\t" +
                                "Trunk Lines: " + str(self.switchboard_list[i].trunk_lines) + "\n")

    def add_switchboard(self, area_code):
        """
        add switchboard should create a switchboard and add it to your network.

        By default it is not connected to any other boards and has no phone lines attached.
        :param area_code: the area code for the new switchboard
        :return:
        """
        switchboard = Switchboard(area_code)
        self.switchboard_list.append(switchboard)

    def connect_switchboards(self, area_1, area_2):
        """
            Connect switchboards should connect the two switchboards (creates a trunk line between them)
            so that long distance calls can be made.
        :param area_1: area-code 1
        :param area_2: area-code 2
        :return: success/failure
        """

        for i in range(len(self.switchboard_list)):
            if area_1 == self.switchboard_list[i].area_code:
                variable = self.switchboard_list[i]
                for j in range(len(self.switchboard_list)):
                    if area_2 == self.switchboard_list[j].area_code:
                        variable_2 = self.switchboard_list[j]
                        self.switchboard_list[i].add_trunk_connection(variable_2)
                        self.switchboard_list[j].add_trunk_connection(variable)

    def display(self):
        """
            Display should output the status of the phone network as described in the project.
        """
        for switchboard in self.switchboard_list:
            print("Switchboard with area code: ", switchboard.area_code)

            print("\t", "Trunk lines are: ")
            for line in switchboard.trunk_lines:
                print("\t\t", "Trunk line connection to:", line.area_code)

            print("\t", "Local phone numbers are: ")
            for phone in switchboard.switchboard_phone_number_list:
                if phone.connected == None:
                    print("\t\t", "Phone with number:", phone.number, "is not in use")
                else:
                    print("\t\t", "Phone with number:", phone.number, "is connected to", phone.connected.switchboard.area_code, "-", phone.connected.number)
        print()


if __name__ == '__main__' :
    the_network = Network()
    s = input('Enter command: ')
    while s.strip().lower() != QUIT :
        split_command = s.split()
        if len(split_command) == 3 and split_command[0].lower() == SWITCH_CONNECT :
            area_1 = int(split_command[1])
            area_2 = int(split_command[2])
            the_network.connect_switchboards(area_1, area_2)

        elif len(split_command) == 2 and split_command[0].lower() == SWITCH_ADD :
            the_network.add_switchboard(int(split_command[1]))

        elif len(split_command) == 2 and split_command[0].lower() == PHONE_ADD :
            number_parts = split_command[1].split(HYPHEN)
            area_code = int(number_parts[0])
            phone_number = int(''.join(number_parts[1 :]))

            for i in range(len(the_network.switchboard_list)):
                if area_code == the_network.switchboard_list[i].area_code:
                    the_network.switchboard_list[i].add_phone(phone_number)

        elif len(split_command) == 2 and split_command[0].lower() == NETWORK_SAVE :
            the_network.save_network(split_command[1])
            print('Network saved to {}.'.format(split_command[1]))

        elif len(split_command) == 2 and split_command[0].lower() == NETWORK_LOAD :
            the_network.load_network(split_command[1])
            print('Network loaded from {}.'.format(split_command[1]))

        elif len(split_command) == 3 and split_command[0].lower() == START_CALL :
            src_number_parts = split_command[1].split(HYPHEN)
            src_area_code = int(src_number_parts[0])
            src_number = int(''.join(src_number_parts[1 :]))

            dest_number_parts = split_command[2].split(HYPHEN)
            dest_area_code = int(dest_number_parts[0])
            dest_number = int(''.join(dest_number_parts[1 :]))

            for s in range(len(the_network.switchboard_list)):
                if src_area_code == the_network.switchboard_list[s].area_code:
                    for d in range(len(the_network.switchboard_list[s].switchboard_phone_number_list)):
                        if the_network.switchboard_list[s].switchboard_phone_number_list[d].number == src_number:
                            the_network.switchboard_list[s].switchboard_phone_number_list[d].connect(dest_area_code, dest_number)

        elif len(split_command) == 2 and split_command[0].lower() == END_CALL :
            number_parts = split_command[1].split('-')
            area_code = int(number_parts[0])
            number = int(''.join(number_parts[1 :]))

            for i in range(len(the_network.switchboard_list)):
                if area_code == the_network.switchboard_list[i].area_code:
                    for j in range(len(the_network.switchboard_list[i].switchboard_phone_number_list)):
                        if number == the_network.switchboard_list[i].switchboard_phone_number_list[j].number:
                            if the_network.switchboard_list[i].switchboard_phone_number_list[j].connected != None:
                                the_network.switchboard_list[i].switchboard_phone_number_list[j].disconnect()
                                print("Connection terminated")
                            else:
                                print("Unable to disconnect")


        elif len(split_command) >= 1 and split_command[0].lower() == DISPLAY :
            the_network.display()

        s = input('Enter command: ')




