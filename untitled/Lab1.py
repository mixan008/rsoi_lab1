from flask import Flask, redirect, request, render_template
import requests

app = Flask(__name__)

CLIENT_ID = "d762b3ed16ef51c2f258656d5c0fc88c"
CLIENT_SECRET = "ce8af9a23f706dfb6d818c6bd7dd722c"
REDIRECT_CODE_URL = "http://localhost:27005/codeflow/auth"
AUTH_URL = "https://soundcloud.com/connect"
TOKEN_URL = "https://api.soundcloud.com/oauth2/token"


TOKEN = ''


@app.route("/")
def hello():
    return "Welcome to Simple RuCenter client!"


# -----------------------------------------------------------
# ------------ WebServer Version: Code Flow -----------------
# -----------------------------------------------------------

@app.route("/codeflow/index")
def index():
    global TOKEN

    headers = {"Authorization": "Bearer " + TOKEN}
    resp = requests.get("", headers=headers)
    j = resp.json()
    keys = j.keys();
    if 'error' in keys:
        return "ERROR: " + j['error'];
    if not 'contents' in keys:
        return "ERROR: Undefined Error!"
    files = j['contents']
    return render_template('filesView.html', files=files, filesNum=len(files))


@app.route("/codeflow/auth")
def auth():
    global TOKEN
    code = request.args.get('code', '')
    if not code:
        return redirect(create_auth_url('code', REDIRECT_CODE_URL))
    resp = requests.post(create_token_url(code, REDIRECT_CODE_URL))
    j = resp.json()
    keys = j.keys()
    if 'error_description' in keys:
        return j['error_description']
    if not 'access_token' in keys:
        return 'Undefined Error!'
    TOKEN = j['access_token']
    return redirect('/codeflow/index')


def create_auth_url(resptype, redirecturi):
    return AUTH_URL + "?response_type=" + resptype + "&client_id=" + CLIENT_ID + "&redirect_uri=" + redirecturi


def create_token_url(code, redirectUri):
    return TOKEN_URL + "?code=" + code + "&grant_type=authorization_code&client_id=" + CLIENT_ID + "&client_secret=" + CLIENT_SECRET + "&redirect_uri=" + redirectUri


if __name__ == "__main__":
    app.run(debug=True, port=27005)
