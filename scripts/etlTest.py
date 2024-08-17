from etl import extract_data, transform_data, load_data
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

def test_transform_data():
    data_id = extract_data("mock data", account)
    transform_tx_hash = transform_data(data_id, "transformed data", account)
    assert transform_tx_hash is not None
    print(f"Test transformData: SUCCESS, Transaction: {transform_tx_hash}")

def test_load_data():
    data_id = extract_data("mock data", account)
    load_data_output = load_data(data_id)
    assert load_data_output == "mock data"
    print(f"Test loadData: SUCCESS, Data: {load_data_output}")

if __name__ == "__main__":
    test_extract_data()
    test_transform_data()
    test_load_data()
