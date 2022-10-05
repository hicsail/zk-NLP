# # #!/bin/sh

[ -e miniwizpl_test ] && rm miniwizpl_test
[ -e miniwizpl_test.cpp  ] && rm miniwizpl_test.cpp 

while getopts f:c: flag
do
    case "${flag}" in
        f) folder=${OPTARG};;
        c) code=${OPTARG};;
    esac
done

if [ -z "$folder" ]
then
    if [ -z "$code" ]
    then
        path_to="simple_demos/simple.py"
        echo "No file/folder assigned - Defult test file selected ..."
    else
        path_to=$code
    fi
else
    slash="/"
    path_to=$folder$slash$code
fi

cp /code/$path_to /usr/src/app/examples/$path_to

echo "Running $path_to ....";
echo "$code";

if python3 /usr/src/app/examples/$path_to /usr/src/app/examples/dfa_test_input.txt
    then
        source ./compile.sh
    else
        echo "Error in the python script - abort"
fi