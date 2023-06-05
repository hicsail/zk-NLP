local_dir="/code/substring_search/"
container_dir="/usr/src/app/examples/substring_search/"

# Copying the latest util.py into the common directory in container
cp "$local_dir"common/util.py "$container_dir"common/util.py

# Copying the latest test files.py into the tests directory in container
cp -r "$local_dir"tests "$container_dir"

# Executing each uint test file
run_test() {
    file=$1
    echo "testing with $file .... ";
    python3 "$container_dir"tests/unit/"$file"
}

run_test "test_util.py"
run_test "test_util_generate_text.py"
run_test "test_util_generate_target.py"

# Executing E2E tests for IR0 statements

origin_dir=$local_dir"IR0/"
dest_dir=$container_dir"/IR0/"

run_e2e_test() {
    test_file=$1
    statement=$2
    cp "$origin_dir""$statement" "$dest_dir""$statement"
    echo "testing with $test_file .... ";
    python3 "$container_dir"tests/e2e/"$test_file"
}

run_e2e_test "test_statement_after_all_multi.py" "after_all_multi.py"
run_e2e_test "test_statement_after_multi.py" "after_multi.py"
run_e2e_test "test_statement_begins_multi.py" "begins_multi.py"
run_e2e_test "test_statement_between_multi.py" "between_multi.py"
run_e2e_test "test_statement_point_to_multi.py" "point_to_multi.py"
run_e2e_test "test_statement_after_all.py" "after_all.py"
run_e2e_test "test_statement_after.py" "after.py"
run_e2e_test "test_statement_begins.py" "begins.py"
run_e2e_test "test_statement_between.py" "between.py"
run_e2e_test "test_statement_point_to.py" "point_to.py"
run_e2e_test "test_statement_string_search.py" "string_search.py"
run_e2e_test "test_statement_stringlist_search.py" "stringlist_search.py"
run_e2e_test "test_statement_stringlist_search_counter.py" "stringlist_search_counter.py"
