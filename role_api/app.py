from flask import Flask, request

app = Flask(__name__)

@app.route("/roles", ["GET"])
def get_roles():
    pass

@app.route("/role/{role_id}", ["GET"])
def get_role(role_id):
    pass

@app.route("/role/{role_id}", ["PUT"])
def put_role(role_id):
    pass

@app.route("/role/{role_id}", ["DELETE"])
def delete_role(role_id):
    pass

@app.route("/user/{user_id}", ["GET"])
def get_user_roles(user_id):
    pass

@app.route("/user/{user_id}", ["PUT"])
def add_role_to_user(user_id):
    pass

@app.route("/user/{user_id}", ["DELETE"])
def delete_role_from_user(user_id):
    pass

@app.route("/check", ["POST"])
def check_role(user_id):
    pass

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
    )
