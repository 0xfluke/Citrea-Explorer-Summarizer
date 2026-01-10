import requests
from web3 import Web3
from datetime import datetime

# --- CONFIGURATION (Update with your correct URLs) ---
RPC_URL = "https://rpc.testnet.citrea.xyz"
TRANSACTION_DETAILS_URL = "https://explorer.testnet.citrea.xyz/api/v2/transactions/"
TRANSACTION_LOGS_URL = "https://explorer.testnet.citrea.xyz/api/v2/transactions/{}/logs"

# --- TOKEN IDENTIFIER FUNCTION (No changes) ---
MINIMAL_ERC20_ABI = [{"constant":True,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"type":"function"}, {"constant":True,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"type":"function"}]
def get_token_info(token_address):
    # ... (unchanged)
    try:
        w3 = Web3(Web3.HTTPProvider(RPC_URL))
        token_address = w3.to_checksum_address(token_address)
        contract = w3.eth.contract(address=token_address, abi=MINIMAL_ERC20_ABI)
        symbol = contract.functions.symbol().call()
        decimals = contract.functions.decimals().call()
        return {"symbol": symbol, "decimals": decimals}
    except Exception as e:
        return None

# --- MAIN SCRIPT LOGIC ---
tx_hash = input("Please enter your DEX swap transaction hash: ")

details_response = requests.get(f"{TRANSACTION_DETAILS_URL}{tx_hash}")
logs_response = requests.get(TRANSACTION_LOGS_URL.format(tx_hash))

if details_response.status_code == 200 and logs_response.status_code == 200:
    tx_data = details_response.json()
    logs_data = logs_response.json()
    
    from_address = tx_data['from']['hash']
    timestamp_str = tx_data['timestamp']
    logs = logs_data.get('items', [])
    
    dt_object = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
    readable_date = dt_object.astimezone().strftime("%b %d, %Y, %I:%M %p %Z")

    # Find the main Swap event to identify the pool
    swap_log = next((log for log in logs if 'Swap' in log.get('decoded', {}).get('method_call', '')), None)

    if swap_log:
        pool_address = swap_log['address']['hash']
        transfers = [log for log in logs if 'Transfer' in log.get('decoded', {}).get('method_call', '')]

        # --- NEW, MORE ROBUST LOGIC ---
        # The token going OUT is the one transferred TO the pool
        token_out_log = next((t for t in transfers if t['decoded']['parameters'][1]['value'].lower() == pool_address.lower()), None)
        # The token coming IN is the one transferred FROM the pool
        token_in_log = next((t for t in transfers if t['decoded']['parameters'][0]['value'].lower() == pool_address.lower()), None)
        
        if token_in_log and token_out_log:
            amount_out = int(token_out_log['data'], 16)
            amount_in = int(token_in_log['data'], 16)
            
            token_out_addr = token_out_log['address']['hash']
            token_in_addr = token_in_log['address']['hash']

            info_out = get_token_info(token_out_addr)
            info_in = get_token_info(token_in_addr)

            if info_out and info_in:
                final_amount_out = amount_out / (10**info_out['decimals'])
                final_amount_in = amount_in / (10**info_in['decimals'])

                summary = (f"On {readable_date}, {from_address} used Satsuma DEX to swap "
                           f"{final_amount_out:.6f} {info_out['symbol']} for {final_amount_in:.6f} {info_in['symbol']}.")
                print("\n--- DEX Swap Summary ---")
                print(summary)
            else:
                print("Could not fetch token details.")
        else:
            print("Could not determine the incoming and outgoing tokens from the pool transfers.")
    else:
        print("Could not find a 'Swap' event in the transaction logs.")
else:
    print(f"Failed to fetch data. Details: {details_response.status_code}, Logs: {logs_response.status_code}")
