GRAMMAR = {
    "non-terminals": [
        "SENT-E",
        "SENT-T",
        "SENT-F",
    ],
    "terminals": [
        "parenthesis::(",
        "parenthesis::)",
        "int-lit",
        "id",
        "arithmetic-op::+",
        "arithmetic-op::*",
    ],
    "start": "SENT-E",
    "derivations": [
        ("SENT-E", "SENT-E arithmetic-op::+ SENT-T"),
        ("SENT-E", "SENT-T"),
        ("SENT-T", "SENT-T arithmetic-op::* SENT-F"),
        ("SENT-T", "SENT-F"),
        ("SENT-F", "parenthesis::( SENT-E parenthesis::)"),
        ("SENT-F", "id"),
        ("SENT-F", "int-lit"),
    ]
}
