def cvt_to_bool(expr: str):
    if expr == 'Yes':
        return True
    elif expr == 'No':
        return False
    else:
        raise Exception('Can not convert expression to bool')