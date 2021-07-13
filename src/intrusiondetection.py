##*===============================================
##* INFORMATION
##*===============================================
# Script Version = 1.0.0
# Script Date = 7/9/2021
# Script Author = Joe Aguirre
# Description = Osquery OSX Intrustion Detection script
##*===============================================

from utils import LogHandler, email
import logging

# Logging
log_handle = LogHandler().logger # delete 'utils.' and unedit utils import line for packaging
log = logging.LoggerAdapter(log_handle, {})

import json
log_file = open('/var/log/osquery/osqueryd.results.log', 'r')

detections = []
for item in log_file:
    #if "suspicious_outbound" in item: ### For testing purposes
    if "pack_osx-attacks" in item:
        json_item = json.loads(item)
        detections.append(json_item)

if detections:
    import getpass
    password=getpass.getpass("Enter your e-mail password\n") # Only for testing; Leverage a secrets vault (ie AWS SecretsManager)

    json_detections=json.dumps(detections, indent=4, sort_keys=True)
    endpoint=detections[0]['hostIdentifier']
    email(sender="joeaguirre0@gmail.com", receiver="joe_aguirre@intuit.com", password=password, smtp_server="smtp.gmail.com", port=465, 
    subject=f"OSX INTRUSION DETECTED: {endpoint}", detection=json_detections)