# Project-Code-Nornir
Nornir Project to Connect and extract output based on NAPALM getters and parse output/save in Excel file.

You can check my article on Linkedin for details on how to set up GNS lab and use this script. https://www.linkedin.com/posts/kjaved_nornir-networkautomation-napalm-activity-6708690032410075136-hqH1

Note: Please note that below scripts/libraries or configurations are for learning purposes only, do not use them in production environment.

Introduction:

We will be using network automation framework “Nornir”. First we need to understand what is a framework; a framework gives us a basic structure around which we can write our code in a standardized manner. Frameworks are more application specific e.g. flask or django are python frameworks for developing web applications. Similarly we have Nornir to interact with networking devices and writing automation code in python. Automation framework is also important to connect to multiple devices at the same time (concurrently), which greatly reduce response time when it comes to many devices in our inventory.   

We have other frameworks options like Ansible but Nornir is different in the way that we write our own python code to control the automation. Ansible is written in python but to use it we have to write the instructions in its DSL format (YAML). There are also speed concerns, Nornir is faster when it comes to thousands of devices in our inventory. Nornir provides us an interface that does a lot of heavy lifting for us


Installation:

1: Install and integrate GNS3 GUI/GNS3 VM.
2: Install venv “python and nornir” on your Linux or MAC environment. In my case I will be using PyCharm (venv “Python + Nornir”) on Windows 10. For communication with the GNS3    Lab setup I installed “Microsoft KM-TEST Loopback adopter”. 
3 Cisco “IOS” image for Cisco emulated devices in GNS3.
* Please check the link for details https://www.linkedin.com/pulse/gns3-21-gui-vm-installation-integration-steps-khurram-javed
4: Install Nornir/Python
5; Make GNS3 lab as per the topology in the screenshot above.
6: Copy config.yml file in your IDE
7: Copy group.yml file in your IDE
8: Copy hosts.yml file in your IDE
9: Copy nornir_script.py in your IDE

Configuration Steps:

1. Configure the Microsoft KM-TEST Loopback adapter with the ip address in “192.168.122.100/24” subnet.
2. Configure the IP Address on R1-R5 “IOS” Router interfaces connected to “Ether Hub” from the same subnet as the appliance, below is one example from R1

        R1(config)#interface ethernet 2/0
        R1(config-if)#ip address 192.168.122.101 255.255.255.0
        R1(config-if)#no shutdown
3. You have to configure R1-R5 for SSHv2

        (config)#hostname (R1-R5)
        (config)#ip domain-name python.com
        (config)#crypto key generate rsa (use 1024 bit)
        (config)#enable password cisco
        (config)#username gnslab password cisco
        (config)#username gnslab privilege 15
        (config)#ip scp server enable
        (config)#line vty 0 4
        (config-line)#login local
        (config-line)#transport input ssh
        (config-line)#exit
4. Try to ping and SSH the R1-e2/0 ip addresses from your IDE  (Should work if above steps are correct).
5. Run the nornir_script.py from your IDE, you can check the output on the screen and the Excel file will be saved in the same folder where the script file is saved.

you can use below references for further study.

•	Book “Python network programming conquer all your networking challenges with the powerful python language” by Abhishek Ratan, Eric Chou, Pradeeban Kathiravelu.
•	https://www.youtube.com/watch?v=w9X-jzTweek
•	https://nornir.readthedocs.io/en/stable/tutorials/intro/overview.html
•	https://pynet.twb-tech.com/blog/nornir/intro.html
•	Book “Network Programmability and Automation: Skills for the Next-Generation Network Engineer” by Jason Edelman, Scott S. Lowe and Matt Oswalt
