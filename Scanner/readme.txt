JSON Scanner - DFA Implementation

Overview:
This project implements a simple scanner (lexical analyser) using DFAs. The scanner reads input from a file and processes it character by character and outputs the tokens that represent JSON data elements, such as strings, numbers, booleans, operators/symbols and null.

How to run:
1. This project reads input from a file, which is set to test01.txt by default. Save your JSON input in the file and 
   ensure it's in the same directory as the python file.
2. Make sure the input file is in plain text containing valid JSON content.   
3. Either open the project in an IDE and run json_scanner_dfa.py, or run it directly in terminal.   

Assumptions:
1. It is assumed that the input passed will be valid JSON only. If unexpected or invalid input is found the program will throw a ScannerError.
2. Supported JSON Types:
    Strings ("name", "age")
    Numbers (30, -69.420)
    Booleans (True, False)
    null
    Symbols/Operators ([, ], :, ',', [, ])

How the code works:
    Token Class:
        Represents a token extracted from JSON input, where token_type represents the type of token, and value represents the value of the token
    
    ScannerError Class:
        Error handling for invalid characters. It throws an error message whenever a character is read that doesn't belong to a valid token

    DFA Transition Table:
        the self.transitions table defines how the scanner transitions between states based on current state and input character.
        It is of the form (current_state, input) : next_state.
    
    Transition Decision Logic:
        A block of if-elif statements that check input character type, set the appropriate state and call the relevant method to read the token type, otherwise raise a ScannerError

    Methods to handle token types:
        read_string(): Processes a complete string enclosed in double quotes.
        read_number(): Handles numbers, including integers, decimals, and negatives.
        read_boolean(): Verifies and reads true and false.
        read_null(): Verifies and reads the null keyword.

    Main Function:
        Initialises the scanner and reads input file into a string and prints tokens.

    The code uses DFA state transitions to break JSON input into tokens. Each element (String, number, boolean, structural operator, null, etc.) is assigned a state,
    and the scanner navigates between states to correctly identify and extract each token.


