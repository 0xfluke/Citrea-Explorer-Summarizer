
#NECESSARY LIBRARIES
import requests #For API calls
import web3 #For blockchain interaction
from datetime import datetime #For handling timestamps

#DEFINING VARIABLES FOR PULLING DATA (REKT)
RPC_URL = requests.get("https://rpc.testnet.citrea.xyz")
#TRANSACTION_DETAILS_URL = requests.get("https://explorer.testnet.citrea.xyz/api/v2/transactions/0x0ab39026dab5a301bd0f05ca865cd007ea737cff7fbb4c8bbdab5305ddfb8435")
#TRANSACTION_LOGS_URL = requests.get("https://explorer.testnet.citrea.xyz/api/v2/transactions/0x0ab39026dab5a301bd0f05ca865cd007ea737cff7fbb4c8bbdab5305ddfb8435/logs")

#FUCKUP-1: I realized that if I use request.get() on tx variables, I need to put the exact URL there. But I want to accept user input so I need to change that URL by removing the hash and keeping it as a string only.

#DEFINING VARIABLES FOR PULLING DATA
TRANSACTION_DETAILS_URL = "https://explorer.testnet.citrea.xyz/api/v2/transactions/"
TRANSACTION_LOGS_URL = "https://explorer.testnet.citrea.xyz/api/v2/transactions/{}/logs"