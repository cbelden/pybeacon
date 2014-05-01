import subprocess
import os
import logging
from logger import BeaconLogger


class BeaconScanner():
    def __init__(self, logpath, debug=False, debug_handler=None, devname='hci0', rssi_threshold=-100):
        """Creates a new Scanner object."""
        # Set up beacon logging
        self._beaconlog = BeaconLogger(logpath, 'beacon_logger')
        self._devname = devname

        # Set up info/debug logging (default output to stdout)
        self._log = logging.getLogger(__name__)
        debug_handler = debug_handler if debug_handler else logging.StreamHandler()
        self._log.addHandler(debug_handler)
        
        # Info logging will be suppressed if not debugging
        if debug:
            self._log.setLevel(logging.INFO)

        # Set rssi threshold
        self._rssi_threshold = rssi_threshold

    def _lescan(self):
        """Executes the hcitool lescan command and checks for expected output."""
        self._log.info('Starting LEscan...')
        command = ['sudo', 'stdbuf', '-oL', 'hcitool', 'lescan']
        lescan = subprocess.Popen(command, stdout=subprocess.PIPE)
        r = lescan.stdout.readline()

        # Check if output is indicative of a successful lescan
        if r != 'LE Scan ...\n':
            # Kill process and return False
            self._log.warn('LEscan command failed.')
            os.system('sudo kill %s' % lescan.pid)
            return False

        return True

    def _toggle_dongle(self):
        """Toggles the Bluetooth dongle: off/on."""
        # Turn Bluetooth dongle off
        self._log.info('Turning off bt dongle')
        command = ['sudo', 'hciconfig', self._devname, 'down']
        p = subprocess.Popen(command, stdout=subprocess.PIPE)
        p.wait()

        # Turn Bluetooth dongle on
        self._log.info('Turning on bt dongle')
        command[3] = 'up'
        p = subprocess.Popen(command, stdout=subprocess.PIPE)
        p.wait()

    def _recover_lescan(self):
        """Attempts to restart the lescan command. Exits if this fails."""
        self._log.warn("LEscan command failed. Attempting to recover.")
        
        # Toggling on and off the bt dongle historically works
        self._toggle_dongle()

        # Try to start lescan; exit if failure
        if not self._lescan():
            self._log.error("Error: lescan could not recover.")
            exit(1)

    def _hcidump(self):
        """Executes the hcitools hcidump command which outputs all bluetooth activity."""
        self._log.info('Starting hcidump...')
        command = ['sudo', 'stdbuf', '-oL', 'hcidump']
        return subprocess.Popen(command, stdout=subprocess.PIPE)

    def log_beacons(self):
        """Indefinitely logs the ID and RSSI of advertising Bluetooth LE devices."""
        # Execute lescan command: listens for advertising btle devices
        if not self._lescan():
            self._recover_lescan()

        # Execute hcidump command: outputs all 
        hcidump = self._hcidump()

        while 1:
            # Read device information
            r = hcidump.stdout.readline()
            info = r.strip().split()

            if info[0] == 'bdaddr':
                beaconID =  info[1]

            elif info[0] == 'RSSI:':
                rssi = info[1]

		# Log beacon data if RSSI is above the threshold
	        if int(rssi) > self._rssi_threshold:
                    # Log beacon data
                    self._beaconlog.log_beacon(beaconID, rssi)
                    self._log.info('Logging beacon.. ID: %s\tRSSI: %s' % (beaconID, rssi))

