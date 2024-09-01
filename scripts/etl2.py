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
contract_address = '0xB8bCacbC21c19b3c58D71B9Af03185D41a42B6D0'  # Your deployed contract address

# Initialize contract
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Encryption key (must be 16, 24, or 32 bytes long)
key = b'Sixteen byte key'

def encrypt_data(data, key):
    """Encrypt data before storing on the blockchain."""
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode('latin-1'))
    return base64.b64encode(cipher.nonce + tag + ciphertext).decode('latin-1')

def decrypt_data(ciphertext, key):
    """Decrypt data retrieved from the blockchain."""
    raw = base64.b64decode(ciphertext)
    cipher = AES.new(key, AES.MODE_EAX, nonce=raw[:16])
    decrypted_data = cipher.decrypt(raw[32:])  
    return decrypted_data.decode('latin-1')

def extract_data(data, account):
    """Extract data into the blockchain."""
    encrypted_data = encrypt_data(data, key)
    tx_hash = contract.functions.extractData(encrypted_data).transact({'from': account})
    web3.eth.wait_for_transaction_receipt(tx_hash)

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
    current_encrypted_data = contract.functions.loadData(data_id_bytes32).call()
    decrypted_data = decrypt_data(current_encrypted_data, key)
    combined_data = decrypted_data + additional_data
    encrypted_data = encrypt_data(combined_data, key)
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
