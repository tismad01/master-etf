import sys
sys.path.append(r'C:\Users\borot\Downloads\cubetl-master\cubetl-master')

import hashlib
from web3 import Web3
import json
from cubetl import flow, fs, util, script
from cubetl.core.context import Context


ganache_url = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

if web3.is_connected():
    print("Connected to Ethereum node")
else:
    raise Exception("Failed to connect to Ethereum node")

with open('build/contracts/SecureETL.json') as f:
    contract_json = json.load(f)
contract_abi = contract_json['abi']
contract_address = '0xB8bCacbC21c19b3c58D71B9Af03185D41a42B6D0'

contract = web3.eth.contract(address=contract_address, abi=contract_abi)
account = web3.eth.accounts[0]

def cubetl_config(ctx):
    ctx.add('directorycsv.process', flow.Chain(steps=[
        fs.DirectoryList(path="C:/Users/borot/Desktop/master/rad/master-etf"),
        fs.FileInfo(path=lambda m: m['path']),
        util.Print(),
        script.Function(process_with_blockchain),
        util.Print()
    ]))

def process_with_blockchain(ctx, m):
    """Process data with blockchain to ensure integrity."""
    data_hash = hashlib.sha256(m['path'].encode()).hexdigest()
    print(f"Hash before storing on blockchain: {data_hash}")

    tx_hash = contract.functions.extractData(data_hash).transact({'from': account})
    print(f"Transaction Hash: {tx_hash.hex()}")

    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    event_data = contract.events.DataExtracted().process_receipt(tx_receipt)

    data_id = event_data[0]['args']['id'].hex()  # Convert bytes to hex string
    print(f"Data ID stored on blockchain: {data_id}")

    try:
        loaded_hash = contract.functions.loadData(bytes.fromhex(data_id)).call({'from': account})
        print(f"Loaded data from blockchain: {loaded_hash}")
        if loaded_hash == data_hash:
            print("Data integrity verified with blockchain.")
        else:
            print("Data integrity failed!")
    except Exception as e:
        print(f"Error loading data from blockchain: {str(e)}")
        print("Data not found or other error in contract logic.")

    simulate_data_tampering(data_id, data_hash)

def simulate_data_tampering(data_id, original_hash):
    """Simulate tampering by modifying the data and checking blockchain integrity."""
    try:
        print(f"Attempting to tamper with data ID: {data_id}")
        tampered_data_hash = hashlib.sha256((original_hash + "tampered").encode()).hexdigest()
        print(f"Tampered Data Hash: {tampered_data_hash}")

        tx_hash = contract.functions.extractData(tampered_data_hash).transact({'from': account})
        web3.eth.wait_for_transaction_receipt(tx_hash)
        print("Tampering attempt successful - This should not happen!")
    except Exception as e:
        print("Tampering detected and prevented successfully:", e)

def run_cubetl_process(ctx, process_name):
    """Run the CubETL process."""
    ctx.run(process_name)

def test_cubetl_with_blockchain():
    """Test the CubETL process with blockchain."""
    print("Running CubETL process with blockchain verification...")
    ctx = Context()
    cubetl_config(ctx)
    run_cubetl_process(ctx, 'directorycsv.process')
    print("CubETL process completed. Data integrity verified with blockchain.")

def test_cubetl_without_blockchain():
    """Test the CubETL process without blockchain."""
    print("Running CubETL process without blockchain verification...")
    
    ctx = Context()
    
    ctx.add('directorycsv.process', flow.Chain(steps=[
        fs.DirectoryList(path="C:/Users/borot/Desktop/master/rad/master-etf"),
        fs.FileInfo(path=lambda m: m['path']),
        script.Function(lambda ctx, m: simulate_data_tampering(m['path'], hashlib.sha256(m['path'].encode()).hexdigest())),  # Simulate tampering
        util.Print()
    ]))
    
    run_cubetl_process(ctx, 'directorycsv.process')
    print("CubETL process completed without blockchain verification. Data integrity not guaranteed.")

if __name__ == "__main__":
    test_cubetl_without_blockchain()
    test_cubetl_with_blockchain()
