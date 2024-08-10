const SecureETL = artifacts.require("SecureETL");

module.exports = function (deployer) {
  deployer.deploy(SecureETL);
};
