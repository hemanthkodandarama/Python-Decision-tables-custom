import json

supportedActionTypes = ['Threshold','Aggregation','ConsecutiveDay']

def GetHoursRange(metadata):
    return metadata['HoursRange'][0],metadata['HoursRange'][1] if len(metadata['HoursRange']) == 2 else None

def GetPayHours(timeentry,fromRange,toRange):
    payhours = (timeentry['TimeEntryHours'] - fromRange)
    if toRange != None:
        payhours = (toRange - fromRange) if timeentry['TimeEntryHours'] >= toRange else timeentry['TimeEntryHours']
    return payhours

def ApplyActions(conditionName,alltimeEntries,timeentry,decisiontbl):
    if not (timeentry and timeentry['actions']):
        return
    
    for action in timeentry['actions']:
        if not action.has_key('MetaData'):
            continue
        metadata = json.loads("{ %s }" % (action['MetaData']))
        if not metadata['Type'] in supportedActionTypes:
            continue

        cmd = 'Apply%sAction(action,metadata,conditionName,alltimeEntries,timeentry,decisiontbl)' % (metadata['Type'])
        canexit = eval(cmd)
        if canexit:
            return

def ApplyThresholdAction(action,metadata,conditionName,alltimeEntries,timeentry,decisiontbl):
    fromRange,toRange = GetHoursRange(metadata)
    payhours = GetPayHours(timeentry,fromRange,toRange)
    action['PayHours'] = action['PayHours'] + payhours if action.has_key('PayHours') else payhours

def ApplyAggregationAction(aggregateaction,metadata,conditionName,alltimeEntries,timeentry,decisiontbl):
    fromRange,toRange = GetHoursRange(metadata)
    rtpaycode = metadata['RTPayCode']
    dayNumber = metadata['Days']
    totalrthours = GetTotalPayHours(alltimeEntries,rtpaycode,timeentry,dayNumber)
    diffrtHours = (totalrthours - fromRange) if totalrthours > fromRange else 0
    if diffrtHours > 0:
        for action in timeentry['actions']:
            if not (action.has_key('MetaData') and action.has_key('PayHours') \
                        and action.has_key('PayCode') and action['PayCode'] == rtpaycode):
                continue
            diffHoursToUpdate = action['PayHours'] - diffrtHours if action['PayHours'] >= diffrtHours else action['PayHours']
            hrstodeduct = action['PayHours'] - diffHoursToUpdate
            diffrtHours -= hrstodeduct
            action['PayHours'] = diffHoursToUpdate
            aggregateaction['PayHours'] = aggregateaction['PayHours'] + hrstodeduct if aggregateaction.has_key('PayHours') else hrstodeduct
            if diffrtHours == 0:
                return

def ApplyConsecutiveDayAction(action,metadata,conditionName,alltimeEntries,timeentry,decisiontbl):
    isconsecutiveDay = True
    for entry in alltimeEntries:
        isconsecutiveDay = False if entry['TimeEntryHours'] == 0 else isconsecutiveDay

    if isconsecutiveDay and (alltimeEntries.index(timeentry) + 1) == metadata['DayNumber']:
       fromRange,toRange = GetHoursRange(metadata)
       payhours = GetPayHours(timeentry,fromRange,toRange)
       action['PayHours'] = action['PayHours'] + payhours if action.has_key('PayHours') else payhours
       if entry['TimeEntryHours'] <= toRange or toRange is None:
           return True

def GetTotalPayHours(alltimeEntries,paycode,currenttimeentry,dayNumber):
    totalHours = 0
    for timeentry in alltimeEntries:
        if alltimeEntries.index(timeentry) >= dayNumber:
            continue
        for action in timeentry['actions']:
            if not action.has_key('MetaData'):
                continue
            metadata = json.loads("{ %s }" % (action['MetaData']))
            totalHours += action['PayHours'] if action.has_key('PayHours') and action['PayCode'] == paycode else 0 
    
    return totalHours
         
        
