def Between(number,fromnumber,tonumber):
    return number >= fromnumber and number<=tonumber

def GetPayDetails(timeentry,paycodes):
    data = ','
    for paycode in paycodes:
        data += ' %s = %s ,' %( paycode ,(str(timeentry[paycode])  if timeentry.has_key(paycode) else '0'))
    return data;

def MapActionPayData(test_timeEntries,paycodes):
    printData = ''
    for timeentry in test_timeEntries:
        for action in timeentry['actions']:
            if not (action.has_key('MetaData') and action.has_key('PayHours') \
                            and action.has_key('PayCode') and action['PayHours'] >0):
                    continue
            if not timeentry.has_key(action['PayCode']):
                timeentry[action['PayCode']]=0

            timeentry[action['PayCode']] += action['PayHours'] 

        printData+= '\n %s - %s - %s  ==  %s ' % ( timeentry['DayNumber'],timeentry['Date'],timeentry['TimeEntryHours'] , GetPayDetails(timeentry,paycodes))

    return printData