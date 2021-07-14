##*===============================================
##* INFORMATION
##*===============================================
# Script Version = 1.0.0
# Script Date = 7/13/2021
# Script Author = Joe Aguirre
# Description = Osquery deployment script
##*===============================================

from utils import LogHandler, osquery_install, service_check, email, osquery_uninstall, intrustionapp_uninstall, intrustionapp_install
import logging
import os
import getpass

# Logging
log_handle = LogHandler().logger # delete 'utils.' and unedit utils import line for packaging
log = logging.LoggerAdapter(log_handle, {})

# Only for testing! Leverage a secrets vault (ie AWS SecretsManager)!
os.environ['EMAIL_PASS']=getpass.getpass("Enter your e-mail password\n")

# Current Directory
dir_path = os.path.dirname(os.path.realpath(__file__))

# Uninstalls old installs to start fresh
log.info(f"Uninstalling Osquery (If Needed)...")
osquery_uninstall()
log.info(f"Uninstalling Intrusion Detection App (If Needed)...")
intrustionapp_uninstall()

# Downloads, Installs, Configures, & Validates osquery
log.info(f"Installing Osquery...")
osquery_install("4.9.0")

# NOTE: Sending notifs by e-mail is NOT a scalable option. This needs to go into Splunk Forwarder or at least AWS API Gateway
# Launchctl Osqueryd Service Smoke Test
if not service_check("com.datadog.osqueryd"):
    log.error("Osqueryd service was not found! Sending e-mail notification.")
    email(sender="????????@gmail.com", receiver="????????@intuit.com", password=os.environ['EMAIL_PASS'], smtp_server="smtp.gmail.com", port=465, subject="ERROR: osqueryd service was not found!")

# Deploys Intrusion Detection app
log.info(f"Deploying Intrusion Detection app...")
intrustionapp_install()

# NOTE: Sending notifs by e-mail is NOT a scalable option. This needs to go into Splunk Forwarder or at least AWS API Gateway
# Launchctl Intrusion Detection Service Smoke Test
if not service_check("com.datadog.intrusiondetection"):
    log.error("Intrusion Detection service was not found! Sending e-mail notification.")
    email(sender="????????@gmail.com", receiver="????????@intuit.com", password=os.environ['EMAIL_PASS'], smtp_server="smtp.gmail.com", port=465, subject="ERROR: Intrusion Detection service was not found!")