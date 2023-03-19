from picographics import PicoGraphics, DISPLAY_INKY_PACK
from pimoroni import Button
from time import sleep
import network
import socket
import ujson
import _thread


# Display mode. 1 = current readings, 2 = max readings and 3 = min readings.
display_mode = 1

json_in_use = (False, False) # item 0 is writing readings item 1 is display reading

# Set the display
display = PicoGraphics(display=DISPLAY_INKY_PACK)

def update_display(display_mode):
    global display
    global json_in_use
    display.set_pen(15)
    display.clear()
    display.set_pen(0)
    display.set_font("bitmap8")
    display.set_thickness(1)
    while json_in_use[0] == True:
        sleep(1)
    json_in_use = (False, True)
    with open("readings.json", "r") as f:
        data = ujson.load(f)
        if display_mode == 1:
            display.text("Current readings are:", 0, 0, scale=2)
            i = 18
            display.text(f"pm2.5 = {data['current_reading']['pm2_5']} ug/m^3", 0, i, wordwrap=250, scale=2)
            if data["current_reading"]["pm2_5"] >= 25:
                display.text("Health risk-too high", 155, i+4, scale=1)
            else:
                display.text("safe", 155, i+4, scale=1)
            i += 18
            display.text(f"pm10 = {data['current_reading']['pm10']} ug/m^3", 0, i, wordwrap=250, scale=2)
            if data["current_reading"]["pm10"] >= 50:
                display.text("Health risk-too high", 15, i+4, scale=1)
            else:
                display.text("safe", 150, i+4, scale=1)
            i += 18
            display.text(f"pm1 = {data['current_reading']['pm1']} ug/m^3", 0, i, wordwrap=250, scale=2)
            i += 18
            display.text(f"temperature = {data['current_reading']['temperature']} °C", 0, i, wordwrap=250, scale=2)
            i += 18
            display.text(f"air pressure = {data['current_reading']['pressure']} hPa", 0, i, wordwrap=250, scale=2)
            i += 18
            display.text(f"humidity = {data['current_reading']['humidity']}%", 0, i, wordwrap=250, scale=2)
            i += 18
            del i
            
        elif display_mode == 2:
            display.text("Maximum readings are:", 0, 0, scale=2)
            i = 18
            display.text(f"pm2.5 = {data['max_readings']['pm2_5']} ug/m^3", 0, i, wordwrap=250, scale=2)
            if data["max_readings"]["pm2_5"] >= 25:
                display.text("Health risk-too high", 155, i+4, scale=1)
            else:
                display.text("safe", 155, i+4, scale=1)
            i += 18
            display.text(f"pm10 = {data['max_readings']['pm10']} ug/m^3", 0, i, wordwrap=250, scale=2)
            if data["max_readings"]["pm10"] >= 50:
                display.text("Health risk-too high", 150, i+4, scale=1)
            else:
                display.text("safe", 150, i+4, scale=1)
            i += 18
            display.text(f"pm1 = {data['max_readings']['pm1']} ug/m^3", 0, i, wordwrap=250, scale=2)
            i += 18
            display.text(f"temperature = {data['max_readings']['temperature']} °C", 0, i, wordwrap=250, scale=2)
            i += 18
            display.text(f"air pressure = {data['max_readings']['pressure']} hPa", 0, i, wordwrap=250, scale=2)
            i += 18
            display.text(f"humidity = {data['max_readings']['humidity']}%", 0, i, wordwrap=250, scale=2)
            i += 18
            del i
            
        elif display_mode == 3:
            display.text("Minimum readings are:", 0, 0, scale=2)
            i = 18
            display.text(f"pm2.5 = {data['min_readings']['pm2_5']} ug/m^3", 0, i, wordwrap=250, scale=2)
            if data["min_readings"]["pm2_5"] >= 25:
                display.text("Health risk-too high", 155, i+4, scale=1)
            else:
                display.text("safe", 155, i+4, scale=1)
            i += 18
            display.text(f"pm10 = {data['min_readings']['pm10']} ug/m^3", 0, i, wordwrap=250, scale=2)
            if data["min_readings"]["pm10"] >= 50:
                display.text("Health risk-too high", 150, i+4, scale=1)
            else:
                display.text("safe", 150, i+4, scale=1)
            i += 18
            display.text(f"pm1 = {data['min_readings']['pm1']} ug/m^3", 0, i, wordwrap=250, scale=2)
            i += 18
            display.text(f"temperature = {data['min_readings']['temperature']} °C", 0, i, wordwrap=250, scale=2)
            i += 18
            display.text(f"air pressure = {data['min_readings']['pressure']} hPa", 0, i, wordwrap=250, scale=2)
            i += 18
            display.text(f"humidity = {data['min_readings']['humidity']}%", 0, i, wordwrap=250, scale=2)
            i += 18
            del i
        display.text("current->", 252, 20, wordwrap=296, scale=1)
        display.text("maximum->", 251, 60, wordwrap=296, scale=1)
        display.text("minimum->", 251, 100, wordwrap=296, scale=1)
    
    json_in_use = (False, False)
    display.update()

    

def button_checking():
    global display_mode
    global update_display
    button_a = Button(12)
    button_b = Button(13)
    button_c = Button(14)
    while True:
        if button_a.read():
            display_mode = 1
            update_display(display_mode)
        elif button_b.read():
            display_mode = 2
            update_display(display_mode)
        elif button_c.read():
            display_mode = 3
            update_display(display_mode)
        sleep (0.1 )

    
# join the wifi
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect('ssid', 'password')
while not sta.isconnected():
    pass


#create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket
server_socket.bind(("192.168.1.121", 204))

# become a server socket
server_socket.listen(5)

# create display updating thread
button_checking_thread = _thread.start_new_thread(button_checking, ())

while True:
    # establish a connection
    client_socket, addr = server_socket.accept()

    print("Got a connection from %s" % str(addr))
    
    # receive data from the client
    reading = eval(client_socket.recv(1024).decode("ascii"))
    
    # send a thank you message to the client.
    response = 'Thank you for sending readings'+ "\r\n"
    client_socket.send(response.encode('ascii'))
    client_socket.close()
    
    print(str(reading))


    while json_in_use[1] == True:
        sleep(1)
    json_in_use = (True, False)
    with open('readings.json', 'r') as f:
        data = ujson.load(f)

        data["current_reading"] = reading
        for key, value in reading.items():
            if value > data["max_readings"][key]:
                data["max_readings"][key] = value
            if value < data["min_readings"][key]:
                data["min_readings"][key] = value

    with open('readings.json', 'w') as f:
        ujson.dump(data, f)
    
    json_in_use = (False, False)
    update_display(display_mode)
    del reading
    

    
    
        

