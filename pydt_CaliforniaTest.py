import pydt
import numpy as np
import Util

decisiontbl = pydt.load_xls("California-DecisionTable.xls")
test_timeEntries = pydt.load_xls_list_dict("California-TimeEntries.xls")

pydt.MapTimeAndDecisionData(test_timeEntries,decisiontbl)

paycodes = map(lambda x: x,np.unique(map(lambda x: x[5] , decisiontbl["data"])))
ConditionNames = pydt.GetUniqueConditionsNames(decisiontbl)

for entry in test_timeEntries:
    pydt.ProcessTimeEntry(ConditionNames,test_timeEntries,entry,decisiontbl)

printdata = Util.MapActionPayData(test_timeEntries,paycodes)
print(printdata)