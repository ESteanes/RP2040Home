# mqtt-home
A simple micro-python mqtt client which enables simple plug-and-play functionality and interoperability with Home Assistant. 
```  
"availability_topic": "home/wateringsystem/back/status",
"state_topic": "home/wateringsystem/back/output/solenoid3",
"command_topic": "home/wateringsystem/back/output/solenoid3/set",
```

The overall standard of MQTT topics that will be used going forward is:
`<area>/<entity>/<location>/<property>/<object>/<modifier>` but there's no set requirement on structure.

topic_prefix is: `<area>/<entity>/<location>`

This simplifies it down to:
`<topic_prefix>/<property>/<object>/<modifier>`