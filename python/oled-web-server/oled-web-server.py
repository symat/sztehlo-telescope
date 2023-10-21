from flask import Flask, request, abort
from flask import render_template

app = Flask(__name__)

rowNum = 4
colNum = 3
boxNum = rowNum * colNum
initialText = "\nNincs infó...\n"
maxHeight = 3
maxWidth = 30



def messageToLines(message):
    tuncMessage = str(message)[-10 * maxHeight * maxWidth :]
    targetLines = []
    for sourceLine in tuncMessage.splitlines():
        if len(sourceLine) == 0:
            targetLines.append("")
        subStrings = [sourceLine[i:i + maxWidth] for i in range(0, len(sourceLine), maxWidth)]
        targetLines.extend(subStrings)
    return targetLines[- maxHeight :]


   
currentMessageLines = {}
for i in range(boxNum):
    currentMessageLines[i+1] = { "ip": "n/a", "messages": messageToLines(initialText) } 

@app.get("/")
def index():
    oleds = ""
    for id in range(boxNum):
        oleds += render_template('oled.html', id=id+1, initialText="", ip="n/a")
    return render_template("index.html", oleds=oleds)


@app.get("/messages")
def getMessages():
    return currentMessageLines


@app.post("/messages/<id>")
def postMessage(id):
    if not str(id).isdigit():
        abort(400)
    idNum = int(id)
    if idNum < 1 or idNum > boxNum:
        abort(400)
    
    content_type = request.headers.get('Content-Type')
    if content_type != 'application/json':
        abort(400)
    
    json = request.json
    if "ip" not in json and "message" not in json:
        abort(400) 
    currentMessageLines[idNum]["ip"] = json["ip"]
    currentMessageLines[idNum]["messages"].extend(messageToLines(json["message"]))
    currentMessageLines[idNum]["messages"] = currentMessageLines[idNum]["messages"][- maxHeight :]
    return ""



