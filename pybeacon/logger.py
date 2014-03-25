from datetime import datetime
import logging
import os


class BeaconLogger():
    def __init__(self, name='beacon-logger'):
        """
        Instantiates a logging session.
        """
        # Initialize logger
        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.INFO)
        self._log_date = datetime.min

        # Create logs dir if necessary
        if not os.path.exists('logs'):
            self._makedir('logs')
    
    def _makedir(self, path):
        """
        Makes a new directory in the current directory.
        """
        try:
            os.makedirs(path)
        except OSError:
            return False

        return True

    def _get_new_log_file(self):
        """
        If necessary (ie the old log date is expired by a day), create a new
        logging directory and generate the new path for the new log file.
        """
        now = datetime.now()
        delta = now - self._log_date
        log_dir = 'logs/' + str(now.date())

        # generate new log file if expired and directory doesnt already exist
        if delta.days > 0 and not os.path.exists(log_dir):
            self._makedir(log_dir)

        logfile = str(now.hour) + '.txt'

        return log_dir + '/' + logfile

    def _log_expired(self):
        """
        Checks if the date associated with the current log file has expired.
        Returns true if it has expired, false otherwise.
        """
        now = datetime.now()
        delta = now - self._log_date

        if delta.days > 0 or delta.seconds >= 3600:
            return True

        return False

    def _assign_handler(self):
        """
        Creates a new log dir/file as needed. Checks if the current handler
        is current; if not, a new log dir/file is created and a new handler
        is assigned to it.
        """
        # check if date associated w/ current log file has expired
        if not self._log_expired():
            print 'log not expired'
            return

        # get current handler
        handlers = self._logger.handlers

        if len(handlers) > 0:
            # remove current file handler
            cur_fh = self._logger.handlers[0]
            self._logger.removeHandler(cur_fh)

        # need to make a new log output dir/file
        new_path = self._get_new_log_file()
        new_fh = logging.FileHandler(new_path)

        # Add new handler and update log date
        self._logger.addHandler(new_fh)
        self._log_date = datetime.now()

    def logBeacon(self, beaconID, rssi):
        """
        Logs the beaconID and rssi value.
        """
        # assign correct handler
        self._assign_handler()
        
        # log message
        msg = str(datetime.now()) + '\t' + beaconID + '\t' + rssi
        self._logger.info(msg)
        
