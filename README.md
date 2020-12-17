# The Enigma
The Enigma Machine is an encryption tool used by the Germans during the second world war to secure their communications. 

On a physical Enigma machine, each keypress would show up on what is called the lamp board providing the cyphertext.The Enigma algorithm is symmetrical meaning that the original text can be obtained by entering cyphertext back into the machine with the same settings used to encrypt. 


To break down the Enigma's operation simply, when the operator presses a key, an electric connection is made from the key, through three rotors bidirectionally. The complex electrical connection ends at the lampboard which displays the unique encrypted character. The magic happens with what are called the rotors. The rotors apply a letter substitution encryption scheme. Each rotor has a different configuration. Every time a key is pressed, one or more rotors rotate which completely changes the electrical path the same letter would take on the next key press. This project emulates the complex electrical connections driving the Enigma encryption algorithm.

## Enigma Components
Like a real Enigma operator in the field, you have the same settings at your disposal provide security to your messages.

*The important parameters to understand are the following:*

### Rotors
1. The rotors are where the letter scrambling happens by substituting one letter by another. The scrambling produced by the rotors change each time a letter passes through with rotor rotation.
2. The German Army Enigma M3 model uses three rotors. The operator has total of 5 rotors to choose from. The order of selected rotors also matters.

### Rotor starting position
The starting position specifies where each rotor will begin scrambling messages.

For example each rotor may be setup as such:
```
rotor_selection = [4, 24, 9]
```
- Rotor in position 1 (leftmost) will be at position D (4th letter)
- Rotor in position 2 (middle) will be at position X (24th letter)
- Rotor in position 3 (rightmost) will be at position I (9th letter)

### Rotor Ring setting
The ring setting adds an extra level of complexity to the rotor. Each rotor has a preset "default" wiring. For example the type I rotor would encrypt the alphabet like such:

```
'ABCDEFGHIJKLMNOPQRSTUVWXYZ' -> 'EKMFLGDQVZNTOWYHXUSPAIBRCJ'
```

A becomes E, B becomes K, and so on.

The ring setting is typically shown as either a letter or its numerical position. I.e a ring setting of B is the same thing as a ring setting of 2. 

**The ring setting does two things:**
1. Shift the encoded output letters up by X places
2. Shift the alignment of the new output by X places to the right

**Note: x is the ring setting minus the default setting (1).**

Looking at our example above with rotor one:

- Step 1: Shift the encoded output letter up by 1 places
```
EKMFLGDQVZNTOWYHXUSPAIBRCJ
		becomes
FLNGMHERWAOUPXZIYVTQBJCSDK
```

- step 2: Shift the alignment of the new output 1 place to the right
```
FLNGMHERWAOUPXZIYVTQBJCSDK
		becomes
KFLNGMHERWAOUPXZIYVTQBJCSD
```
So now A is encrypted into K, B is encrypted into F, etc..

The ring settings are specified as such:
```
ring_positions = [2,6,8]
```
- Rotor in position 1 (leftmost) will be at ring setting 2
- Rotor in position 2 (middle) will be at ring setting 6
- Rotor in position 3 (rightmost) will be at ring setting 8

### Plugboard Connecitons
A plugboard is similar to an old-fashioned telephone switch board that has ten wires, each wire having two ends that can be plugged into a slot. Each plug wire can connect two letters to be a pair (by plugging one end of the wire to one letter’s slot and the other end to another letter). The two letters in a pair will swap over, so if “A” is connected to “Z,” “A” becomes “Z” and “Z” becomes “A.” This provides an extra level of scrambling.

Plugboard parameters can be specified like so
```
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

```

### Reflector
The reflector redirects the output from the rotors back into the rotors in the other direction. By default, the most common reflector UKWB is used, but others are available if you want to modify the string for it in my code.

```
reflector = 'YRUHQSLDPXNGOKMIEBFZCWVJAT'
```


## Usage
For now the only way to change the settings used is by modifying the parameters inside the enigma_machine.py file. I wrote the EnigmaMachine class so that if you wanted to, you could import it as a module and feed it all the required arguments. 

To run my Enigma emulator simply run:
```
python3 enigma_machine.py
```
