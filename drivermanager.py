"""driver_manager.py
When using remotedriver to get chromedriver in current process,
kill origin driver process at remote driver and check driver alive.
If driver dead, it should be restart
"""

import os
import signal
import psutil


class DriverManager:
    """DriverManager"""

    @staticmethod
    def kill(driver_path):
        """kill_driver

        :param driver_path:
        """
        pid = None
        for process in psutil.process_iter():
            if process.cmdline()[0] == driver_path:
                pid = process.pid
        if pid:
            os.kill(pid, signal.SIGTERM)

    @staticmethod
    def isalive(driver):
        """check_alive

        :param driver:
        """
        try:
            _ = driver.title
            return True
        except Exception as e:
            return False
