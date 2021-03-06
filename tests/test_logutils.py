"""Module that defines tests for :mod:`~pyutils.logutils`

Every functions in :mod:`~pyutils.logutils` are tested here.

"""

from copy import deepcopy
import logging
import unittest

from .utils import TestBase
from pyutils.logutils import get_error_msg, setup_logging_from_cfg


class TestFunctions(TestBase):
    # TODO
    test_module_name = "logutils"

    # @unittest.skip("test_get_error_msg()")
    def test_get_error_msg(self):
        """Test that get_error_msg() returns an error message.

        This function tests that :meth:`~pyutils.logutils.get_error_msg` returns
        an error message from an exception.

        """
        self.logger.warning("\n<color>test_get_error_msg()</color>")
        self.logger.info("Testing <color>get_error_msg()</color>...")
        exc = IOError("The file doesn't exist")
        error_msg = get_error_msg(exc)
        expected = "[OSError] The file doesn't exist"
        msg = "The error message '{}' is different from the expected one " \
              "'{}'".format(error_msg, expected)
        self.assertTrue(error_msg == expected, msg)
        self.logger.info("<color>The error message is the expected one:</color> "
                         "{}".format(error_msg))

    # @unittest.skip("test_setup_logging_case_1()")
    def test_setup_logging_case_1(self):
        """Test that setup_logging() can successfully setup logging from a
        YAML config file.

        Case 1 tests that :meth:`~pyutils.logutils.setup_logging` TODO ...

        """
        self.logger.warning("\n\n<color>test_setup_logging_case_1()</color>")
        self.logger.info("Testing <color>case 1 of setup_logging()</color> "
                         "with a YAML logging config file...")
        self.setup_logging_for_testing(self.yaml_logging_cfg_path)

    # @unittest.skip("test_setup_logging_case_2()")
    def test_setup_logging_case_2(self):
        """Test that setup_logging() can successfully setup logging from a dict.

        Case 2 tests that :meth:`~pyutils.logutils.setup_logging` TODO ...

        """
        self.logger.warning("\n\n<color>test_setup_logging_case_2()</color>")
        self.logger.info("Testing <color>case 2 of setup_logging()</color> "
                         "with a logging config dict...")
        self.setup_logging_for_testing(self.logging_cfg_dict)

    # @unittest.skip("test_setup_logging_case_3()")
    def test_setup_logging_case_3(self):
        """Test setup_logging() when the logging config file doesn't exist.

        Case 3 tests that :meth:`~pyutils.logutils.setup_logging` raises an
        :exc:`OSError` exception when the logging config file doesn't exist.

        """
        self.logger.warning("\n\n<color>test_setup_logging_case_3()</color>")
        self.logger.info("Testing <color>case 3 of setup_logging()</color> "
                         "when a config file doesn't exist...")
        with self.assertRaises(OSError) as cm:
            setup_logging_from_cfg("bad_logging_config.yaml")
        self.logger.info("<color>Raised an OSError exception as expected:"
                         "</color> {}".format(get_error_msg(cm.exception)))

    # @unittest.skip("test_setup_logging_case_4()")
    def test_setup_logging_case_4(self):
        """Test setup_logging() when the logging config dict has an invalid
        value.

        Case 4 tests that :meth:`~pyutils.logutils.setup_logging` raises an
        :exc:`ValueError` exception when the logging config dict is invalid,
        e.g. a logging handler's class is written incorrectly.

        """
        self.logger.warning("\n\n<color>test_setup_logging_case_4()</color>")
        self.logger.info("Testing <color>case 4 of setup_logging()</color> "
                         "with an invalid config dict...")
        # Corrupt a logging handler's class
        # NOTE: if I use copy instead of deepcopy, logging_cfg will also
        # reflect the corrupted handler's class
        corrupted_cfg = deepcopy(self.logging_cfg_dict)
        corrupted_cfg['handlers']['console']['class'] = 'bad.handler.class'
        # Setup logging with the corrupted config dict
        with self.assertRaises(ValueError) as cm:
            setup_logging_from_cfg(corrupted_cfg)
        self.logger.info("<color>Raised a ValueError exception as expected:"
                         "</color> {}".format(get_error_msg(cm.exception)))

    # @unittest.skip("test_setup_logging_case_5()")
    def test_setup_logging_case_5(self):
        """Test setup_logging() when the logging config dict is missing an
        important key.

        Case 5 tests that :meth:`~pyutils.logutils.setup_logging` raises a
        :exc:`KeyError` exception when the logging config dict is missing an
        important key, i.e. a key that is needed in
        :meth:`~pyutils.logutils.setup_logging`.

        """
        self.logger.warning("\n\n<color>test_setup_logging_case_5()</color>")
        self.logger.info("Testing <color>case 5 of setup_logging()</color>...")
        # Remove a key from the logging config dict
        corrupted_cfg = deepcopy(self.logging_cfg_dict)
        expected_missing_key = 'handlers'
        del corrupted_cfg[expected_missing_key]
        # Setup logging with the corrupted config dict
        with self.assertRaises(KeyError) as cm:
            setup_logging_from_cfg(corrupted_cfg)
        missing_key = cm.exception.args[0]
        msg = "The actual missing key ('{}') is not the expected one " \
              "('{}')".format(missing_key, expected_missing_key)
        self.assertTrue(expected_missing_key == missing_key, msg)
        self.logger.info("<color>Raised a KeyError exception as expected:"
                         "</color> {}".format(get_error_msg(cm.exception)))

    def setup_logging_for_testing(self, logging_cfg):
        """Setup logging for testing from a logging config file or dict.

        Depending on `logging_cfg`, this function setups logging for testing
        from a logging config file or dict.

        Parameters
        ----------
        logging_cfg

        Notes
        -----
        This function is called by :meth:`test_setup_logging_case_1` and
        :meth:`test_setup_logging_case_2`.

        """
        # NOTE: if I put the next line in the context manager, it will complain
        # that the expected log was not triggered on 'scripts.scraper'
        ret_cfg_dict = setup_logging_from_cfg(logging_cfg)
        logger = logging.getLogger('scripts.scraper')
        with self.assertLogs(logger, 'INFO') as cm:
            logger.info('first message')
        msg = "Log emitted not as expected"
        self.assertEqual(cm.output[0],
                         'INFO:scripts.scraper:first message',
                         msg)
        self.logger.info("<color>Log emitted as expected</color>")
        msg = "The returned logging config dict doesn't have the expected keys"
        self.assertSequenceEqual(list(ret_cfg_dict.keys()),
                                 list(self.logging_cfg_dict),
                                 msg)
        how = "dict" if isinstance(logging_cfg, dict) else "file"
        self.logger.info("Successfully setup logging with the logging config "
                         "{}!".format(how))


if __name__ == '__main__':
    unittest.main()
