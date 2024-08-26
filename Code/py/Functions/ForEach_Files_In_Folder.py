# import required module
import os
# assign directory
directory = 'C:\RPADATA\RPA_240_SYC_1118\Input\2022-09-19'
 
# iterate over files in
# that directory
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        print(f)