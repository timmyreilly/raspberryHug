from azure.storage import TableService, Entity, QueueService
import time
import redis
import spidev
from tokens import *


spi = spidev.SpiDev()
spi.open(0,0)

myaccount = getAccount()
mykey = getKey()

#table_service = TableService(account_name=myaccount, account_key=mykey)
queue_service = QueueService(account_name=myaccount, account_key=mykey)

queue_service.create_queue('acceldata')

i = 0

#TableSlotList = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, $

periods = ('a', 'b', 'c', 'd')

#table_service.insert_or_replace_entity(accel2, accel, tableSlot, periodSlot)

record = {}

#records = {'aX': generateX(),'aY': generateY(),'aZ': generateZ(),'bX': generateX(),'bY': generateY(),'bZ': generateZ(), 'cX': generateX(),'$

def analog_read(channel):
        r = spi.xfer2([1, (8 + channel) << 4, 0])
        adc_out = ((r[1]&3) << 8) + r[2]
        return adc_out

a_r = analog_read

while True:
	for abcd in periods: 
		time.sleep(0.2)
		record.update({abcd+'X': a_r(0), abcd+'Y': a_r(1), abcd+'Z': a_r(2)})
		print record
	print sorted(record)
	queue_service.put_message('acceldata', unicode(record))



