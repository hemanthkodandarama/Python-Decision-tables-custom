import json

supportedKeyTypes = ['Aggregation','ConsecutiveDay']

def ApplyActions(conditionName,alltimeEntries,timeentry,decisiontbl):
    if not (timeentry and timeentry['actions']):
        return 0
    
    for action in timeentry['actions']:
        if not action.has_key('MetaData'):
            continue 

        metadata = json.loads("{ %s }" % (action['MetaData']))
        fromRange,toRange = GetHoursRange(metadata)
        if not metadata.has_key('KeyType'):
            payhours = (timeentry['TimeEntryHours'] - fromRange)
            if toRange != None:
                payhours = (toRange - fromRange) if timeentry['TimeEntryHours'] >= toRange else timeentry['TimeEntryHours']
            action['PayHours'] = action['PayHours'] + payhours if action.has_key('PayHours') else payhours
        else:
            if metadata['KeyType'] in supportedKeyTypes:
                cmd = 'Apply%sAction(action,metadata,conditionName,alltimeEntries,timeentry,decisiontbl)' % (metadata['KeyType'])
                eval(cmd)

    

def GetHoursRange(metadata):
    return metadata['HoursRange'][0],metadata['HoursRange'][1] if len(metadata['HoursRange']) == 2 else None

def ApplyAggregationAction(aggregateaction,metadata,conditionName,alltimeEntries,timeentry,decisiontbl):
    fromRange,toRange = GetHoursRange(metadata)
    # to do days logic
    rtpaycode = metadata['RTPayCode']
    totalrthours = GetTotalPayHours(alltimeEntries,rtpaycode)
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
    fromRange,toRange = GetHoursRange(metadata)
    isconsecutiveDay = True
    for entry in alltimeEntries:
        isconsecutiveDay = False if entry['TimeEntryHours'] == 0 else isconsecutiveDay

    if isconsecutiveDay:
        action['PayHours'] = timeentry['TimeEntryHours']
        for otheraction in timeentry['actions']:
            if otheraction == action:
                continue
            otheraction['PayHours'] = 0

def GetTotalPayHours(alltimeEntries,paycode):
    totalHours = 0
    for timeentry in alltimeEntries:
        for action in timeentry['actions']:
            if not action.has_key('MetaData'):
                continue
            metadata = json.loads("{ %s }" % (action['MetaData']))
            totalHours += action['PayHours'] if action.has_key('PayHours') and action['PayCode'] == paycode else 0 
    
    return totalHours
         
        
