import requests   # version 2.28.0


def test_signup():
    user_dict = {
        'login': 'login',
        'email': 'email@mail.ru',
        'name': 'name',
        'password': 'password'
    }
    req = requests.post('http://0.0.0.0:5000/signup', user_dict)
    return req.status_code, req.text


def test_login():
    user_dict = {
        'login': 'login',
        'password': 'password'
    }
    req = requests.post('http://0.0.0.0:5000/login', user_dict)
    return req.status_code, req.json()


def test_refresh(refresh_token):
    headers = {
        'Authorization': 'Bearer ' + refresh_token
    }
    req = requests.post('http://0.0.0.0:5000/refresh', headers=headers)
    return req.status_code, req.json()


def test_info(access_token):
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    req = requests.get('http://0.0.0.0:5000/info', headers=headers)
    return req.status_code, req.json()


if __name__ == '__main__':
    print(test_signup())
    code, jwt = test_login()
    print(code)
    print(jwt['access_token'])
    print(jwt['refresh_token'])

    code, jwt = test_refresh(jwt['refresh_token'])
    print('test_refresh', code, jwt)

    access_token = jwt['access_token']
    refresh_token = jwt['refresh_token']
    code, info = test_info(jwt['access_token'])
    print('test_info', code, info)
