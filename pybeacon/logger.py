from datetime import datetime
import logging
import os


class BeaconLogger():
    def __init__(self, logpath, name=__name__):
        """Instantiates the BeaconLogger."""

        # Create the logpath if it does not exist.
        if not os.path.exists(logpath):
            try:
                os.makedirs(logpath)
            except OSError, e:
                print "Error creating the specified logpath."
                raise e
    
        # Instantiate logging information
        self._logpath = logpath
        self._log_datetime = datetime.min
        self._log = logging.getLogger(name)
        self._log.setLevel(logging.INFO)


    def _make_log_dir(self, path):
        """Makes a new directory in the main log folder."""

        try:
            os.makedirs('/'.join([self._logpath, path]))
        except OSError, e:
            # Return True if dir already exists
            if e.args[0] is 17:
                return

            # Some other error; raise exception
            raise e

        return


    def _get_new_log_file(self, date, hour):
        """Creates new log directories as needed and returns the path to the current log file."""

        # Get folder name for this particular date
        dayfolder = str(date)

        # Generate new log directory if necessary
        if not os.path.exists('/'.join([self._logpath, dayfolder])):
            self._make_log_dir(dayfolder)

        # Return the path to the current log file
        filename = str(hour) + '.txt'
        return '/'.join([self._logpath, dayfolder, filename])


    def _log_expired(self, date, hour):
        """Returns true if the current log handler does not coincide with the current time/date."""

        if date != self._log_datetime.date() or hour != self._log_datetime.hour:
            return True

        return False


    def _assign_handler(self, date, hour):
        """Assigns a new log handler to the logger."""

        # Get current handler
        handlers = self._log.handlers

        # Remove current file handler
        if len(handler) > 0:
            cur_fh = handlers[0]
            self._log.removeHandler(cur_fh)

        # Assign a new handler for the new log file
        new_path = self._get_new_log_file(date, hour)
        new_fh = logging.FileHandler(new_path)

        # Add new log handler and update the associated datetime
        self._log.addHandler(new_fh)
        self._log_datetime = datetime.now()


    def log_beacon(self, beaconID, rssi):
        """Logs the beaconID and rssi value."""

        # Get timestamp data
        now = datetime.now()
        today = now.date()
        hr = now.hour

        # Assigns appropriate file handler for current datetime
        if self._log_expired(today, hr):
            self._assign_handler(today, hr)
        
        # Log message
        msg = str(now) + '\t' + beaconID + '\t' + rssi
        self._log.info(msg)
        
