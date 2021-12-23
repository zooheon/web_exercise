from app import flask_app

# app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=1234, debug=True)
    # flask_app.run(host="127.0.0.1", port=5127)