# Common commands

## Links
[General ros.org link](http://wiki.ros.org/ROS/Tutorials/UnderstandingTopics)
---

rostopic commands can be very helpful in analyzing topic messages to make it easier to connect other nodes to them. Common commands are:

To display live messages on topic:

`rostopic echo <topic>`

To display active topics:

`rostopic list`

To display active topics in more detail (see which topics are being published and subscribed to, as well as topic message info)

`rostopic list -v`

To see which nodes are publishing and/or subscribing to a topic:

`rostopic info <topic>`

To see type of message on topic:

`rostopic type <topic>`

To see details of a message type: (this is useful for knowing how to format messages for that topic)

`rosmsg show <message type>`

To publish to a topic from command line:

`rostopic pub <topic> <msg_type> <args>`

Note* there can be many optional arguments between "pub" and "<topic>". For examples, see the ROS wiki link (above)

