<h1 class='liketext'><img src="https://github.com/ftsiadimos/netspy2ban/blob/master/icons/netspy2ban.png" width="40" height="40"  margin-left: 4px alt="Logo" />NetSpy2Ban</h1>
 
NetSpy2Ban is a graphic user interface program for Fedora 22 OS. The program serves three functions. The first function is to view connected network cards and their speed. The second is to allow real time monitoring of your network connections. Lastly, NetSpy2Ban includes a graphic user interface to provide user-friendly functionality for the Fail2Ban service.

<a href="https://github.com/ftsiadimos/netspy2ban/blob/master/rpms/netspy2ban-1.0-1.fc22.noarch.rpm?raw=true" target="_blank">Download</a> the rpm file package for easy installation. Install the package through the software manager or with the following command through the terminal "sudo dnf install netspy2ban-1.0-1.fc22.noarch.rpm"

<h1 class='liketext'>Overview</h1>

<br><br><p align="center">
STATUS: The Status icon shows network speeds and new network cards accessing the system (e.g., if a virtual machine starts, the user will see the virtual card). The bottom window section shows general system information.
<br><br>
<img src="https://github.com/ftsiadimos/netspy2ban/blob/master/icons/ima1.png" width="500" height="390" alt="image1"/><br>
<br>
NETWORKING: The networking icon shows network connections. The Source column shows the IP address that is starting a connection, and the Destination column shows the receiving system's IP address. If a user clicks on any of the rows, more information will appear in the bottom window section.
<br><br>
<img src="https://github.com/ftsiadimos/netspy2ban/blob/master/icons/ima2.png" width="500" height="390" alt="image2"/><br>
<br>
A popup message will appear on the user's desktop every time an attempt is made to access the user's system.
<br><br>
<img src="https://github.com/ftsiadimos/netspy2ban/blob/master/icons/task1ima.png" width="300" height="140" alt="notify-image1"/><br>
<br>
FAIL2BAN: In the General Settings section, the ban-time setting allows the user to specify in seconds how long Fail2Ban will block the IP address. The find-time setting is the moving window within which Fail2Ban keeps track of failed access attempts. In the Service Settings section, from the drop-down menu, a user can select a service. On the left side, the user can enable/disable that service. On the right side the user can specify how many times failed access attempts are made until Fail2Ban blocks the IP address.
<br><br>
<img src="https://github.com/ftsiadimos/netspy2ban/blob/master/icons/ima3.png" width="500" height="390" alt="imag3"/><br>
<br>
<img src="https://github.com/ftsiadimos/netspy2ban/blob/master/icons/task2ima.png" width="300" height="140" alt="notify-image2"/></p>
