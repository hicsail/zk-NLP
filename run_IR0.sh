# # #!/bin/sh

[ -e miniwizpl_test_ir0.ins  ] && rm miniwizpl_test_ir0.ins
[ -e miniwizpl_test_ir0.rel  ] && rm miniwizpl_test_ir0.rel
[ -e miniwizpl_test_ir0.rel  ] && rm miniwizpl_test_ir0.wit

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
                        wtk-firealarm miniwizpl_test_ir0.rel miniwizpl_test_ir0.wit miniwizpl_test_ir0.ins
                    else
                        echo "Error in the python script - abort"
                fi

            else
                if [ "$operation" = "debug" ]
                    then 
                        echo "Running in debug mode"
                        if python3 /usr/src/app/examples/$file /usr/src/app/examples/dfa_test_input.txt "debug"
                            then
                                echo 'Check the output above'
                            else
                                echo "Error in the python script - abort"
                        fi
                    else
                        cp /code/dfa_test_input.txt /usr/src/app/examples/dfa_test_input.txt
                        if [ "$operation" = "debug/own" ]
                            then 
                                echo "Running with your own text input in debug mode"
                                if python3 /usr/src/app/examples/$file /usr/src/app/examples/dfa_test_input.txt "debug/own"
                                    then
                                        echo 'Check the output above'
                                fi
                            else
                                echo "Running with your own text input"
                                if python3 /usr/src/app/examples/$file /usr/src/app/examples/dfa_test_input.txt
                                    then
                                        wtk-firealarm miniwizpl_test_ir0.rel miniwizpl_test_ir0.wit miniwizpl_test_ir0.ins
                                    else
                                        echo "Error in the python script - abort"
                                fi
                        fi
                fi
        fi
fi