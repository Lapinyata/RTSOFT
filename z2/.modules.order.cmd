cmd_/home/trickster/driverMark/modules.order := {   echo /home/trickster/driverMark/test.ko; :; } | awk '!x[$$0]++' - > /home/trickster/driverMark/modules.order
