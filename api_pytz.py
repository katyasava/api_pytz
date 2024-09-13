import datetime
import json
import pytz
from wsgiref.simple_server import make_server

def get_time(path):
    tzname = path.strip('/') or 'GMT'
    try:
        tz = pytz.timezone(tzname)
        current_time = datetime.datetime.now(tz).strftime('%H:%M:%S %d.%m.%Y %Z')
        response_body = f'''
            <html>
                <body>
                    {current_time}
                </body>
            </html>
        '''
        headers = [('Content-Type', 'text/html')]
        return response_body, headers, 200
    except pytz.UnknownTimeZoneError:
        return error_messages('Unknown time zone', 400)
    except Exception as e:
        return error_messages(f'Internal server error: {str(e)}', 500)

def post_convert(data, path):
    try:
        date_time_str = data['date']
        source_tzname = data['tz']
        target_tzname = path.strip('/api/v1/convert/')
        
        source_tz = pytz.timezone(source_tzname)
        target_tz = pytz.timezone(target_tzname)
        date_time = datetime.datetime.strptime(date_time_str, '%m.%d.%Y %H:%M:%S').replace(tzinfo=source_tz)
        converted_date_time = date_time.astimezone(target_tz)
        
        headers = [('Content-Type', 'application/json')]
        response_body = json.dumps({'converted_time': converted_date_time.strftime('%H:%M:%S %d.%m.%Y %Z')})
        return response_body, headers, 200
    except (KeyError, ValueError):
        return error_messages('Invalid input data', 400)
    except pytz.UnknownTimeZoneError:
        return error_messages('Unknown time zone', 400)
    except Exception as e:
        return error_messages(f'Internal server error: {str(e)}', 500)

def post_datediff(data, path):
    try:
        first_date_time_str = data['first_date']
        first_tzname = data['first_tz']
        second_date_time_str = data['second_date']
        second_tzname = data['second_tz']
        
        first_tz = pytz.timezone(first_tzname)
        second_tz = pytz.timezone(second_tzname)
        first_date_time = datetime.datetime.strptime(first_date_time_str, '%d.%m.%Y %H:%M:%S').replace(tzinfo=first_tz)
        second_date_time = datetime.datetime.strptime(second_date_time_str, '%I:%M%p %Y-%m-%d').replace(tzinfo=second_tz)
        
        time_difference = (first_date_time - second_date_time).total_seconds()
        headers = [('Content-Type', 'application/json')]
        response_body = json.dumps({'time_difference_seconds': time_difference})
        return response_body, headers, 200
    except (KeyError, ValueError):
        return error_messages('Invalid input data', 400)
    except pytz.UnknownTimeZoneError:
        return error_messages('Unknown time zone', 400)
    except Exception as e:
        return error_messages(f'Internal server error: {str(e)}', 500)

def error_messages(message, status_code):
    headers = [('Content-Type', 'text/html')]
    response_body = f'''
        <html>
            <body>
                <p>Error {status_code}</p>
                <p>{message}</p>
            </body>
        </html>
    '''
    return response_body, headers, status_code

def app(environ, response):
    method = environ['REQUEST_METHOD']
    path = environ['PATH_INFO']
    
    if method == 'GET':
        response_body, headers, status_code = get_time(path)
    elif method == 'POST' and '/api/v1/convert' in path:
        request_body_size = int(environ['CONTENT_LENGTH'])
        request_body = environ['wsgi.input'].read(request_body_size).decode('utf-8')
        data = json.loads(request_body)
        response_body, headers, status_code = post_convert(data, path)
    elif method == 'POST' and path == '/api/v1/datediff':
        request_body_size = int(environ['CONTENT_LENGTH'])
        request_body = environ['wsgi.input'].read(request_body_size).decode('utf-8')
        data = json.loads(request_body)
        response_body, headers, status_code = post_datediff(data, path)
    else:
        response_body, headers, status_code = error_messages('Unknown request', 404)

    response(f'{status_code} {"OK" if status_code == 200 else "ERROR"}', headers)
    return [response_body.encode('utf-8')]

if __name__ == '__main__':
    port_address = 8080
    with make_server('', port_address, app) as httpd:
        print(f"Starting on port: {port_address}")
        httpd.serve_forever()
