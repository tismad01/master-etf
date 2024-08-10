from web3 import Web3
import json
from Crypto.Cipher import AES
import base64

# Connect to local blockchain (Ganache)
ganache_url = "http://127.0.0.1:8545"  # Default URL for Ganache
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Check if connection is successful
if web3.is_connected():
    print("Connected to Ethereum node")
else:
    raise Exception("Failed to connect to Ethereum node")

# Load the contract ABI and address
with open('build/contracts/SecureETL.json') as f:
    contract_json = json.load(f)
contract_abi = contract_json['abi']
contract_address = '0xed2eC9E309F77a8Ab1268020199Fc5C412aBdb93'  # Your deployed contract address

# Initialize contract
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Encryption key (must be 16, 24, or 32 bytes long)
key = b'Sixteen byte key'

def encrypt_data(data, key):
    """Encrypt data before storing on the blockchain."""
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode('utf-8'))
    return base64.b64encode(cipher.nonce + tag + ciphertext).decode('utf-8')

def decrypt_data(ciphertext, key):
    """Decrypt data retrieved from the blockchain."""
    raw = base64.b64decode(ciphertext)
    cipher = AES.new(key, AES.MODE_EAX, nonce=raw[:16])
    return cipher.decrypt(raw[32:]).decode('utf-8')

def extract_data(data, account):
    """Extract data into the blockchain."""
    encrypted_data = encrypt_data(data, key)
    tx_hash = contract.functions.extractData(encrypted_data).transact({'from': account})
    web3.eth.wait_for_transaction_receipt(tx_hash)

    # Extract data ID from transaction receipt logs
    receipt = web3.eth.get_transaction_receipt(tx_hash)
    data_id = receipt['logs'][0]['topics'][1].hex()
    return data_id

def transform_data_step1(data_id, new_data, account):
    """First step of transforming data stored in the blockchain."""
    data_id_bytes32 = Web3.to_bytes(hexstr=data_id)
    encrypted_data = encrypt_data(new_data, key)
    tx_hash = contract.functions.transformDataStep1(data_id_bytes32, encrypted_data).transact({'from': account})
    web3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_hash.hex()

def transform_data_step2(data_id, additional_data, account):
    """Second step of transforming data stored in the blockchain."""
    data_id_bytes32 = Web3.to_bytes(hexstr=data_id)
    encrypted_data = encrypt_data(additional_data, key)
    tx_hash = contract.functions.transformDataStep2(data_id_bytes32, encrypted_data).transact({'from': account})
    web3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_hash.hex()

def load_data(data_id):
    """Load data from the blockchain."""
    data_id_bytes32 = Web3.to_bytes(hexstr=data_id)
    encrypted_data = contract.functions.loadData(data_id_bytes32).call()
    return decrypt_data(encrypted_data, key)

def main():
    # Use the first Ganache account for transactions
    account = web3.eth.accounts[0]

    # Extract data
    data_id = extract_data("initial data", account)
    print(f"Extracted Data ID: {data_id}")

    # Transform data (step 1)
    transform_tx_hash1 = transform_data_step1(data_id, "transformed data step 1", account)
    print(f"Data transformed (step 1) with Transaction Hash: {transform_tx_hash1}")

    # Transform data (step 2)
    transform_tx_hash2 = transform_data_step2(data_id, "additional transformation step 2", account)
    print(f"Data transformed (step 2) with Transaction Hash: {transform_tx_hash2}")

    # Load data
    loaded_data = load_data(data_id)
    print(f"Loaded Data: {loaded_data}")

if __name__ == "__main__":
    main()
