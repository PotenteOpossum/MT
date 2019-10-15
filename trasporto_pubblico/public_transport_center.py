import requests
import csv

app_id = ""
app_code = ""

vehicles = ["car", "pedestrian", "publicTransport", "bicycle"] 

center_districts = {
	"1": [45.062409, 7.677056], #ok
	"2": [45.032255, 7.617829], #ok
	"3": [45.064613, 7.636485], #ok
	"4": [45.084897, 7.643180], #ok
	"5": [45.106010, 7.654496], #ok
	"6": [45.108510, 7.704181], #ok
	"7": [45.069203, 7.719901], #ok
	"8": [45.041084, 7.683335] 	#ok
}

hours = ["08", "13", "19", "23"]
date = "2019-10-21" #lunedì

csv_head = ["starting_hour", "from", "to", "travel_time", "distance"]

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
	percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
	filledLength = int(length * iteration // total)
	bar = fill * filledLength + '-' * (length - filledLength)
	print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
	if iteration == total: 
		print()

def calculateroute(hour, starting_point, actual_distric, file_name, vehicle):
	for center in center_districts:
		if center != actual_distric:
			url = """https://route.api.here.com/routing/7.2/calculateroute.json?app_id=%s&app_code=%s&waypoint0=geo!%s,%s&waypoint1=geo!%s,%s&departure=%sT%s:00:00Z&mode=fastest;%s;traffic:enabled&combineChange=true""" % (app_id, app_code, starting_point[0], starting_point[1], center_districts[center][0], center_districts[center][1], date, hour, vehicle)
			response = requests.post(url).json()
			travelTime = int(response['response']['route'][0]['summary']['travelTime'] / 60)
			distance = (response['response']['route'][0]['summary']['distance'] / 1000)
			# print("tempo: ",travelTime," minuti")
			# print("distanza: ", distance," km")
			new_line = [hour, actual_distric, center, travelTime, distance]
			with open(file_name, 'a', newline='') as csvFile:
				wr = csv.writer(csvFile, quoting=csv.QUOTE_ALL)
				wr.writerow(new_line)

def create_file(vehicle):
	file_name = vehicle + "_dist.csv"
	with open(file_name, 'w', newline='') as csvFile:
		wr = csv.writer(csvFile, quoting=csv.QUOTE_ALL)
		wr.writerow(csv_head)
	l = len(hours)
	printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
	i = 0
	for hour in hours:
		printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
		i += 1
		for center in center_districts:
			calculateroute(hour, center_districts[center], center, file_name, vehicle)

for vehicle in vehicles:
	print("\n\n")
	print("-------   ", vehicle.upper(),"   -------")
	print("\n")
	create_file(vehicle)