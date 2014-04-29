from pybeacon.scanner import BeaconScanner
from logging import FileHandler

# Set beacon log path
beaconpath = '/home/pi/pybeacon/beacon_records'

# Get BeaconScanner instance
b_scanner = BeaconScanner(beaconpath, debug=True)
b_scanner.log_beacons()

