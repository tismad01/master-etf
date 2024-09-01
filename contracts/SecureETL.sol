// SPDX-License-Identifier: MIT
pragma solidity >=0.8.19;

import {AccessControl} from '../node_modules/@openzeppelin/contracts/access/AccessControl.sol';

contract SecureETL is AccessControl {
    bytes32 public constant EXTRACTOR_ROLE = keccak256("EXTRACTOR_ROLE");
    bytes32 public constant TRANSFORMER_ROLE = keccak256("TRANSFORMER_ROLE");
    bytes32 public constant LOADER_ROLE = keccak256("LOADER_ROLE");

    struct DataRecord {
        string data;
        uint256 timestamp;
    }

    struct TransformationRecord {
        string data;
        uint256 timestamp;
        address transformer;
    }

    mapping(bytes32 => DataRecord) public dataRecords;
    mapping(bytes32 => TransformationRecord[]) public transformationHistory;
    mapping(string => bool) private existingData;

    event DataExtracted(bytes32 indexed id, string data, uint256 timestamp);
    event DataTransformed(bytes32 indexed id, string data, uint256 timestamp);
    event DataLoaded(bytes32 indexed id, string data, uint256 timestamp);

    constructor() {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(EXTRACTOR_ROLE, msg.sender);
        _grantRole(TRANSFORMER_ROLE, msg.sender);
        _grantRole(LOADER_ROLE, msg.sender);
    }

    // Function to extract data and store it on the blockchain
        function extractData(string memory data) public onlyRole(EXTRACTOR_ROLE) returns (bytes32) {
        bytes32 id = keccak256(abi.encodePacked(data, block.timestamp));
        require(!existingData[data], "Data already exists or tampered attempt detected");
        require(dataRecords[id].timestamp == 0, "Data already exists or tampered attempt detected");
        
        dataRecords[id] = DataRecord(data, block.timestamp);
        existingData[data] = true; // Mark this data as existing
        emit DataExtracted(id, data, block.timestamp);
        return id;
    }

    // First step of transforming the data
    function transformDataStep1(bytes32 id, string memory newData) public onlyRole(TRANSFORMER_ROLE) {
        require(dataRecords[id].timestamp != 0, "Data not found");
        require(keccak256(abi.encodePacked(dataRecords[id].data)) != keccak256(abi.encodePacked("restricted")), "Data transformation restricted");

        dataRecords[id].data = newData;
        dataRecords[id].timestamp = block.timestamp;
        emit DataTransformed(id, newData, block.timestamp);

        transformationHistory[id].push(TransformationRecord(newData, block.timestamp, msg.sender));
    }

    // Second step of transforming the data
    function transformDataStep2(bytes32 id, string memory additionalData) public onlyRole(TRANSFORMER_ROLE) {
        require(transformationHistory[id].length > 0, "Previous transformation required");

        dataRecords[id].data = additionalData;  
        dataRecords[id].timestamp = block.timestamp;
        emit DataTransformed(id, additionalData, block.timestamp);

        transformationHistory[id].push(TransformationRecord(additionalData, block.timestamp, msg.sender));
    }


    // Function to load data from the blockchain
    function loadData(bytes32 id) public view onlyRole(LOADER_ROLE) returns (string memory) {
        require(dataRecords[id].timestamp != 0, "Data not found");
        return dataRecords[id].data;
    }

    // Function to retrieve the transformation history for a specific data record
    function getTransformationHistory(bytes32 id) public view returns (TransformationRecord[] memory) {
        return transformationHistory[id];
    }
}
