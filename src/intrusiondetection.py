##*===============================================
##* INFORMATION
##*===============================================
# Script Version = 1.0.0
# Script Date = 7/9/2021
# Script Author = Joe Aguirre
# Description = Osquery deployment script
##*===============================================

from utils import LogHandler, osquery_install, service_check, error_email
import logging
import subprocess

# Logging
#log_handle = LogHandler().logger # delete 'utils.' and unedit utils import line for packaging
#log = logging.LoggerAdapter(log_handle, {})

#subprocess.run
#grep "pack_osx-attacks" /var/log/osquery/osqueryd.results.log
import json
log_file = open('/var/log/osquery/osqueryd.results.log', 'r')
import getpass
password=getpass.getpass("Enter your e-mail password\n") # Only for testing; Leverage a secrets vault (ie AWS SecretsManager)
detections = []
for item in log_file:
    if "etc" in item:
        detections.append(item)
    else: 
        detections = False
json_item = json.dumps(detections)
endpoint = (json_item["hostIdentifier"])
print(json_item)
#if detections:
    #error_email(sender="joeaguirre0@gmail.com", receiver="joe_aguirre@intuit.com", password=password, smtp_server="smtp.gmail.com", port=465, subject=f"OSX INTRUSION DETECTED: {endpoint} Attack Occurred")
    #if "pack_osx-attacks" in item:
        #error_email(sender="joeaguirre0@gmail.com", receiver="joe_aguirre@intuit.com", password=password, smtp_server="smtp.gmail.com", port=465, subject="INTRUSION DETECTED: OSX Attack Occurred")