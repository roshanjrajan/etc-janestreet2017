#!/usr/bin/python
from __future__ import print_function

import sys
import socket
import json
import random

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("test-exch-DATAGODS", 25000))
    return s.makefile('rw', 1)

def write(exchange, obj):
    json.dump(obj, exchange)
    exchange.write("\n")

def read(exchange):
    return json.loads(exchange.readline())

def submit(exchange,t_t, symbol, orderType, price, number):
	orderID = random.randint(1, 10**5)
	write(exchange, {"type": t_t, "order_id": orderID, "symbol": symbol, "dir": orderType, "price": price, "size": number})

def trash_strat(priceVale, numberVale, priceValbz, numberValbz):
    can = priceVale * numberVale + 10
    number=min(numberValbz,numberVale)
    bz_value = priceValbz * number - 10
    vale_value = priceVale * number
    if vale_value>bz_value:
        return(1)
    elif bz_value>vale_value:
        return(0)
    return(23)

def main():
    v_tran = 0
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
            if symbol == 'BOND':
	        print(message)
                for sell_order in message['sell']:
                    if int(sell_order[0])<1000:
                            orderID=random.randint(1, 10**5)
                            write(exchange, {"type": "add", "order_id": orderID, "symbol": "BOND", "dir": "BUY", "price": sell_order[0], "size": sell_order[1]})
                for buy_order in message['buy']:
                    if int(buy_order[0])>=1002:
                        orderID=random.randint(1, 10**5)
                        number_being_sold=buy_order[1]
                        if bond_counter>number_being_sold:
                            write(exchange, {"type": "add", "order_id": orderID, "symbol": "BOND", "dir": "SELL", "price": buy_order[0], "size": number_being_sold})
            if symbol =='VALBZ':
                if len(message['sell']):
                    VALBZ_price=message['sell'][0][0]
                    VALBZ_number=message['sell'][0][1]
                    v_tran += 1

            if symbol == 'VALE':
                if len(message['sell']):
		    VALE_price=message['sell'][0][0]
                    VALE_number=message['sell'][0][1]
                    v_tran +=1
            if(v_tran == 2):
                v_trade=trash_strat(VALE_price,VALE_number,VALBZ_price,VALBZ_number)
                if v_trade==1:
                    submit(exchange, 'add','VALBZ', 'BUY', VALBZ_price, min(VALBZ_number,VALE_number))
                    submit(exchange, 'add','VALE', 'SELL', VALE_price, min(VALBZ_number,VALE_number))
                elif v_trade==0:
                    submit(exchange, 'add','VALE', 'BUY', VALE_price, min(VALBZ_number,VALE_number))
                    submit(exchange, 'add','VALBZ', 'SELL', VALBZ_price, min(VALBZ_number,VALE_number))
                v_tran = 0

        if type_of_order == 'fill':
            if message['symbol']=='BOND':
                if message['dir']== 'BUY':
                    print(message)
		    bond_counter=bond_counter+int(message['size'])
                if message['dir'] == 'SELL':
		    print(message)
                    bond_counter=bond_counter-int(message['size'])
		if message['symbol']=='VALBZ' or message['symbol']=='VALE':
                    if message['dir']== 'BUY':
                        print(message)
                        write(exchange, {"type": 'convert', "order_id":random.randint(1, 10**5) , "symbol": message['symbol'], "dir": "SELL", "size": message['size']})
	if type_of_order=='ack':
		print(message)
#	if type_of_order=='reject':
#		print(message)
	if type_of_order=='error':
		print(message)

if __name__ == "__main__":
    main()
