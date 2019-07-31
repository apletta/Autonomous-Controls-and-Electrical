# ROSBAG

## Links
[Main ros.org link](http://wiki.ros.org/rosbag)

[More helpful link for commands](http://wiki.ros.org/rosbag/Commandline)

---

This directory is intended to help with the ros command "rosbag."

### List of commands
* `record`
    * Record a bag file with the contents of specific topics
    * **Usage:** `rosbag record <topic names>`
    * **Ex:** `rosbog record topic1 topic2 topic3`

* `info`
    * Summarize the contents of a bag file
    * **Usage:** `rosbag info <bag files>`
    * **Ex:** `rosbag info example.bag`

* `play`
    * Play back the contents of one or more bag files
    * **Usage:** `rosbag play <bag files>`
    * **Ex:** `rosbag play example.bag`

* `check`
    * Determine whether a bag is playable in the current system, or if it can be migrated
    * Is helpful if determining if bag is allowed to play using a messages that are available
    * **Usage:** `rosbag check <bag file>`
    * **Ex:** `rosbag check example.bag`

* `fix`
    * Repair the messages in a bag file so that it can be played in the current system
    * **Usage:** `rosbag fix <in bag> <out bag> [rules file]`
    * **Ex:** `rosbag fix example.bag output.bag myrules.bmr`

* `filter`
    * Convert a bag file using Python expressions
    * **Usage:** `rosbag <in bag> <out bag> <expression>`
    * **Ex:** `example.bag output.bag "t.to_sec() <= 1284703931.86"`
        * Example filters out all parts of the bag greater than the specified time

* `compress`
    * Compress one or more bag files
    * **Usage:** `rosbag compress <bag files>`
    * **Ex:** `rosbag compress example.bag` 
    
* `decompress`
    * Decompress one or more bag files
    * **Usage:** `rosbag decompress <bag files>`
    * **Ex:** `rosbag decompress example.bag`

* `reindex`
    * Reindex one or more broken bag files
    * Primarily for bag files that were recorded in earlier versions of ros
    * **Usage:** `rosbag reindex <bag files>`
    * **Ex:** `rosbag reindex example.bag`

### Acquired knowledge

| Date Added | Note |
| --- | ---|
| 5-18-19 | This is an example |
