from azure.storage import TableService, Entity, QueueService
import time
import redis
import spidev
from tokens import *
import ptvsd
ptvsd.enable_attach('xplatDebug')

spi = spidev.SpiDev()
spi.open(0,0)

myaccount = getAccount()
mykey = getKey()

table_service = TableService(account_name=myaccount, account_key=mykey)
queue_service = QueueService(account_name=myaccount, account_key=mykey)

queue_service.create_queue('acceldata')

i = 0

TableSlotList = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42,43,44,45,46,47,48,49,50)

periods = ('a', 'b', 'c', 'd')

#table_service.insert_or_replace_entity(accel2, accel, tableSlot, periodSlot)

record = {}

#records = {'aX': generateX(),'aY': generateY(),'aZ': generateZ(),'bX': generateX(),'bY': generateY(),'bZ': generateZ(), 'cX': generateX(),'cY': generateY(),'cZ': generateZ(),'cX': generateX(),'cY': generateY(),'cZ': generateZ() }

def analog_read(channel):
	r = spi.xfer2([1, (8 + channel) << 4, 0])
	adc_out = ((r[1]&3) << 8) + r[2]
	return adc_out

while True: 
    for tableSlot in TableSlotList:
        for abcd in periods:
            time.sleep(0.1) 
            record.update({abcd+'X': analog_read(0), abcd+'Y': analog_read(1), abcd+'Z': analog_read(2)})
        print record
	
        table_service.insert_or_replace_entity('accel4', 'slot', tableSlot, record)
	queue_service.put_message('acceldata', unicode(record))

