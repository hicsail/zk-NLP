# # #!/bin/sh

[ -e miniwizpl_test_ir0.ins  ] && rm miniwizpl_test_ir0.ins
[ -e miniwizpl_test_ir0.rel  ] && rm miniwizpl_test_ir0.rel
[ -e miniwizpl_test_ir0.rel  ] && rm miniwizpl_test_ir0.wit

while getopts f:c:o: flag
do
    case "${flag}" in
        f) folder=${OPTARG};;
        c) code=${OPTARG};;
        o) operation=${OPTARG};;
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
cp /code/dfa_test_input.txt /usr/src/app/examples/dfa_test_input.txt
mv /usr/src/app/miniwizpl_test_ir0.ins   /usr/src/app/wiztoolkit/miniwizpl_test_ir0.ins
mv /usr/src/app/miniwizpl_test_ir0.wit   /usr/src/app/wiztoolkit/miniwizpl_test_ir0.wit
mv /usr/src/app/miniwizpl_test_ir0.rel   /usr/src/app/wiztoolkit/miniwizpl_test_ir0.rel

echo "Running $path_to .... $operation";

if [ "$operation" = "test" ]
    then 
        echo "Running synthetic test case"
        if python3 /usr/src/app/examples/$path_to "test"
            then
                cd wiztoolkit
                wtk-bolt bolt miniwizpl_test_ir0.rel miniwizpl_test_ir0.wit miniwizpl_test_ir0.ins
                cd ..
            else
                echo "Error in the python script - abort"
        fi

    else
        if [ "$operation" = "debug" ]
            then 
                echo "Running in debug mode"
                if python3 /usr/src/app/examples/$path_to /usr/src/app/examples/dfa_test_input.txt "debug"
                    then
                        echo 'Check the output above'
                    else
                        echo "Error in the python script - abort"
                fi
            else
                echo "Running with your own text input"
                if python3 /usr/src/app/examples/$path_to /usr/src/app/examples/dfa_test_input.txt
                    then
                        cd wiztoolkit
                        wtk-bolt bolt miniwizpl_test_ir0.rel miniwizpl_test_ir0.wit miniwizpl_test_ir0.ins
                        cd ..
                    else
                        echo "Error in the python script - abort"
                fi
        fi
fi