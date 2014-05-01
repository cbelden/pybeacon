<h2>pybeacon</h2>
<h4>Overview</h4>
<p>
The pybeacon tool is a Python package that is designed to log Bluetooth LE beacons. The package leverages the commands in the Linux bluez Bluetooth module and tracks the device ID, rssi value, and timestamp of all advertising Bluetooth LE devices.<br>
The intended way to use this package is illustrated in test.py: simply create a new BeaconScanner object and call its log_beacons() method. The BeaconScanner will continuously log beacons until you kill the process. For our senior design project, we run the run.py module on bootup.
</p>
<h4>What you need</h4>
<ul>
<li>Rasbperry Pi (all testing/development implemented using Pi Model B running Raspbian)</li>
<li>bluez (linux bluetooth library) - http://www.bluez.org/</li>
<li>bluetooth dongle</li>
</ul>
<h4>Author Info</h4>
<p>
Calvin Belden<br>
University of Notre Dame<br>
EE Senior Design Project - Team GreenSpace<br>
</p>
