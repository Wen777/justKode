from pymongo import MongoClient
from flask import Flask
from docker import Client 
import json

cli = Client(base_url='unix://var/run/docker.sock')
monCli = MongoClient('mongodb://localhost:27017/')
db_rest = monCli['rest']
db_meteor = monCli['meteor']
freeports = set(range(8000,9001))
app = Flask(__name__)

@app.route("/ping")
def ping():
    msg = ""
    jobData = db.job.find_one({ "$query":{}, "$orderby":{'createAt':-1} })

    if jobData:
        msg = runContainer(jobData)
    if msg:
        db.job.update({"_id":jobData["_id"]},{"$set":{"command":"done"}})
        return json.dumps(msg)
    else:
        assert "raise error, msg is empty dict."
        return msg

def run_container(jobData):
    container = cli.create_container(image=jobData['image'])
    if container:
        return container
    else:
        return {"error":"error"}

def port_sync():
    allContainer = cli.continaers()
    usedPorts = sum(list(map(lambda x: x['Ports'], allContainer)), [])
    freeports.difference_update(usedPorts)

if __name__ == "__main__":
    app.run(debug=True)
    portSync()

