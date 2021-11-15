from flask import Flask
from flask import request

# We need to impersonate https://2.endpointhealth.duosecurity.com
# Duo Health app does check for a valid certificate here.


app = Flask(__name__)


@app.route("/v1/healthapp/device/health", methods=['OPTIONS', 'GET', 'POST'])
def health():
    print("OH BOY HERE IT COMES!")
    print(request.method)
    print(request.data)
    return "Valid Result!"


def main() -> None:
    app.run(host="localhost", port=443, debug=True, ssl_context='adhoc')

main()
