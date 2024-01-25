from threading import Thread
from flask import Flask

app=Flask(__name__)
@app.route
def main():
    return "online"


def run_flask():
    app.run("0.0.0.0","80")


def keep():
    Thread(target=run_flask).start