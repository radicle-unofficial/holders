#!/usr/bin/python3
'''
Counting LBP Holders of Radicle

Block    12039504
Contract 0x31c8eacbffdd875c74b94b077895bd78cf1e64a3
FromTX   0xade852fd2265723b66198b46dd08718e1754fd0b0468ad1d25651355ef9984db
'''

import os
import sys
import calendar
import time
import json
import fire
import requests as r

LBP_START = '0xade852fd2265723b66198b46dd08718e1754fd0b0468ad1d25651355ef9984db'
LBP_END = "0xd5b0fe040bd08ea685489b3bd8e3bfe447a4b7ca7e88e513c0aa2da2057c2c7d"
TXNS = 'https://api.ethplorer.io/getTokenHistory/\
0x31c8eacbffdd875c74b94b077895bd78cf1e64a3?apiKey={KEY}&type=transfer\
&limit=1000&timestamp={TS}'
API_KEY_PATH = "API_KEY"
TXNS_PATH = "txns.json"
LBP_ORIGINAL_HOLDERS_PATH = "lbp_original_holders.json"
LBP_HOLDERS_PATH = "lbp_holders.json"


def key():
    '''
    Get API_KEY of ethplorer
    '''
    if os.path.exists(API_KEY_PATH) is False:
        return 'freekey'

    with open(API_KEY_PATH) as api_key:
        return api_key.read()


def txns(api_key, ts, history):
    '''
    Get all transfer events of Radicle from the LBP

    ## Data format
    ```json
    {
      transactionHash,
      timestamp,
      value,
      from,
      to
    }
    ```
    '''
    print('Fetching txns start at %s...' % ts)
    res = json.loads(r.get(
        TXNS.replace("{TS}", str(ts)).replace('{KEY}', api_key)
    ).text)

    # If request failed
    if 'error' in res:
        print(res['error']['message'])
        sys.exit(1)

    # Apply new format for counting
    for op in res['operations']:
        # Append to history
        history.append({
            'transactionHash': op['transactionHash'],
            'timestamp': op['timestamp'],
            'value': op['value'],
            'from': op['from'],
            'to': op['to']
        })

        # Finish fetching while reaching the initial tx of LBP
        if op['transactionHash'] == LBP_START:
            print('\n-------------------------------------\n')
            print('Total txns: %s' % len(history))
            return history

    # Keep fetching to the LBP init TX
    print('Current txns: %s' % len(history))
    return txns(api_key, history[len(history) - 1]['timestamp'], history)


def process():
    '''
    Process LBP buyers and holders
    '''
    with open(TXNS_PATH) as f:
        txns = json.loads(f.read())

    lbp = False
    buyers = {}
    sellers = set([])
    lbp_sellers = set([])

    # Get buyers and sellers
    for tx in txns:
        sellers.add(tx['from'])

        if tx['transactionHash'] == LBP_END:
            lbp = True

        if lbp is False:
            continue

        # Count lbp sellers
        lbp_sellers.add(tx['from'])

        # Count buyer and their RADs
        buyer = tx['to']
        if buyer in buyers:
            buyers[buyer] = str(int(buyers[buyer]) + int(tx['value']))
        else:
            buyers[buyer] = tx['value']

    # Write LBP contributors
    if os.path.exists(LBP_ORIGINAL_HOLDERS_PATH) is False:
        lbp_oringal_holders = dict(filter(lambda t: t[0] not in lbp_sellers, buyers.items()))
        with open(LBP_ORIGINAL_HOLDERS_PATH, 'w') as out:
            json.dump(lbp_oringal_holders, out)

    # Write LBP holders
    if os.path.exists(LBP_HOLDERS_PATH) is False:
        holders = dict(filter(lambda t: t[0] not in sellers, buyers.items()))
        with open(LBP_HOLDERS_PATH, 'w') as out:
            json.dump(holders, out)


def format_holders():
    with open(LBP_HOLDERS_PATH) as f:
        holders = json.loads(f.read())
        fmt = "".join([
            '        %s  %s\n' % (holder, value) for (holder, value) in holders.items()
        ])
        output = '''
        holder                                      Bought RADs in LBP
        -----------------------------------------------------------------------\n%s
        '''
        print(output % fmt)


class Cmd():
    def count(self):
        '''
        Count the LBP holders
        '''
        with open(LBP_ORIGINAL_HOLDERS_PATH) as f:
            lbp_original_holders = json.loads(f.read())

        with open(LBP_HOLDERS_PATH) as f:
            lbp_holders = json.loads(f.read())

        print('LBP holders:  %s' % len(lbp_holders))
        print(
            'Total Amount: %s' % (
                int(sum(int(v) for v in lbp_holders.values())) / pow(10,18))
        )
        print('LBP original holders:   %s' % len(lbp_original_holders))
        print(
            'Total Amount:           %s' % (
                int(sum(int(v) for v in lbp_original_holders.values())) / pow(10,18))
        )


    def holders(self):
        '''
        Format the LBP holders
        '''
        with open(LBP_HOLDERS_PATH) as f:
            holders = json.loads(f.read())

        fmt = "".join([
            '        %s  %s\n' % (
                holder, int(value) / pow(10, 18)
            ) for (holder, value) in holders.items()
        ])
        output = '''
        holder                                      Bought RADs in LBP
        -----------------------------------------------------------------------\n%s
        '''
        print(output % fmt)


if __name__ == '__main__':
    '''
    Fetch LBP txns and write the result to txns.json if not exists,
    the order of the data list is from now to the start of the LBP.
    '''
    if os.path.exists(TXNS_PATH) is False:
        timestamp = calendar.timegm(time.gmtime())
        with open(TXNS_PATH, 'w') as out:
            json.dump(txns(key(), timestamp, []), out)

    if os.path.exists(LBP_HOLDERS_PATH) is False:
        process()

    fire.Fire(Cmd)
