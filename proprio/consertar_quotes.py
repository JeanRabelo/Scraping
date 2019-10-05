import re

# open your csv and read as a text string
with open(my_csv_path, 'r') as f:
    my_csv_text = f.read()

find_str = 'The String, that should replaced'
replace_str = 'The string that should replace the old striong'

# substitute
new_csv_str = re.sub(find_str, replace_str, my_csv_text)

# open new file and save
new_csv_path = './my_new_csv.csv' # or whatever path and name you want
with open(new_csv_path, 'w') as f:
    f.write(new_csv_str)
