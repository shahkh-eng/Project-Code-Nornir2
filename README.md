# Project-Code-Nornir2

A Python network automation tool built with **Nornir 3**, **NAPALM**, and **OpenPyXL** to concurrently collect structured device facts, interface status, and IP addressing from Cisco IOS routers and export the parsed results into a formatted multi-sheet Excel workbook (`.xlsx`).

> **Note:** These scripts and lab configurations are intended for learning, testing, and lab validation (such as GNS3 or Cisco DevNet Sandboxes). Review and harden security settings before running in a production environment.

---

## Use Case

Network engineers frequently need up-to-date inventory and interface documentation across multiple routers. Manually running `show` commands and copying output into spreadsheets is slow and error-prone.

Using **Nornir** (a pure-Python automation framework with multithreaded execution) and **NAPALM** (a vendor-neutral abstraction layer), this project:
- Connects concurrently to multiple Cisco IOS devices (`R1`–`R5`) over SSH.
- Executes structured NAPALM getters (`facts`, `interfaces`, `interfaces_ip` by default, or custom getters via CLI).
- Handles unreachable or failed hosts gracefully without crashing the run.
- Exports clean, styled tables into an Excel report (`.xlsx`) in the project directory.

---

## Technology Stack

- **Python:** 3.10+
- **Automation Framework:** Nornir (`2.5.x`)
- **Device Abstraction:** NAPALM (`5.2.x`) & `nornir-napalm` (`0.6.x`)
- **Reporting:** OpenPyXL (`3.1.x`)
- **Configuration & Secrets:** YAML inventory + `.env` / environment variables (`python-dotenv`, `nornir-utils`)

---

## Lab Topology

![GNS3 Lab Topology](GNS3%20Lab%20Topology.jpg)

---

## Prerequisites

1. **Python 3.10 or higher** ([Download Python](https://www.python.org/downloads/)).
2. **Cisco IOS devices** in **GNS3** (or a **Cisco DevNet Sandbox** such as the [DevNet Sandbox Catalog](https://devnetsandbox.cisco.com/)) reachable via SSHv2 with SCP enabled.
   - For Windows + GNS3 communication, configure the **Microsoft KM-TEST Loopback Adapter** (see my [GNS3 GUI/VM Setup Guide](https://www.linkedin.com/pulse/gns3-21-gui-vm-installation-integration-steps-khurram-javed) and [LinkedIn walkthrough](https://www.linkedin.com/posts/kjaved_nornir-networkautomation-napalm-activity-6708690032410075136-hqH1)).

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/shahkh-eng/Project-Code-Nornir2.git
cd Project-Code-Nornir2
```

### 2. Create and activate a virtual environment

**Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install --upgrade pip
```

---

## Configuration

### 1. Review Inventory Files

- `config.yml` — Configures Nornir's `SimpleInventory`, `load_credentials` transform function, and multithreaded runner.
- `hosts.yml` — Defines your target routers (`R1`–`R5`, e.g., `192.168.122.101`–`192.168.122.105`).
- `group.yml` — Defines shared platform (`ios`) and NAPALM connection options.
- `defaults.yml` — Defines global defaults (SSH port `22`).

### 2. Lab Router Setup (GNS3 IOS Example)

1. Configure your loopback adapter / management bridge in the `192.168.122.0/24` subnet (e.g., `192.168.122.100/24`).
2. Configure the management interface on `R1`–`R5` (example for `R1`):

```ios
R1(config)# interface ethernet 2/0
R1(config-if)# ip address 192.168.122.101 255.255.255.0
R1(config-if)# no shutdown
```

3. Enable SSHv2 and SCP (required by NAPALM IOS driver) on `R1`–`R5`:

```ios
hostname R1
ip domain-name python.com
crypto key generate rsa modulus 1024
enable secret cisco
username gnslab privilege 15 secret cisco
ip scp server enable
line vty 0 4
 login local
 transport input ssh
exit
```

4. Verify connectivity by pinging and SSHing to `192.168.122.101` from your terminal before running the script.

---

## Usage

Run the script with default settings (`facts`, `interfaces`, `interfaces_ip`):

```bash
python nornir_script.py
```

View all available CLI options:

```bash
python nornir_script.py --help
```

### Examples

Specify a custom Excel output filename and NAPALM getters:

```bash
python nornir_script.py --getters facts interfaces interfaces_ip --output network_inventory.xlsx
```

Filter to a specific host or enable verbose Nornir output:

```bash
python nornir_script.py --host R1 --verbose
```

Non-interactive mode (requires `NORNIR_USERNAME` and `NORNIR_PASSWORD` to be set in environment or `.env`):

```bash
python nornir_script.py --non-interactive
```

---

## Output

The script displays task execution results in the console and saves an Excel workbook (default: `nornir_napalm_report_<timestamp>.xlsx`) containing:
- **Summary:** Host reachability, vendor, model, OS version, serial number, uptime, and any error details.
- **Interfaces:** Interface status (`enabled` / `is_up`), MAC address, speed, MTU, and descriptions.
- **Interfaces_IP:** Layer 3 IPv4/IPv6 addresses and prefix lengths per interface.
- **Extra_Getters:** JSON-formatted output if additional getters (e.g., `arp_table`, `bgp_neighbors`) are requested.

---

## Known Issues & Troubleshooting

- **SSH Legacy Algorithms on Older IOS Images:** If connecting to older GNS3 Cisco IOS images fails with Paramiko key-exchange errors, check your host SSH client settings or adjust `optional_args` in `group.yml`.
- **SCP Required:** NAPALM uses SCP for certain Cisco IOS operations; ensure `ip scp server enable` is configured on each router.

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## References

- [Nornir Documentation](https://nornir.readthedocs.io/en/stable/)
- [NAPALM Documentation](https://napalm.readthedocs.io/en/latest/)
- [Cisco DevNet Sandbox](https://devnetsandbox.cisco.com/)
- Book: *Python Network Programming* by Abhishek Ratan, Eric Chou, Pradeeban Kathiravelu
- Book: *Network Programmability and Automation* by Jason Edelman, Scott S. Lowe, and Matt Oswalt
- [Nornir Tutorial — Kirk Byers](https://pynet.twb-tech.com/blog/nornir/intro.html)
- [Nornir Video Overview](https://www.youtube.com/watch?v=w9X-jzTweek)
