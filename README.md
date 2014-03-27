Calvin Belden<br>
University of Notre Dame<br>
Senior Design<br>
Team GreenSpace<br>

<h2>pybeacon</h2>
<h4>Overview</h4>
<p>
pybeacon is a Python module that is designed to log Bluetooth LE beacons. All testing and development has been implemented using a Raspberry Pi running Raspbian.<br>
The intended way to use this package is illustrated in pybeacon_test.py; simply create a new BeaconScanner object and call its logBeacons() method. The BeaconScanner will continuously log beacons until you ctl+c.
</p>
<h4>What you need besides this module:</h4>
<p>
-bluez (linux bluetooth module)<br>
-bluetooth dongle<br>
<p>
