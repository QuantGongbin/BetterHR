def err_json(type):
    '''

    :param type: 代表错误码
    0    代表返回的数目为0
    1    代表未输入查询字符串
    99   代表输入不符合规定
    :return:
    '''
    if type == 0:
        e = {
            'type':'query',
            'status':'failed',
            'reason':'未查询到相关数据',
            'number':0

        }
        return e
    elif type == 1:
        e = {
            'type': 'query',
            'status': 'failed',
            'reason': '未输入查询字符串',
            'number': 0

        }
        return e
    elif type == 99:
        e = {
            'type': 'query',
            'status': 'failed',
            'reason': '输入不符合规定，请重新查询',
            'number': 0

        }
        return e