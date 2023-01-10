# Copying the latest util.py into the container

local="/code/substring_search/common/"
container="/usr/src/app/examples/substring_search/common/"

util='util.py'
testutil='test_util.py'

cp $local$util $container$util
cp $local$testutil $container$testutil

python3 $container$testutil