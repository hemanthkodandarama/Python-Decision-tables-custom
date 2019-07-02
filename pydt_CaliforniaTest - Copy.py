import pydt

#test_fact = { "Time Entry Hours" : 20, "Day Number" : 0, "Weekly Total Hours" : 20,"Regular Time PayCode":"" }

#test_table = {
#    "condition_headers" : [ ["A" , "Time Entry Hours"], ["B", "Day Number"], ["C", "Weekly Total Hours"],["D", "Regular Time PayCode"]],
#    "action_headers" : [ ["G","Threshold Name"],["H","Premium"], ["I","Pay Code"]],

#    "data" : [
#              {
#                "row": 2,
#                "A": "<= 20", # "0-8"
#                "B": "",
#                "C": "",
#                "D": "",
#                "F": "Regular Time",
#                "G": 1,
#                "H": "RT"
#              },
#              {
#                "row": 3,
#                "A": "8-12",
#                "B": "",
#                "C": "",
#                "D": "",
#                "F": "Daily Threshold1",
#                "G": 1.5,
#                "H": "DT1"
#              },
#              {
#                "row": 4,
#                "A": ">12",
#                "B": "",
#                "C": "",
#                "D": "",
#                "F": "Daily Threshold2",
#                "G": 2,
#                "H": "DT2"
#              },
#              {
#                "row": 5,
#                "A": "",
#                "B": "",
#                "C": ">40",
#                "D": "RT",
#                "F": "Weekly Threshold",
#                "G": 1.5,
#                "H": "WT"
#              },
#              {
#                "row": 6,
#                "A": ">8",
#                "B": "==7",
#                "C": "",
#                "D": "",
#                "F": "7th Day Threshold",
#                "G": 1.5,
#                "H": "DT7"
#              }
#            ]

#}


##and now some crude test code
#pydt.process_dt(test_fact, test_table)
#print "RESULT: " + str(test_fact)
#if not test_fact.has_key("Premium") :
#	print("ERROR: no premium was calculated")
#if  test_fact["Premium"] == '245' :
#	print("PASSED STEP 1")
#else :
#	print("FAILED STEP 1: Premium was " + test_fact["Premium"])

#some simple test
tbl = pydt.load_xls("California-DecisionTable.xls")
if tbl['condition_headers'][0][1] == "Age" :
	print "PASSED STEP 2"
else:
	print "FAILED STEP 2"

#now test it all, end to end
#test_fact = { "Age" : 42, "Risk" : "'HIGH'", "PolicyType" : "'COMPREHENSIVE'" }
test_fact = { "Time Entry Hours" : 20, "Day Number" : 0, "Weekly Total Hours" : 20,"Regular Time PayCode":"" }
pydt.process_dt(test_fact, tbl)
if not test_fact.has_key("Premium") :
	print("ERROR: no premium was calculated")
premium = test_fact["Premium"]
if premium == 245 :
	print("PASSED STEP 3")
else :
	print("FAILED STEP 3: Premium was " + test_fact["Premium"])
