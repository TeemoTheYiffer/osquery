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
* Setup a Datadog trial and send osquery logs to Datadog
* Use Datadog to send alerts to Corp IT Security

| Link | Purpose |
|---|---|
| [Osquery Docs](https://osquery.readthedocs.io/en/stable/) | Documentation for Osquery |
| [Osquery GitHub](https://github.com/osquery/osquery)  | GitHub for Osquery  |
| [Osquery Schema](https://osquery.io/schema/4.9.0/)  | SQL Schema for Osquery |
| [Palantir Github](https://github.com/palantir/osquery-configuration/tree/89c2ae5c7fcad242696e6febb16c05abb0375155) | Example Osquery GitHub by Palantir  |

# Deployment Scope
Targets all physical Mac endpoints. The python script is capable of handling end-to-end deployment, including uninstallation if required. Ideally however, JAMF would be leveraged to build a PKG/DMG and handle policy deployments

# Configuration
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
9.  Install requirements (`requirements.txt`) for Intuit API Tool.
    - `pip install -r requirements.txt`
10. Install latest version of `py2app`.
    - `pip install py2app`
11. Package your python app with py2app within your venv.
    - `python setup.py py2app`
12. This creates a `dist` folder which contains your `main.app`. This app contains all required libraries, including a virtualized python. You would want to test the `main.app` by double clicking it and running it. If you have issues, try running the `main` shell script, path: `main.app/Contents/MacOS/main`, within the `main.app` itself to get a console output and see any error.

