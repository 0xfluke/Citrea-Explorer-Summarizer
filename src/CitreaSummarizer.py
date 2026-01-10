import requests
import json
from datetime import datetime

# The base URL for the API endpoint for transactions
api_url = "https://explorer.testnet.citrea.xyz/api/v2/transactions/"

# The specific transaction hash we want to look up
tx_hash = input("Please enter the transaction hash: ")

# Construct the full URL and make the GET request
response = requests.get(f"{api_url}{tx_hash}")

# Check if the request was successful
if response.status_code == 200:
    # Convert the JSON response text into a Python dictionary
    transaction_data = response.json()
    
    # --- EXTRACT ALL THE DATA ---
    from_address = transaction_data['from']['hash']
    to_address = transaction_data['to']['hash']
    timestamp_str = transaction_data['timestamp']
    value_smallest_unit = int(transaction_data['value']) # Convert string to integer
    
    # --- PROCESS THE DATA ---
    # Convert the value to the main currency unit (assuming 18 decimal places)
    value_main_unit = value_smallest_unit / (10**18)
    
    # Convert the timestamp string into a more readable format
    # Example: "2025-10-01T00:56:02.000000Z" -> "Oct 01, 2025, 03:56 AM" (in your local timezone)
    dt_object = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
    readable_date = dt_object.astimezone().strftime("%b %d, %Y, %I:%M %p")

    # --- ASSEMBLE THE FINAL SENTENCE ---
    summary = (
        f"On {readable_date}, the address {from_address} "
        f"sent {value_main_unit:.8f} CITREA to the address {to_address}."
    )
    
    print("\n--- Transaction Summary ---")
    print(summary)

else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
