'''
Counting LBP Holders of Radicle

BlockNO  11927445
Contract 0x31c8eacbffdd875c74b94b077895bd78cf1e64a3
Date     Feb-25-2021 04:39:03 PM +UTC
FromTX   0xade852fd2265723b66198b46dd08718e1754fd0b0468ad1d25651355ef9984db
'''
import os
import sys
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

    with open(API_KEY_PATH) as api_key:
        return api_key.read()


def txns(api_key, timestamp, history):
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
    print(f'Fetching txns start at {timestamp}...')
    res = json.loads(r.get(
        TXNS.replace("{TS}", str(timestamp)).replace('{KEY}', api_key)
    ).text)

    # If request failed
    if 'error' in res:
        print(res['error']['message'])
        sys.exit(1)

    # Apply new format for counting
    for operation in res['operations']:
        # Finish fetching while reaching the initial tx of LBP
        if operation['transactionHash'] == LBP:
            print(f'Total txns: {len(history)}')
            return history

        # Append to history
        history.append({
            'transactionHash': operation['transactionHash'],
            'timestamp': operation['timestamp'],
            'value': operation['value'],
            'from': operation['from'],
            'to': operation['to']
        })

    # Keep fetching to the LBP init TX
    print(f'Current txns: {len(history)}')
    return txns(api_key, history[len(history) - 1]['timestamp'], history)


def main():
    '''
    Main FN
    '''
    timestamp = calendar.timegm(time.gmtime())
    with open('holders.json', 'w') as out:
        json.dump(txns(key(), timestamp, []), out)


main()
