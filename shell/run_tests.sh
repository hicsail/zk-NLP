local="/code/substring_search/"
container="/usr/src/app/examples/substring_search/"


# Copying the latest util.py into the common directory in container

utildir="common/"
file='util.py'
cp $local$utildir$file $container$utildir$file


# Copying the latest test files.py into the tests directory in container

testdir="tests/"
cp -r $local$testdir $container


# Executing each uint test file

file='test_util.py'
echo "testing with $file .... ";
python3 $container$testdir$file

file='test_util_generate_text.py'
echo "testing with $file .... ";
python3 $container$testdir$file

file='test_util_generate_target.py'
echo "testing with $file .... ";
python3 $container$testdir$file


# Executing E2E tests for IR0 statements

origin=$local"IR0/"
dest=$container"/IR0/"


# after all multi
test_file='test_statement_after_all_multi.py'
statement='after_all_multi.py'

cp $origin$statement $dest$statement
echo "testing with $test_file .... ";
python3 $container$testdir$test_file


# after multi
test_file='test_statement_after_multi.py'
statement='after_multi.py'

cp $origin$statement $dest$statement
echo "testing with $test_file .... ";
python3 $container$testdir$test_file


# begins multi
test_file='test_statement_begins_multi.py'
statement='begins_multi.py'

cp $origin$statement $dest$statement
echo "testing with $test_file .... ";
python3 $container$testdir$test_file


# between multi
test_file='test_statement_between_multi.py'
statement='between_multi.py'

cp $origin$statement $dest$statement
echo "testing with $test_file .... ";
python3 $container$testdir$test_file


# point_to multi
test_file='test_statement_point_to_multi.py'
statement='point_to_multi.py'

cp $origin$statement $dest$statement
echo "testing with $test_file .... ";
python3 $container$testdir$test_file


## after all
test_file='test_statement_after_all.py'
statement='after_all.py'

cp $origin$statement $dest$statement
echo "testing with $test_file .... ";
python3 $container$testdir$test_file


# after
test_file='test_statement_after.py'
statement='after.py'

cp $origin$statement $dest$statement
echo "testing with $test_file .... ";
python3 $container$testdir$test_file


# begins
test_file='test_statement_begins.py'
statement='begins.py'

cp $origin$statement $dest$statement
echo "testing with $test_file .... ";
python3 $container$testdir$test_file


# between
test_file='test_statement_between.py'
statement='between.py'

cp $origin$statement $dest$statement
echo "testing with $test_file .... ";
python3 $container$testdir$test_file


# point_to
test_file='test_statement_point_to.py'
statement='point_to.py'

cp $origin$statement $dest$statement
echo "testing with $test_file .... ";
python3 $container$testdir$test_file


# string_search
test_file='test_statement_string_search.py'
statement='string_search.py'

cp $origin$statement $dest$statement
echo "testing with $test_file .... ";
python3 $container$testdir$test_file


# stringlist_search
test_file='test_statement_stringlist_search.py'
statement='stringlist_search.py'

cp $origin$statement $dest$statement
echo "testing with $test_file .... ";
python3 $container$testdir$test_file