// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;


contract Ballot{
	uint public candidateCount = 0;  

  struct Candidate{
    uint id;
    string name;
    bool vote;
  }

  mapping(uint => Candidate) public candidates;
  
  constructor() public{
    createCandidate("Alice");
  }
  
  function createCandidate(string memory _content) public{
  candidateCount ++;
  candidates[candidateCount] = Candidate(candidateCount,_content, false);
  }

}
