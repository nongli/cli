#!/usr/bin/python
# Copyright 2016 Cerebro Data, Inc. All Rights Reserved.

import unittest
import cerebro_cli

class CliTest(unittest.TestCase):
  def test_get_status(self):
    api_url = "http://localhost:8000/api/"
    (available, status) = cerebro_cli.get_status(api_url)
    self.assertFalse(available, msg="No server should be running")

if __name__ == "__main__":
  unittest.main()
