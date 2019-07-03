import pydt
import numpy as np

decisiontbl = pydt.load_xls("California-DecisionTable.xls")
ConditionNames = pydt.GetUniqueConditionsNames(decisiontbl)
test_timeEntries = pydt.load_xls_list_dict("California-TimeEntries.xls")
pydt.MapTimeAndDecisionData(test_timeEntries,decisiontbl)

paycodes = map(lambda x: x,np.unique(map(lambda x: x[5] , decisiontbl["data"])))

#pydt.ProcessTimeEntry(ConditionNames,test_timeEntries,test_timeEntries[5],decisiontbl)
for entry in test_timeEntries:
    pydt.ProcessTimeEntry(ConditionNames,test_timeEntries,entry,decisiontbl)

def GetPayDetails(timeentry):
    data = ','
    for paycode in paycodes:
        data += ' %s = %s ,' %( paycode ,(str(timeentry[paycode])  if timeentry.has_key(paycode) else '0'))
    return data;

for timeentry in test_timeEntries:
    for action in timeentry['actions']:
        if not (action.has_key('MetaData') and action.has_key('PayHours') \
                        and action.has_key('PayCode') and action['PayHours'] >0):
                continue
        if not timeentry.has_key(action['PayCode']):
            timeentry[action['PayCode']]=0

        timeentry[action['PayCode']] += action['PayHours'] 
    print(' %s - %s - %s  ==  %s ' % ( timeentry['DayNumber'],timeentry['Date'],timeentry['TimeEntryHours'] , GetPayDetails(timeentry)))
