#!/usr/bin/python
# Copyright 2016 Cerebro Data, Inc. All Rights Reserved.

from optparse import OptionParser
import requests
import sys

STATUS_OK = 200

def print_usage():
  print "usage: cerebro-cli [options] <command> <subcommand> [parameters]"
  print '''To see help text, you can run:

  cerebro-cli commands
  cerebro-cli <command> help
  cerebro-cli <command> <subcommand> help'''

def print_commands():
  print '''
commands
users
status
'''

def get_status(api_url):
  try:
    response = requests.get(api_url + "status")
    if response.status_code == STATUS_OK:
      return True, response.text
    else:
      return False, "Unavailable"
  except requests.exceptions.RequestException:
    return False, "Unavailable"

def get_users(api_url):
  response = requests.get(api_url + "users")
  print response
  print response.json()

def handle_status(api_url):
  available, status = get_status(api_url)
  if not available:
    print "Service unavailable"
  else:
    print "Service available. Status: " + status

def users_usage():
  print "usage: cerebro-cli [options] users <subcommand> [parameters]"
  print '''valid subcommands are:
list
'''

def handle_users(api_url, args):
  if len(args) == 1:
    users_usage()
    sys.exit(1)

  cmd = args[1]
  if cmd == "list":
    get_users(api_url)

def main():
  parser = OptionParser()
  parser.add_option("-s", "--server", type="string", dest="server", default="localhost:8080",
                    help="Host:port of the server to connect to.")
  options, args = parser.parse_args()

  api_url = "http://" + options.server + "/api/"

  if len(args) == 0:
    print_usage()
    print "cerebro-cli error: too few arguments"
    sys.exit(1)

  cmd = args[0]
  if cmd == "commands":
    print_commands()
    sys.exit(0)
  elif cmd == "status":
    handle_status(api_url)
    sys.exit(0)

  try:
    if cmd == "users":
      handle_users(api_url, args)
    else:
      print_usage()
      print "cerebro-cli error: Invalid command. valid commands are:"
      print_commands()
      sys.exit(1)
  except requests.exceptions.RequestException:
    print "cerebro-cli error: unable to connect to server: " + options.server
    sys.exit(1)

if __name__ == '__main__':
  sys.exit(main())

