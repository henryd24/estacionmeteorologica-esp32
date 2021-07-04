import machine
import os
def read_channel(num_samples,pin):
  pin_value = pin.read()
  adc_samples=[]
  for i in range(num_samples):
    adc_samples.append(pin_value)
  adc_samples.sort() 
  mean = (adc_samples[i//2]+adc_samples[i//2+1])/2
  return mean

def scaling(zero_sensor, span_sensor, zero_adc, span_adc, mean):
  m = (span_sensor-zero_sensor)/(span_adc-zero_adc)
  scaled = m*(mean-zero_adc)+zero_sensor
  return scaled
