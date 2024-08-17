from etl2 import extract_data, transform_data_step1, transform_data_step2, load_data
from web3 import Web3
import json

ganache_url = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

if web3.is_connected():
    print("Connected to Ethereum node")
else:
    raise Exception("Failed to connect to Ethereum node")

account = web3.eth.accounts[0]

def test_extract_data():
    data_id = extract_data("mock data", account)
    assert data_id is not None
    print(f"Test extractData: SUCCESS, data_id: {data_id}")

def test_transform_data_step1():
    data_id = extract_data("mock data", account)
    transform_tx_hash = transform_data_step1(data_id, "transformed data", account)
    assert transform_tx_hash is not None
    print(f"Test transformDataStep1: SUCCESS, Transaction: {transform_tx_hash}")

def test_transform_data_step2():
    data_id = extract_data("mock data", account)
    transform_data_step1(data_id, "transformed data", account)
    transform_tx_hash = transform_data_step2(data_id, "added transformation", account)
    assert transform_tx_hash is not None
    print(f"Test transformDataStep2: SUCCESS, Transaction: {transform_tx_hash}")

def test_load_data():
    data_id = extract_data("initial data", account)
    
    transform_data_step1(data_id, "transformed data", account)
    loaded_data_step1 = load_data(data_id)

    assert loaded_data_step1 == "transformed data", f"Expected transformed data, but got {loaded_data_step1}"
    print("Test step 1 loadData: SUCCESS")

    transform_data_step2(data_id, "additional data", account)
    loaded_data_step2 = load_data(data_id)
    
    expected_data = "transformed dataadditional data"
    assert loaded_data_step2 == expected_data, f"Expected {expected_data}, but got {loaded_data_step2}"
    print("Test step 2 loadData: SUCCESS")

if __name__ == "__main__":
    test_extract_data()
    test_transform_data_step1()
    test_transform_data_step2()
    test_load_data()
