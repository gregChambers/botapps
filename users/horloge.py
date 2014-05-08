#!/usr/bin/env python

# Name: botapp_living_colors
# Author: Willy Garnier, garnie_w@yahoo.fr
# License: BSD

import time
import signal
import os, sys

import roslib; 
roslib.load_manifest('aisoy_sdk_actuator')
roslib.load_manifest('aisoy_sdk_sensor')
roslib.load_manifest('aisoy_common')
from libaisoy_sdk_actuator import *;
from libaisoy_sdk_sensor import *;
from libaisoy_common import *

####### USAGE python horlage.py (defil|switch|trait) ##################
if len(sys.argv) > 1:
  mode = sys.argv[1]
else:
  mode = 'defil'
#'trait'
#'switch'

#To stop when press Control + C
def signal_handler(signal, frame):
    print 'You pressed Ctrl+C!'
    actuator. setColor(0,0,1)
    string = stringclear()
    actuator.mouthDraw(string)

    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
print 'Press Ctrl+C to stop'

#Normal
def defil(heure, minute):
    heure_minute = heure +  'H' + minute
    actuator.mouthPrint(heure_minute)

#New
def trait(heure, minute):
  string = stringclear()
#  print heure[0]
#  print heure[1]
#  print minute[0]
#  print minute[1]
  i = 1
  while i <= int(heure[0]) and i < 3:
    string = string[0:i-1] + 'x' + string[i:]
    i += 1
#    print 'i =' + str(i)
#    print string

  j = 1
  while j <= int(heure[1]) and j < 10:
    string = string[0:20 + j-1] + 'x' + string[20 + j:]
    j += 1
#    print 'j =' + str(j)
#    print string
 
  k = 1
  while k <= int(minute[0]) and k < 6:
    string = string[0:40 + k-1] + 'x' + string[40 + k:]
    k += 1
#    print 'k =' + str(k)
#    print string
  
  l = 1
  while l <= int(minute[1]) and l < 10:
    string = string[0:60 + l-1] + 'x' + string[60 + l:]
    l += 1
#    print 'l =' + str(l)
#    print string

#  print string
  actuator.mouthDraw(string)

#remplace le caractere de string position pos par replace
def replace(string, pos, replace):
  string = string[:pos] + replace + string[pos+1:]
  return string

def stringclear():
  return '0000000000000000000000000000000000000000000000000000000000000000000000'

#encode une string en tableau designant l`emplacement des x
def encoder(string):
  tableau=[]
  i = 0 
  while i < len(string):
    if string[i] == 'x':
      tableau.append(i)
    i += 1
  return tableau

#decode le tableau et place les x au bon endrois
def decoder(tableau, string):
  i = 0 
  while i < len(tableau):
    string = replace(string, tableau[i],'x')
    i += 1
  return string

tableau0hg = encoder('xxx0000000x0x0000000x0x0000000x0x0000000xxx000000000000000000000000000')
tableau1hg = encoder('0x00000000xx000000000x000000000x000000000x0000000000000000000000000000')
tableau2hg = encoder('xxx000000000x0000000xxx0000000x000000000xxx000000000000000000000000000')

tableau0hd = encoder('0000xxx0000000x0x0000000x0x0000000x0x0000000xxx00000000000000000000000')
tableau1hd = encoder('00000x00000000xx000000000x000000000x000000000x000000000000000000000000')
tableau2hd = encoder('0000xxx000000000x0000000xxx0000000x000000000xxx00000000000000000000000')
tableau3hd = encoder('0000xxx000000000x0000000xxx000000000x0000000xxx00000000000000000000000')
tableau4hd = encoder('0000x000000000x000000000xxx000000000x000000000x00000000000000000000000')
tableau5hd = encoder('0000xxx0000000x000000000xxx000000000x0000000xxx00000000000000000000000')
tableau6hd = encoder('0000xxx0000000x000000000xxx0000000x0x0000000xxx00000000000000000000000')
tableau7hd = encoder('0000xxx000000000x000000000x000000000x000000000x00000000000000000000000')
tableau8hd = encoder('0000xxx0000000x0x0000000xxx0000000x0x0000000xxx00000000000000000000000')
tableau9hd = encoder('0000xxx0000000x0x0000000xxx000000000x0000000xxx00000000000000000000000')

tableau0bg = encoder('00000000000000000000000xxx0000000x0x0000000x0x0000000x0x0000000xxx0000')
tableau1bg = encoder('000000000000000000000000x00000000xx000000000x000000000x000000000x00000')
tableau2bg = encoder('00000000000000000000000xxx000000000x0000000xxx0000000x000000000xxx0000')
tableau3bg = encoder('00000000000000000000000xxx000000000x0000000xxx000000000x0000000xxx0000')
tableau4bg = encoder('00000000000000000000000x000000000x000000000xxx000000000x000000000x0000')
tableau5bg = encoder('00000000000000000000000xxx0000000x000000000xxx000000000x0000000xxx0000')

tableau0bd = encoder('000000000000000000000000000xxx0000000x0x0000000x0x0000000x0x0000000xxx')
tableau1bd = encoder('0000000000000000000000000000x00000000xx000000000x000000000x000000000x0')
tableau2bd = encoder('000000000000000000000000000xxx000000000x0000000xxx0000000x000000000xxx')
tableau3bd = encoder('000000000000000000000000000xxx000000000x0000000xxx000000000x0000000xxx')
tableau4bd = encoder('000000000000000000000000000x000000000x000000000xxx000000000x000000000x')
tableau5bd = encoder('000000000000000000000000000xxx0000000x000000000xxx000000000x0000000xxx')
tableau6bd = encoder('000000000000000000000000000xxx0000000x000000000xxx0000000x0x0000000xxx')
tableau7bd = encoder('000000000000000000000000000xxx000000000x000000000x000000000x000000000x')
tableau8bd = encoder('000000000000000000000000000xxx0000000x0x0000000xxx0000000x0x0000000xxx')
tableau9bd = encoder('000000000000000000000000000xxx0000000x0x0000000xxx000000000x0000000xxx')

def heure_switch(heure, minute):
  stringh = stringclear()
  if heure[0] == '0':
    stringh = decoder(tableau0hg, stringh)
  elif  heure[0] == '1':
    stringh = decoder(tableau1hg, stringh)
  else:
    stringh = decoder(tableau2hg, stringh)
  
  if heure[1] == '0':
    stringh = decoder(tableau0hd, stringh)
  elif  heure[1] == '1':
    stringh = decoder(tableau1hd, stringh)
  elif  heure[1] == '2':
    stringh = decoder(tableau2hd, stringh)
  elif  heure[1] == '3':
    stringh = decoder(tableau3hd, stringh)
  elif  heure[1] == '4':
    stringh = decoder(tableau4hd, stringh)
  elif  heure[1] == '5':
    stringh = decoder(tableau5hd, stringh)
  elif  heure[1] == '6':
    stringh = decoder(tableau6hd, stringh)
  elif  heure[1] == '7':
    stringh = decoder(tableau7hd, stringh)
  elif  heure[1] == '8':
    stringh = decoder(tableau8hd, stringh)
  else:
    stringh = decoder(tableau9hd, stringh)

  #print 'heure: ' + string
  
  #minute
  stringm = stringclear()
  if minute[0] == '0':
    stringm = decoder(tableau0bg, stringm)
  elif  minute[0] == '1':
    stringm = decoder(tableau1bg, stringm)
  elif  minute[0] == '2':
    stringm = decoder(tableau2bg, stringm)
  elif  minute[0] == '3':
    stringm = decoder(tableau3bg, stringm)
  elif  minute[0] == '4':
    stringm = decoder(tableau4bg, stringm)
  else:
    stringm = decoder(tableau5bg, stringm)
    
  if minute[1] == '0':
    stringm = decoder(tableau0bd, stringm)
  elif  minute[1] == '1':
    stringm = decoder(tableau1bd, stringm)
  elif  minute[1] == '2':
    stringm = decoder(tableau2bd, stringm)
  elif  minute[1] == '3':
    stringm = decoder(tableau3bd, stringm)
  elif  minute[1] == '4':
    stringm = decoder(tableau4bd, stringm)
  elif  minute[1] == '5':
    stringm = decoder(tableau5bd, stringm)
  elif  minute[1] == '6':
    stringm = decoder(tableau6bd, stringm)
  elif  minute[1] == '7':
    stringm = decoder(tableau7bd, stringm)
  elif  minute[1] == '8':
    stringm = decoder(tableau8bd, stringm)
  else:
    stringm = decoder(tableau9bd, stringm)

#  seconde = time.strftime('%S',time.localtime())

  while int(time.strftime('%S',time.localtime())) < 56:
    actuator.mouthDraw(stringh)
    time.sleep(2)
    actuator.mouthDraw(stringm)
    time.sleep(2)
 # seconde = time.strftime('%S',time.localtime())

    
def print_heure(heure, minute, mode='defil'):
    actuator. setColor(1,1,1)

    if mode == 'trait':
        trait(heure, minute)

    elif mode == 'switch':
        heure_switch(heure, minute)
    
    else:
        defil(heure, minute)

    actuator. setColor(0,1,0)


actuator = Actuator()
sensor = Sensor()

heure = time.strftime('%H',time.localtime())
minute = time.strftime('%M',time.localtime())
#heure_minute = heure +  ':' + minute
print_heure(heure, minute, mode)

signal.signal(signal.SIGINT, signal_handler)
#actuator.mouthPrint(heure_minute)
#print heure_minute
actuator. setColor(0,1,0)

while True:

    if (minute != time.strftime('%M',time.localtime())):
        heure = time.strftime('%H',time.localtime())
        minute = time.strftime('%M',time.localtime())
#        heure_minute = heure +  ':' + minute
        signal.signal(signal.SIGINT, signal_handler)
#        print "param " + heure_minute
#        actuator.mouthPrint(heure_minute)
        print_heure(heure, minute, mode)

    time.sleep(1)
#    print "heure " + time.strftime('%H:%M',time.localtime())

    continue
