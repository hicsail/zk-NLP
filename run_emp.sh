# # #!/bin/sh

[ -e miniwizpl_test ] && rm miniwizpl_test
[ -e miniwizpl_test.cpp  ] && rm miniwizpl_test.cpp 


while getopts f:c:o: flag
do
    case "${flag}" in
        f) file=${OPTARG};;
        o) operation=${OPTARG};;
    esac
done

if [ -z "$file" ]
    then
        echo "Please specify an object code"
    else
        cp /code/$file /usr/src/app/examples/$file

        echo "Running $file .... $operation";

        if [ "$operation" = "test" ]
            then 
                echo "Running synthetic test case"
                if python3 /usr/src/app/examples/$file "test"
                    then
                        source ./compile.sh
                    else
                        echo "Error in the python script - abort"
                fi

            else
                if [ "$operation" = "debug" ]
                    then 
                        echo "Running in debug mode"
                        if python3 /usr/src/app/examples/$file /usr/src/app/examples/dfa_test_input.txt "debug"
                            then
                                echo 'Check the lines above'
                            else
                                echo "Error in the python script - abort"
                        fi
                    else
                        echo "Running with your own text input"
                        if python3 /usr/src/app/examples/$file /usr/src/app/examples/dfa_test_input.txt
                            then
                                source ./compile.sh
                            else
                                echo "Error in the python script - abort"
                        fi
                fi
        fi
fi