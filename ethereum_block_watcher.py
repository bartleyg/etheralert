from __future__ import absolute_import, unicode_literals
import json
import requests
import time
import sys

from textcelery.tasks import send_text
from app.models import Alert

from web3 import Web3

from etheralert.settings import ETHERSCAN_API_KEY

URL_ETHERSCAN_API = 'https://api.etherscan.io/api?apikey=' + ETHERSCAN_API_KEY + '&module=proxy&action='


def search_block_for_receiver_addresses(block):
    #Alert.objects.filter(address=tx_address)
    for entry in Alert.objects.all():
        for tx in block['transactions']:
            if tx['to'] is None:
                # case when contract creation is transactino there is no 'to'
                continue
            elif tx['to'].lower() == entry.address.lower():
                print(' sending text to', entry.phone_number, 'for', entry.address)
                tx = convert_tx_hex_to_decimal(tx)
                send_text.apply_async((entry, tx))

def convert_tx_hex_to_decimal(tx):
    # change hex to int, wei to ETH, Decimal to string before texting
    tx['value'] = str(Web3.fromWei(int(tx['value'], 16), 'ether'))
    tx['blockNumber'] = int(tx['blockNumber'], 16)
    return tx

def get_etherscan_block_tip_number_hex():
    ACTION = 'eth_blockNumber'
    try:
        r = requests.get(URL_ETHERSCAN_API + ACTION)
        blockNumber = json.loads(r.text)['result']
    except:
        print('api error')
        return False
    # etherscan numbers are hexadecimal. we want decimal.
    return int(blockNumber, 16)

def get_etherscan_block(blockNumber):
    ACTION = 'eth_getBlockByNumber&boolean=true&tag='
    try:
        r = requests.get(URL_ETHERSCAN_API + ACTION + blockNumber)
        block = json.loads(r.text)['result']
    except:
        print('api error')
        return False
    return block


if __name__ == '__main__':
    print('running ethereum')
    firstRun = True
    lastBlockNumber = 0

    while True:
        blockNumber = get_etherscan_block_tip_number_hex()

        # only get next block if we are at least 2 behind tip (which isn't stable)
        if blockNumber > lastBlockNumber + 1:
            if not firstRun:
                block = get_etherscan_block(hex(lastBlockNumber + 1))
            else:
                block = get_etherscan_block(hex(blockNumber - 1))
                firstRun = False

            search_block_for_receiver_addresses(block)

            lastBlockNumber = int(block['number'], 16)
            print(lastBlockNumber, block['hash'])

        time.sleep(0.5)
