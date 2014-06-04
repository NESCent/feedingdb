from selenium import selenium
import unittest

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, "*chrome", "http://feeding-dev.nescent.org/")
        self.selenium.start()
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)
        