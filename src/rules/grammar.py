GRAMMAR = {
    "non-terminals": [
        "sentence",
        "sub",
    ],
    "terminals": [
        "parenthesis::(",
        "parenthesis::)",
        "int-lit",
        "arithmetic-op::+",
    ],
    "start": "sentence",
    "derivations": [
        ("sentence", "sentence arithmetic-op::+ sub"),
        ("sentence", "sub"),
        ("sub", "int-lit"),
        ("sub", "parenthesis::( sentence parenthesis::)"),
    ]
}
