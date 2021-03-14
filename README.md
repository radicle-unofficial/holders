# LBP Holders

This repo is for counting the holders of RAD from LBP till block `12039504`.

Here we are using ethplorer for fetching the records of transfer
events, for using this script yourselves, go to https://ethplorer.io/ 
and generate a API_KEY unless you'll fetching the txns with limit 10
in every request.

Feel free to modify or contribute to this script.


## Result

```
LBP holders:  1097
Total Amount: 1079558.0705975965
```

## Files

Here are several files genereated by this script at Block Number
12039504, you can view or re-generate using this `main.py`.


* `txns.json`

The `holders.json` contains the record of all transfer events
from the LBP till block `12039504`, with format:

```gql
{
    transactionHash,
    timestamp,
    value,
    from,
    to
}
```


* `lbp_buyers.json`

Addresses who bought RAD in the LBP


* `lbp_contributors.json`

Addresses who bought RAD in the LBP


* `lbp_holders.json`

Addresses who bought RAD and didn't sell them till block 12039504


## LICENSE

MIT
