import subprocess
import os


class Scanner():
    def __init__(self, debug=False):
        self.debug = debug

    def lescan(self):
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

    def toggle_dongle(self):
        # can usually just restart the bt dongle to recover
        if self.debug: print 'turning off bt dongle'
        command = ['sudo', 'hciconfig', 'hci0', 'down']
        p = subprocess.Popen(command, stdout=subprocess.PIPE)
        p.wait()

        if self.debug: print 'turning on bt dongle'
        command[3] = 'up'
        p = subprocess.Popen(command, stdout=subprocess.PIPE)
        p.wait()


    def recover_lescan(self):
        """
        Attempts to restart the lescan command. Exits if this fails.
        """
        if self.debug: print "lescan command failed. attempting to recover."
        
        # togging on and off the bt dongle usually works
        self.toggle_dongle()

        # now try to start lescan; exit if failure
        if not self.lescan():
            if self.debug: print "Error: lescan could not recover"
            exit(1)

    def hcidump(self):
        """
        Executes the hcitools hcidump command which outputs all bluetooth activity.
        Returns:
            -hcidump process handle
        """
        command = ['sudo', 'stdbuf', '-oL', 'hcidump']
        return subprocess.Popen(command, stdout=subprocess.PIPE)
        

    def log_beacons(self):
        """
        Logs the id and RSSI of advertising btle devices.
        """
        # kickoff the lescan command
        if not self.lescan():
            self.recover_lescan()

        # get advertising devices
        hcidump = self.hcidump()

        # read device information
        while 1:
            r = hcidump.stdout.readline()
            info = r.strip().split()

            if info[0] == 'bdaddr':
                print 'Device ID:\t', info[1]

            elif info[0] == 'RSSI:':
                print 'RSSI:     \t', info[1]

