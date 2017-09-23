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

def main():
    exchange = connect()
    write(exchange, {"type": "hello", "team": "DATAGODS"})
    hello_from_exchange = read(exchange)
    print("The exchange replied:", hello_from_exchange, file=sys.stderr)
    bond_counter=0
    while(1):
        message = read(exchange)
        print(message)
        type_of_order=message['type']
        print(type_of_order)
        if type_of_order == 'book':
            symbol = message['symbol']
            if symbol == 'BOND':
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
        if type_of_order == 'fill':
            if message[symbol]='BOND':
                if message['dir'] = 'BUY':
                    bond_counter=bond_counter+int(message['size'])
                if message['dir'] = 'SELL':
                    bond_counter=bond_counter-int(message['size'])
if __name__ == "__main__":
    main()
