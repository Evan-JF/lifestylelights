from flask import Flask, request
from flask_cors import CORS
import subprocess
import json
import os

app = Flask(__name__)
#CORS(app)

BULB_IPV4 = "192.168.1.177"

@app.route("/")
def default_route():
    print("Bulb status retrieved")
    result = get_bulb_status()
    return result

@app.route("/toggle_bulb")
def toggle_bulb():
    print("Toggling bulb.")
    bulb_status = get_bulb_on_status()

    if bulb_status:
        print("off")
        return run_bulb_command("-f")
    else:
        print("on")
        return run_bulb_command("-o")
    
@app.route("/set_bulb_color")
def set_bulb_color():
    red = request.args.get('red')
    green = request.args.get('green')
    blue = request.args.get('blue')

    print("Setting bulb color.")

    return run_bulb_command(["-c", f'{red},{green},{blue}'])


def get_bulb_status():
    result = run_bulb_command("-i")

    print("Result: ", result)

    return result
    

def get_bulb_on_status():
    result = run_bulb_command("-i")

    data = json.loads(result)

    return data['emitting']

def run_bulb_command(cmd: str):

    args = ['./riz/riz', f'{BULB_IPV4}']

    if type(cmd) == str:
        args.append(cmd)
    else:
        for arg in cmd:
            args.append(arg)

    result = subprocess.run(args, stdout=subprocess.PIPE)

    return result.stdout.decode("utf-8").replace("\\n", "")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(debug=True, host="0.0.0.0", port=port)