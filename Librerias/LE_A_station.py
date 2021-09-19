import machine, esp32
import time
import os
import adc_manager
import _thread
import Lib_RTC
import Lib_FIle
import DS1302
import json

global num, speed, pluviometer_value, anemometer_value, timer_pluviometer


def save_data(k):
  global speed, pluviometer_value, anemometer_value
  date = str(rck.Year()) + '-' + str(rck.Month()) + '-' + str(rck.Day())
  Lib_FIle.i_o_file(date, speed, pluviometer_value, 0, 3, anemometer_value)
  pluviometer_value = 0
  with open('value.json', 'w') as file:
  	json.dump(0, file, indent=4)
  machine.deepsleep(20000)


def scale(x):
  global num, speed
  speed = num*(2.25/3)
  num = 0


def pulse(p):
  global num
  num = num + 1


def debounce(pin):
  global timer_pluviometer
  timer_pluviometer.init(mode=machine.Timer.ONE_SHOT,
                         period=300, callback=pulse_pluviometer)


def pulse_pluviometer(pin):
  global pluviometer_value
  try:
    with open('value.json') as file:
        value = json.load(file)
    with open('value.json', 'w') as file:
        json.dump(value+1, file, indent=4)
  except:
    value = 1
    with open('value.json', 'w') as file:
      json.dump(value, file, indent=4)
  pluviometer_value = value


if __name__=='__main__':
  anemometer_wind_direction  = machine.ADC(machine.Pin(35))
  anemometer_wind_direction.atten(machine.ADC.ATTN_11DB)
  solar_radiaton = machine.ADC(machine.Pin(34))
  solar_radiaton.atten(machine.ADC.ATTN_11DB)
  pluviometer = machine.Pin(4,machine.Pin.IN, machine.Pin.PULL_UP)
  pluviometer.irq(debounce, machine.Pin.IRQ_RISING)
  timer_pluviometer = machine.Timer(1)
  num = 0
  speed = 0
  anemometer_value = 0
  pluviometer_value = 0
  rck = Lib_RTC.time_machine(13,12,14) #the pins are placed in the order pin_sclk,pin_dio,pin_rst
  esp32.wake_on_ext0(pin = pluviometer, level = esp32.WAKEUP_ANY_HIGH)
  anemometer_value = adc_manager.read_channel(100,anemometer_wind_direction)
  anemometer_value = adc_manager.scaling(0,359,0,4049,anemometer_value)
  solar_radiaton_value = adc_manager.read_channel(5000,solar_radiaton)
  solar_radiaton_value = adc_manager.scaling(0,1800,0,4049,solar_radiaton_value)
  save_data()
