from main import login

"""
 [{'nm': 'CAM-101', 'cls': 2, 'id': 9925, 'mu': 3, 'uacl': 19327369763},
  {'nm': 'CAM-115', 'cls': 2, 'id': 9931, 'mu': 3, 'uacl': 19327369763},
  {'nm': 'CAM-121', 'cls': 2, 'id': 9919, 'mu': 3, 'uacl': 19327369763}]
"""


def getUnits():
    sdk = login()
    parametersUnit = {
        'spec': {
            'itemsType': 'avl_unit',
            'propName': 'sys_name',
            'propValueMask': '*',
            'sortType': 'sys_name',
        },
        'force': 0,
        'flags': 1,
        'from': 0,
        'to': 0
    }
    units = sdk.core_search_items(parametersUnit)
    return units
