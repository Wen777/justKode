DockerJobs = new Mongo.Collection("job");

if (Meteor.isClient) {
  // counter starts at 0
  Meteor.subscribe("jobs");

  Template.hello.helpers({
    counter: function () {
      return DockerJobs.find().count();
    }
  });

  Template.hello.events({
    'click button': function () {
      Meteor.call("runContainer");
    }
  });
}

if (Meteor.isServer) {
  Meteor.startup(function () {
    // code to run on server at startup
  });
  Meteor.publish("jobs", function () {
    return DockerJobs.find();
  })

  Meteor.methods({
  
  runContainer: function () {
    job = DockerJobs.insert({command: "run", image: "c3h3/ipython:agilearning"});
    if (job) {
      HTTP.get("http://127.0.0.1:5000/ping")
    }
  }

  });
}
