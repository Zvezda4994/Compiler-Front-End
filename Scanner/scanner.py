import os

#Represents a piece of JSON
class Token:
    def __init__(self, token_type, value):
        self.token_type = token_type #Stores the type of token
        self.value = value #Stores the value of token

    def __str__(self):
        return f"{self.token_type}: {self.value}"

#error handling for invalid tokens
class ScannerError(Exception):
    def __init__(self, position, character):
        self.position = position
        self.character = character
        super().__init__(f"Scanner Error: Invalid character '{character}' at position {position}")

#Main implementation of DFA
class JSONScannerDFA:
    def __init__(self, input_string):
        self.input = input_string
        self.current_index = 0
        self.state = "START"

        #Define DFA transitions (State, Input) -> Next State
        self.transitions = {
            ("START", "{"): "LEFT_BRACE",
            ("START", "}"): "RIGHT_BRACE",
            ("START", ":"): "COLON",
            ("START", ","): "COMMA",
            ("START", "["): "LEFT_BRACKET",
            ("START", "]"): "RIGHT_BRACKET",
            ("START", "\""): "IN_STRING",
            ("IN_STRING", "\""): "STRING_END",
            ("START", "-"): "IN_NUMBER",
            ("START", "digit"): "IN_NUMBER",
            ("START", "t"): "IN_TRUE",
            ("START", "f"): "IN_FALSE",
            ("START", "n"): "IN_NULL",
        }

    #Resets scanner to original state and position
    def reset(self):
        self.state = "START"
        self.current_index = 0

    #Checks if state is final state
    def is_accepting(self, state):
        # Define final accepting states
        return state in ["LEFT_BRACE", "RIGHT_BRACE", "COLON", "COMMA",
                         "LEFT_BRACKET", "RIGHT_BRACKET", "STRING", "NUMBER",
                         "BOOLEAN", "NULL"]

    # Identifying and returning the next token
    def get_next_token(self):
        self.skip_whitespace()

        # Checks if scanner has reached end of input
        if self.current_index >= len(self.input):
            return None

        # Start processing input character by character
        char = self.input[self.current_index]

        # Determine transition based on current state and character
        if char.isdigit():
            self.state = self.transitions.get(("START", "digit"), "INVALID")
            return self.read_number()
        elif char == '-':
            self.state = self.transitions.get(("START", "-"), "INVALID")
            return self.read_number()
        elif char == '"':
            self.state = self.transitions.get(("START", "\""), "INVALID")
            return self.read_string()
        elif char in "{}:,[]":
            self.state = self.transitions.get(("START", char), "INVALID")
            self.current_index += 1
            if self.state == "INVALID":
                raise ScannerError(self.current_index, char)
            return Token(self.state, char)
        elif char == 't':
            self.state = self.transitions.get(("START", "t"), "INVALID")
            return self.read_boolean()
        elif char == 'f':
            self.state = self.transitions.get(("START", "f"), "INVALID")
            return self.read_boolean()
        elif char == 'n':
            self.state = self.transitions.get(("START", "n"), "INVALID")
            return self.read_null()
        else:
            raise ScannerError(self.current_index, char)

    #Method to read a string
    def read_string(self):
        string_value = ""
        self.current_index += 1  # Skip the opening quote

        while self.current_index < len(self.input) and self.input[self.current_index] != '"':
            string_value += self.input[self.current_index]
            self.current_index += 1

        self.current_index += 1  # Skip the closing quote
        return Token("STRING", string_value)

    #Method to read a number
    def read_number(self):
        num_value = ""
        while self.current_index < len(self.input) and (self.input[self.current_index].isdigit() or self.input[self.current_index] in '.-'):
            num_value += self.input[self.current_index]
            self.current_index += 1
        return Token("NUMBER", num_value)

    #Method to read booleans
    def read_boolean(self):
        start = self.current_index
        word = self.input[start:start + 4]
        if word == "true":
            self.current_index += 4
            return Token("BOOLEAN", "true")
        word = self.input[start:start + 5]
        if word == "false":
            self.current_index += 5
            return Token("BOOLEAN", "false")
        raise ScannerError(self.current_index, word)

    #Method to read null
    def read_null(self):
        word = self.input[self.current_index:self.current_index + 4]
        if word == "null":
            self.current_index += 4
            return Token("NULL", "null")
        raise ScannerError(self.current_index, word)

    #Method to skip empty spaces
    def skip_whitespace(self):
        while self.current_index < len(self.input) and self.input[self.current_index].isspace():
            self.current_index += 1

import os

def main():
    # Define the input file
    input_file = "test01.txt"  # File to read input from

    # Generate the output file name based on the input file name
    base_name, ext = os.path.splitext(input_file)
    output_file = f"{base_name}_output{ext}"

    # Read input from the file
    with open(input_file, 'r') as file:
        input_data = file.read().strip()

    scanner = JSONScannerDFA(input_data)

    # Open the output file for writing tokens
    with open(output_file, 'w') as outfile:
        # Process and write tokens
        token = scanner.get_next_token()
        while token is not None:
            # Write the token to the output file
            outfile.write(f"<{token.token_type}, {token.value}>\n")
            # print the token to the console
            print(token)
            token = scanner.get_next_token()

    print(f"Tokens have been written to {output_file}") 

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
