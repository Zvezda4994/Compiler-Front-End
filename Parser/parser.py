import os

# Token class
class Token:
    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value

    def __str__(self):
        return f"<{self.token_type}, {self.value}>"

# Parse tree node class
class ParseTreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def __str__(self):
        # Print tree readably
        return self.print_tree(0)

    def print_tree(self, level):
        result = "  " * level + str(self.value) + "\n"
        for child in self.children:
            result += child.print_tree(level + 1)
        return result

# Match function to read tokens
def match(expected_type):
    global current_token, tokens, token_index

    if current_token.token_type == expected_type:
        # Store the value of the token before moving on
        value = current_token.value
        # Go to next token, update current token (none if at the end of the list) and return the consumed token
        token_index += 1
        current_token = tokens[token_index] if token_index < len(tokens) else None
        return value  # Return the value of the matched token
    else:
        raise SyntaxError(f"Expected {expected_type}, but got {current_token.token_type}")


# Parsing functions for grammar
def parse_object():
    node = ParseTreeNode("object")
    keys_seen = set()  # Set to track keys already seen 

    match("LEFT_BRACE")
    if current_token.token_type != "RIGHT_BRACE": # If not an empty object, call parse_pair() to process the key value pair
        pair_node = parse_pair()
        key_value = pair_node.children[0].children[0].value
        if key_value in keys_seen:
            raise SemanticError(f"Error type 5: Duplicate key '{key_value}' found.") # Duplicate Key (Type 5) Error
        keys_seen.add(key_value)
        node.add_child(pair_node)

        # Loop to handle multiple key-value pairs separated by commas
        while current_token.token_type == "COMMA":
            match("COMMA")
            pair_node = parse_pair()
            key_value = pair_node.children[0].children[0].value
            if key_value in keys_seen:
                raise SemanticError(f"Error type 5: Duplicate key '{key_value}' found.") # Duplicate Key (Type 5) Error
            keys_seen.add(key_value)
            node.add_child(pair_node)
    match("RIGHT_BRACE")

    return node

# Parsing key-value pairs
def parse_pair():
    node = ParseTreeNode("pair")

    # Semantic check for String
    if current_token.token_type == "STRING":
        key_value = match("STRING")
        if key_value == "" or all(char.isspace() for char in key_value):
            raise SemanticError(f"Error type 2: Empty Key.")  # Empty Key (Type 2) Error
        if key_value.lower() in ["true", "false", "null"]:
            raise SemanticError(f"Error type 4: Reserved keyword '{key_value}' cannot be a dictionary key")  # Reserved Keyword (Type 4) Error
        
        key_node = ParseTreeNode("key")
        key_node.add_child(ParseTreeNode(key_value))
        node.add_child(key_node)

        # Match ':' to parse the value, create value node, add value as child of the node and add as child to pair node
        match("COLON")
        value_node = ParseTreeNode("value")
        value_child_node, _ = parse_value()  
        value_node.add_child(value_child_node)
        node.add_child(value_node)
    else:
        raise SyntaxError("key in pair should be type STRING")

    return node




# Parsing the types of values in grammar
def parse_value():
    if current_token.token_type == "STRING":
        value = match("STRING")
        if value.lower() in ["true", "false", "null"]:
            raise SemanticError(f"Error type 7: Reserved keyword '{value}' cannot be used as a string.")  # Reserved Keyword (Type 7 - Similar to Type 4) Error
        return ParseTreeNode(value), "STRING"
    elif current_token.token_type == "NUMBER":
        value = match("NUMBER")
        if value.startswith(".") or value.endswith(".") or value.count(".") > 1:
            raise SemanticError(f"Error type 1: Invalid decimal number '{value}'.")  # Invalid Decimal (Type 1) Error
        if value.startswith("0") and len(value) > 1 and not value.startswith("0."):
            raise SemanticError(f"Error type 3: Leading zeros in number '{value}'.")  # Inconsistent Formatting (Type 3) Error
        return ParseTreeNode(value), "NUMBER"
    elif current_token.token_type in ["BOOLEAN", "NULL"]:
        return ParseTreeNode(match(current_token.token_type)), current_token.token_type
    elif current_token.token_type == "LEFT_BRACE":
        return parse_object(), "OBJECT"
    elif current_token.token_type == "LEFT_BRACKET":
        return parse_array(), "ARRAY"
    else:
        raise SyntaxError("Invalid value")




# Parsing an array 
def parse_array():
    node = ParseTreeNode("array")
    element_type = None  # Tracking the type of element in the array

    match("LEFT_BRACKET")
    if current_token.token_type != "RIGHT_BRACKET":  # If array isn't empty, call parse_value() to get values
        first_value_node, element_type = parse_value()
        node.add_child(first_value_node)

        while current_token.token_type == "COMMA":  # Handle multiple values separated by commas
            match("COMMA")
            value_node, value_type = parse_value()
            if value_type != element_type:
                raise SemanticError("Error type 6: List elements must be of the same type.")  # Type Inconsistency (Type 6) Error (Type shi)
            node.add_child(value_node)
    match("RIGHT_BRACKET")

    return node



#Check the type of the first token to call the appropriate method
def parse(tokens_input):
    global current_token, token_index, tokens
    tokens = tokens_input 

    token_index = 0
    current_token = tokens[token_index] if tokens else None

    if current_token.token_type == "LEFT_BRACE":
        return parse_object()
    elif current_token.token_type == "LEFT_BRACKET":
        return parse_array()
    else:
        raise SyntaxError("Input must start with an object or array")

# Converting the token text to an actual token stream
def parse_tokens(token_stream):
    tokens = []
    for line in token_stream.splitlines():
        parts = line.strip("<>").split(", ")
        token_type = parts[0]
        value = parts[1] if len(parts) > 1 else None
        tokens.append(Token(token_type, value))
    return tokens

class SemanticError(Exception):
    def __init__(self, message):
        super().__init__(message)

# Main function to process all the files
def main():
    input_folder = "tokenstreams/"
    output_folder = "parsetrees/"

    # Largely unnecessary, but ran into some issues with the terminal sometimes so this might help
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Simple loop to go file by file and convert input token text to token streams
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".txt"):
            with open(input_folder + file_name, 'r') as f:
                tokens = parse_tokens(f.read())  # Read and convert token text to token stream (list of objects)

            #Create parse trees and write output files in hte output folder
            try:
                parse_tree = parse(tokens)
                output_file = output_folder + file_name.replace(".txt", "_tree.txt")
                with open(output_file, 'w') as f:
                    f.write(str(parse_tree))
                print(f"Parsed {file_name} successfully!")
            except (SyntaxError, SemanticError) as e: # Error handling
                error_file = output_folder + file_name.replace(".txt", "_error.txt")
                with open(error_file, 'w') as f:
                    f.write(str(e))
                print(f"Error in {file_name}: {e}")


if __name__ == "__main__":
    main()
    


