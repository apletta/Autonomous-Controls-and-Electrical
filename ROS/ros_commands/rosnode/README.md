# ROSNODE

## Links
[General ros.org link](http://wiki.ros.org/rosnode)

---

### List of commands

* `info`
    * Display information abouta  node, including publications and subscriptions
    * **Usage:** `rosnode info <node-name>`
    * **Ex:** `rosnode info /node_name`

* `kill`
    * Stops one or more nodes
    * **Usage:** There are two different uses
       1. `rosnode kill <node-names>`
            * **Ex:** `rosnode kill node_name1 node_name2 node_name3`
       2. `rosnode kill`
            * Will prompt user with a list of nodes to kill and options

* `list`
   * **Usage:** There are two different uses 
       1. `rosnode list`
            * Displays a list of current nodes 
       2. `rosnode list <namespace>`
            * Display a list of current nodes inside /namespace
            * **Ex:** `rosnode list /my_namespace`

* `machine`
    * List nodes running on a particular machine
    * **Usage:** `rosnode machine <machine_name>`
    * **Ex:** `rosnode machine ninja.local`

* `ping`
    * Ping a node repeatedly
    * Checking if node is active
    * **Usage:** `rosnode ping <node-name>`
    * **Ex:** `rosnode ping /node_name`

* `cleanup`
    * **NOT RECOMMENDED**
    * Purge the registration of any node taht cannot be contacted immediately
    * **Usage:** `rosnode cleanup`

### Acquired knowledge

| Date Added | Note |
| --- | --- |
| 5-18-19 | This is an example |
