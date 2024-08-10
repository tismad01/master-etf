const ETLSecurity = artifacts.require("ETLSecurity");

/**
 * @dev Deploys the ETLSecurity contract to the Ethereum blockchain.
 */
module.exports = function(deployer) {
    deployer.deploy(ETLSecurity);
};
