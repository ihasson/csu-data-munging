import readData as rd
import Student as sdt
import sys
import re

data = rd.big_merge(hsd=rd.read_Large_HS(),csd=rd.read_College_Seq())

f = open("training2.txt",'w')

lines = []
for s in data:
    hsc = data[s].hsCourses
    if len(hsc[0].High_School) > 1:
        for c in hsc:
          lines.append("   ,"+str(c.High_School)+"  a,"+str(c.descr)+"\n")
f.writelines(lines)
f.close()
