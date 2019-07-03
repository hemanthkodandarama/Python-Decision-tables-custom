import json

supportedKeyTypes = ['Aggregation','ConsecutiveDay']

#name = 'world'
#program ='python'
#print('Hello %s!  This is %s.'%(name,program))
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
                payhours = (toRange - fromRange) if timeentry['TimeEntryHours'] > toRange else timeentry['TimeEntryHours']
            action['PayHours'] = action['PayHours'] + payhours if action.has_key('PayHours') else payhours
        else:
            if metadata['KeyType'] in supportedKeyTypes:
                cmd = 'Apply%sAction(action,metadata,conditionName,alltimeEntries,timeentry,decisiontbl)' % (metadata['KeyType'])
                eval(cmd)
        print('todo')
    

def GetHoursRange(metadata):
    return metadata['HoursRange'][0],metadata['HoursRange'][1] if len(metadata['HoursRange']) == 2 else None

def ApplyAggregationAction(action,metadata,conditionName,alltimeEntries,timeentry,decisiontbl):
    fromRange,toRange = GetHoursRange(metadata)
    # to do days logic
    paycode = metadata['RTPayCode']
    totalrthours = GetTotalPayHours(alltimeEntries,paycode)
    diffrtHours = (totalrthours - fromRange) if totalrthours > fromRange else 0
    if diffrtHours>0:
        for action in timeentry['actions']:
            if not action.has_key('MetaData'):
                continue
            
            
    print('todo')

def GetTotalPayHours(alltimeEntries,paycode):
    totalHours = 0
    for timeentry in alltimeEntries:
        for action in timeentry['actions']:
            if not action.has_key('MetaData'):
                continue
            metadata = json.loads("{ %s }" % (action['MetaData']))
            totalHours += action['PayHours'] if action.has_key('PayHours') and  action['PayCode'] == paycode else 0 
        return totalHours
         
        
