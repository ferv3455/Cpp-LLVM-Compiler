GRAMMAR = {
    'non-terminals': [
        # Program
        'PROGRAM',
        'MACROS',
        'STATEMENTS',

        # 'SENT-E',
        # 'SENT-T',
        # 'SENT-P',
        # 'SENT-Q',
        # 'SENT-A',
        # 'SENT-I',

        # Statements
        'ST',
        'LABEL-ST',
        'SEL-ST',
        'ITER-ST',
        'JMP-ST',
        'CMPD-ST',
        'DECL-ST',
        'FUNC-ST',
        # 'TRY-ST',
        'EXPR-ST',

        'FOR-COND',
        'INIT-LIST',

        # Declaration statements
        'DECL',
        'DECL-SPECS',
        'DECL-SPEC',
        'TYPE-SPECS',
        'TYPE-SPEC',
        'DECLARATORS',
        'ID-DECL',

        # FIXME: Function definition statements
        'FUNC-DECL',
        'PARAM-LIST',
        'PARAMS',

        # Expression statements
        'EXPR',
        'EXPR-L17',
        'EXPR-L16',
        'EXPR-L15',
        'EXPR-L14',
        'EXPR-L13',
        'EXPR-L12',
        'EXPR-L11',
        'EXPR-L10',
        'EXPR-L7',
        'EXPR-L6',
        'EXPR-L5',
        'EXPR-L3',
        'EXPR-L2',
        'EXPR-L1',

        'ARG-LIST',
        'ID',
        'OPERAND',
    ],
    'terminals': [
        'macro',

        'using',
        'typename',

        'inline',
        'explicit',
        'virtual',
        'friend',
        'constexpr',
        'static',
        'extern',
        'mutable',

        'namespace',
        'class',
        'struct',
        'union',
        'enum',
        'auto',
        'decltype',
        'id',
        'void',
        'bool',
        'int',
        'float',
        'double',
        'long',
        'short',
        'unsigned',
        'signed',
        'char',
        'wchar_t',
        'char16_t',
        'char32_t',

        'if',
        'else',
        'switch',
        'case',
        'default',

        'while',
        'do',
        'for',
        'break',
        'continue',
        'return',
        'goto',
        'typedef',

        'new',
        'delete',

        'comma',
        'colon',
        'double-colon',

        'hex-lit',
        'oct-lit',
        'int-lit',
        'float-lit',
        'char-lit',
        'str-lit',
        'id',

        'true',
        'false',

        'parenthesis::(',
        'parenthesis::)',
        'bracket::[',
        'bracket::]',
        'brace::{',
        'brace::}',
        'semicolon',

        'arithmetic-op::+',
        'arithmetic-op::-',
        'arithmetic-op::*',
        'arithmetic-op::/',
        'arithmetic-op::%',
        'relational-op',
        'logical-op::&&',
        'logical-op::||',
        'logical-op::!',
        'assignment-op',
        'arithm-assign-op',
        'bit-assign-op',
        'increment-op',
        'member-op',
        'ptr-member-op',
        'bit-op::<<',
        'bit-op::>>',
        'bit-op::>>',
        'bit-op::&',
        'bit-op::^',
        'bit-op::|',
        'bit-op::~',
    ],
    'start': 'PROGRAM',
    'derivations': [
        # The entire program
        ('PROGRAM', 'MACROS STATEMENTS'),
        ('PROGRAM', 'STATEMENTS'),

        # Macros
        # FIXME: marcos can only be at the top now
        ('MACROS', 'macro MACROS'),
        ('MACROS', 'macro'),

        # Statements
        ('STATEMENTS', 'ST STATEMENTS'),
        ('STATEMENTS', 'ST'),
        ('ST', 'LABEL-ST'),
        ('ST', 'SEL-ST'),
        ('ST', 'ITER-ST'),
        ('ST', 'JMP-ST'),
        ('ST', 'CMPD-ST'),
        ('ST', 'DECL-ST'),
        ('ST', 'FUNC-ST'),
        # ('ST', 'TRY-ST'),
        ('ST', 'EXPR-ST'),

        # Labeled statements
        ('LABEL-ST', 'id colon'),
        ('LABEL-ST', 'case EXPR colon'),
        ('LABEL-ST', 'default colon'),

        # Selection statements
        ('SEL-ST', 'if parenthesis::( EXPR parenthesis::) ST'),
        ('SEL-ST', 'if parenthesis::( EXPR parenthesis::) ST else ST'),
        ('SEL-ST', 'switch parenthesis::( EXPR parenthesis::) ST'),

        # Iteration statements
        ('ITER-ST', 'while parenthesis::( EXPR parenthesis::) ST'),
        ('ITER-ST', 'do ST while parenthesis::( EXPR parenthesis::)'),
        ('ITER-ST', 'for parenthesis::( FOR-COND parenthesis::) ST'),
        ('FOR-COND', 'DECL semicolon EXPR semicolon EXPR'),  # FIXME
        ('FOR-COND', 'DECL semicolon EXPR semicolon EXPR'),  # FIXME

        # Jump statements
        ('JMP-ST', 'break semicolon'),
        ('JMP-ST', 'continue semicolon'),
        ('JMP-ST', 'return semicolon'),
        ('JMP-ST', 'return EXPR semicolon'),
        ('JMP-ST', 'return INIT-LIST semicolon'),
        ('JMP-ST', 'goto ID semicolon'),

        ('INIT-LIST', 'brace::{ brace::}'),
        ('INIT-LIST', 'brace::{ EXPR brace::}'),

        # Compound statements
        ('CMPD-ST', 'brace::{ brace::}'),
        ('CMPD-ST', 'brace::{ STATEMENTS brace::}'),

        # Declaration statements
        ('DECL-ST', 'DECL semicolon'),
        ('DECL', 'using namespace ID'),
        ('DECL', 'using ID'),
        ('DECL', 'DECL-SPECS TYPE-SPECS DECLARATORS'),
        ('DECL', 'TYPE-SPECS DECLARATORS'),

        #   Specifiers
        ('DECL-SPECS', 'DECL-SPEC DECL-SPECS'),
        ('DECL-SPECS', 'DECL-SPEC'),
        ('DECL-SPEC', 'typedef'),
        ('DECL-SPEC', 'inline'),
        ('DECL-SPEC', 'explicit'),
        ('DECL-SPEC', 'virtual'),
        ('DECL-SPEC', 'friend'),
        ('DECL-SPEC', 'constexpr'),
        ('DECL-SPEC', 'static'),
        ('DECL-SPEC', 'extern'),
        ('DECL-SPEC', 'mutable'),
        ('TYPE-SPECS', 'TYPE-SPEC TYPE-SPECS'),
        ('TYPE-SPECS', 'TYPE-SPEC'),
        ('TYPE-SPEC', 'namespace'),
        ('TYPE-SPEC', 'class'),
        ('TYPE-SPEC', 'struct'),
        ('TYPE-SPEC', 'union'),
        ('TYPE-SPEC', 'enum'),
        ('TYPE-SPEC', 'auto'),
        ('TYPE-SPEC', 'decltype'),
        ('TYPE-SPEC', 'ID'),
        ('TYPE-SPEC', 'void'),
        ('TYPE-SPEC', 'bool'),
        ('TYPE-SPEC', 'int'),
        ('TYPE-SPEC', 'float'),
        ('TYPE-SPEC', 'double'),
        ('TYPE-SPEC', 'long'),
        ('TYPE-SPEC', 'short'),
        ('TYPE-SPEC', 'unsigned'),
        ('TYPE-SPEC', 'signed'),
        ('TYPE-SPEC', 'char'),
        ('TYPE-SPEC', 'wchar_t'),
        ('TYPE-SPEC', 'char16_t'),
        ('TYPE-SPEC', 'char32_t'),

        #   Declarators
        ('DECLARATORS', 'ID-DECL DECLARATORS'),
        ('DECLARATORS', 'ID-DECL'),
        ('ID-DECL', 'id'),
        ('ID-DECL', 'id PARAM-LIST'),
        ('ID-DECL', 'id ARG-LIST'),
        ('ID-DECL', 'id assignment-op EXPR'),
        ('ID-DECL', 'id bracket::[  EXPR bracket::]'),
        ('ID-DECL', 'id bracket::[  EXPR bracket::] assignment-op INIT-LIST'),
        ('ID-DECL', 'id assignment-op EXPR'),

        # Function definition statements
        ('FUNC-ST', 'TYPE-SPECS id PARAM-LIST CMPD-ST'),
        ('FUNC-ST', 'DECL-SPECS TYPE-SPECS id PARAM-LIST CMPD-ST'),
        ('PARAM-LIST', 'parenthesis::( parenthesis::)'),
        ('PARAM-LIST', 'parenthesis::( PARAMS parenthesis::)'),
        ('PARAMS', 'DECL comma PARAMS'),
        ('PARAMS', 'DECL'),

        # TODO: Try statements

        # Expression statements
        ('EXPR-ST', 'EXPR semicolon'),
        ('EXPR', 'EXPR-L17'),

        # Level 17: comma, left to right
        ('EXPR-L17', 'EXPR-L17 comma EXPR-L16'),
        ('EXPR-L17', 'EXPR-L16'),

        # Level 16: assignment, right to left
        ('EXPR-L16', 'EXPR-L15 assignment-op EXPR-L16'),
        ('EXPR-L16', 'EXPR-L15 arithm-assign-op EXPR-L16'),
        ('EXPR-L16', 'EXPR-L15 bit-assign-op EXPR-L16'),
        ('EXPR-L16', 'EXPR-L15'),

        # Level 15: ||, left to right
        ('EXPR-L15', 'EXPR-L15 logical-op::|| EXPR-L14'),
        ('EXPR-L15', 'EXPR-L14'),

        # Level 14: &&, left to right
        ('EXPR-L14', 'EXPR-L14 logical-op::&& EXPR-L13'),
        ('EXPR-L14', 'EXPR-L13'),

        # Level 13: |, left to right
        ('EXPR-L13', 'EXPR-L13 bit-op::| EXPR-L12'),
        ('EXPR-L13', 'EXPR-L12'),

        # Level 12: ^, left to right
        ('EXPR-L12', 'EXPR-L12 bit-op::^ EXPR-L11'),
        ('EXPR-L12', 'EXPR-L11'),

        # Level 11: &, left to right
        ('EXPR-L11', 'EXPR-L11 bit-op::& EXPR-L10'),
        ('EXPR-L11', 'EXPR-L10'),

        # Level 10: relational-op, left to right
        ('EXPR-L10', 'EXPR-L10 relational-op EXPR-L7'),
        ('EXPR-L10', 'EXPR-L7'),

        # Level 7: << >>, left to right
        ('EXPR-L7', 'EXPR-L7 bit-op::<< EXPR-L6'),
        ('EXPR-L7', 'EXPR-L7 bit-op::>> EXPR-L6'),
        ('EXPR-L7', 'EXPR-L6'),

        # Level 6: +-, left to right
        ('EXPR-L6', 'EXPR-L6 arithmetic-op::+ EXPR-L5'),
        ('EXPR-L6', 'EXPR-L6 arithmetic-op::- EXPR-L5'),
        ('EXPR-L6', 'EXPR-L5'),

        # Level 5: */%, left to right
        ('EXPR-L5', 'EXPR-L5 arithmetic-op::* EXPR-L3'),
        ('EXPR-L5', 'EXPR-L5 arithmetic-op::/ EXPR-L3'),
        ('EXPR-L5', 'EXPR-L5 arithmetic-op::% EXPR-L3'),
        ('EXPR-L5', 'EXPR-L3'),

        # Level 3: right to left
        ('EXPR-L3', 'increment-op EXPR-L3'),
        ('EXPR-L3', 'arithmetic-op::+ EXPR-L3'),
        ('EXPR-L3', 'arithmetic-op::- EXPR-L3'),
        ('EXPR-L3', 'logical-op::! EXPR-L3'),
        ('EXPR-L3', 'bit-op::~ EXPR-L3'),
        ('EXPR-L3', 'arithmetic-op::* EXPR-L3'),
        ('EXPR-L3', 'bit-op::& EXPR-L3'),
        ('EXPR-L3', 'new EXPR-L3'),
        ('EXPR-L3', 'new bracket::[ bracket::] EXPR-L3'),
        ('EXPR-L3', 'delete EXPR-L3'),
        ('EXPR-L3', 'delete bracket::[ bracket::] EXPR-L3'),
        ('EXPR-L3', 'EXPR-L2'),

        # Level 2: left to right
        ('EXPR-L2', 'EXPR-L2 member-op EXPR-L1'),
        ('EXPR-L2', 'EXPR-L2 ptr-member-op EXPR-L1'),
        ('EXPR-L2', 'EXPR-L2 ARG-LIST'),
        ('EXPR-L2', 'EXPR-L2 bracket::[ EXPR bracket::]'),
        ('EXPR-L2', 'EXPR-L2 increment-op'),
        ('EXPR-L2', 'EXPR-L1'),
        ('ARG-LIST', 'parenthesis::( parenthesis::)'),
        ('ARG-LIST', 'parenthesis::( EXPR parenthesis::)'),

        # Level 1: double-colon, left to right
        ('EXPR-L1', 'ID'),
        ('EXPR-L1', 'OPERAND'),

        # ID
        ('ID', 'ID double-colon id'),
        ('ID', 'id'),

        # Operand
        ('OPERAND', 'parenthesis::( EXPR parenthesis::)'),
        ('OPERAND', 'hex-lit'),
        ('OPERAND', 'oct-lit'),
        ('OPERAND', 'int-lit'),
        ('OPERAND', 'float-lit'),
        ('OPERAND', 'char-lit'),
        ('OPERAND', 'str-lit'),
        ('OPERAND', 'true'),
        ('OPERAND', 'false'),
    ]
}
