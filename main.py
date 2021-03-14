'''
Counting LBP Holders of Radicle

BlockNO  11927445
Contract 0x31c8eacbffdd875c74b94b077895bd78cf1e64a3
Date     Feb-25-2021 04:39:03 PM +UTC
FromTX   0xade852fd2265723b66198b46dd08718e1754fd0b0468ad1d25651355ef9984db
'''
import os
import calendar
import time
import json
import requests as r

LBP = '0xade852fd2265723b66198b46dd08718e1754fd0b0468ad1d25651355ef9984db'
TXNS = 'https://api.ethplorer.io/getTokenHistory/\
0x31c8eacbffdd875c74b94b077895bd78cf1e64a3?apiKey={KEY}&type=transfer\
&limit=1000&timestamp={TS}'
API_KEY_PATH = "API_KEY"


def key():
    '''
    Get API_KEY of ethplorer
    '''
    if os.path.exists(API_KEY_PATH) is False:
        return 'freekey'

    with open("API_KEY") as api_key:
        return api_key.read()


def txns(api_key, timestamp, history):
    '''
    Get all txns of Radicle
    '''
    print(f'Fetching txns start at {timestamp}...')
    res = r.get(TXNS.replace("{TS}", str(timestamp)).replace('{KEY}', api_key))
    ops = json.loads(res.text)['operations']

    # Apply new format for counting
    for operation in ops:
        # Finish fetching while reaching the initial tx of LBP
        if operation['transactionHash'] == LBP:
            return history

        # Append to history
        history.append({
            'timestamp': operation['timestamp'],
            'value': operation['value'],
            'from': operation['from'],
            'to': operation['to']
        })

    # Keep fetching to the LBP init TX
    print(f'Currentt txns: {len(history)}')
    return txns(key, history[len(history) - 1]['timestamp'], history)


def main():
    '''
    Main FN
    '''
    timestamp = calendar.timegm(time.gmtime())
    with open('holders.json') as out:
        json.dump(txns(key(), timestamp, []), out)


main()
