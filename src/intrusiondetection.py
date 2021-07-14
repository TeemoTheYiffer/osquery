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
import os
import getpass
import json

# Logging
log_handle = LogHandler().logger # delete 'utils.' and unedit utils import line for packaging
log = logging.LoggerAdapter(log_handle, {})

# Only for testing! Leverage a secrets vault (ie AWS SecretsManager)!
os.environ['EMAIL_PASS']=getpass.getpass("Enter your e-mail password\n")

log_file = open('/var/log/osquery/osqueryd.results.log', 'r')

log.info(f"Reviewing /var/log/osquery/osqueryd.results.log...")
detections = []
for item in log_file:
    #if "suspicious_outbound" in item: ### For testing purposes
    if "pack_osx-attacks" in item:
        json_item = json.loads(item)
        detections.append(json_item)

# NOTE: Sending notifs by e-mail is NOT a scalable option. This needs to go into Splunk Forwarder or at least AWS API Gateway
if detections:
    log.info(f"Detection found! Sending alert via e-mail.")
    json_detections=json.dumps(detections, indent=4, sort_keys=True)
    endpoint=detections[0]['hostIdentifier']
    email(sender="????????@gmail.com", receiver="????????@intuit.com", password=os.environ['EMAIL_PASS'], smtp_server="smtp.gmail.com", port=465, 
    subject=f"OSX INTRUSION DETECTED: {endpoint}", detection=json_detections)
else:
    log.info(f"No detection found.")