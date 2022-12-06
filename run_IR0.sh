# # #!/bin/sh

while getopts f:c:o:s:t: flag
do
    case "${flag}" in
        f) file=${OPTARG};;
        o) operation=${OPTARG};;
        s) size=${OPTARG};;
        t) tests=${OPTARG};;
    esac
done

[ -e $tests/miniwizpl_test_ir0.ins  ] && rm $tests//miniwizpl_test_ir0.ins
[ -e $tests/miniwizpl_test_ir0.rel  ] && rm $tests//miniwizpl_test_ir0.rel
[ -e $tests/miniwizpl_test_ir0.rel  ] && rm $tests//miniwizpl_test_ir0.wit

if [ -z "$file" ]
    then
        echo "Please specify an object code"
    else
        cp /code/$file /usr/src/app/examples/$file
        
        echo "Running $file .... $operation";

        if [ "$operation" = "test" ]
            then 
                echo "Running synthetic test case"
                if python3 /usr/src/app/examples/$file "dummy" "test" $size $tests
                    then
                        wtk-firealarm $tests//miniwizpl_test_ir0.rel $tests//miniwizpl_test_ir0.wit ./tests/miniwizpl_test_ir0.ins
                    else
                        echo "Error in the python script - abort"
                fi

            else
                if [ "$operation" = "debug" ]
                    then 
                        echo "Running in debug mode"
                        if python3 /usr/src/app/examples/$file "dummy" "debug" $size $tests
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
                                if python3 /usr/src/app/examples/$file /usr/src/app/examples/dfa_test_input.txt "debug/own" "dummy" $tests
                                    then
                                        echo 'Check the output above'
                                fi
                            else
                                echo "Running with your own text input"
                                if python3 /usr/src/app/examples/$file /usr/src/app/examples/dfa_test_input.txt "dummy" "dummy" $tests
                                    then
                                        wtk-firealarm ./tests/miniwizpl_test_ir0.rel ./tests/miniwizpl_test_ir0.wit ./tests/miniwizpl_test_ir0.ins
                                    else
                                        echo "Error in the python script - abort"
                                fi
                        fi
                fi
        fi
fi