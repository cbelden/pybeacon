from pybeacon.scanner import BeaconScanner
from logging import FileHandler


fh = FileHandler('/home/pi/gspace/daemon.log')
b_scanner = BeaconScanner(debug=True, loghandler=fh)
b_scanner.log_beacons()

