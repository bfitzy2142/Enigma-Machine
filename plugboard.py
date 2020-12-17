#!/usr/bin/env python3


class Plugboard():

    """
    This class is used to maintain attributes of the plugboard
    of the Enigma Cypher machine.

    Wikipedia Definition:
    A plugboard is similar to an old-fashioned telephone
    switch board that has ten wires, each wire having two
    ends that can be plugged into a slot. Each plug wire
    can connect two letters to be a pair (by plugging one
    end of the wire to one letter’s slot and the other end
    to another letter). The two letters in a pair will swap
    over, so if “A” is connected to “Z,” “A” becomes “Z” and
    “Z” becomes “A.” This provides an extra level of
    scrambling for the military.

    Read more about it here:
    https://en.wikipedia.org/wiki/Enigma_machine#Plugboard
    """

    def __init__(self, plugs_attached):
        """Initiator for plugboard object

        Args:
            plugs_attached (list): [description]
        """
        self.links = plugs_attached

    def get_char_to_index(self, char):
        """Converts a letter to its
        index value as part of a list

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

    def swap(self, index):
        """Goes through the plugboard list
        and returns the char index for the
        the swap candidate

        Args:
            index (int): index of original
            char

        Returns:
            int: index of the swapped char
        """
        letter = self.get_char_from_index(index)
        swap = self.find_swap(letter)
        swap_index = self.get_char_to_index(swap)
        return swap_index

    def find_swap(self, char):
        """returns the linked char (if available)
        to emulate the plug board setting

        Args:
            char (char): input char

        Returns:
            [type]: adjacent swap char
        """
        for link in self.links:
            if (char in link):
                for letter in link:
                    if (letter is not char):
                        return letter
        return char

    def get_plugs(self):
        """returns plugboard list

        Returns:
            list: plugboard connections
        """
        return self.links
