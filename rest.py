from pymongo import MongoClient
from flask import Flask
from docker import Client 
import json

cli = Client(base_url='unix://var/run/docker.sock')
monCli = MongoClient('mongodb://localhost:27017/')
db = monCli['job']

app = Flask(__name__)

@app.route("/ping")
def ping():
    msg = ""
    jobCollection = db.job
    jobData = jobCollection.find_one({ "$query":{}, "$orderby":{'createAt':-1} })

    if jobData:
        msg = runContainer(jobData)
    if msg:
        jobCollection.update({"_id":jobData["_id"]},{"$set":{"command":"done"}})
        return json.dumps(msg)
    else:
        assert "raise error, msg is empty dict."
        return msg

def runContainer(jobData):
    container = cli.create_container(image=jobData['image'])
    if container:
        return container
    else:
        return {"error":"error"}

if __name__ == "__main__":
    app.run(debug=True)

