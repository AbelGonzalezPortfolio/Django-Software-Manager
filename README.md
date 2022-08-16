# Project Goal
- Website to facilitate OIT's tasks. Which includes:
  - Windows Device Management.
  - Software Management.
  - Google Accounts Management. 

# Project Design
- [ ] Menu that switches between Device, Software and Google Management pages.
- Device Page:
  - [x] List of AD hostnames.
  - [x] Ip Address
    - [x] Update IP Addresses from admin actions
  - [ ] Ethernet Mac Address
  - [ ] Wi-Fi Mac Address
  - [ ] ~~Logged on user~~
  - [x] Device Status:
    - [x] Network Status.
    - [x] Powershell Status.
    - [x] Firewall setting status.
  - [x] Last refresh date
  - [x] Sort
  - [x] Sync action
  - [ ] Enable/Disable Action
  - [ ] Firewall rule check
- [ ] Device detail page
- Software Page:
  - [x] Software name
  - [x] Version
  - [ ] Publisher
  - [x] Clients
  - [ ] Delete Action
- Google Accounts Management.
  - [ ] Delegate Email from to
  - [ ] Suspend User
  - [ ] Display out of office message


- [ ] get_ip.ps1 replace domain field
- [ ] get_ad_devices.ps1 replace workstations OU field
- [ ] enable_remoting server ip address
- [ ] 

# Bugs
- [ ] Ad_sync should delete in bulk not one by one.