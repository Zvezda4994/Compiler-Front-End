Readme: Semantic Analysis of a JSON Parser

Input:
Place your input files in the 'tokenstreams' folder (12 test txts are provided originally for examples).
The format should be one token per line in the form of <TYPE, VALUE> 

Output:
When you run parser.py, it will create parse trees and store them in the 'parsetrees' folder for output.
If there is an error, the error file will be generated and stored in the 'parsetrees' folder for the same.

Example Input/Output
Input:  
<LEFT_BRACE, {>
<STRING, name>
<COLON, :>
<STRING, schlawg>
<COMMA, ,>
<STRING, age>
<COLON, :>
<NUMBER, 30>
<COMMA, ,>
<STRING, is_student>
<COLON, :>
<BOOLEAN, false>
<RIGHT_BRACE, }>

Output:
object
  pair
    key
      name
    value
      schlawg
  pair
    key
      age
    value
      30
  pair
    key
      is_student
    value
      false


Input:
<LEFT_BRACE, {>
<STRING, >
<COLON, :>
<STRING, John>
<RIGHT_BRACE, }>

Output:
Error type 2: Empty Key.