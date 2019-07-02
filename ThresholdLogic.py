def ThresholdLogicProcess(entry,tempentry):
    if not (tempentry and tempentry['action'] and tempentry['action']['ThresholdName']):
        return 0
    
    