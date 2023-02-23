## Osquery
The purpose of these scripts is to leverage osquery to detect the presence of a persistent attacker on MacOS environment.
The scripts do the following:
* Deploy a specific version of osquery
* Ensure osquery is always running
* Check the configuration integrity of osquery
* Send an email if the osquery configuration is incorrect
* Fix the osquery configuration if incorrect
* Create an osquery configuration that will detect the presence of a persistent attacker
* Send an email if a persistent attacker is detected

| Link | Purpose |
|---|---|
| [Osquery Docs](https://osquery.readthedocs.io/en/stable/) | Documentation for Osquery |
| [Osquery GitHub](https://github.com/osquery/osquery)  | GitHub for Osquery  |
| [Osquery Schema](https://osquery.io/schema/4.9.0/)  | SQL Schema for Osquery |

# How to Use
NOTE: Before using this, please change the e-mail address from `joeaguirre0@gmail.com` and `joe_aguirre@company.com` to two correct e-mail addresses in the following files:
* `intrustiondetection.py`: Line 38
* `utils.py`: Line 165
* `osquery.py`: Line 39 & 49

__Also change the same files abobe in both `osquery.app` and `intrustiondetection.app` as well!__

1. Unzip `osquery.zip` and `intrusiondetection.zip`
2. Run `osquery.app/Contents/MacOS/osquery` script as it will ask you for your e-mail & sudo password
    - Ideally you would want to utilize a safe secrets manager or JAMF for both your e-mail password & JAMF can run sudo
3. That's it! 

# Deployment Scope
Targets all physical Mac endpoints. The python script is capable of handling end-to-end deployment, including uninstallation if required. Ideally however, JAMF would be leveraged to build a PKG/DMG and handle policy deployments

# Configuration
NOTE: Before using this, please change the e-mail address from `????????@gmail.com` and `????????@company.com` to two correct e-mail addresses in the following files:
* `intrustiondetection.py`: Line 38
* `utils.py`: Line 165
* `osquery.py`: Line 39 & 49

__Also change the same files abobe in both `osquery.app` and `intrustiondetection.app` as well!__

The following configuration is modifiable and located within [Datadog.conf](config/datadog.conf). 

**NOTE: Any changes made to `datadog.conf` would be reflected in production, as `utils.py` pulls the configuration.**

## Datadog.conf
Security Specific
* "new_process_listeners": "List new processes listening in on network ports"
* "suspicious_outbound": "List suspicious outbound processes with IP traffic to ports not in (80, 443)"
* "suspicious_deletions": "List running processes whose binaries have been suspiciously deleted"
* "etc_hosts": "List the contents of /etc/hosts"
* "event_taps": "Returns information about installed event taps. Can be used to detect keyloggers"
* "ip_forwarding_enabled": "Discover hosts that have IP forwarding enabled"

Generic OS Data
* "last": "System logins and logouts"
* "network_interfaces_snapshot": "Retrieve the interface name, IP address, and MAC address for all interfaces on the host."
* "os_version": "List the version of the resident operating system"
* "osquery_info": "Information about the resident osquery process"
* "platform_info": "Information about EFI/UEFI/ROM and platform/boot."
* "users": "Local system users."

Packs
* "osx-attacks": "/var/osquery/packs/osx-attacks.conf",
* "incident-response": "/var/osquery/packs/incident-response.conf",
* "unwanted-chrome-extensions": "/var/osquery/packs/unwanted-chrome-extensions.conf"

# Development Setup 
1. Install Apple Xcode Command Line Tools via Terminal.
    - `xcode-select --install`
2. Install Brew (Mac-specific Package Manager).
    - `/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`
    - `brew cleanup`
3. Install Pyenv (Python Version Manager).
    - `brew install pyenv`
4. Install Python 3.9.4 with shared framework enabled (required for PyInstaller).
    - `env PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install 3.9.4`
5. Activate Py3.9.4 shell (Verify you're on py3.9.4 via `python -V`)
    - `eval "$(pyven init -)"`
    - set global by running: pyenv global 3.9.4
6. Install virtualenv (Virtual Environment Manager).
    - `pip install virtualenv`
7. Create your virtual environment (Be sure to `cd` to the correct path you want it in, if not enter full path).
    - `python -m venv <my_env_name>`
8. Initialize your virtual environment (Verify you're in via `which python`).
    - `source <my_env_name>/bin/activate`
9.  Install requirements (`requirements.txt`).
    - `pip install -r requirements.txt`
10. Install latest version of `py2app`.
    - `pip install py2app`
11. Package your python apps with py2app within your venv.
    - `python setup.py py2app` for the main `osquery.app` deployment
    - `python intrusion_setup.py py2app` for the Intrusion Detection `intrusiondetection.app` app
12. This creates a `dist` folder which contains your `osquery.app`. This app contains all required libraries, including a virtualized python. You would want to test the `osquery.app` by double clicking it and running it. If you have issues, try running the `osquery` shell script, path: `osquery.app/Contents/MacOS/osquery`, within the `osquery.app` itself to get a console output and see any error. You can now modify the original scripts under `osquery.app/Contents/MacOS/Resources` to retrofit the app.

