#!/usr/lib/bash
/usr/src/app/miniwizpl_test 1 12349 &
/usr/src/app/miniwizpl_test 2 12349

msg=$(ls -la nofile 2>&1)
echo $msg