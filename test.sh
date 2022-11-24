CMD="$1"
FILE="./example/$2.cpp"

set -e

exists=false
valid=false

if [ -z ${FILE##*.cpp} ]; then
    if [ -f "$FILE" ]; then
        exists=true
    fi
fi

CMDList="lexer parser"

if [[ $CMDList =~ (^|[[:space:]])$CMD($|[[:space:]]) ]]; then
    valid=true
fi

if $exists && $valid; then
    echo ==========TESTING $CMD: $FILE==========
    make $CMD
    echo [SUCCESS] make $CMD
    chmod +x ./bin/$CMD
    echo [SUCCESS] chmod +x ./bin/$CMD
    ./bin/$CMD $CMD $FILE
else
    if ! $valid; then
        echo [ERROR] command invalid: $CMD
    else
        echo [ERROR] file invalid: $FILE
    fi
fi
