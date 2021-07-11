##*===============================================
##* INFORMATION
##*===============================================
# Script Version = 1.0.0
# Script Date = 7/9/2021
# Script Author = Joe Aguirre
# Description = Utilities script
##*===============================================

import subprocess
import os
from pylogrus import PyLogrus, JsonFormatter
import logging
import platform

class LogHandler:
    """
    Format logging to be easily searchable via Splunk
    """
    logging.setLoggerClass(PyLogrus)
    enabled_fields = [
        ('levelname', 'level'),
        'filename',
        ('funcName', 'func'),
        'lineno',
        'pathname',
        ('asctime', 'timestamp'),
        ('message', 'msg')
    ]
    formatter = JsonFormatter(enabled_fields=enabled_fields, sort_keys=True, datefmt='Z')
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)

    # to lowercase
    formatter.override_level_names(
        {'INFO': 'info', 'DEBUG': 'debug', 'ERROR': 'error', 'CRITICAL': 'fatal', 'WARNING': 'warn', 'WARN': 'warn'})

    def __init__(self, log_level="INFO", logger_name=__name__):
        self.logger = logging.getLogger(logger_name)
        self.logger.addHandler(self.sh)
        self.logger.propagate = False
        self.__setlevel(log_level)

    def __setlevel(self, log_level):
        self.logger.setLevel(log_level)

def error_email(sender, receiver, password, smtp_server, port, subject, error=None):
    import datetime
    import socket
    import getpass
    import smtplib
    import ssl
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    # Gather local device information
    current_date = datetime.datetime.now()
    host_name = socket.gethostname()
    OS = platform.platform()
    logged_user = getpass.getuser()

    # Build e-mail message
    messeage= MIMEMultipart('alternative')
    messeage["Subject"]= subject
    messeage["From"]= sender
    messeage["To"]= receiver
    html = f"""
    <html>
    <body>
        <p>
        Date: {current_date}<br>
        Endpoint: {host_name}<br>
        Operating System: {OS}<br>
        Currently Logged-in User: {logged_user}<br>
        Error (If Applicable): {error}<br>
        </p>
    </body>
    </html>
    """
    messeage.attach(MIMEText(html,"html"))
    context = ssl.create_default_context()

    try:
        print("Sending your email... Please wait...")
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender, password)
            server.sendmail(
                sender,receiver,messeage.as_string()
                )
        print("\n(*) Email sent successfully (*)") 
    except Exception as e:
        log.error(f"Error_Email - Error_Msg={e}")
        raise e

def service_check(service_name):
    """Service existence check for executable and OS."""
    log.info(f"Initiating {service_name} service test")
    try:
        # Checks for service in System domain
        runner = subprocess.run(['launchctl','print',f'system/{service_name}'], capture_output=True, text=True)
        if "state = running" in runner.stdout:
            return True
        else:
            # Checks for service in User domain if not found in System domain
            runner = subprocess.run(['launchctl','print',f'gui/{int(os.geteuid())}/{service_name}'], capture_output=True, text=True)
            if "state = running" in runner.stdout:
                return True
            else:
                log.info(f"{service_name} Error: {runner.stderr}")
                return False
    except Exception as e:
        log.error(f"Process_Check - Mac Error - Error_Msg={e}")
        raise e

def osquery_install(version):
    """Checks Operating System & installs appropiate osquery"""
    OS = platform.platform()
    if "macOS" in OS:
        log.info(f"MacOS Detected - Initiating osquery deployment")
        try:
            # Download version from GitHub
            url = f"https://github.com/osquery/osquery/releases/download/{version}/osquery-{version}.pkg"
            subprocess.run(['curl','-OL', url], capture_output=True, text=True)

            # Install
            subprocess.run(['sudo','installer', '-pkg', f"osquery-{version}.pkg", '-target', '/'], capture_output=True, text=True)

            # Configure
            subprocess.run(['sudo', 'cp', 'datadog.conf', '/var/osquery/osquery.conf'], capture_output=True, text=True)
            subprocess.run(['sudo', 'cp', 'datadog.flags', '/var/osquery/osquery.flags'], capture_output=True, text=True)

            # Smoke test configuration file (just to be sure)
            test = subprocess.run(['osqueryi', '--config_path', '/var/osquery/osquery.conf', '--config_check'], capture_output=True, text=True)
            if test.stderr:
                import getpass
                password=getpass.getpass("Enter your e-mail password\n") # Only for testing; Leverage a secrets vault (ie AWS SecretsManager)
                error_email(sender="joeaguirre0@gmail.com", receiver="joe_aguirre@intuit.com", password=password, smtp_server="smtp.gmail.com", port=465, subject="ERROR: osquery.conf misconfigured!", error=test.stderr)

                # To fix the faulty config file, this downloads a pre-tuned Palantir config file but ideally a Datadog-specific config file should be stored in a GitHub & pulled
                palantir_config = "https://raw.githubusercontent.com/palantir/osquery-configuration/89c2ae5c7fcad242696e6febb16c05abb0375155/Classic/Endpoints/MacOS/osquery.conf"
                subprocess.run(['curl','-o', 'plantir.conf', palantir_config], capture_output=True, text=True)
                subprocess.run(['sudo', 'cp', 'plantir.conf', '/var/osquery/osquery.conf'], capture_output=True, text=True)
                return

            # Load LaunchDaemon
            subprocess.run(['sudo', 'cp', 'com.datadog.osqueryd.plist', '/Library/LaunchDaemons'], capture_output=True, text=True)
            subprocess.run(['sudo', 'launchctl', 'load', '/Library/LaunchDaemons/com.datadog.osqueryd.plist',], capture_output=True, text=True)


        except Exception as e:
            log.error(f"osquery_install - MacOS Error - Error_Msg={e}")
            raise e
        log.info(f"Osquery deployment complete")
    elif "Linux" in OS:
        pass
    else:
        log.error(f"Error - OS not detected")
        return

def osquery_uninstall():
    # Unload and remove LaunchDaemon
    subprocess.run(['sudo', 'launchctl', 'unload', '/Library/LaunchDaemons/com.datadog.osqueryd.plist',], capture_output=True, text=True)
    subprocess.run(['sudo', 'rm', '/Library/LaunchDaemons/com.datadog.osqueryd.plist'], capture_output=True, text=True)

    # Remove files/directories created by osquery installer pkg
    subprocess.run(['sudo', 'rm', '-rf', '/private/var/log/osquery'], capture_output=True, text=True)
    subprocess.run(['sudo', 'rm', '-rf', '/private/var/osquery'], capture_output=True, text=True)
    subprocess.run(['sudo', 'rm', '-rf', '/usr/local/bin/osquery*'], capture_output=True, text=True)
    subprocess.run(['sudo', 'pkgutil', '--forget', 'com.datadog.osquery'], capture_output=True, text=True)

def process_check(process_name):
    """Process existence check for executable and OS."""
    log.info(f"Initiating {process_name} process check")
    try:
        if subprocess.call(['pgrep',f'{process_name}']) == 0:
            return True
        else:
            return False
    except Exception as e:
        log.error(f"Process_Check - Mac Error - Error_Msg={e}")
        raise e

log_handle = LogHandler().logger
log = logging.LoggerAdapter(log_handle, {})