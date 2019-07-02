import pydt
import copy
from ThresholdLogic import ThresholdLogicProcess

#some simple test
#decisiontbl = pydt.load_xls("California-DecisionTable.xls")
#if tbl['condition_headers'][0][1] == "Age" :
#	print "PASSED STEP 2"
#else:
#	print "FAILED STEP 2"

#now test it all, end to end
#test_fact = { "Age" : 42, "Risk" : "'HIGH'", "PolicyType" : "'COMPREHENSIVE'" }
#test_fact = { "Time Entry Hours" : 20, "Day Number" : 0, "Weekly Total Hours" : 20,"Regular Time PayCode":"" }
#test_fact = { "TimeEntryHours" : 20}
decisiontbl = pydt.load_xls("California-DecisionTable.xls")
test_timeEntries = pydt.load_xls_list_dict("California-TimeEntries.xls")
for entry in test_timeEntries:
    entry['Type']='"Threshold Logic"'
    entry['actions']=[]
    for col in decisiontbl['condition_headers']:
        if not entry.has_key(col[1]) : 
            entry[col[1]]=""   

#for entry in test_timeEntries:
#    tempentry = copy.deepcopy(entry)
#    tempentry['action']={}
#    weeklytotal
#    while tempentry['TimeEntrHours'] > 0 :
#        pydt.process_dt(tempentry, decisiontbl)
#        tempentry['TimeEntrHours'] = ThresholdLogicProcess(entry,tempentry['action'])
#    entry['actions'].append(tempentry['action'])

test_timeEntries[0]['action']={}
pydt.process_dt(test_timeEntries[0], decisiontbl)

if not test_fact.has_key("Premium") :
	print("ERROR: no premium was calculated")
premium = test_fact["Premium"]
if premium == 245 :
	print("PASSED STEP 3")
else :
	print("FAILED STEP 3: Premium was " + test_fact["Premium"])
