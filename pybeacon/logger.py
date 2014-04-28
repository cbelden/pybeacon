from datetime import datetime
import logging
import os


class BeaconLogger():
    def __init__(self, logpath, name=__name__):
        """Instantiates the BeaconLogger."""

        # Check that the directory specified by logpath exists
        if os.path.exists(self._logpath):
            self._logpath = logpath.rstrip('/')
        else:
            print "Warning: specified log directory '" + logpath + "' does not exist."

        mindate = datetime.min
        self._log_date = {'date': mindate.date(), 'hour': mindate.hour}
        self._log = logging.getLogger(name)
        self._log.setLevel(logging.INFO)


    def _makedir(self, path):
        """Makes a new directory if it does not already exist. Returns true on success, false otherwise."""

        try:
            os.makedirs(path)
        except OSError, e:
            # Return True if dir already exists
            if e.args[0] is 17:
                return True
            
            # Return False; some other error
            else:
                return False

        return True


    def _get_new_log_file(self, date, hour):
        """Creates new log directory if needed and returns path to new log file."""

        log_dir = '/'.join([self._logpath, str(date)])

        # Generate new log directory if necessary
        if not os.path.exists(log_dir):
            self._makedir(log_dir)

        logfile = str(hour) + '.txt'

        return '/'.join([log_dir, logfile])


    def _log_expired(self):

        """Checks if the date associated with the current log file has expired."""

        now = datetime.now()
        current_date = now.date()
        current_hour = now.hour
        prev_date =  self._log_date['date']
        prev_hour = self._log_date['hour']

        if current_date is not prev_date or current_hour is not prev_hour:
            return True

        return False


    def _assign_handler(self):
        """Assigns a new log handler to the logger."""

        # Get current handler
        handlers = self._log.handlers

        # Remove current file handler
        if len(handlers) > 0:
            cur_fh = self._log.handlers[0]
            self._log.removeHandler(cur_fh)

        # Create the new log output dir/file
        now = datetime.now()
        new_path = self._get_new_log_file(now.date(), now.hour)
        new_fh = logging.FileHandler(new_path)

        # Add new handler and update the associated log date
        self._log.addHandler(new_fh)
        self._log_date['date'] = now.date()
        self._log_date['hour'] = now.hour


    def logBeacon(self, beaconID, rssi):
        """Logs the beaconID and rssi value."""

        # Assign new handler if date associated w/ current log file has expired
        if self._log_expired():
            self._assign_handler()
        
        # Log message
        msg = str(datetime.now()) + '\t' + beaconID + '\t' + rssi
        self._log.info(msg)
        
