##
# This file is for testing the latest version 
# of the course matching.
##
from analysis import *
import random

#
def make_test(file_name="tmp_sample_test1.txt"):
    lines = []
    random_students = []
    for i in range(332):
        random_students.append(random.choice(list(DATASET.keys())))
    
    for k in random_students:
        stdnt = DATASET[k]
        for hsc in stdnt.hsCourses:
            line = "  | "+ hsc.course_label+" | "+ hsc.descr + '\n'
            lines.append(line)
    f = open(file_name,'w')
    f.writelines(lines)
    f.close()

for i in range(5):
    make_test("sample_test"+str(i)+".txt")

