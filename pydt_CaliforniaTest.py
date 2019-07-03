import pydt

decisiontbl = pydt.load_xls("California-DecisionTable.xls")
ConditionNames = pydt.GetUniqueConditionsNames(decisiontbl)
test_timeEntries = pydt.load_xls_list_dict("California-TimeEntries.xls")
pydt.MapTimeAndDecisionData(test_timeEntries,decisiontbl)

#for entry in test_timeEntries:
#    pydt.ProcessTimeEntry(ConditionNames,test_timeEntries,entry,decisiontbl)

pydt.ProcessTimeEntry(ConditionNames,test_timeEntries,test_timeEntries[5],decisiontbl)



    #pydt.process_dt(entry, decisiontbl)

    #for condition in ConditionNames:
    #    cmd = "Conditions.%s.ApplyActions(condition,test_timeEntries,entry,decisiontbl)" % (condition)
    #    eval(cmd)


print('exit')