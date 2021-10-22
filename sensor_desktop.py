#Script for BM680 and luma oled screen from pimoroni                                                                                                                                                                                      
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106
import time
import bme680
from PIL import ImageFont

font_size = 15
font = ImageFont.truetype("verdana.ttf", font_size)

try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except IOError:
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

# These oversampling settings can be tweaked to
# change the balance between accuracy and noise in
# the data.

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)

serial = i2c(port=1, address=0x3C)
device = sh1106(serial, width=128, height=128, rotate=2)

sensor.data.temperature = 0
sensor.data.pressure = 0
sensor.data.humidity = 0

#subprograms
def temp():
    return " %.2f Cº" \
        % (sensor.data.temperature)

def humi():
    return " %.2f %%" \
        % (sensor.data.humidity)

def pres():
    return "%.2f hPa" \
        % (sensor.data.pressure)

#main program
while True:
    '''
    if sensor.get_sensor_data():
        output = '{0:.2f} Cº,  {1:.2f} hPa,  {2:.3f} %RH'.format(
            sensor.data.temperature,
            sensor.data.pressure,
            sensor.data.humidity)
        print(output)
    '''    
    sensor.get_sensor_data()    

    with canvas(device) as draw: #I would like to move text to save OLED pixels
       #draw.rectangle(device.bounding_box, outline="white", fill="black")
        draw.text((10, 15), "TEMP : ", fill="white", font=font)
        draw.text((50, 15), temp(), fill="white", font=font)

        draw.text((10, 50), "HUMI : ", fill="white", font=font)
        draw.text((50, 50), humi(), fill="white", font=font)

        draw.text((10, 85), "PRES : ", fill="white", font=font)
        draw.text((50, 85), pres(), fill="white", font=font)


    time.sleep(5)



