#!/usr/bin/python
from __future__ import print_function

import sys
import socket
import json
import random
vale_list=[]
valbz_list=[]
fp_days=120
def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("test-exch-DATAGODS", 25000))
    return s.makefile('rw', 1)

def write(exchange, obj):
    json.dump(obj, exchange)
    exchange.write("\n")

def read(exchange):
    return json.loads(exchange.readline())

def vale_strat(priceVale):
    vale_list.append(priceVale)
    if(len(vale_list) >= fp_days):
        vale_list.pop(0)
    
    fair_vale = sum(vale_list)/len(vale_list)
    print(fair_vale)
    if(priceVale<fair_vale):
        return(1)
    elif(priceVale>fair_vale):
        return(0)

def valbz_strat(priceValbz):
    valbz_list.append(priceValbz)	
    if(len(valbz_list) >= fp_days):
	valbz_list.pop(0)
    fair_valbz = sum(valbz_list)/len(valbz_list)
    print(fair_valbz)
    if(priceValbz<fair_valbz):
        return(1)
    elif(priceValbz>fair_valbz):
        return(0)


def main():
    exchange = connect()
    write(exchange, {"type": "hello", "team": "DATAGODS"})
    hello_from_exchange = read(exchange)
    print("The exchange replied:", hello_from_exchange, file=sys.stderr)
    bond_counter=0
    while(1):
        message = read(exchange)
        type_of_order=message['type']
        if type_of_order == 'book':
	    symbol = message['symbol']
            #if symbol == 'BOND':
	        #print(message)
            #    for sell_order in message['sell']:
            #        if int(sell_order[0])<1000:
            #                orderID=random.randint(1, 10**5)
            #                write(exchange, {"type": "add", "order_id": orderID, "symbol": "BOND", "dir": "BUY", "price": sell_order[0], "size": sell_order[1]})
            #    for buy_order in message['buy']:
            #        if int(buy_order[0])>=1002:
            #            orderID=random.randint(1, 10**5)
            #            number_being_sold=buy_order[1]
            #            if bond_counter>number_being_sold:
            #                write(exchange, {"type": "add", "order_id": orderID, "symbol": "BOND", "dir": "SELL", "price": buy_order[0], "size": number_being_sold})
            if symbol =='VALBZ':
		print(message)
		if len(message['sell']):
                    VALBZ_price=message['sell'][0][0]
                    VALBZ_number=message['sell'][0][1]
                    if valbz_strat(VALBZ_price):
			print('VALBZ_BUY')
                        orderID=random.randint(1, 10**5)
                        print({"type": "add", "order_id": orderID, "symbol": "VALBZ", "dir": "BUY", "price": VALBZ_price, "size": VALBZ_number})
			write(exchange, {"type": "add", "order_id": orderID, "symbol": "VALBZ", "dir": "BUY", "price": VALBZ_price, "size": VALBZ_number})


            if symbol == 'VALE':
		print(message)
                if len(message['sell']):
		    VALE_price=message['sell'][0][0]
                    VALE_number=message['sell'][0][1]
                    if vale_strat(VALE_price):
                        print('VALEBUY')
                        orderID=random.randint(1, 10**5)
                        print( {"type": "add", "order_id": orderID, "symbol": "VALE", "dir": "BUY", "price": VALE_price, "size": VALE_number})
			write(exchange, {"type": "add", "order_id": orderID, "symbol": "VALE", "dir": "BUY", "price": VALE_price, "size": VALE_number})


            #if ValBZ_strat(priceVal,priceValb,numberVal,numberValb)== 1 :
            #    write(exchange, {"type": "add", "order_id": orderID, "symbol": "VALBZ", "dir": "BUY", "price": sell_order[0], "size": sell_order[1]})
            #    write(exchange, {"type": "add", "order_id": orderID, "symbol": "VALE", "dir": "BUY", "price": sell_order[0], "size": sell_order[1]})


        if type_of_order == 'fill':
		if message['symbol']=='VALBZ' or message['symbol']=='VALE':
                	if message['dir']== 'BUY':
                    		print(message)
				bond_counter=bond_counter+int(message['size'])
                	if message['dir'] == 'SELL':
				print(message)
                    		bond_counter=bond_counter-int(message['size'])
	if type_of_order=='ack':
		print(message)
	if type_of_order=='reject':
		print(message)
	if type_of_order=='error':
		print(message)

if __name__ == "__main__":
    main()
