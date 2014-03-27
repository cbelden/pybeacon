from datetime import datetime
import logging
import os


class BeaconLogger():
    def __init__(self, name=__name__):
        """Instantiates a logging session."""
        # Initialize logging
        self._logpath = 'logs'
        self._log_date = datetime.min
        self._log = logging.getLogger(name)
        self._log.setLevel(logging.INFO)

        # Create logs dir if necessary
        if not os.path.exists(self._logpath):
            self._makedir(self._logpath)
    
    def _makedir(self, path):
        """Makes a new directory in the current directory of execution."""
        try:
            os.makedirs(path)
        except OSError:
            return False

        return True

    def _get_new_log_file(self):
        """Creates new log directory if needed and return path to new log file."""
        now = datetime.now()
        delta = now - self._log_date
        log_dir = self._logpath + '/' + str(now.date())

        # Generate new log file if expired and directory doesnt already exist
        if delta.days > 0 and not os.path.exists(log_dir):
            self._makedir(log_dir)

        logfile = str(now.hour) + '.txt'

        return log_dir + '/' + logfile

    def _log_expired(self):
        """Checks if the date associated with the current log file has expired."""
        now = datetime.now()
        delta = now - self._log_date

        if delta.days > 0 or delta.seconds >= 3600:
            return True

        return False

    def _assign_handler(self):
        """Assigns a new log handler to the logger."""
        # Get current handler
        handlers = self._log.handlers

        if len(handlers) > 0:
            # Remove current file handler
            cur_fh = self._log.handlers[0]
            self._log.removeHandler(cur_fh)

        # Need to make a new log output dir/file
        new_path = self._get_new_log_file()
        new_fh = logging.FileHandler(new_path)

        # Add new handler and update log date
        self._log.addHandler(new_fh)
        self._log_date = datetime.now()

    def logBeacon(self, beaconID, rssi):
        """Logs the beaconID and rssi value."""
        # Assign new handler if date associated w/ current log file has expired
        if self._log_expired():
            self._assign_handler()
        
        # Log message
        msg = str(datetime.now()) + '\t' + beaconID + '\t' + rssi
        self._log.info(msg)
        
