# Blockchain-Based ETL Security Solution

This project demonstrates the use of blockchain technology to secure Extract, Transform, Load (ETL) processes. The solution utilizes Ethereum smart contracts to ensure data integrity and immutability during ETL operations.

It showcases a robust integration of blockchain technology to enhance the security of ETL processes. By leveraging Ethereum smart contracts, the solution ensures data integrity and provides a secure, tamper-proof method for data handling in ETL operations.

## Project Structure

```bash
master-etf/
│
├── contracts/
│   └── ETLSecurity.sol
│   └── SecureETL.sol
│   └── SimpleContract.sol
│
├── build/
│   └── contracts/
│       └── ETLSecurity.json  # all generated after compilation
│       └── SecureETL.json 
│       └── SimpleContract.json  
│
├── migrations/
│   └── 2_deploy_contracts.js
│   └── 2_deploy_secure_etl.js
│
├── scripts/
│   └── etl.py
│   └── etl2.py
│   └── etlTest.py
│   └── etl2Test.py
│   ├── cubetlTest.py             
│   └── cubetl_config.py  
│
├── truffle-config.js
│
└── requirements.txt
```

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
- **CubETL**: Framework and tool for data ETL (Extract, Transform and Load) in Python [Download from here](https://github.com/jjmontesl/cubetl)

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

    Open scripts/etl.py, scripts/etl2.py and/or scripts/cubetlTest.py.
    Replace '0xMockAddress' with the deployed contract addresses from the migration output.

3. **Execute the ETL scripts**:

    python scripts/etl.py 

This script performs the following operations:
    Extracts data to the blockchain.
    Transforms data in the blockchain.
    Loads data from the blockchain.

    python scripts/etl2.py

This script performs the following operations with role-based access control:
    Extracts data with role enforcement.
    Applies multiple transformation steps, each requiring specific roles.
    Loads and retrieves transformed data, ensuring only authorized roles can access it.
    The output will display transaction IDs, role validations, and loaded data.

The output will display transaction IDs and loaded data.

### 5. Run the tests

1. **Test the basic ETL process**:

    python scripts/etlTest.py

This test script checks:
    Data extraction to the blockchain.
    Data transformation on the blockchain.
    Data loading from the blockchain.

2. **Test the role-based secure ETL process**:

    python scripts/etl2Test.py

This test script checks:
    Data extraction with role enforcement.
    Multi-step data transformation with role enforcement.
    Data loading with role-based access control.

3. **Test the role-based secure ETL process**:

    python scripts/cubetlTest.py

This script simulates an ETL process using CubETL without blockchain verification, demonstrating potential tampering scenarios as well as the integration of CubETL with blockchain to ensure data integrity and resistance to tampering. It verifies that the ETL process is secure and data remains immutable.
