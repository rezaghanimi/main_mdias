
def datetime_to_str(records):
    '''
    处理时间
    :return: 
    '''
    for record in records:
        for key in record:
            if type(record[key]).__name__ in ['datetime', 'date']:
                record[key] = str(record[key])
    return records
