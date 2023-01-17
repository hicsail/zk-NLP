local="/code/substring_search/"
container="/usr/src/app/examples/substring_search/"


# Copying the latest util.py into the common directory in container
dir="common/"
file='util.py'
cp $local$dir$file $container$dir$file


# Copying the latest test files.py into the tests directory in container
dir="tests/"
cp -r $local$dir $container


# Executing each uint test file
file='test_util.py'
echo "testing with $file .... ";
python3 $container$dir$file

file='test_util_generate_text.py'
echo "testing with $file .... ";
python3 $container$dir$file

file='test_util_generate_target.py'
echo "testing with $file .... ";
python3 $container$dir$file


# Executing E2E test

file='test_statement_after_all.py'
orig="/code/substring_search/IR0_stringlist_search_after_all.py"
dest="/usr/src/app/examples/substring_search/IR0_stringlist_search_after_all.py"

cp $orig $dest
echo "testing with $file .... ";
python3 $container$dir$file


file='test_statement_after.py'
orig="/code/substring_search/IR0_stringlist_search_after.py"
dest="/usr/src/app/examples/substring_search/IR0_stringlist_search_after.py"

cp $orig $dest
echo "testing with $file .... ";
python3 $container$dir$file


file='test_statement_begins.py'
orig="/code/substring_search/IR0_stringlist_search_begins.py"
dest="/usr/src/app/examples/substring_search/IR0_stringlist_search_begins.py"

cp $orig $dest
echo "testing with $file .... ";
python3 $container$dir$file


file='test_statement_between.py'
orig="/code/substring_search/IR0_stringlist_search_between.py"
dest="/usr/src/app/examples/substring_search/IR0_stringlist_search_between.py"

cp $orig $dest
echo "testing with $file .... ";
python3 $container$dir$file


file='test_statement_point_to.py'
orig="/code/substring_search/IR0_stringlist_search_point_to.py"
dest="/usr/src/app/examples/substring_search/IR0_stringlist_search_point_to.py"

cp $orig $dest
echo "testing with $file .... ";
python3 $container$dir$file


file='test_statement_string_search.py'
orig="/code/substring_search/IR0_string_search.py"
dest="/usr/src/app/examples/substring_search/IR0_string_search.py"

cp $orig $dest
echo "testing with $file .... ";
python3 $container$dir$file


file='test_statement_stringlist_search.py'
orig="/code/substring_search/IR0_stringlist_search.py"
dest="/usr/src/app/examples/substring_search/IR0_stringlist_search.py"

cp $orig $dest
echo "testing with $file .... ";
python3 $container$dir$file