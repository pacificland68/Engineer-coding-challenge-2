import csv
import json
import re
from collections import OrderedDict

#quickSort
def quickSort(arr, left, right):
    i = left
    j = right

    if i <= j:
        temp = arr[left]
        while i != j:
            while i < j and float(arr[j]['PPG']) <= float(temp['PPG']):
                j -= 1
                
            arr[i] = arr[j]
            while i < j and float(arr[i]['PPG']) >= float(temp['PPG']):
                i += 1
            arr[j] = arr[i]
            
        arr[j] = temp
        quickSort(arr, left, i-1)
        quickSort(arr, i+1, right)

#find the gold, silver and bronze player
def calculate(players):
    quickSort(players, 0, len(players)-1)

#find the gold, silver and bronze player
def award(result):
    leaders = []
    num = ["Gold", "Silver", "Bronze"]
    for i in range(3):
        leader = OrderedDict()
        leader[num[i]] = players[i]["Name"]
        leader["PPG"] = players[i]["PPG"]
        leaders.append(leader)
    result['Leaders'] = leaders

def category(result):
    position = OrderedDict()
    po = [0,0,0,0,0]
    po_name = ["PG", "C", "PF", "SG", "SF"]
    for row in result["Players"]:
        if row["Position"] == po_name[0]:
            po[0] += 1
        elif row["Position"] == po_name[1]:
            po[1] += 1
        elif row["Position"] == po_name[2]:
            po[2] += 1
        elif row["Position"] == po_name[3]:
            po[3] += 1
        elif row["Position"] == po_name[4]:
            po[4] += 1

    for i in range(5):
        position[po_name[i]] = po[i]
    result[""] = position

def average_height(result):
    sum = 0.0
    for row in result["Players"]:
        temp = row["Height"].replace(' ','').replace("ft", ',').replace("in",',')
        feet = float(temp.split(',')[0])
        
        inn = float(temp.split(',')[1])*0.0833
        sum = sum + (feet + inn)*30.48
    average = sum / float(14)
    # print(average)
    result['AverageHeight'] = round(average,2)

with open('chicago-bulls.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    result = OrderedDict()

    #calculate average
    total_PPG = 0.0
    
    next(csv_reader, None)
    players = []
    for row in csv_reader:
        players_info = OrderedDict()
        players_info["Id"] = row[0]
        players_info["Position"] = row[1]
        players_info["Number"] = row[2]
        players_info["Country"] = row[3]
        players_info["Name"] = row[4]
        players_info["Height"] = row[5]
        players_info["Weight"] = row[6]
        players_info["University"] = row[7]
        players_info["PPG"] = row[8]
        total_PPG += float(row[8])
        players.append(players_info)
    result['Players'] = players
    quickSort(players, 0, len(players)-1)
    result['AveragePPG'] = round(total_PPG/14, 2)
    award(result)
    category(result)
    average_height(result)
    print(json.dumps(result, indent=4))
    


