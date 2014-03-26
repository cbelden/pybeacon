import subprocess
import os
import logging


class Scanner():
    def __init__(self, logging=False, loghandler=logging.StreamHandler()):
        """
        Overview:
            Initializes the Scanner object. If logging is true, a logger is created that writes to
            the specified handler (stderr if not specified).
        Input:
            -logging: specifies whether or not logging is turned on
            -loghandler: particular log handler (specifies output destination)
        """
        # Set up logging
        self._log = logging.getLogger(__name__)
        self._log.addHandler(loghandler)
        
        # Info logging will be suppressed if logging is not specified
        if logging:
            self._log.setLevel(logging.INFO)

    def _lescan(self):
        """
        Overview:
            Executes the hcitool lescan command and checks for expected output.

        Returns:
            True if output is standard upon successful execution; returns false if the command fails.
        """
        command = ['sudo', 'stdbuf', '-oL', 'hcitool', 'lescan']
        lescan = subprocess.Popen(command, stdout=subprocess.PIPE)
        r = lescan.stdout.readline()

        # return true if output is regular; false otherwise
        if r != 'LE Scan ...\n':
            # need to 'sudo kill' process because it is executed as root
            os.system('sudo kill %s' % lescan.pid)
            return False

        return True

    def _toggle_dongle(self):
        """
        Overview:
            Toggles the Bluetooth dongle: off/on.
        """
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
        """
        Overview:
            Attempts to restart the lescan command. Exits if this fails.
        """
        self._log.warn("LEscan command failed. Attempting to recover.")
        
        # Toggling on and off the bt dongle historically works
        self._toggle_dongle()

        # Try to start lescan; exit if failure
        if not self._lescan():
            self._log.error("Error: lescan could not recover.")
            exit(1)

    def _hcidump(self):
        """
        Overview:
            Executes the hcitools hcidump command which outputs all bluetooth activity.
        Returns:
            -hcidump process handle
        """
        command = ['sudo', 'stdbuf', '-oL', 'hcidump']
        return subprocess.Popen(command, stdout=subprocess.PIPE)

    def log_beacons(self):
        """
        Overview:
            Indefinitely logs the ID and RSSI of advertising Bluetooth LE devices.
        """
        # kickoff the lescan command
        if not self._lescan():
            self._recover_lescan()

        # get advertising devices
        hcidump = self._hcidump()

        # read device information
        while 1:
            r = hcidump.stdout.readline()
            info = r.strip().split()

            if info[0] == 'bdaddr':
                print 'Device ID:\t', info[1]

            elif info[0] == 'RSSI:':
                print 'RSSI:     \t', info[1]

