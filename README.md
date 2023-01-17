# Casual Syntax Explanation
The random generator only supports top-level generators at the moment.

## Top-Level Generators
A top-level generator is a file with a name on the first line, a blank line, and a choice body.

## Choice Body
A choice body consists of a choice header and a number of INTERPOLATION_BLOCK equal to the number of '$'
in the choice header.

## Choice Header
A choice header is a line of text containing 0 or more '$'.

## Subchoice
A subchoice is number of choice lines, each (ignoring leading whitespace) containing an integer 
representing the weight to give that choice, followed by a space, followed by the text of that
choice.

# Formal Syntax
```
; Whitespace is ignored when leading a line. Convention is to indent by 4 spaces for each level.
<COMMENT> ::= ";" ; Not gonna include this everywhere. Anything on a line after a comment is ignored.
<GENERATOR> ::= <HEADER> <CHOICE_BLOCK>
<RESOURCE> ::= <HEADER> <INTERPOLATION_BLOCK>
<HEADER> ::= <NAME> <NEWLINE> <IMPORTS> <NEWLINE>  ; i.e. there's a blank line between each section
<IMPORTS> ::= *(<IMPORT> <NEWLINE>)
<IMPORT> ::= ("resource" | "generator") <SPACE> <IMPORT_HANDLE> ":" <FILENAME>
<IMPORT_HANDLE> ::= "1*[a-zA-Z_]"
<FILENAME> ::= "1*[a-zA-Z_-.]"
<NAME> ::= <RAW_TEXT_LINE>

<CHOICE_BLOCK> ::= <CHOICE_EXPRESSION> <INTERPOLATION_BLOCKS>

<CHOICE_EXPRESSION> ::= (<CHOICE_MARKER_FRAGMENTS> | <TEXT>) <NEWLINE>  ; i.e. N <INTERPOLATION_MARKER> interspersed throughout text, or plain text. Blank not currently allowed.
; TODO: Consider finding a better name than "marker" for these. Something more like "clause".
<CHOICE_MARKER_FRAGMENTS> ::= 1*([<TEXT>] <CHOICE_MARKER>) [<TEXT>]
<CHOICE_MARKER> ::= <INTERPOLATION_MARKER> | <IMPORT_INTERPOLATION_MARKER>
<INTERPOLATION_MARKER> ::= "$"
<IMPORT_INTERPOLATION_MARKER> ::= "@" (<SPACE_DELIMITED_IMPORT_HANDLE> | <BRACKET_DELIMITED_IMPORT_HANDLE>)
<SPACE_DELIMITED_IMPORT_HANDLE> ::= <IMPORT_HANDLE> " "
<BRACKET_DELIMITED_IMPORT_HANDLE> ::= "{" <IMPORT_HANDLE> "}"

<INTERPOLATION_BLOCKS> ::= N*(<INTERPOLATION_BLOCK>)  ; N equals the number of <INTERPOLATION_MARKER> in the <CHOICE_EXPRESSION>.
<INTERPOLATION_BLOCK> ::= *(<WEIGHTED_CHOICE>) <INTERPOLATION_BLOCK_END>
<WEIGHTED_CHOICE> ::= <WEIGHT> [<SPACE> <WEIGHTED_CHOICE_VALUE>] <NEWLINE>; Empty choices are allowed.
<WEIGHT> ::= <INTEGER> | "[" <INT_COMMAND_EXPRESSION> "]"  ; Consider allowing full expression later
<WEIGHTED_CHOICE_VALUE> ::= (<TEXT> | <CHOICE_BLOCK>)
<INTERPOLATION_BLOCK_END> ::= "$" <NEWLINE>

<RAW_TEXT_LINE> ::= <RAW_TEXT> <NEWLINE>
<TEXT> ::=  1*([<RAW_TEXT>] <COMMAND_INTERPOLATION>) [<RAW_TEXT>] | <RAW_TEXT>
<RAW_TEXT> ::= "[^\n$@#]"
<NEWLINE> ::= "\n"
<INTEGER> ::= 1*[1234567890]
<SPACE> ::= " "

; TODO: Support new command syntax to allow expressions and constants. This will require renaming
; the command_expression class to command_interpolation, adding support for expressions and
; constants, and getting it implemented in weighted choice weights as well as command 
; interpolations.
<COMMAND_INTERPOLATION> ::= "#" "(" 1*(<COMMAND_EXPRESSION>) ")" ; Possibly add <COMMAND_MARKER> <SIMPLE_COMMAND>  form later.
<COMMAND_EXPRESSION> ::= <INT_COMMAND_EXPRESSION> | <STR_COMMAND_EXPRESSION>
<INT_COMMAND_EXPRESSION> ::= 1*<INT_COMMAND> *(<INT_OP> <INT_COMMAND>)
<STR_COMMAND_EXPRESSION> ::= 1*<STR_COMMAND> *(<STR_OP> <STR_COMMAND>)
<INT_VAL> ::= <INT_COMMAND> | <CONST_INT>
<STR_VAL> ::= <STR_COMMAND> | <CONST_STR>
<COMMAND> ::= <INT_COMMAND> | <STR_COMMAND>
<INT_COMMAND> ::= <INT_COMMAND_NAME> <ARGUMENTS>
<STR_COMMAND> ::= <STR_COMMAND_NAME> <ARGUMENTS>
<ARGUMENTS> ::= "(" *(<ARGUMENT> ",") [<ARGUMENT>] ")"
<ARGUMENT> ::= [a-zA-Z0-9] | <COMMAND_EXPRESSION>
<INT_COMMAND_NAME> ::= "iconstant" | "random"  ; See commands.py for all, not listing them here.
<STR_COMMAND_NAME> ::= "constant" | "cow"
<INT_OP> ::= "+" | "-" | "/" | "*" | "^"
<STR_OP> ::= "+"
<CONST_INT> ::= <INTEGER>
<CONST_STR> ::= <RAW_TEXT>
; [iconstant(10)]
```