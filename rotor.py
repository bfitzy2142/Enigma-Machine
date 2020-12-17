#!/usr/bin/env python3


class Rotor():
    """ The rotor object is used to maintain state of a single rotor object
    as part of the enigma cypher machine. The rotors are where the letter
    scrambling happens by substituting one letter by another, the parameters
    of which change each time a letter passes through with rotor rotation. Some
    parameters are setup beforehand by the Enigma operator such as the ring
    setting (Ringstellung in German), and initial rotor postion. The rotor
    settings along with the plugboard are what make the Enigma secure.
    To be exact, the Enigma has 158,962,555,217,826,360,000
    different settings.

    Read more about it here:
    https://en.wikipedia.org/wiki/Enigma_machine#Rotors
    https://en.wikipedia.org/wiki/Enigma_rotor_details


    Brad Fitzgerald
    December 2020
    """

    def __init__(self, rotor_string, position, rotor_number, ring_position):
        """initiator for rotor class

        Args:
            rotor_string ([str): 26 letter scrambled encoding scheme

            position (int): maps the current character at the front of the
            26 letter encoding stack

            rotor_number (int): marks the rotor type (typically 1 to 5)
            ring_position (int): Changes the initial mapping from ab..z to
            a shifted postion left by rotor_number positions

            For details on how an actual rotor works:
            http://www.ellsbury.com/ultraenigmawirings.htm
        """
        self.position = position
        self.rotor_number = rotor_number
        self.rotor_string = rotor_string

        # Configure the turnover postion
        self.turnover = 0
        if (self.rotor_number == 1):
            self.turnover = 18
        elif (self.rotor_number == 2):
            self.turnover = 6
        elif (self.rotor_number == 3):
            self.turnover = 23
        elif (self.rotor_number == 4):
            self.turnover = 11
        elif (self.rotor_number == 5):
            self.turnover = 1

        self.ring_position = ring_position

        self.rotor_config = self.generate_rotor(rotor_string)

    def generate_rotor(self, rotor_string):
        """Sets up rotor configuration

        Args:
            rotor_string (str): 26 letter scrambled encoding scheme

        Returns:
            [list]: each list item contains a mapping from
            one letter to another.
        """

        a = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

        position_array = []

        if self.ring_position != 1:
            for item in rotor_string:
                shift_char = self.apply_ring_setting(item)
                newchar = a[shift_char]
                position_array.append(newchar)
            for iteration in range(0, self.ring_position - 1):
                position_array.insert(0, position_array.pop())
        else:
            for char in rotor_string:
                position_array.append(char)

        rotor_config = []

        for index in range(0, len(a)):
            rotor_config.append([a[index], position_array[index]])

        if self.position != 1:
            for iteration in range(0, self.position-1):
                item_to_pop = rotor_config[0]
                rotor_config.pop(0)
                rotor_config.append(item_to_pop)

        return rotor_config

    def apply_ring_setting(self, input_char):
        """returns amount of positions to shift
           the original rotor char configuration

        Args:
            input_char (str): char to be shifted

        Returns:
            int: number of letters up the alphabet
                 to shift to.
        """
        index = self.get_char_to_index(input_char)
        shift = index + (self.ring_position - 1)
        if (shift > 25):
            overflow = shift - 26
            shift = overflow

        return shift

    def get_char_to_index(self, char):
        """Converts a letter to its index
        value as part of a list

        Args:
            char (str): actual letter as a char

        Returns:
            int: position of char in list of alphabit
        """
        a = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for index, letter in enumerate(a):
            if (letter is char):
                return index

    def use_rotor(self, input_val, rotor_direction):
        """convers input letter into scrambled output

        Args:
            input_val (int): number representation of the input char

            rotor_direction (str): Expecting "Right" or "Left" to
            indicate the incoming direction

        Returns:
            int: number representation of output char
        """
        if (rotor_direction == "left"):
            item = self.rotor_config[input_val]
            char_to_translate = item[1]

            for index, char_pair in enumerate(self.rotor_config):
                if (char_pair[0] == char_to_translate):
                    return index

        elif (rotor_direction == "right"):
            item = self.rotor_config[input_val]
            char_to_translate = item[0]

            for index, char_pair in enumerate(self.rotor_config):
                if (char_pair[1] == char_to_translate):
                    return index

    def update_position(self):
        """increments the postion of this rotor
        and checks to see if the postion needs
        to roll over.

        Returns:
            Boolean:
                True: We've reached all 26
                letters and need to reset to 1

                False: Did not reset postion back
                to 1
        """
        if (self.position == 26):
            self.position = 1
            self.update_list()
        else:
            self.position = self.position + 1
            self.update_list()

    def update_list(self):
        """ Moves the letter mapping left by one
        """
        item_to_pop = self.rotor_config[0]
        self.rotor_config.pop(0)
        self.rotor_config.append(item_to_pop)
