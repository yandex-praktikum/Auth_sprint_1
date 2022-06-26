from flask import Flask, request

app = Flask(__name__)

some_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title></title>
</head>
<body>
<p>Вы искали: {}</p>
<form method="get" action="/">
<input name="query">
</form>
</body>
</html>

'''


@app.route("/")
def main():
    return some_template.format(request.args.get('query', default=''))


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
    )
