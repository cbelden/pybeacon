import unittest
import os
import shutil
from datetime import datetime, timedelta
from logger import BeaconLogger


logfolder = 'beacon_test_logs'


class TestLoggerModule(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        """Deletes the log folder if one exists."""
        if os.path.exists(logfolder):
            shutil.rmtree(logfolder)    

    def test_constructor_no_preexisting_logfolder(self):
        logger = BeaconLogger(logfolder, 'constructor test w/ no preexisting log folder')

        # make sure log file was created
        self.assertEqual(os.path.exists(logfolder), True)

        # make sure log handlers are empty
        self.assertEqual(logger._log.handlers, [])

    def test_constructor_with_existing_logfolder(self):

        # Create logfolder and new logger
        os.makedirs(logfolder)
        logger = BeaconLogger(logfolder, 'constructor test w/ no preexisting log folder')

        # make sure log folder exists
        self.assertEqual(os.path.exists(logfolder), True)

        # make sure log handlers are empty
        self.assertEqual(logger._log.handlers, [])

    def test_make_log_dir(self):
        """Ensure method creates a directory in the primary log folder."""
        logger = BeaconLogger(logfolder, 'test _makedir')
        logger._make_log_dir('floob')

        # make sure the folder was created
        self.assertEqual(os.path.exists('/'.join([logfolder, 'floob'])), True)

        # make sure return value is true if folder already exists
        self.assertEqual(logger._make_log_dir('floob'), None)

    def test_get_new_log_file(self):
        """Tests the method that returns a new path to the current logging file."""

        logger = BeaconLogger(logfolder, 'test get new log file')
        log_dir = '/'.join([logfolder, str(datetime.now().date())])
        somefile = 'somefile.txt'
        
        # create non empty non-expired log directory
        os.makedirs(log_dir)
        open(log_dir + '/' + somefile, 'a').close()

        present = datetime.now()
        new_path = logger._get_new_log_file(present.date(), present.hour)
        expected = '/'.join([log_dir, str(present.hour)]) + '.txt'

        # Make sure path is correct, path exists, and the old file is still there
        self.assertEqual(new_path, expected)
        self.assertEqual(os.path.exists(log_dir), True)
        self.assertEqual(os.path.exists(log_dir + '/' + somefile), True)


    def test_future_log_expired(self):
        """Ensures a log from the future does not crash the system."""
        logger = BeaconLogger(logfolder, 'test if future log expired')
        present = datetime.now()
        future = present + timedelta(days=1)

        logger._log_date = future
        self.assertEqual(logger._log_expired(present.date(), present.hour), True)

    def test_present_log_expired(self):
        """Ensures a log from the present is not expired."""

        logger = BeaconLogger(logfolder, 'test if present log expired')
        present = datetime.now()

        logger._log_datetime = present
        self.assertEqual(logger._log_expired(present.date(), present.hour), False)

    def test_past_log_expired(self):
        """Ensures an old log is expired."""

        logger = BeaconLogger(logfolder, "test past log expired")

        # possible past times (past by a day and hr, just a day, just an hr)
        past = logger._log_datetime
        present = datetime.now()
        past_hr = present - timedelta(hours=1)
        past_day = present - timedelta(days=1)

        logger._log_datetime = past
        self.assertEqual(logger._log_expired(present.date(), present.hour), True)
        logger._log_datetime = past_hr
        self.assertEqual(logger._log_expired(present.date(), present.hour), True)
        logger._log_datetime = past_day
        self.assertEqual(logger._log_expired(present.date(), present.hour), True)

    def test_assign_handler(self):
        """Ensures the correct file handler is assigned."""

        logger = BeaconLogger(logfolder, 'test assign handler')

        # Calculate expected handler path
        now = datetime.now()
        log_path = logfolder + '/' + str(now.date()) + '/' + str(now.hour) + '.txt'
        expected_path = os.getcwd() + '/' + log_path

        # Execute method
        logger._assign_handler(now.date(), now.hour)

        self.assertEqual(logger._log.handlers[0].baseFilename, expected_path)

        # check if we can remove and add a filehandler  
        logger._log_datetime = logger._log_datetime - timedelta(hours=2)
        logger._assign_handler(now.date(), now.hour)

        self.assertEqual(len(logger._log.handlers), 1)
        self.assertEqual(logger._log.handlers[0].baseFilename, expected_path)

    def test_log_beacon(self):
        print 'testing log beacon'
        logger = BeaconLogger(logfolder, 'testing log beacon')
        beaconID = 'SOMEBEACONID'
        rssi = 'SOMERSSI'
        logger.log_beacon(beaconID, rssi)

        # Expected log file path
        now = datetime.now()
        log_path = logfolder + '/' + str(now.date()) + '/' + str(now.hour) + '.txt'
        expected_fh_path = os.getcwd() + '/' + log_path

        # Actual logged message
        f = open(log_path, 'r')
        logged_data = f.readline().strip().split('\t')
        f.close()

        # TODO test that the date is accurate
        self.assertEqual(os.path.exists(log_path), True)
        self.assertEqual(logged_data[1], beaconID)
        self.assertEqual(logged_data[2], rssi)


if __name__ == '__main__':
    unittest.main()

