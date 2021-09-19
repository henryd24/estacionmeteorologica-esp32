import machine
import os
def i_o_file(v_time,v_speed,v_pluvio,v_hum,v_rad,v_dirc):
    path = os.listdir('/datalogger')
    name_file = v_time + '.txt'
    if name_file in path:
        with open('/datalogger' + '/' + name_file,'a') as f:
            f.write(str(v_time) + ';' + str(v_speed) + ';' + str(v_pluvio) + ';' + str(v_hum) + ';' + str(v_rad) + ';' + str(v_dirc) + '\n')
    else:
        with open('/datalogger' + '/' + name_file,'w') as f:
            f.write('TIME;SPEED;PLUVIOMETRO;HUMEDAD;RADIACCION;DIRECCION\n')
