---
title: "PFSense Setup"
description: "Setting up pfSense for home lab"
image: "images/blog/pfsense-setup/pfsense-wallpaper.jpg"
date: 2025-05-10T13:00:00+05:30
categories: ["tutorial"]
tags: ["pfsense", "firewall"]
postType: "featured" # available postType: [featured/regular]
draft: false
sitemapExclude: false
---

Hey everyone! In this blog post, we're going to walk through setting up pfSense for your home lab.  This is a beginner-friendly guide, so if you're new to networking or pfSense, you're in the right place!

You can download pfSense from the official website: [PFsense](https://www.pfsense.org/download/).

<asside>
Make sure you download the correct ISO image for your architecture (e.g., amd 64-bit).
</asside>

#### What is pfSense and How Does it Work?

pfSense is a free and open-source firewall/router distribution based on FreeBSD. Think of it as the gatekeeper of your network. It sits between your internet connection and your home network, controlling all the traffic that flows in and out.  It's much more powerful and flexible than a typical home router, offering advanced features that give you granular control over your network security and performance.

Here's a simplified breakdown of how it works:

1. **Internet Connection:** Your internet service provider (ISP) provides you with an internet connection, which usually connects to your modem.
2. **pfSense Firewall:** Your modem then connects to your pfSense firewall. The firewall acts as the first line of defense for your network.
3. **Network Traffic:** All traffic coming from the internet to your home network, and vice-versa, must pass through the pfSense firewall.
4. **Filtering and Routing:** pfSense examines this traffic based on the rules you configure. It can block unwanted connections, allow specific types of traffic, prioritize certain applications (like gaming or video streaming), and much more.
5. **Home Network:** Finally, the filtered and routed traffic reaches your devices (computers, phones, smart TVs, etc.) connected to your home network.

Essentially, pfSense acts as a sophisticated traffic controller and security guard for your home network.

#### Why Use pfSense in a Home Lab?

Using pfSense in your home lab offers several benefits:

- **Enhanced Security:** pfSense provides a robust firewall, intrusion detection/prevention systems (IDS/IPS), and other security features to protect your network from threats.
- **Advanced Networking Features:** You get access to features like Virtual Private Networks (VPNs), traffic shaping, Quality of Service (QoS), and more, which are typically not available in consumer-grade routers.
- **Customization and Control:** pfSense allows you to customize your network exactly how you want it, giving you fine-grained control over your network traffic.
- **Learning Experience:** Setting up and configuring pfSense is a great way to learn about networking concepts and gain valuable skills.

#### What You'll Need (Virtual Machine Setup)

Before we get started, here's what you'll need to set up pfSense in a virtual machine:

- **Virtualization Software:** You'll need virtualization software installed on your computer. Popular options include VirtualBox (free and open-source), VMware Workstation Player (free for personal use), or Hyper-V (built into Windows Pro and Enterprise).
- **Virtual Machine Resources:** Create a new virtual machine with the following specifications:
    - **CPU:** 1 core
    - **RAM:** 1 GB (at least)
    - **Hard Disk:** 20 GB (or more) - A dynamically allocated disk is usually sufficient.
- **Two Virtual Network Adapters:** Your virtual machine needs two virtual network adapters.
    - One adapter will be connected to your WAN (Wide Area Network) – this will represent the connection to your modem or the internet. In most virtualization software, this is often bridged to your physical network adapter or set to NAT if you're behind another router.
    - The other adapter will be connected to your LAN (Local Area Network) – this will be your internal network. This is often configured as a "host-only" network or a separate virtual network that your other virtual machines or physical devices can connect to.
- **pfSense ISO Image:** You'll need to download the pfSense ISO image from the official website. Make sure you download the correct version for your architecture (e.g., 64-bit).

#### Setting up Virtual Network Adapters

Before we dive into the pfSense installation, we need to configure our virtual network adapters.  This is crucial for how pfSense will manage traffic between your home network and the internet. I'm using VMware Workstation Pro, but the general principles apply to other virtualization software like VirtualBox or Hyper-V.

I've created two virtual networks:

- **NAT (192.168.5.0/24):** This network is handled by VMware and allows my pfSense VM to access the internet. It's configured as a Network Address Translation (NAT) network, which means my pfSense VM will share the host computer's IP address when connecting to the outside world. This network is assigned by my host OS.
- **LAN (192.168.10.0/24):** This is my internal network, the one that will be protected by pfSense. Devices connected to this network will communicate with each other and access the internet through pfSense.

<asside>
My WAN interface will obtain its IP address dynamically from my NAT network (192.168.5.0/24) using DHCP.  This is the default setup for my NAT network in VMware.  For my LAN interface, I'll assign a static IP address within the 192.168.10.0/24 range (like 192.168.10.1).  To make connecting devices easier, I'll configure pfSense to act as a DHCP server for the LAN, automatically assigning IP addresses to devices that join the network. The final step will be setting up the firewall rules to manage network traffic and security..
</asside>

| Name                          | IP               |
|-------------------------------|------------------|
| NAT (Assigned by Host OS)     | 192.168.5.0/24   |
| LAN (Firewall)                | 192.168.10.0/24  |
<br>
{{< image src="images/blog/pfsense-setup/image.png" caption="Figure 1.0 (My NAT)" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title" webp="false" >}}

{{< image src="images/blog/pfsense-setup/image1.png" caption="Figure 1.1 (LAN)" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title" webp="false" >}}

Figure 1.1 illustrates how I've configured the NAT network.  By disabling DHCP and using a separate host virtual adapter, my host computer is now completely isolated from the lab setup, ensuring it doesn't interfere or become part of the testing environment.

#### Installing Pfsense

Creating a new virtual machine in VMware Workstation is easy. 

Simply go to *File* > *New* *Virtual Machine*, or press `ctrl+ n` for a quick start. 

The pfSense download is a `.gz` file. To extract the ISO image, I'm using 7-Zip.  Once extracted, I moved the ISO file to a dedicated folder.  You'll need to unzip the downloaded file and choose a convenient location to store the resulting ISO image.

{{< image src="images/blog/pfsense-setup/1.png" caption="Figure 2.0" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title" webp="false" >}}

In the wizard, you'll be prompted to name your virtual machine.  I'm using "firewall" as my name. You can choose any name you prefer.  The next step is to select the location where the virtual machine's files will be stored. I have a separate disk for my VMware VMs, so I'm installing it there.  Choose the location that best suits your setup.

{{< image src="images/blog/pfsense-setup/image2.png" caption="Figure 2.1" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title" webp="false" >}}

The wizard will now prompt you to configure the storage for your virtual machine. The default size is 20GB, which is sufficient for pfSense. I'm sticking with the default.

{{< image src="images/blog/pfsense-setup/image3.png" caption="Figure 2.2" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title" webp="false" >}}

The wizard will now display a summary of the default configuration.  Before proceeding, we need to customize the hardware settings. Click `"Customize Hardware"` to open the hardware configuration window

{{< image src="images/blog/pfsense-setup/image4.png" caption="Figure 2.3" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title" webp="false" >}}

Now, let's configure the RAM (Memory). 1GB is generally enough for a basic pfSense setup, and that's what I'm using.  You can choose a higher value if you prefer, but make sure you have enough RAM available on your host computer to support the virtual machine.  It's a good idea to have at least 1GB.

{{< image src="images/blog/pfsense-setup/image5.png" caption="Figure 2.4" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title" webp="false" >}}

The default setting of one processor core is sufficient for a basic home lab pfSense installation. I'm leaving it at the default.

{{< image src="images/blog/pfsense-setup/image6.png" caption="Figure 2.5" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title" webp="false" >}}

In the Network section, you'll see the default NAT adapter. As discussed earlier, this will serve as our WAN interface for pfSense.

{{< image src="images/blog/pfsense-setup/image7.png" caption="Figure 2.6" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title" webp="false" >}}

Since we need both WAN and LAN connectivity, you'll need to add a second network adapter to your virtual machine's hardware configuration.  This second adapter will be designated as the LAN interface within pfSense and will be named `em1`.

<asside>

Keep in mind that pfSense names its interfaces sequentially: the first Network Adapter (`em0`) is your WAN (NAT) connection, the second Network Adapter 2 (`em1`) is your LAN, the third Network Adapter 3 would be `em2`, and so on.

</asside>

{{< image src="images/blog/pfsense-setup/image8.png" caption="Figure 2.7" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title" webp="false" >}}

I've named my LAN network "firewall" and connected it to a custom, specific virtual network to isolate it. Feel free to choose a different name and configure your own virtual network as needed.

{{< image src="images/blog/pfsense-setup/image9.png" caption="Figure 2.8" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title" webp="false" >}}

Double-check your virtual machine configuration against Figure 2.9. If everything matches, you're ready to start the installation. Click the "Power On This Virtual Machine" button to launch the virtual machine, or use the keyboard shortcut `ctrl+b`.

{{< image src="images/blog/pfsense-setup/image10.png" caption="Figure 2.9" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title" webp="false" >}}

The virtual machine will now boot from the pfSense ISO image. The installer will begin by verifying the necessary files.  Shortly after, a copyright and distribution notice will appear.  You can use the arrow keys to scroll through the notice and press Enter to accept the terms and proceed.

{{< image src="images/blog/pfsense-setup/image11.png" caption="Figure 2.10" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title" webp="false" >}}

You'll now be prompted to begin the pfSense installation. Simply press Enter to proceed.

{{< image src="images/blog/pfsense-setup/image12.png" caption="Figure 2.11" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title" webp="false" >}}

Simply press Enter to proceed.

{{< image src="images/blog/pfsense-setup/image13.png" caption="Figure 2.12" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title" webp="false" >}}

The next step is to configure the WAN interface.  Figure 2.13 shows the two network interfaces.  Remember that `em0` is our WAN connection. Select `em0` and press Enter to proceed.

{{< image src="images/blog/pfsense-setup/image14.png" caption="Figure 2.13" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title" webp="false" >}}

The WAN interface configuration will now appear. Since we're using NAT, the defaults are usually correct. Choose "Continue" and press Enter.

{{< image src="images/blog/pfsense-setup/image15.png" caption="Figure 2.14" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title" webp="false" >}}

You'll now see the LAN interface configuration screen. We'll configure the LAN settings after the pfSense installation is complete, so select "None" and press Enter to skip this step for now.

{{< image src="images/blog/pfsense-setup/image16.png" caption="Figure 2.15" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title" webp="false" >}}

{{< image src="images/blog/pfsense-setup/image17.png" caption="Figure 2.16" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title" webp="false" >}}

{{< image src="images/blog/pfsense-setup/image18.png" caption="Figure 2.17" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title" webp="false" >}}

The installer will now perform a network connectivity check.  Once this is complete, you'll see a message related to an active subscription.  pfSense Community Edition (CE) is free and comes with a default free subscription, so you don't need to worry about this.  Choose "Install CE" and press Enter to proceed.

{{< image src="images/blog/pfsense-setup/image19.png" caption="Figure 2.18" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title" webp="false" >}}

{{< image src="images/blog/pfsense-setup/image20.png" caption="Figure 2.19" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title" webp="false" >}}

From `Figure 2.20` to `2.23`, the focus is on storage options.  The default settings are generally the most efficient for most users, so simply press Enter to accept them and continue.

{{< image src="images/blog/pfsense-setup/image21.png" caption="Figure 2.20" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title" webp="false" >}}

{{< image src="images/blog/pfsense-setup/image22.png" caption="Figure 2.21" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title" webp="false" >}}

{{< image src="images/blog/pfsense-setup/image23.png" caption="Figure 2.22" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title" webp="false" >}}

{{< image src="images/blog/pfsense-setup/image24.png" caption="Figure 2.23" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title" webp="false" >}}

The next step is to choose the pfSense version to install.  For optimal security and performance, it's essential to use the latest version.  Select the newest version from the list (for me, that's 2.7.2) and press Enter to proceed.

{{< image src="images/blog/pfsense-setup/image25.png" caption="Figure 2.24" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title" webp="false" >}}

pfSense will now download and install additional packages, which can take more than 5 minutes.  After this process finishes, you'll be presented with a prompt (as shown in Figure 2.25). Press Enter to continue.  You will then be prompted to reboot the system. Select "Reboot" and press Enter.

{{< image src="images/blog/pfsense-setup/image26.png" caption="Figure 2.25" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title" webp="false" >}}

{{< image src="images/blog/pfsense-setup/image27.png" caption="Figure 2.26" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title" webp="false" >}}

#### Configuration LAN

After rebooting, you'll see a screen similar to `Figure 3.0`.  Notice that even though we haven't configured the LAN interface yet, it might show a default IP address (like 192.168.1.1). Now it's time to properly configure our LAN settings.

{{< image src="images/blog/pfsense-setup/image28.png" caption="Figure 3.0" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title" webp="false" >}}

We're now going to configure the IP address for our LAN interface.  Enter `2` and press Enter to access the interface configuration menu.  You'll then be shown the available interfaces.  Select the LAN interface (it will likely be `2` again) and press Enter.

{{< image src="images/blog/pfsense-setup/image29.png" caption="Figure 3.1" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title" webp="false" >}}

You'll be asked if you want to configure the LAN interface using DHCP. We've disabled DHCP on the virtual network adapter and pfSense will handle DHCP for our LAN, type `n` and press Enter.  Now, enter the IP address you want to assign to your pfSense LAN interface.  A common practice is to use the first available address in your LAN subnet (e.g., 192.168.10.1). I'm using 192.168.10.0/24, so I'll enter 192.168.10.1.  For the subnet mask, enter `24`.  If you're new to networking, a subnet mask of 24 is a good starting point for a home network.  Finally, you'll be asked for the IPv4 upstream gateway address.  Since we're configuring the LAN, we don't need a gateway here, so just press Enter to leave it blank.

{{< image src="images/blog/pfsense-setup/2.png" caption="Figure 3.2" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title" webp="false" >}}

The installer will now ask if you want to enable IPv6.  Since we're not using IPv6, type `n` and press Enter to skip it.  Next, you'll be asked if you want to enable the DHCP server for your LAN.  We need this to automatically assign IP addresses to devices on our network, so type `y` and press Enter.  You'll then be prompted to specify the DHCP address range.  I've chosen 192.168.10.200 as the starting address and 192.168.10.254 as the ending address.  Finally, the installer will ask about using HTTP for the web GUI.  The default is HTTPS, which is more secure, so type `n` to keep the HTTPS setting and press Enter.

{{< image src="images/blog/pfsense-setup/image30.png" caption="Figure 3.3" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title" webp="false" >}}

One final press of the Enter key will display the network configuration summary, as shown in Figure 3.4.

{{< image src="images/blog/pfsense-setup/image31.png" caption="Figure 3.4" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title" webp="false" >}}

#### Workstation Setup (Kali Purple Example)

Now that pfSense is configured, we need to connect our workstation to the LAN.  I'm using Kali Purple as my workstation. I've configured its network adapter to connect to the same virtual network as the pfSense LAN interface (named "firewall"). This allows pfSense to act as the DHCP server, automatically assigning an IP address to the workstation.  You can use any operating system you prefer for your lab workstation.

{{< image src="images/blog/pfsense-setup/image32.png" caption="Figure 4.0" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title" webp="false" >}}

After booting and using the `ifconfig` command in the terminal, I confirmed that pfSense assigned the IP address 192.168.10.200 to my workstation. This is the first address in our configured DHCP range.

```bash
ifconfig

eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.10.200  netmask 255.255.255.0  broadcast 192.168.10.255
        inet6 fe80::20c:29ff:fe3e:ef21  prefixlen 64  scopeid 0x20<link>
        ether 00:0c:29:3e:ef:21  txqueuelen 1000  (Ethernet)
        RX packets 14  bytes 1939 (1.8 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 282  bytes 98596 (96.2 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
        device interrupt 19  base 0x2000  

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 2580  bytes 221728 (216.5 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 2580  bytes 221728 (216.5 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

Since your workstation is directly connected to the pfSense LAN interface, we can access the pfSense web interface by navigating to its LAN IP address, which we previously set to 192.168.10.1, in your web browser. pfSense uses HTTPS by default, your browser will likely display a security warning.  This is because the certificate pfSense uses is self-signed and not issued by a trusted Certificate Authority.  Simply accept the risk and continue to proceed to the pfSense login page.  The default username is `admin`, and the default password is `pfsense`

{{< image src="images/blog/pfsense-setup/image33.png" caption="Figure 4.1" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title" webp="false" >}}

{{< image src="images/blog/pfsense-setup/image34.png" caption="Figure 4.2" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title" webp="false" >}}

After logging in with the default credentials, the very first thing you should do is change the default password.  I'm changing mine to a strong, unique password (`admin` 🤣)

{{< image src="images/blog/pfsense-setup/image35.png" caption="Figure 4.3" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title" webp="false" >}}

{{< image src="images/blog/pfsense-setup/image36.png" caption="Figure 4.4" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title" webp="false" >}}

{{< image src="images/blog/pfsense-setup/image37.png" caption="Figure 4.5" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title" webp="false" >}}

Navigating to *Firewall* -> *Rules* -> *LAN*, you'll see the default rule that allows all traffic from the LAN interface to the internet. This explains why your workstation, connected to the pfSense LAN, has unrestricted internet access.  

> **To Do/Task:** As an exercise, use the "Edit" option for the default LAN rule and modify it to block all traffic. This will help you understand how firewall rules work and how to control network access.  This exercise is crucial for learning how to secure your network.

{{< image src="images/blog/pfsense-setup/image38.png" caption="Figure 4.6" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title" webp="false" >}}

{{< image src="images/blog/pfsense-setup/image39.png" caption="Figure 4.7" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title" webp="false" >}}

{{< image src="images/blog/pfsense-setup/image40.png" caption="Figure 4.8" alt="alter-text" height="" width="" position="center" command="fill" option="q100" class="img-fluid" title="image title" webp="false" >}}

#### Summary

So, that's it!  We've now got pfSense up and running in our virtual lab.  We covered everything from setting up the virtual networks to configuring pfSense and connecting a workstation.

Thanks for reading! I hope this guide was helpful.  Apologies for the numerous screenshots, but I wanted to make the process as clear as possible.
