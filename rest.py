from pymongo import MongoClient
from flask import Flask
from docker import Client 

cli = Client(base_url='unix://var/run/docker.sock')
monCli = MongoClient('mongodb://localhost:27017/')
jobDB = monCli['job']

app = Flask(__name__)

@app.route("/ping")
def ping():
    msg = ""
    jobCollection = jobDB.job
    jobData = jobCollection.find_one({ "$query":{}, "$orderby":{'createAt':-1} })

    if jobData != None:
        msg = runContainer(jobData)
    if msg != "":
        return "python server received 'ping' request!"
    else:
        assert "raise error, msg is empty string."
        pass

def runContainer(jobData):
    container = cli.create_container(image=jobData['image'])
    #FIXME update job status
    print(container)
    return "Done"

if __name__ == "__main__":
    app.run(debug=True)

