local="/code/substring_search/"
container="/usr/src/app/examples/substring_search/"


# Copying the latest util.py into the common directory in container
dir="common/"
file='util.py'
cp $local$dir$file $container$dir$file


# Copying the latest unit test files.py into the unittests directory in container
dir="unittests/"
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
