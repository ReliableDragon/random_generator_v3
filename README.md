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
<CHOICE_MARKER_FRAGMENTS> ::= 1*([<TEXT>] <CHOICE_MARKER>) [<TEXT>]
<CHOICE_MARKER> ::= <INTERPOLATION_MARKER> | <IMPORT_INTERPOLATION_MARKER>
<INTERPOLATION_MARKER> ::= "$"
<IMPORT_INTERPOLATION_MARKER> ::= "@" (<SPACE_DELIMITED_IMPORT_HANDLE> | <BRACKET_DELIMITED_IMPORT_HANDLE>)
<SPACE_DELIMITED_IMPORT_HANDLE> ::= <IMPORT_HANDLE> " "
<BRACKET_DELIMITED_IMPORT_HANDLE> ::= "{" <IMPORT_HANDLE> "}"

<INTERPOLATION_BLOCKS> ::= N*(<INTERPOLATION_BLOCK>)  ; N equals the number of <INTERPOLATION_MARKER> in the <CHOICE_EXPRESSION>.
<INTERPOLATION_BLOCK> ::= *(<WEIGHTED_CHOICE> <NEWLINE>) <INTERPOLATION_BLOCK_END> <NEWLINE>
<WEIGHTED_CHOICE> ::= <PADDING> <INTEGER> [<SPACE> <CHOICE_VALUE>]  ; Empty choices are allowed.
<CHOICE_VALUE> ::= (<TEXT> | <CHOICE_BLOCK>)
<INTERPOLATION_BLOCK_END> ::= <PADDING> "$"

<RAW_TEXT_LINE> ::= <RAW_TEXT> <NEWLINE>
<TEXT> ::=  1*([<RAW_TEXT>] <COMMAND_EXPRESSION>) [<RAW_TEXT>] | <RAW_TEXT>
<RAW_TEXT> ::= "[^\n]"
<NEWLINE> ::= "\n"
<PADDING> ::= *" "  ; Convention is 4 spaces for each level of nesting.
<INTEGER> ::= 1*[1234567890]
<SPACE> ::= " "

<COMMAND_EXPRESSION> ::= "#" "(" 1*<COMMAND> ")"  ; Possibly add <COMMAND_MARKER> <SIMPLE_COMMAND>  form later.
<COMMAND> ::= <FUNCTION>
<FUNCTION> ::= <COMMAND_NAME> "(" *(<ARGUMENT> ",") [<ARGUMENT>] ")"
<ARGUMENT> ::= [a-zA-Z0-9] | <COMMAND>
<COMMAND_NAME> ::= "gauss" | "normal" | "random"
; Test $ demo
;   10 #(gauss(4, 5))one
;   10 #gauss(4, 5) two
;   10 @[#gauss(4, 5)]three
```