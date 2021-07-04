import machine
import machine
import time
import os
import adc_manager
import _thread
import Lib_RTC
import Lib_FIle
import DS1302
import json
import esp32
import plus_numbers
global num,speed,pluviometer_value,anemometer_value,timer_pluviometer, solar_radiaton_value
import network
import utime as time
from umqttsimple import MQTTClient
import uping
import ujson
import ubinascii



global mqtt_server,port, user
mqtt_server = "industrial.api.ubidots.com"
port = 1883
client_id = ubinascii.hexlify(machine.unique_id())

def connect_and_subscribe():
	global mqtt_server,port
	client = MQTTClient(client_id, mqtt_server, user=user,password="", port=port)
	try:
		client.connect()
		print("Me conecte al broker mqtt")
	except:
		print("No me pude conectar al broker mqtt")
	return client

def mqttrestart():
	print("Conexion con broker fallo.")
	machine.reset()

def publish(datos):
	global speed,pluviometer_value,anemometer_value,solar_radiaton_value,user
	with open("settings.json","r") as file:
		settings = file.read()
	settings = ujson.loads(settings)
	sampletime = settings["sample_time_sec"]
	user = settings["token"]
	try:
		transmitted	= False
		while not transmitted:
			station = network.WLAN(network.STA_IF)
			station.active(True)
			station.connect(settings["ssid"], settings["password_wlan"]) # Connect to an AP
			while not station.isconnected():
				time.sleep(0.1)
			print("Conectado a la red wlan")
			tx, rx = uping.ping("8.8.8.8")
			if rx == 0:
				save_data(0)
			else:
				save_data(0)
				try:
					print("Conectandose a mqttserver")
					client = connect_and_subscribe()
				except Exception as e:
					print("Error Conectandose al Broker ",e)
					mqttrestart()
				print("MQTT conectado")

				datos = ujson.dumps({"wind_direction":{"value":anemometer_value},"pluviometer_value":{"value":pluviometer_value*0.2},"solar_radiation":{"value":solar_radiaton_value}}).encode("UTF-8")
				client.publish("/v1.6/devices/weather",datos)
			
			print("Datos publicados")
	except Exception as e:
		print("Error general: ", e)

def save_data(k):
	global speed,pluviometer_value,anemometer_value,solar_radiaton_value
	date = str(rck.Year()) + '-' + str(rck.Month()) + '-' + str(rck.Day())
	Lib_FIle.i_o_file(date,speed,pluviometer_value*0.2,0,solar_radiaton_value,anemometer_value)
	with open('value.json', 'w') as file:
		json.dump(0, file)
	
def scale(x):
	global num,speed
	speed = num*(2.25/3)
	num = 0

def pulse(p):
	global num
	num = num + 1

def debounce(pin):
	global timer_pluviometer
	timer_pluviometer.init(mode=machine.Timer.ONE_SHOT, period = 300, callback = pulse_pluviometer)

def pulse_pluviometer(pin):
	global pluviometer_value
	try:
		with open('value.json') as file:
			value = json.load(file)
		with open('value.json', 'w') as file:
			json.dump(value+1, file)
	except:
		value = 1
		with open('value.json', 'w') as file:
			json.dump(value, file)
	pluviometer_value = value

def save_time(num):
	with open('save.json', 'w') as file:
		json.dump(num, file)


if __name__=='__main__':
	tiempo_muestreo = 60
	pluviometer = machine.Pin(4,machine.Pin.IN, machine.Pin.PULL_DOWN)
	pluviometer.irq(debounce, machine.Pin.IRQ_RISING)
	timer_pluviometer = machine.Timer(2)
	esp32.wake_on_ext0(pin = pluviometer, level = esp32.WAKEUP_ANY_HIGH)
	rck = Lib_RTC.time_machine(13,12,14) #the pins are placed in the order pin_sclk,pin_dio,pin_rst
	if machine.wake_reason()==2:
		pulse_pluviometer(4)
		with open('save.json') as file:
			time = json.load(file)
		time_two = tiempo_muestreo-(plus_numbers.time_seconds(rck)-time)
		machine.deepsleep(time_two*1000)
	else:
		anemometer_wind_direction	= machine.ADC(machine.Pin(35))
		anemometer_wind_direction.atten(machine.ADC.ATTN_11DB)
		solar_radiaton = machine.ADC(machine.Pin(34))
		solar_radiaton.atten(machine.ADC.ATTN_11DB)
		
		num = 0
		speed = 0
		anemometer_value = 0
		pluviometer_value = 0
		
		anemometer_value = adc_manager.read_channel(100,anemometer_wind_direction)
		anemometer_value = adc_manager.scaling(0,359,0,4049,anemometer_value)
		solar_radiaton_value = adc_manager.read_channel(5000,solar_radiaton)
		solar_radiaton_value = adc_manager.scaling(0,1800,0,4049,solar_radiaton_value)
		try:
			with open('value.json') as file:
				pluviometer_value = json.load(file)
		except:
			value = 0
			with open('value.json', 'w') as file:
				json.dump(value, file)
		publish("settings.json")
		total = plus_numbers.time_seconds(rck)
		save_time(total)

		machine.deepsleep(tiempo_muestreo*1000)

