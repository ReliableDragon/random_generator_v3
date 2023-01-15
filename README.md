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
<GENERATOR> ::= <NAME> <NEWLINE> <CHOICE_BLOCK>
<NAME> ::= <TEXT_LINE>

<CHOICE_BLOCK> ::= <CHOICE_EXPRESSION> <NEWLINE> <INTERPOLATION_BLOCKS>

<CHOICE_EXPRESSION> ::= 1*([<TEXT>] <INTERPOLATION_MARKER>) [<TEXT>] | <TEXT> ; i.e. N <INTERPOLATION_MARKER> interspersed throughout text, or plain text. Blank not currently allowed.
<INTERPOLATION_MARKER> ::= "$"

<INTERPOLATION_BLOCKS> ::= N*(<INTERPOLATION_BLOCK>)  ; N equals the number of <INTERPOLATION_MARKER> in the <CHOICE_EXPRESSION>.
<INTERPOLATION_BLOCK> ::= *(<WEIGHTED_CHOICE> <NEWLINE>) <INTERPOLATION_BLOCK_END> <NEWLINE>
<WEIGHTED_CHOICE> ::= <PADDING> <INTEGER> [<SPACE> (<TEXT> | <CHOICE_BLOCK>)]  ; Empty choices are allowed.
<INTERPOLATION_BLOCK_END> ::= <PADDING> "$"

<TEXT_LINE> ::= <TEXT> <NEWLINE>
<TEXT> ::= <REGEX [^\n]>  ; No newlines. Not sure how to write that concisely in BNF.
<NEWLINE> ::= "\n"
<PADDING> ::= *" "  ; Convention is 4 spaces for each level of nesting.
<INTEGER> ::= 1*[1234567890]
<SPACE> ::= " "
```