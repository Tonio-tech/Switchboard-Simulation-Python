"""
File:    switchboard.py
Author:  Toni Olafunmiloye
Date:    12/4/20
Section: 41
E-mail:  
Description: The file in the switchboard class
"""

"""
    Switchboard class

"""

from phone import Phone


class Switchboard:
    def __init__(self, area_code):
        """
        :param area_code: the area code to which the switchboard will be associated.
        """
        self.area_code = area_code
        self.switchboard_phone_number_list = []
        self.trunk_lines = []

    def add_phone(self, phone_number):
        """
        This function should add a local phone connection by creating a phone object
        and storing it in this class.  How you do that is up to you.

        :param phone_number: phone number without area code
        :return: depends on implementation / None
        """
        if phone_number in self.switchboard_phone_number_list:
            print("This phone number has already been added")
        else:
            phone = Phone(phone_number, self)
            self.switchboard_phone_number_list.append(phone)


    def add_trunk_connection(self, switchboard):
        """
        Connect the switchboard (self) to the switchboard (switchboard)

        :param switchboard: should be either the area code or switchboard object to connect.
        :return: success/failure, None, or it's up to you
        """
        self.trunk_lines.append(switchboard)

    def connect_call(self, area_code, number, previous_codes):
        """
        This must be a recursive function.

        :param area_code: the area code to which the destination phone belongs
        :param number: the phone number of the destination phone without area code.
        :param previous_codes: you must keep track of the previously tracked codes
        :return: Depends on your implementation, possibly the path to the destination phone.
        """

        for line in self.trunk_lines:
            if line.area_code not in previous_codes:
                if line.area_code == area_code:
                    for i in line.switchboard_phone_number_list:
                        if number == i.number:
                            return i
                previous_codes.append(self.area_code)
                return line.connect_call(area_code, number, previous_codes)

        if self.trunk_lines == []:
            if self.area_code == area_code:
                for i in self.switchboard_phone_number_list:
                    if number == i.number:
                        return i


