import datetime
import os

# print(os.path.abspath("test"))
# print(os.path.basename("/Users/dell/desktop/test"))
# print(os.path.dirname("/Users/dell/desktop/test"))


# print(os.path.join("/Users/dell/desktop","/test"))
# print(os.path.abspath(os.path.join("/Users/dell/desktop","test")))

file = 'test.txt'
file = os.path.realpath(file)
print(os.path.exists(file))
# os.system(f'explorer /select, {file}')