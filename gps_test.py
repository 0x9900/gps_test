#!/usr/bin/python

"""This program run on linux and reads the information from the GPS
through the gps service daemon (gpsd)."""

import os
import select
import string
import sys
import termios
import threading
import time
import tty

from argparse import ArgumentParser
from operator import attrgetter

from gps import gps, WATCH_ENABLE


__author__ = "Fred C."
__email__ = "<github-fred@hidzz.com>"
__version__ = '0.1.1'


class Root(object):
  """Store global variables"""
  timer = 5

class GpsPoller(threading.Thread):
  """Spawn a thread and read the gps info when they are available"""

  _gpsd = None

  def __init__(self):
    threading.Thread.__init__(self)
    self._gpsd = gps(mode=WATCH_ENABLE) # starting the stream of info
    self.current_value = None
    self.running = True           # setting the thread running to true

  def run(self):
    # this will continue to loop and grab EACH set of gpsd info
    while self.running:
      _ = self._gpsd.waiting(60) and self._gpsd.next()

  def gps_data(self):
    """return the gpsd internal object"""
    if not self.running:
      raise SystemError('GpsPoller not running')
    return self._gpsd


def to_grid(dec_lat, dec_lon):
  """Convert gps coordonated into square grid"""
  try:
    adj_lat = dec_lat + 90.0
    adj_lon = dec_lon + 180.0

    grid_lat_sq = string.uppercase[int(adj_lat/10)]
    grid_lon_sq = string.uppercase[int(adj_lon/20)]

    grid_lat_field = str(int(adj_lat%10))
    grid_lon_field = str(int((adj_lon/2)%10))

    adj_lat_remainder = (adj_lat - int(adj_lat)) * 60
    adj_lon_remainder = ((adj_lon) - int(adj_lon/2)*2) * 60

    grid_lat_subsq = string.lowercase[int(adj_lat_remainder/2.5)]
    grid_lon_subsq = string.lowercase[int(adj_lon_remainder/5)]
  except ValueError:
    return "NoGrid"

  grid = (grid_lon_sq + grid_lat_sq + grid_lon_field + grid_lat_field
          + grid_lon_subsq + grid_lat_subsq)
  return grid

def getch():
  """Non blocking Read. Return any character from the keyboard"""
  sysfd = sys.stdin.fileno()
  old_settings = termios.tcgetattr(sysfd)
  try:
    tty.setraw(sysfd)
    [fdin, _0, _1] = select.select([sysfd], [], [], Root.timer)
    if fdin:
      char = sys.stdin.read(1)
    else:
      char = ''
  finally:
    termios.tcsetattr(sysfd, termios.TCSADRAIN, old_settings)
  return char

def clear():
  """Clean the screen and return the cursor the the origin"""
  sys.stdout.write('\033[2j\033c\x1bc')

def read_gps(gps_p):
  """Display the gps informations"""

  print 'Staring gps thread'
  gps_p.start()                   # start it up
  gpsd = gps_p.gps_data()

  while not getattr(gpsd, 'satellites'):
    print 'Waiting for satellite informations'
    time.sleep(1)

  while gps_p.running:
    clear()
    print ' GPS readings'
    print '-' * 60
    print 'time utc    ', gpsd.utc
    print 'latitude    ', gpsd.fix.latitude
    print 'longitude   ', gpsd.fix.longitude
    print 'altitude (m)', gpsd.fix.altitude
    print 'eps         ', gpsd.fix.eps
    print 'epx         ', gpsd.fix.epx
    print 'epv         ', gpsd.fix.epv
    print 'ept         ', gpsd.fix.ept
    print 'speed (m/s) ', gpsd.fix.speed
    print 'climb       ', gpsd.fix.climb
    print 'track       ', gpsd.fix.track
    print 'mode        ', gpsd.fix.mode
    print 'grid        ', to_grid(gpsd.fix.latitude, gpsd.fix.longitude)
    if gpsd.satellites:
      print 'satellites  '
      for sat in sorted(gpsd.satellites, key=attrgetter('used'), reverse=True):
        print '	', sat
    print '-' * 60
    print ' Press [ Q ] to quit, [ Space ] Refresh'
    key_pressed = getch()
    if key_pressed and key_pressed.upper() == 'Q':
      break

  gps_p.running = False
  gps_p.join()

def main():
  """At the beginning there a main function"""
  parser = ArgumentParser(prog=os.path.basename(__file__),
                          description=__doc__)
  parser.add_argument('-v', '--version', action='version', version=__version__,
                      help='Program version')
  parser.add_argument('-d', '--delay', default=Root.timer, type=int,
                      help='Polling interval [default: %(default)s]')
  options = parser.parse_args()

  if options.delay < 0:
    raise parser.error("Argument error")
  Root.timer = options.delay

  try:
    gps_p = GpsPoller()          # create the thread
    read_gps(gps_p)
    raise SystemExit
  except Exception as err:
    print "\nKilling Thread..."
    if err:
      print err
    gps_p.running = False
    gps_p.join()                 # wait for the thread to finish
  print "Done.\nExiting."

if __name__ == "__main__":
  main()
