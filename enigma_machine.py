#!/usr/bin/env python3

from rotor import Rotor
from plugboard import Plugboard


class EnigmaMachine():

    """
    A programmatic implementation of the infamous Enigma encryption algorithm.

    To be honest, I made this because I was
    bored and this felt like a challenge.

    Wikipedia Description:
    The Enigma machine is an encryption device developed and used in
    the early to mid-20th century to protect commercial, diplomatic
    and military communication. It was employed extensively by Nazi
    Germany during World War II, in all branches of the German military.

    Read more about it here:
    https://en.wikipedia.org/wiki/Enigma_machine


    Brad Fitzgerald
    December 2020
    """
    def __init__(
                self,
                rotor_selection,
                rotor_settings,
                plugs,
                ring_positions,
                reflector
            ):

        """
            Rotor_selection: Which rotors are in use and which order.
            List would look like this: [4, 2, 5]

            rotor_settings: list of starting positions for left, middle,
            and right rotor. i.e index 0 is for left rotor, 1 for middle,
            and 2 for right rotor.

            List would look like this: [1, 6, 16]

            plugs: List of enabled plugboard settings.

            List would look like this: [
                "QH",
                "EN",
                "RM",
                "TL",
                "YS",
                "UI",
                "OK",
                "PC",
                "DV",
                "FG"
            ]

        """

        # Wiring for rotors I to V
        self.rotor_settings_strings = [
            "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
            "AJDKSIRUXBLHWTMCQGZNPYFVOE",
            "BDFHJLCPRTXVZNYEIWGAKMUSQO",
            "ESOVPZJAYQUIRHXLNFTGKDCMWB",
            "VZBRGITYUPSDNHLXAWMJQOFECK"
        ]

        self.rotor_settings = rotor_settings
        self.rotor_selection = rotor_selection
        self.ring_positions = ring_positions

        self.rotor_list = self.setup_rotors(self.rotor_selection,
                                            self.rotor_settings
                                            )
        self.plugboard = Plugboard(plugs)

        self.reflector = reflector

    def setup_rotors(self, rotor_selection, rotor_settings):
        """[summary]

        Args:
            rotor_selection ([type]): [description]
            rotor_settings ([type]): [description]

        Returns:
            [type]: [description]
        """

        # Setup rotor strings
        rotor_str = []

        for index, obj in enumerate(self.rotor_selection):
            selection_index = rotor_selection[index] - 1
            rotor_wiring = self.rotor_settings_strings[selection_index]
            rotor_str.append(rotor_wiring)

        # Setup ring settings
        ring_pos = []
        for index, obj in enumerate(self.ring_positions):
            ring_pos.append(self.ring_positions[index])

        rotor_list = []

        # Configure rotors and rotor attributes
        for index, obj in enumerate(rotor_selection):
            rotor_list.append(Rotor(rotor_str[index],
                                    rotor_settings[index],
                                    rotor_selection[index],
                                    ring_pos[index]
                                    ))
        return rotor_list

    def encode_message(self, message):
        """Takes a string and encodes each char of the string
        printing the final result

        Args:
            message (string): message to transform
        """
        character_list = self.convert_message_to_numbers(message)

        encoded_message = []
        for index, value in enumerate(character_list):
            encoded_char = self.encode_letter(value)
            encoded_message.append(encoded_char)
        print('')
        print(f"Ciphertext:")
        print(self.convert_numbers_to_letters(encoded_message))

    def encode_letter(self, char_index):
        """Translates inputted chars into scrambled char
        based on current rotor/plugbard setting

        Args:
            char_index (int): index of char within
            alphabit list (i.e 0 = A, 1 = B, etc)

        Returns:
            int: index of transformed char
        """

        # Move rotor position by one and check if others need to be moved
        self.move_rotors()

        # Pass char through plugboard and get index
        plugboard_out = self.plugboard.swap(char_index)

        rotor_input_left = plugboard_out

        # Move letter through rotors from left to right
        for rotor in reversed(self.rotor_list):
            rotor_input_left = rotor.use_rotor(rotor_input_left, "left")

        # Run letter through reflector
        reflector_output = self.calculate_reflection(
                                                    rotor_input_left,
                                                    self.reflector
                                                    )

        rotor_input_right = reflector_output

        # Move letter through rotors from right to left
        for rotor in self.rotor_list:
            rotor_input_right = rotor.use_rotor(rotor_input_right, "right")

        # Apply plug board logic
        plugboard_out = self.plugboard.swap(rotor_input_right)

        return plugboard_out

    def move_rotors(self):
        """Logic to move rotors. If the turnover position is hit on
        one rotor, the next rotor to the left turns over
        """
        # Always move the right most rotor one postion
        self.rotor_list[2].update_position()

        # Check if middle rotor should rotate
        if (self.rotor_list[2].position == self.rotor_list[2].turnover):
            self.rotor_list[1].update_position()

        # Check if middle rotor is on turnover and preform a double step
        elif (self.rotor_list[1].position == self.rotor_list[1].turnover-1):
            self.rotor_list[1].update_position()
            self.rotor_list[0].update_position()

    def calculate_reflection(self, input_val, reflector):
        """Run input character through reflector

        Args:
            input_val (int): index of character in alphabit
            reflector (str): reflector character string

        Returns:
            [int]: index of reflected character
        """
        char_to_reflect = reflector[input_val]
        return self.get_char_to_index(char_to_reflect)

    def convert_numbers_to_letters(self, number_list):
        """converts index of character to character itself
        and store resulting message in list

        Args:
            number_list (list): list of index values for characters

        Returns:
            string: message resulting from enigma encryption
        """
        message = ''
        for x in number_list:
            message = message + self.get_char_from_index(x)
        return message

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

    def get_char_from_index(self, index):
        """Returns the char matching the index of the
        alphabit list

        Args:
            index (int): [description]

        Returns:
            [type]: [description]
        """
        a = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        return a[index]

    def convert_message_to_numbers(self, message):
        """converts character to index position within
        alphabit and store resulting integers in a list

        Args:
            message (string): message to be encrypted

        Returns:
            list: list of index values for each char of the
            message
        """
        a = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

        message_as_char_index = []
        for char in message.upper():
            if char not in a:
                continue
            for index, letter in enumerate(a):
                if (char is letter):
                    message_as_char_index.append(index)

        return message_as_char_index

    def print_settings(self):
        """Prints a welcome message to the user and shows
           the current configuration
        """
        print(" _____________________________________________________")
        print("|                                                     |")
        print("|                    Enigma model M3                  |")
        print("|_____________________________________________________|")
        print('')
        print("                     Configuration:")
        print('')
        print(f"Reflector Config: {self.reflector}")
        print('')
        print("Rotor Order:")
        for selection in self.rotor_selection:
            print(selection, sep=',', end=' ', flush=True)
        print('')
        print("Starting Position:")
        for pos in self.rotor_settings:
            print(pos, sep=',', end=' ', flush=True)
        print('')
        print("Ring Setting:")
        for ring in self.ring_positions:
            print(ring, sep=',', end=' ', flush=True)
        print('')
        print(f"Plugboard connections:")
        for plug in self.plugboard.get_plugs():
            print(plug, sep=',', end=' ', flush=True)
        print('')
        print("******************************************************")


def main():
    """This provides basic functionality of this program.
    I designed the EnigmaMachine class so that it could be
    called upon by another module in the future if need be.
    """

    # Rotor Selection and Order
    rotor_selection = [2, 4, 5]

    # Rotor initial position
    rotor_settings = [25, 1, 6]

    # Ring setting (Ringstellung)
    ring_positions = [3, 19, 6]

    # Reflector string (Umkehrwalze) B
    reflector = 'YRUHQSLDPXNGOKMIEBFZCWVJAT'

    # plugboard connections (Steckerbrett)
    plugs = [
            "AV",
            "BS",
            "CG",
            "DL",
            "FU",
            "HZ",
            "IN",
            "KM",
            "OW",
            "RX"
        ]

    e = EnigmaMachine(
            rotor_selection,
            rotor_settings,
            plugs,
            ring_positions,
            reflector
        )

    e.print_settings()
    message = input("Enter a message:")
    e.encode_message(message)


if (__name__ == '__main__'):
    main()
