var ballot = artifacts.require("./Ballot.sol")

module.exports = function(deployer){
  deployer.deploy(ballot);
};
