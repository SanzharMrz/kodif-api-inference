from constants import TRIGGER_SENTENCES

def parse_text(input_text):
    """_summary_
    Args:
        parsed_list (_type_): _description_
    Returns:
        _type_: _description_
    """
    parsed_list = input_text.split('\n\n')
    
    filtered_list = []
    flags_count = 0
    for row in parsed_list:
        if len(row) <= 2: 
            flags_count += 0.25
            continue
        flags = sum([trigger in row or row in trigger for trigger in TRIGGER_SENTENCES])
        flags_count += flags
        if flags_count > 2: break
        if flags and len(row) <= 20: break
        if len(row) > 1 and row in TRIGGER_SENTENCES: continue
        filtered_list.append(row)
    return ' '.join(filtered_list)
