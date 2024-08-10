# Blockchain-Based ETL Security Solution

This project demonstrates the use of blockchain technology to secure Extract, Transform, Load (ETL) processes. The solution utilizes Ethereum smart contracts to ensure data integrity and immutability during ETL operations.

## Project Structure


master-etf/
│
├── contracts/
│   └── ETLSecurity.sol
│
├── build/
│   └── contracts/
│       └── ETLSecurity.json  # generated after compilation
│
├── migrations/
│   └── 2_deploy_contracts.js
│
├── scripts/
│   └── etl.py
│
├── truffle-config.js
│
└── requirements.txt

- **`contracts/`**: Contains the Solidity smart contract.
- **`build/`**: Contains compiled contract JSON files (generated after compilation).
- **`migrations/`**: Contains scripts for deploying contracts.
- **`scripts/`**: Contains the Python script for interacting with the blockchain.
- **`truffle-config.js`**: Configuration file for Truffle.
- **`requirements.txt`**: Python dependencies.

## Prerequisites

Ensure you have the following tools installed:

- **Node.js** and **npm**: [Install here](https://nodejs.org/)
- **Python** and **pip**: [Install here](https://www.python.org/)
- **Ganache**: [Download GUI](https://trufflesuite.com/ganache/) or install CLI with npm
- **Truffle**: JavaScript-based framework for blockchain development
- **Web3.py**: Python library to interact with Ethereum blockchain

## Installation Steps

### 1. Set Up Ganache

1. **Install Ganache CLI (optional)**:

   npm install -g ganache-cli

2. **Run Ganache**:

    ganache-cli
Ganache provides a local Ethereum blockchain running on http://127.0.0.1:8545.

### 2. Set Up the Project

1. **Clone the repository**:

    git clone https://github.com/tismad01/master-etf.git
    cd master-etf

2. **Install Truffle globally**:

    npm install -g truffle

3. **Install project dependencies**:

    npm install

### 3. Compile and Deploy Smart Contracts

1. **Compile Smart Contracts**:

    truffle compile

2. **Deploy Contracts to Ganache**:

    truffle migrate

### 4. Run the Python Script

1. **Install Python dependencies**:

    pip install -r requirements.txt

2. **Update the etl.py script**:

    Open scripts/etl.py.
    Replace '0xMockAddress' with the deployed contract address.

3. **Execute the ETL script**:

    python scripts/etl.py

This script performs the following operations:
    Extracts data to the blockchain.
    Transforms data in the blockchain.
    Loads data from the blockchain.

The output will display transaction IDs and loaded data.
