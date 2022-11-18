FILE="$1"
valid=false

if [ -z ${FILE##*.cpp} ]; then
    valid=true
fi

if "$valid"; then
    FILE_NO_SUFFIX="${FILE%".cpp"}"
    suffix=".ll"
    clang++ -emit-llvm -S $FILE
    echo ============ Output: $FILE_NO_SUFFIX.ll ============
    cat $FILE_NO_SUFFIX.ll
else
    echo Filename invalid
fi
