#this is PyDT - Python Decision Tables
# (c) 2007 Michael Neale (michael@michaelneale.net)
# Use entirely at your own risk !
# Licenced under LGPL unless stated otherwise

from Util import Between

#this is the actual "engine" if you can call it that.
def process_dt(fact, table) :
	def make_header(hdr) :
	    splut = hdr[1].split(' ')
	    if len(splut) > 1 :
	    #if hdr[1].contains(' ') :
	        #itms = hdr[1].split(' ')
	        return [hdr[0], fact[splut[0]] + ' ' + splut[1]]
	    else :
	        ######- to check hemanth return [hdr[0], fact[hdr[1]]]
	        return [hdr[0], fact[hdr[1]]]
	#calc the headers
	headers = map(make_header, table['condition_headers'])
	#lets try a map based approach
	####eval_table_index = -1
	def eval_table(row) :
	    ###global eval_table_index
	    ###eval_table_index += 1
	    #go through all the conditions, evaluating
	    def check_condition(condition) :
	    #for condition in headers :

	        col_index = condition[0]
	        if not row.has_key(col_index) :
	            return False
	        if not condition[1] :
	            return False
	        value = row[col_index]
	        # condtions added to check test -- HEmanth
	        value = value if bool(value) else  "== True"
            #6.0Between({value},0,8)

	        predicate = (str(condition[1]) if str(value).find('{value}') == -1 else '')  + str(value).replace('{value}',str(condition[1]))
	        return not eval(predicate)
	    size = len(filter(check_condition,headers))
	    if size == 0 :
	        #for action in table['action_headers'] :
	        def apply_actions(action) :
	            col_label = action[0]
	            if (row.has_key(col_label)) :
	                #fact[action[1]] = row[col_label]
	                if len(fact['actions']) != (table['data'].index(row)):
	                    fact['actions'].append({})
	                factaction=fact['actions'][table['data'].index(row)-1]
                    ##table['data'].index(row)
	                #fact['action'][action[1]] = row[col_label]
	                factaction[action[1]] = row[col_label]
	        map(apply_actions, table['action_headers'])
	map(eval_table, table['data'])




# Load a XLS into a decision table structure for processing
def load_xls(file_name) :
	import xlrd
	book = xlrd.open_workbook(file_name)
	sh = book.sheet_by_index(0)	
        condition_headers, action_headers, data = [],[],[]
	for rx in range(sh.nrows):
		if rx == 0 :		
			divider = 0
			for cx in range(sh.ncols):
				cv = sh.cell_value(rowx=rx, colx=cx)				
				if cv == "" : 
					continue
				if cv == "*" or cv == 'actions:' :
					divider = cx
				else:
					if divider == 0 : #we are in conditions
						condition_headers.append([cx, cv])
					else: #we are in actions
						action_headers.append([cx, cv])
		else:	
			data_row = {}
			#print condition_headers
			for cx in range(sh.ncols):
				cv = sh.cell_value(rowx=rx, colx=cx)
				if cv != "":
					data_row[cx] = cv
			if len(data_row) > 0 :
				data.append(data_row)
	return {
		"condition_headers" : condition_headers,
		"action_headers" : action_headers,
		"data" : data
		}


def load_xls_list_dict(file_name) :
	import xlrd
    # Open the workbook and select the first worksheet
	wb = xlrd.open_workbook(file_name)
	sh = wb.sheet_by_index(0)
    # List to hold dictionaries
	data_list = []
    # Iterate through each row in worksheet and fetch values into dict
	headers = sh.row_values(0)
	for rownum in range(1, sh.nrows):
		data = {}
		for cols in range(sh.ncols):
		    row_values = sh.row_values(rownum)
		    data[headers[cols]] = row_values[cols]
		data_list.append(data)
	return data_list
