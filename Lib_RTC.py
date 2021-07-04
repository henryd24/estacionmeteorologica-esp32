import DS1302
import machine

def time_machine(pin_sclk,pin_dio,pin_rst):
    sclk = machine.Pin(pin_sclk)
    dio = machine.Pin(pin_dio)
    rst = machine.Pin(pin_rst)
    

    ds = DS1302.DS1302(sclk,dio,rst)
    year = ds.Year()
    month = ds.Month()
    day = ds.Day()
    hour = ds.Hour()
    minute = ds.Minute()
    second = ds.Second()
    rtc = machine.RTC()
    rtc.init((year,month,day,hour,minute,second,0,0))
    
    return ds


