import subprocess
import os
import logging
from logger import BeaconLogger


class Scanner():
    def __init__(self, debug=False, loghandler=logging.StreamHandler()):
        """Creates a new Scanner object."""
        # Set up beacon logging
        self._beaconlog = BeaconLogger('beacon-logger')

        # Set up debug logging
        self._log = logging.getLogger(__name__)
        self._log.addHandler(loghandler)
        
        # Info logging will be suppressed if logging is not specified
        if debug:
            self._log.setLevel(logging.INFO)

    def _lescan(self):
        """Executes the hcitool lescan command and checks for expected output."""
        self._log.info('Starting LEscan...')
        command = ['sudo', 'stdbuf', '-oL', 'hcitool', 'lescan']
        lescan = subprocess.Popen(command, stdout=subprocess.PIPE)
        r = lescan.stdout.readline()

        # Check if output is indicative of a successful lescan
        if r != 'LE Scan ...\n':
            # Kill process and return False
            os.system('sudo kill %s' % lescan.pid)
            return False

        return True

    def _toggle_dongle(self):
        """Toggles the Bluetooth dongle: off/on."""
        # Turn Bluetooth dongle off
        self._log.info('Turning off bt dongle')
        command = ['sudo', 'hciconfig', 'hci0', 'down']
        p = subprocess.Popen(command, stdout=subprocess.PIPE)
        p.wait()

        # Turn Bluetooth dongle on
        self._log.info('turning on bt dongle')
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
        self._log.info('Starting hcidump..')
        command = ['sudo', 'stdbuf', '-oL', 'hcidump']
        return subprocess.Popen(command, stdout=subprocess.PIPE)

    def log_beacons(self):
        """Indefinitely logs the ID and RSSI of advertising Bluetooth LE devices."""
        # Execute lescan command: listens for btle devices
        if not self._lescan():
            self._recover_lescan()

        # Execute hcidump command: outputs all 
        hcidump = self._hcidump()

        # read device information
        while 1:
            r = hcidump.stdout.readline()
            info = r.strip().split()

            if info[0] == 'bdaddr':
                beaconID =  info[1]

            elif info[0] == 'RSSI:':
                rssi = info[1]

                # log beacon
                self._beaconlog.logBeacon(beaconID, rssi)
                self._log.info('Beacon: %s\tRSSI: %s' % (beaconID, rssi))

