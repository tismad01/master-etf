import json
from cubetl import flow, fs, util, script

def cubetl_config(ctx):
    ctx.add('directorycsv.process', flow.Chain(steps=[
        fs.DirectoryList(path="C:/Users/borot/Desktop/master/rad/master-etf"), 
        fs.FileInfo(path=lambda m: m['path']),
        util.Print(),  
        script.Function(process_with_blockchain),
        util.Print()  
    ]))

def process_with_blockchain(ctx, m):
    """Funkcija koja vrši verifikaciju podataka uz pomoć blockchain-a."""
    import hashlib
    from web3 import Web3

    ganache_url = "http://127.0.0.1:8545"
    web3 = Web3(Web3.HTTPProvider(ganache_url))

    if web3.is_connected():
        print("Connected to Ethereum node")
    else:
        raise Exception("Failed to connect to Ethereum node")

    with open('build/contracts/SecureETL.json') as f:
        contract_json = json.load(f)
    contract_abi = contract_json['abi']
    contract_address = '0x1E97F9e2A8acac38314c2643cd31D23e3136559e'  # Replace with your contract address

    contract = web3.eth.contract(address=contract_address, abi=contract_abi)
    account = web3.eth.accounts[0]

    data_hash = hashlib.sha256(m['path'].encode()).hexdigest()

    tx_hash = contract.functions.storeDataHash(data_hash).transact({'from': account})
    web3.eth.wait_for_transaction_receipt(tx_hash)
    
    m['blockchain_tx'] = tx_hash.hex()
