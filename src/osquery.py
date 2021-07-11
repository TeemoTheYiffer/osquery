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

# Logging
log_handle = LogHandler().logger # delete 'utils.' and unedit utils import line for packaging
log = logging.LoggerAdapter(log_handle, {})

# Downloads, Installs, Configures, & Validates osquery
osquery_install("4.9.0")

# Launchctl Osqueryd Service Smoke Test
if not service_check("com.datadog.osqueryd"):
    log.error("Osqueryd service was not found! Sending e-mail notification.")
    import getpass
    password=getpass.getpass("Enter your e-mail password\n") # Only for testing; Leverage a secrets vault (ie AWS SecretsManager)
    error_email(sender="joeaguirre0@gmail.com", receiver="joe_aguirre@intuit.com", password=password, smtp_server="smtp.gmail.com", port=465, subject="ERROR: osqueryd service was not found!")