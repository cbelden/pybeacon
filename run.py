from pybeacon.scanner import BeaconScanner
from logging import FileHandler

# Set up debugging file handler (gets verbose output from the BeaconScanner)
dh = FileHandler('/home/pi/pybeacon_records/debug/output.log')

# Set beacon log path
beaconpath = '/home/pi/pybeacon_records/beacon_records'

# Get BeaconScanner instance
b_scanner = BeaconScanner(beaconpath, debug=True, debug_handler=dh)
b_scanner.log_beacons()

