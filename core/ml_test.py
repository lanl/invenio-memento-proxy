__author__ = 'Yorick Chollet'

def application(env, start_response):
    """
    WSGI application object. This is the start point of the server. Timegate /
    TimeMap requests are parsed here.
    :param env: Dictionary containing environment variables from the client request
    :param start_response: Callback function used to send HTTP status and headers to the server.
    :return: The response body, in a list of one str element.
    """

    # Extracting HTTP request values

    req_path = env.get('REQUEST_URI', '/')
    print req_path

    BASE = '/Users/r297174/Documents/polymer_project'

    tot = BASE+req_path

    length = '0'
    status = '404'
    dat = []
    try:
        with open(tot) as f:
            dat = [f.read()]
            length = str(len(dat[0]))
            status = '200'
            # print dat
            # print length

    except Exception as e:
        print e

    headers = [
        ('Content-Length', length),
        ('Connection', 'close')
    ]
    start_response(status, headers)
    return dat