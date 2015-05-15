import time

from tokens import *
from helperFunctions import *
from azure.storage import TableService, Entity, QueueService

import spidev
spi = spidev.SpiDev()
spi.open(0,0)


myaccount = getAccount()
mykey = getKey()

table_service = TableService(account_name=myaccount, account_key=mykey)

TableSlotNeutral = return_list_generator(0,999)
TableSlotShaking = return_list_generator(1000, 1999) 
TableSlotSpinning = return_list_generator(2000, 2999)

periods = ('a', 'b', 'c', 'd')
record = {}

table_service.create_table(getMLTableName())

def analog_read(channel):
        r = spi.xfer2([1, (8 + channel) << 4, 0])
        adc_out = ((r[1]&3) << 8) + r[2]
        return adc_out

a_r = analog_read

while True: 
    x = get_input_type()
    print x
    if x == 'n':
        print 'In 5 seconds start neutral'
        print 'send 2000 points of data to ML set marked neutral'
        time.sleep(5.0)
        print 'START'
        time.sleep(0.5)
        for tableSlot in TableSlotNeutral:
	    print tableSlot
            for abcd in periods:
                time.sleep(0.2)
                record.update({abcd+'X': a_r(0), abcd+'Y': a_r(1), abcd+'Z': a_r(2)})
            print record
            table_service.insert_or_replace_entity(getMLTableName(), 'NEUTRAL', tableSlot, record)

    elif x == 's':
        print 'In 5 seconds start shaking'
        print 'send 2000 points of data to ML set marked shaking'
        time.sleep(5.0)
        print 'START'
        time.sleep(0.5)
        for tableSlot in TableSlotShaking:
            print tableSlot
            for abcd in periods:
                time.sleep(0.2)
                record.update({abcd+'X': a_r(0), abcd+'Y': a_r(1), abcd+'Z': a_r(2)})
            print record
            table_service.insert_or_replace_entity(getMLTableName(), 'SHAKING', tableSlot, record)
    
    elif x == 'a':
	print 'In 5 seconds start being spinning'
	print 'send 2000 points of data to ML set marked spinning'
	time.sleep(5.0)
	print 'START'
	time.sleep(0.5)
	for tableSlot in TableSlotSpinning:
	    print tableSlot
	    for abcd in periods:
		time.sleep(0.2)
		record.update({abcd+'X': a_r(0), abcd+'Y': a_r(1), abcd+'Z': a_r(2)})
	    print record
	    table_service.insert_or_replace_entity(getMLTableName(), 'SPINNING', tableSlot, record)	

		


