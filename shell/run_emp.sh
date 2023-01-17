# # #!/bin/sh


# Removing existing intermediate representations

[ -e miniwizpl_test ] && rm miniwizpl_test
[ -e miniwizpl_test.cpp  ] && rm miniwizpl_test.cpp 



# Taking tags from the command line

while getopts f:c:o: flag
do
    case "${flag}" in
        f) file=${OPTARG};;
        o) operation=${OPTARG};;
    esac
done



# Checking if a file name is properly specified

if [ -z "$file" ]
    then
        echo "Please specify an object code"
        exit 1
fi



# Copying the latest util.py into the container

local="/code/substring_search/common/util.py"
container="/usr/src/app/examples/substring_search/common/util.py"
cp $local $container



# Configuring names and directory, and copying a designated statement file

dir="/usr/src/app/examples/substring_search/EMP/"
orig="/code/substring_search/EMP/"
cp $orig$file.py $dir$file.py


# Actual Execution

echo "Running $file .... $operation";

if [ "$operation" = "test" ]

    then 

        echo "Running synthetic test case"

        if python3 $dir$file.py "test"
            then
                source ./compile.sh
            else
                echo "Error in the python script - abort"
        fi

    else

        echo "Running with your own text input in debug mode"
        cp /code/dfa_test_input.txt /usr/src/app/examples/dfa_test_input.txt

        if python3 $dir$file.py "debug"
            then
                source ./compile.sh
            else
                echo "Error in the python script - abort"
        fi

fi
