**Citrea-Explorer-Summarizer**
In previous version, we created a simple summary around:
- FROM
- TO
- VALUE
- TIMESTAMP

Data from a transaction on Citrea blockchain. To take this one step forward, we wanted to display a summary that can automatically detect the interacted contracts and show the related protocol name and action.

In v2, we analyzed the SWAP function of Satsuma DEX through their SwapRouter contract.

We defined an example output like this:
"On {timestamp}, {from_address} used Satsuma DEX to swap {value_cbtc} cBTC for {value_usdc} USDC."

In order to understand the process and define it in a code, we analyzed a simple swap transaction on Satsuma.

So far, I found 2 types of transactions on Satsuma:
1) Any Token other than cBTC <> Any Token
2) cBTC <> Any Token

We clasify those seperately because those transactions generate different amount of transfer events.
The first transaction creates the following events:
- AlgebraPool sends WCBTC to SwapRouter
- User sends X Token to "AlgebraPool"
- "AlgebraPool" sends Y Token to User
- SwapRouter sends WCBTC back to AlgebraPool
