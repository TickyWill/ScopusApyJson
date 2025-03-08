"""Useful functions for supporting parsing json response from Scopus API."""

__all__ = ['check_not_none',
           'check_true_to_append',
           'check_true_to_set',
           'get_json_key_value',
          ]

def get_json_key_value(dic, key):
    """Gets the value at key "key" of a hierarchical dict "dic".

    It checks the possible multiple occurences of the key. 
    It returns only the first value in the case of multiple occurences 
    of the key.

    Args:
        dic (dict): The hierarchical dict.
        key (str): The key which value is searched in the dict "dic".
    Returns:
        (str, list or dict): The first value at key "key" in the hierarchical \
        dict "dic" whatever the number of occurences of the key, \
        or None if the dict is empty or if the key is not present.
    """
    value = None
    if dic:
        hit = []
        stack = list(zip(dic.keys(), dic.values()))
        while stack :
            k,v = stack.pop()
            if k==key:
                hit.append(v)
            if isinstance(v, dict):
                stack.extend(list(zip(v.keys(), v.values())))
        if hit:
            value = hit[0]
    return value


def check_not_none(value):
    """Checks if the parameter "value" is not None or not equal to "None".

    Args:
        value (str): The parameter to check.
    Returns:
        (bool): True if value is not None or not equal to "None" (default: False).
   """
    status = False
    if value and value!="None":
        status = True
    return status


def check_true_to_append(dic, key, items_list):
    """Appends to the list "items_list", the value at key "key" of 
    a hierarchical dict "dic" in case the return of the `check_not_none` 
    function is True. 

    Args:
        dic (dict): The hierarchical dict.
        key (str): The key which value is searched in the dict "dic".
        items_list (list): The list to append.
    Returns:
        (list): The list appended with the value at key "key" of a hierarchical \
        dict "dic" (default: unchanged list).
    """
    value = get_json_key_value(dic, key)
    if check_not_none(value):
        items_list.append(value)
    return items_list


def check_true_to_set(dic1, key1, dic2, key2):
    """Sets the value at key "key2" of a dict "dic2" 
    to the value "value" returned by the function `get_json_key_value` 
    applied to the hierarchical dict "dic1" and key "key1" 
    in case the return of the function `check_not_none` 
    applied to value "value" is True. 

    Args:
        dic1 (dict): The hierarchical dict.
        key1 (str): The key which value is searched in the dict "dic1".
        dic2 (dict): The dict to be updated.
        key2 (str): The key at which the dict "dic2" will be updated.
    Returns:
        (dict): The dict "dic2" updated at key "key2" with the value at key \
        "key1" of the hierarchical dict "dic1" (default: unchanged dict "dic2").
    """
    value = get_json_key_value(dic1, key1)
    if check_not_none(value):
        dic2[key2] = value
    return dic2
