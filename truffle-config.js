module.exports = {
  networks: {
    development: {
      host: "127.0.0.1",
      port: 8545, // Updated port number
      network_id: "*", // Match any network id
      gas: 6721975, // Set a high gas limit
      gasPrice: 20000000000 // 20 Gwei (default)
    },
  },
  compilers: {
    solc: {
      version: "0.8.19", // Use a compatible Solidity version
      settings: {
        optimizer: {
          enabled: true,
          runs: 200 // Optimize for how many times you intend to run the code
        },
      },
    },
  },
};
