import csv
def binner_10_bin(value):
	value=int(value)
	#bins the grades into bins of 10
	if value <= 10:
		return 1
	elif value <=20:
		return 2
	elif value <=30:
		return 3
	elif value <=40:
		return 4
	elif value <=50:
		return 5
	elif value <=60:
		return 6
	elif value <=70:
		return 7
	elif value <=80:
		return 8
	elif value <=90:
		return 9
	else:
		return 10

f=open("StudentsPerformance.csv","r")
out = open('StudentsPerformanceBinned.csv', 'w',newline='')
reader = csv.reader(f)
writer = csv.writer(out)

line_counnt=0
for line in reader:
    items=line
    if line_counnt !=0:
    	print(items[5],items[6], items[7])
    	items[5]=binner_10_bin(items[5])
    	items[6]=binner_10_bin(items[6])
    	items[7]=binner_10_bin(items[7])
    	print("Binned",items[5],items[6], items[7])
    writer.writerow(items)
    line_counnt+=1


