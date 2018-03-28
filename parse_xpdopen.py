import glob

file_list = glob.glob("./xpdopen/*.txt")

for f in file_list:
     f_content = open(f)
     print(f)
     print(f_content.readlines())
     break