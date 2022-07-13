// SPDX-License-Identifier: MIT
// This is working !!!

pragma solidity ^0.6.0;

contract SimpleStorage {
    uint256 favoriteNumber = 5; //will initialised with null if not declared
    bool favoriteBool = false;
    string favoriteString = "string";
    int256 favoriteint = -5;
    address favoriteAdress = 0x4fCC5058b5B64f7218444F41ba26fFbE08eE3088;
    bytes32 favoriteBytes = "cat";
    //Struct
    struct People {
        uint256 favoriteNumber;
        string name;
    }
    People public person = People({favoriteNumber: 2, name: "Shashwatesh"}); // for a single

    //for a group of persons using array
    People[] public people;

    //Mappings
    mapping(string => uint256) public nameToFavoriteNumber;

    function store(uint256 _favoriteNuber) public {
        favoriteNumber = _favoriteNuber;
    }

    function retrieve() public view returns (uint256) {
        return favoriteNumber;
    }

    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(People({favoriteNumber: _favoriteNumber, name: _name}));
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }
}
