import getopt as cmd
import sys

def pullCharacterLookUpTable():

	characterMatrix = []
	with open("characterVectors.txt") as f:
		for index,line in enumerate(f):
			characterMatrix.append([])
			vectorString = line
			values = vectorString.split()
			for value in values:
				characterMatrix[index].append(float(value))
			

	return characterMatrix




def main(argv):
	workingCharcterMatrix = pullCharacterLookUpTable()
	printout = str(workingCharcterMatrix[1][53])
	sys.stdout.write("printing character matrix at [1][53]" + printout)
	sys.stdout.flush()


	while(1):
		sentence = sys.stdin.readline()

		words = sentence.split(" ")





if __name__ == "__main__":
	main(sys.argv[1:])