import machine
import time

publiometer  = machine.ADC(machin.Pin(4))
publiometer.atten(machine.ADC.ATTN_11DB)

if __name__=='__main__':
  while True:
    publiometer_value = publiometer.read()
    print(publiometer_value)
    time.sleep(0.1)
