import requests
import cosense

def make_request(method, url, sid, params):
    request_func = getattr(requests, method, None)
    if request_func is None:
        raise TypeError('Unknown method: %s' % (method,))

    headers = {
        'User-Agent': cosense.USER_AGENT
    } 
    cookies = {
        'connect.sid': sid
    }
    if sid is not None:
        result = request_func(url, params=params, headers=headers, cookies=cookies)
    else:
        result = request_func(url, params=params, headers=headers)
    
    return result
