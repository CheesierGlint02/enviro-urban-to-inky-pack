# enviro config file

# you may edit this file by hand but if you enter provisioning mode
# then the file will be automatically overwritten with new details

provisioned = 1

# enter a nickname for this board
nickname = 'enviro-urban'

# network access details
wifi_ssid = 'ssid'
wifi_password = 'password'

# how many log files to keep
log_count = 20

# how often to wake up and take a reading (in minutes)
reading_frequency = 10

# where to upload to ("web_hook", "mqtt", "adafruitio")
destination = ''

# how often to upload data (number of cached readings)
upload_frequency = 5

# web hook settings
custom_http_url = ''
custom_http_username = ''
custom_http_password = ''

# mqtt broker settings
mqtt_broker_address = ''
mqtt_broker_username = ''
mqtt_broker_password = ''

# adafruit ui settings
adafruit_io_username = 'Otto_Lelieveld'
adafruit_io_key = 'aio_qaVJ50YRt7A12JB2SW8vQFxnmgl5'