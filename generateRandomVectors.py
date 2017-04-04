from sys import argv
import random

script, filename = argv

target = open(filename,'w')

target.truncate()

for i in range(0,26):
	for j in range(0,99):
		target.write(str(random.random()))
		target.write(" ")
	target.write("\n")

target.close()