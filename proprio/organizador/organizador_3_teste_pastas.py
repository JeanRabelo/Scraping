import os
import glob

path_dir = r'C:\Users\jean_\Documents\GitHub\Scraping\proprio\organizador\dados'

for filename in glob.glob(os.path.join(path_dir,'*.csv')):
    print(filename)
    print(type(filename))
