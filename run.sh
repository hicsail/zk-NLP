# # #!/bin/sh

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

if python3 /usr/src/app/examples/$path_to
then

    g++  miniwizpl_test.cpp -o miniwizpl_test\
        -pthread -Wall -funroll-loops -Wno-ignored-attributes -Wno-unused-result -march=native -maes -mrdseed -std=c++11 -O3 \
        -I/usr/src/app/miniwizpl/boilerplate\
        -I/usr/lib/openssl/include\
        -L/usr/lib/openssl/lib -lssl -lcrypto \
        -L/usr/src/app/emp-zk/emp-zk -lemp-zk\
        -L/usr/src/app/emp-tool/emp-tool -lemp-tool\
        -L/usr/local/lib -Wl,-R/usr/local/lib    

    chmod ugo+rwx /usr/src/app/miniwizpl_test

    /usr/src/app/miniwizpl_test 1 12349 &
    /usr/src/app/miniwizpl_test 2 12349 &

else
    echo "Error in the python script - abort"
fi