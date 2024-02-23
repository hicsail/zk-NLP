# # #!/bin/sh

# Initialize variables
file=""
operation=""
size=""
target=""

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

# Setting default values for missing parameters.
: ${target:="./irs"}
: ${size:=0}

# Inform the user of defaults only when they are used.
[ -z "$OPTARG" ] && echo "Default test directory set to './irs'"
[ -z "$OPTARG" ] && echo "Default test size set to 0"

dir="/usr/src/app/examples/substring_search/IR0/"
prime=2305843009213693951
prime_fam="p1"
underscore="_"
name="${target}/${file}${underscore}${prime_fam}${underscore}${size}"
rel="${name}.rel"
wit="${name}.type0.wit"
ins="${name}.type0.ins"

# Removing existing files if they exist.
rm -f "$rel" "$wit" "$ins"


# Execution starts.
echo "Running $file .... $operation test size:$size";

# Handling different operations.
if [ "$operation" = "test" ]; then
    echo "Running synthetic test case"
else
    echo "Running with your own text input in debug mode"
fi

python3 "${dir}${file}.py" "$target" "$prime" "$prime_fam" "$size" "$operation";


# firealarm format check

# Check if wtk-firealarm is installed.
if ! command -v wtk-firealarm >/dev/null 2>&1; then
    echo "wtk-firealarm is not installed. Please follow the instructions below to install it:"
    echo "  git clone git@github.mit.edu:sieve-all/wiztoolkit.git"
    echo "  cd wiztoolkit && make && make install"
    echo "  cp /usr/src/app/wiztoolkit/target/wtk-firealarm /usr/bin/wtk-firealarm"
    echo "  cd .. #Go back to the current directory"
    exit 1
fi

if wtk-firealarm "$rel" "$wit" "$ins"; then
    echo "wtk-firealarm successfully completed"
else
    echo "Error during wtk-firealarm"
fi