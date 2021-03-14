# LBP Holders

This repo is for counting the holders of RAD from LBP till now.

Here we are using ethplorer for fetching the transfer records, 
for using this script yourselves for checking the result, go to 
https://ethplorer.io/ and generate a API_KEY incase fetching
the txns with limit 10.

## `holders.json`

The `holders.json` contains the record of all transfer events
from the LBP till `Mon Mar 15 03:05:16 CST 2021`, with format:

```gql
{
    transactionHash,
    timestamp,
    value,
    from,
    to
}
```


## LICENSE

MIT
