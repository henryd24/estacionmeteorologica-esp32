import machine
import time
global num


def scale(num):
  velocidad = num*(2.25/3)
  #print('pulsos por segundo = ',velocidad)
  num = 0
  return velocidad

def pulse(p):
  global num
  num = num + 1

def speed():

    
if __name__ =='__main__':
  num = 0
  pin_in = machine.Pin(5,machine.Pin.IN,machine.Pin.PULL_UP)
  timer = machine.Timer(0)
  pin_in.irq(trigger=machine.Pin.IRQ_FALLING, handler=pulse)
  timer.init(period=3000, mode=machine.Timer.PERIODIC, callback=scale)
  try:
    while(True):
      pin.on()
      time.sleep(1)
      pin.off()
      time.sleep(2)
  except:
    timer.deinit()
    

