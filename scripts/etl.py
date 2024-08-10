# File: scripts/etl.py

from web3 import Web3
import json

# Connect to local blockchain (Ganache)
ganache_url = "http://127.0.0.1:8545"  # Default URL for Ganache
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Check if connection is successful
if web3.is_connected():
    print("Connected to Ethereum node")
else:
    raise Exception("Failed to connect to Ethereum node")

# Load the contract ABI and address
with open('build/contracts/ETLSecurity.json') as f:
    contract_json = json.load(f)
contract_abi = contract_json['abi']
contract_address = '0xD5d0cc481d5da27CA4C907b7F1D538f53D510A4d'  # Replace with your deployed contract address

# Initialize contract
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

def extract_data(data, account):
    """Extract data into the blockchain."""
    tx_hash = contract.functions.extractData(data).transact({'from': account})
    web3.eth.wait_for_transaction_receipt(tx_hash)

    # Extract data ID from transaction receipt logs
    receipt = web3.eth.get_transaction_receipt(tx_hash)
    # Find the event log with 'DataExtracted' and extract the data ID
    data_id = receipt['logs'][0]['topics'][1].hex()  # Assuming the first log is the correct one
    return data_id

def transform_data(data_id, new_data, account):
    """Transform data stored in the blockchain."""
    # Convert data_id to bytes32
    data_id_bytes32 = Web3.to_bytes(hexstr=data_id)

    tx_hash = contract.functions.transformData(data_id_bytes32, new_data).transact({'from': account})
    web3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_hash.hex()

def load_data(data_id):
    """Load data from the blockchain."""
    # Convert data_id to bytes32
    data_id_bytes32 = Web3.to_bytes(hexstr=data_id)

    data = contract.functions.loadData(data_id_bytes32).call()
    return data

def main():
    # Use the first Ganache account for transactions
    account = web3.eth.accounts[0]

    # Extract data
    data_id = extract_data("initial data", account)
    print(f"Extracted Data ID: {data_id}")

    # Transform data
    transform_tx_hash = transform_data(data_id, "transformed data", account)
    print(f"Data transformed with Transaction Hash: {transform_tx_hash}")

    # Load data
    loaded_data = load_data(data_id)
    print(f"Loaded Data: {loaded_data}")

if __name__ == "__main__":
    main()
