from pybeacon.scanner import BeaconScanner
from logging import FileHandler

# Set beacon log path
beaconpath = '/home/pi/pybeacon_records/beacon_records'

# Get BeaconScanner instance
b_scanner = BeaconScanner(beaconpath, debug=True, rssi_threshold=-90)
b_scanner.log_beacons()

