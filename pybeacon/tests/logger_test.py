import unittest
import os
import shutil
from datetime import datetime, timedelta
from logger import BeaconLogger


class TestLoggerModule(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        if os.path.exists('logs'): shutil.rmtree('logs')

    def test_constructor(self):
        logger = BeaconLogger('constructor')

        # make sure log file was created
        self.assertEqual(os.path.exists('logs'), True)

        # make sure log handlers are empty
        self.assertEqual(logger._logger.handlers, [])

    def test_makedir(self):
        logger = BeaconLogger('makedir')
        logger._makedir('floob')

        # make sure the folder was created
        self.assertEqual(os.path.exists('floob'), True)

        # make sure error is raised creating folder that already exists
        self.assertEqual(logger._makedir('floob'), False)
        
        os.rmdir('floob')

    def test_get_new_log_file(self):
        logger = BeaconLogger('new log file')
        log_dir = 'logs/2014-03-25'
        somefile = 'somefile.txt'
        
        # create non empty non-expired log directory
        os.makedirs(log_dir)
        open(log_dir + '/' + somefile, 'a').close()

        new_path = logger._get_new_log_file()
        expected = log_dir + '/' + str(datetime.now().hour) + '.txt'

        # make sure path is correct and old file is still there
        self.assertEqual(new_path, expected)
        self.assertEqual(os.path.exists(log_dir + '/' + somefile), True)

        # clear log directory
        shutil.rmtree(log_dir)

        new_path = logger._get_new_log_file()

        # make sure new directory is created
        self.assertEqual(new_path, expected)
        self.assertEqual(os.path.exists(log_dir), True)

    def test_future_log_expired(self):
        logger = BeaconLogger('future log expired')
        future = datetime.now() + timedelta(days=1)

        logger._log_date = future
        self.assertEqual(logger._log_expired(), False)

    def test_present_log_expired(self):
        logger = BeaconLogger('present log expired')
        present = datetime.now()

        logger._log_date = present
        self.assertEqual(logger._log_expired(), False)

    def test_past_log_expired(self):
        logger = BeaconLogger('past log expired')

        # possible past times (past by a day and hr, just a day, just an hr)
        past = logger._log_date
        present = datetime.now()
        past_hr = present - timedelta(hours=1)
        past_day = present - timedelta(days=1)

        logger._log_date = past
        self.assertEqual(logger._log_expired(), True)
        logger._log_date = past_hr
        self.assertEqual(logger._log_expired(), True)
        logger._log_date = past_day
        self.assertEqual(logger._log_expired(), True)

    def test_assign_handler(self):
        logger = BeaconLogger('assign handler')
        logger._assign_handler()

        # calculate expected handler path
        now = datetime.now()
        log_path = '/logs/' + str(now.date()) + '/' + str(now.hour) + '.txt'
        expected_path = os.getcwd() + log_path

        self.assertEqual(logger._logger.handlers[0].baseFilename, expected_path)

        # check if we can remove and add a filehandler  
        logger._log_date = logger._log_date - timedelta(hours=2)
        logger._assign_handler()

        self.assertEqual(len(logger._logger.handlers), 1)
        self.assertEqual(logger._logger.handlers[0].baseFilename, expected_path)

    def test_logBeacon(self):
        print 'testing log beacon'
        logger = BeaconLogger('logging')
        beaconID = 'SOMEBEACONID'
        rssi = 'SOMERSSI'
        logger.logBeacon(beaconID, rssi)

        # Expected log file path
        now = datetime.now()
        log_path = 'logs/' + str(now.date()) + '/' + str(now.hour) + '.txt'
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
