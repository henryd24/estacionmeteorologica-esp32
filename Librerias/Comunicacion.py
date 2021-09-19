from machine import UART
from machine import Pin
import time
import os
import sys
import _thread
global uart
def Rx():
  global uart
  while True:
    a = uart.read()
    if a != None:
      print('Palabra Recibida: '+a.decode('UTF-8'))
  uart.read()
if __name__=='__main__':
  uart = UART(2, 9600)
  uart.init(9600, bits=8, parity=None, stop=1, tx = 21, rx = 19) # init with given baudrate 
  uart2= UART(1, 9600)
  uart2.init(9600, bits=8, parity=None, stop=1, tx = 22, rx = 23) # init with given parameters
  _thread.start_new_thread(Rx, ())
  palabra = ''
  while True:
    #chr = sys.stdin.read(1)
    #msg = input('mg')
    #print(type(chr)
    a = uart2.read()
    if a != None:
      if a.decode('UTF-8') == '\r':
        print('Enviando Palabra: '+palabra)
        uart.write(palabra)
      else:
        palabra = palabra + a.decode('UTF-8')
        print(palabra)
  



