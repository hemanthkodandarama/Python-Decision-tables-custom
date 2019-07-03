import pydt
import Conditions

decisiontbl = pydt.load_xls("California-DecisionTable.xls")
ConditionNames = pydt.GetUniqueConditionsNames(decisiontbl)
test_timeEntries = pydt.load_xls_list_dict("California-TimeEntries.xls")
pydt.MapTimeAndDecisionData(test_timeEntries,decisiontbl)

for entry in test_timeEntries:
    pydt.process_dt(entry, decisiontbl)

    for condition in ConditionNames:
        cmd = "Conditions.%s.ApplyActions(condition,test_timeEntries,test_timeEntries[0],decisiontbl)" % (condition)

#for entry in test_timeEntries:
#    entry['actions']=[]
#    for col in decisiontbl['condition_headers']:
#        if not entry.has_key(col[1]) :
#            entry[col[1]]=""

#pydt.process_dt(test_timeEntries[0], decisiontbl)

#for condition in ConditionNames:
#    s = eval("Conditions." + condition +
#    ".ApplyActions(condition,test_timeEntries,test_timeEntries[0],decisiontbl)")
print('exit')