# # #!/bin/sh


# Taking tags from the command line

while getopts f:c:o:s:t: flag
do
    case "${flag}" in
        f) file=${OPTARG};;
        o) operation=${OPTARG};;
        s) size=${OPTARG};;
        t) target=${OPTARG};;
    esac
done



# Checking if a file name is properly specified

if [ -z "$file" ]
    then
        echo "Please specify an object code"
        exit 1
fi



# Setting missing parameters if any

if [ -z "$target"]
    then
        target="./tests"
        echo "test directory is set to './tests' "
fi

if [ -z "$size"]
    then
        size=0
        echo "test size is set to 0 "
fi



# Configuring names and directory

if [ "$file" = "string_search" ]
    then
        dir="/usr/src/app/examples/substring_search/IR0_"
        orig="/code/substring_search/IR0_"
        cp $orig$file.py $dir$file.py
        
    else
        if [ "$file" = "stringlist_search" ]
            then
                dir="/usr/src/app/examples/substring_search/IR0_"
                orig="/code/substring_search/IR0_"
                cp $orig$file.py $dir$file.py
            else
                dir="/usr/src/app/examples/substring_search/IR0_stringlist_search_"
                orig="/code/substring_search/IR0_stringlist_search_"
                cp $orig$file.py $dir$file.py
        fi
fi

prime=2305843009213693951
prime_fam="p1"

underscore="_"
name=$target/$file$underscore$prime_fam$underscore$size
rel=$name.rel
wit=$name.wit
ins=$name.ins

[ -e rel  ] && rm rel
[ -e wit  ] && rm wit
[ -e ins  ] && rm ins



# Actual Execution

echo "Running $file .... $operation test size:$size";

if [ "$operation" = "test" ]
    then 
        echo "Running synthetic test case"
        if python3 $dir$file.py $target $prime $prime_fam $size "test"
            then
                if wtk-firealarm $rel $wit $ins
                    then
                        echo "wtk-firealarm successfully completed"
                    else
                        echo "Error during wtk-firealarm"
                fi
            else
                echo "Error in the python script - abort"
        fi

    else
        echo "Running with your own text input in debug mode"
        cp /code/dfa_test_input.txt /usr/src/app/examples/dfa_test_input.txt
        if python3 $dir$file.py $target $prime $prime_fam $size "debug"
            then
                echo 'Check the output above'
            else
                echo "Error in the python script - abort"
        fi
fi