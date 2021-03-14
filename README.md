# LBP Holders

This repo is for counting the holders of RAD from LBP till now.

Here we are using ethplorer for fetching the records of transfer
events, for using this script yourselves, go to https://ethplorer.io/ 
and generate a API_KEY unless you'll fetching the txns with limit 10
in every request.

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
