import os
import filecmp
from dateutil.relativedelta import *
from datetime import date


def getData(file):
# get a list of dictionary objects from the file
#Input: file name
#Ouput: return a list of dictionary objects where
#the keys are from the first row in the data. and the values are each of the other rows
	inFile = open(file, "r")

	dictlst = []
	lines = inFile.readlines()
	inFile.close()
	for line in lines: 
		values = line.split(",")
		person_dct = {}

		first_name = values[0]
		last_name = values[1]
		email = values[2]
		class_standing = values[3]
		birthday = values[4].strip("\n")

		person_dct["First"] = first_name
		person_dct["Last"] = last_name
		person_dct["Email"] = email
		person_dct["Class"] = class_standing
		person_dct["DOB"] = birthday
		dictlst.append(person_dct)
	return dictlst


def mySort(data,col):
# Sort based on key/column
#Input: list of dictionaries and col (key) to sort on
#Output: Return the first item in the sorted list as a string of just: firstName lastName
	person_lst = []
	sorted_dicts = sorted(data, key = lambda x: x[col])
	for person in sorted_dicts:
		person_lst.append(str(person["First"] + " " + person["Last"]))

	return person_lst[0]
	


def classSizes(data):
# Create a histogram
# Input: list of dictionaries
# Output: Return a list of tuples sorted by the number of students in that class in
# descending order
# [('Senior', 26), ('Junior', 25), ('Freshman', 21), ('Sophomore', 18)]
	fresh_count = 0
	soph_count = 0
	junior_count = 0
	senior_count = 0
	for person_dct in data:
		if person_dct["Class"] == "Freshman":
			fresh_count += 1
		if person_dct["Class"] == "Sophomore":
			soph_count += 1
		if person_dct["Class"] == "Junior":
			junior_count += 1
		if person_dct["Class"] == "Senior":		
			senior_count += 1
	fresh_tup = "Freshman", fresh_count
	soph_tup = "Sophomore", soph_count
	junior_tup = "Junior", junior_count
	senior_tup = "Senior", senior_count

	lst = [fresh_tup, soph_tup, junior_tup, senior_tup]
	return sorted(lst, key = lambda x: x[1], reverse = True)

def findMonth(a):
# Find the most common birth month from this data
# Input: list of dictionaries
# Output: Return the month (1-12) that had the most births in the data
	dct = {}
	for person in a:
		month = person["DOB"].split("/")[0]
		if month not in dct:
			dct[month] = 1
		else:
			dct[month] += 1

	return int(sorted(dct, key = lambda x: dct[x], reverse = True)[0])


def mySortPrint(a,col,fileName):
#Similar to mySort, but instead of returning single
#Student, the sorted data is saved to a csv file.
# as first,last,email
#Input: list of dictionaries, col (key) to sort by and output file name
#Output: No return value, but the file is written
	outfile = open(fileName, "w")
	#output each of the rows
	lst = a[1:]
	sorted_dicts = sorted(lst, key = lambda x: x[col])
	for person in sorted_dicts:
		outfile.write("{},{},{}\n".format(person["First"].strip(),person["Last"].strip(),person["Email"].strip()))

	outfile.close()


def findAge(a):
# Input: list of dictionaries
# Output: Return the average age of the students and round that age to the nearest
# integer.  You will need to work with the DOB and the current date to find the current
# age in years.
	lst = []
	now = date.today()
	right_lst = a[1:]
	for person in right_lst: 
		values = person["DOB"].split("/")
		month_born = int(values[0])
		day_born = int(values[1])
		year_born = int(values[2])
		
		age = (now.year - year_born) - ((now.month, now.day) < (month_born, day_born))
		lst.append(int(age))
	average = int(round(sum(lst)/len(lst)))
	return average
		

################################################################
## DO NOT MODIFY ANY CODE BELOW THIS
################################################################

## We have provided simple test() function used in main() to print what each function returns vs. what it's supposed to return.
def test(got, expected, pts):
  score = 0;
  if got == expected:
    score = pts
    print(" OK ", end=" ")
  else:
    print (" XX ", end=" ")
  print("Got: ",got, "Expected: ",expected)
  return score


# Provided main() calls the above functions with interesting inputs, using test() to check if each result is correct or not.
def main():
	total = 0
	print("Read in Test data and store as a list of dictionaries")
	data = getData('P1DataA.csv')
	data2 = getData('P1DataB.csv')
	total += test(type(data),type([]),50)

	print()
	print("First student sorted by First name:")
	total += test(mySort(data,'First'),'Abbot Le',25)
	total += test(mySort(data2,'First'),'Adam Rocha',25)

	print("First student sorted by Last name:")
	total += test(mySort(data,'Last'),'Elijah Adams',25)
	total += test(mySort(data2,'Last'),'Elijah Adams',25)

	print("First student sorted by Email:")
	total += test(mySort(data,'Email'),'Hope Craft',25)
	total += test(mySort(data2,'Email'),'Orli Humphrey',25)

	print("\nEach grade ordered by size:")
	total += test(classSizes(data),[('Junior', 28), ('Senior', 27), ('Freshman', 23), ('Sophomore', 22)],25)
	total += test(classSizes(data2),[('Senior', 26), ('Junior', 25), ('Freshman', 21), ('Sophomore', 18)],25)

	print("\nThe most common month of the year to be born is:")
	total += test(findMonth(data),3,15)
	total += test(findMonth(data2),3,15)

	print("\nSuccessful sort and print to file:")
	mySortPrint(data,'Last','results.csv')
	if os.path.exists('results.csv'):
		total += test(filecmp.cmp('outfile.csv', 'results.csv'),True,20)

	print("\nTest of extra credit: Calcuate average age")
	total += test(findAge(data), 40, 5)
	total += test(findAge(data2), 42, 5)

	print("Your final score is " + str(total))

# Standard boilerplate to call the main() function that tests all your code
if __name__ == '__main__':
   main()
