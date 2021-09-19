// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

/**
 * @title Ballot
 * @dev Implements voting process along with vote delegation
 */
contract Ballot {
    struct Participant {
        uint256 uid;
        string selection;
        uint256 timestamp;
    }

    struct Option {
        string name;
        uint256 id;
        uint256 voteCount;
    }

    Participant[] public participants;

    mapping(string => uint256) optionsDir;
    Option[] public options;

    function getOptions() public view returns (Option[] memory) {
        return options;
    }

    function getParticipants() public view returns (Participant[] memory) {
        return participants;
    }

    /**
     * @dev Create a new ballot from possible options.
     * @param availableOptions list of selectable options
     */
    constructor(string[] memory availableOptions) {
        for (uint256 i = 0; i < availableOptions.length; i++) {
            createOption(availableOptions[i]);
        }
    }

    /**
     * @dev Create a possible option to vote on
     * @param name list of selectable options
     */
    function createOption(string memory name) public {
        optionsDir[name] = options.length;
        options.push(Option({name: name, id: options.length, voteCount: 0}));
    }

    function hasVoted(uint256 uid) public view returns (bool) {
        for (uint256 i = 0; i < participants.length; i++) {
            if (participants[i].uid == uid) return false;
        }
        return true;
    }

    /**
     * @dev Vote on an available option
     * @param uid unique id of voter
     * @param option name of the option
     * @param timestamp time of vote
     */
    function vote(
        uint256 uid,
        string memory option,
        uint256 timestamp
    ) public {
        require(!hasVoted(uid), "DiVA>> You have already voted.");

        participants.push(Participant(uid, option, timestamp));
        options[optionsDir[option]].voteCount++;
    }

    /**
     * @dev Computes the winning option taking all previous votes into account.
     * @return winner the winning option with its vote count.
     */
    function getWinner() public view returns (Option memory winner) {
        uint256 winningVoteCount = 0;
        uint256 winnerIndex = 0;
        for (uint256 p = 0; p < options.length; p++) {
            if (options[p].voteCount > winningVoteCount) {
                winningVoteCount = options[p].voteCount;
                winnerIndex = p;
            }
        }
        winner = options[winnerIndex];
    }
}
