from selenium import selenium
from basecase import BaseTestCase
import unittest, time, re


class TestLogin(BaseTestCase):
    def test_login(self):
        sel = self.selenium
        sel.open("/admin/")
        sel.click("link=Login")
        sel.wait_for_page_to_load("30000")
        sel.type("id_username", "xxxxx")
        sel.type("id_password", "xxxx")
        sel.click("//input[@value='Log in']")
        sel.wait_for_page_to_load("30000")
        try: self.failUnless(sel.is_text_present("Please enter a correct username and password. Note that both fields are case-sensitive."))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.type("id_username", "xianhua")
        sel.type("id_password", "12345")
        sel.click("//input[@value='Log in']")
        sel.wait_for_page_to_load("30000")
        try: self.failUnless(sel.is_text_present("Site administration"))
        except AssertionError, e: self.verificationErrors.append(str(e))

if __name__ == "__main__":
    unittest.main()