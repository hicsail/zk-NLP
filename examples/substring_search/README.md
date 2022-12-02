# How to write string search algorithm

Your script needs to comply with the following guideline, in order to make your script compilable by miniwizpl and to leverage the predefined shell script in the container.

You can also reference some of existing scripts as working examples:
<ul>
<li> <a href="https://github.com/hicsail/SIEVE/blob/main/examples/substring_search/stringlist_search_after.py"> stringlist_search_after</a>
<li> <a href="https://github.com/hicsail/SIEVE/blob/main/examples/substring_search/stringlist_search_after_all.py"> stringlist_search_after_all</a>
<li> <a href="https://github.com/hicsail/SIEVE/blob/main/examples/substring_search/stringlist_search_begins.py"> stringlist_search_begins</a>
<li> <a href="https://github.com/hicsail/SIEVE/blob/main/examples/substring_search/stringlist_search_between.py"> stringlist_search_between</a>
<li> <a href="https://github.com/hicsail/SIEVE/blob/main/examples/substring_search/stringlist_search_point_to.py"> stringlist_search_point_to</a>
</ul>

## Generating Testing Case

<strong> 1) Import all necessary libraries </strong>

<ul>

```  
import sys
from miniwizpl import *
from miniwizpl.expr import *
from common.util import *
```

</ul>

<strong> 2) Configure Input Text File </strong> 

<ul>
<a href="https://github.com/hicsail/SIEVE/blob/main/examples/substring_search/common/util.py"> util.py </a> defines a function which generates a synthetic test text input. 

In order to use the command line arguments, you'd need something like this:<br>
<u>(** remember to add len(sys.argv)>1 and >2 in the example below to avoid index-out-of-range)</u>
  
```
if (len(sys.argv)>1 and sys.argv[1] =="test") or (len(sys.argv)>2 and sys.argv[2] =="debug"):
    file_data=generate_text()
    string_a, string_target=generate_target(file_data, "point_to")
```

In case yo would like to test the script with your own input, copy and paste the text content in <a href="https://github.com/hicsail/SIEVE/blob/main/examples/dfa_test_input.txt">dfa_test_input.txt</a>

and configure other sub_strings/targets as below:

```
else:
    string_target =  ['not', 'in']
    string_a = 'our'
    with open(sys.argv[1], 'r') as f:
        file_data = f.read()
    file_data = file_data.split()

print("Text: ", file_data, "\n")
print("Target: ", string_target, "\n", "End: ", string_a, "\n",)
# Transform the text file to search into miniwizpl format
file_string = SecretList([word_to_integer(_str) for _str in file_data])
```
</ul>


<strong> 3) Debug Mode </strong>

<ul>
    In order to visually see the progress of DFA transition, you would need to run:
  <pre>public_foreach_unroll</pre>
  Likewise, in order for your python script to compile, you would need to implement:
  <pre>public_foreach</pre>

  Therefore, we suggest to add the following lines around public_foreach method inside the <a style="color:#FFFF00">next_state_fun</a> function.
    
  ```
if len(sys.argv)==3 and sys.argv[2] =="debug":
    latest_state=public_foreach_unroll(text_input, next_state_fun, zero_state)
else:
    latest_state=public_foreach(text_input, next_state_fun, zero_state)

return latest_state
  ```
</ul>
  
<strong> 4) Assert your proof </strong>

This is the change from the previous ver. of miniwizpl library.

<ul>
<pre>
latest_state = run_dfa(dfa, file_string)
assertTrueEMP(latest_state == accept_state)
print_emp(True, 'miniwizpl_test.cpp')
</pre>

The first argument in print_emp, True, will be removed in the next update, but as of now, it needs to be there.
  
In case you need to assert with the OR operation:

<pre>
assertTrueEMP((latest_state == accept_state)|(latest_state == appendedAll_state))
</pre>

</ul>
