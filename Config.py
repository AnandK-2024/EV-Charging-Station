'''
* \copyright
* MIT License
*
* Copyright (c) 2022 Infineon Technologies AG
*
* Permission is hereby granted, free of charge, to any person obtaining a copy
* of this software and associated documentation files (the "Software"), to deal
* in the Software without restriction, including without limitation the rights
* to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
* copies of the Software, and to permit persons to whom the Software is
* furnished to do so, subject to the following conditions:
*
* The above copyright notice and this permission notice shall be included in all
* copies or substantial portions of the Software.
*
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
* IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
* FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
* AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
* LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
* OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
* SOFTWARE
*
* \endcopyright
'''

RPC_ADDRESS = 'http://3.65.2.22:80'

contract_address = "0xA438B1783dee7A3F2edF939A9a9a6D4d2F42b7bD"

abi='''
[
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "UniqueStationId",
				"type": "uint256"
			},
			{
				"indexed": true,
				"internalType": "address",
				"name": "user_address",
				"type": "address"
			},
			{
				"indexed": false,
				"internalType": "string",
				"name": "registration_Status",
				"type": "string"
			}
		],
		"name": "LogRegisterStation",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "address",
				"name": "user_address",
				"type": "address"
			},
			{
				"indexed": false,
				"internalType": "string",
				"name": "registration_Status",
				"type": "string"
			}
		],
		"name": "LogRegisterUser",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "FeeCollected",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "string",
				"name": "charging_Status",
				"type": "string"
			}
		],
		"name": "LogStartCharging",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"internalType": "string",
				"name": "transaction_status",
				"type": "string"
			},
			{
				"indexed": false,
				"internalType": "string",
				"name": "feedback",
				"type": "string"
			}
		],
		"name": "LogStopCharging",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "uint64",
				"name": "UniqueStationId",
				"type": "uint64"
			},
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "location",
				"type": "string"
			},
			{
				"internalType": "uint8",
				"name": "PowerSupply",
				"type": "uint8"
			},
			{
				"internalType": "string",
				"name": "chargingType",
				"type": "string"
			},
			{
				"internalType": "uint8",
				"name": "priceRate",
				"type": "uint8"
			}
		],
		"name": "RegisterChargingStation",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "uint8",
				"name": "Age",
				"type": "uint8"
			},
			{
				"internalType": "string",
				"name": "Gender",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "Contact_number",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "Email",
				"type": "string"
			}
		],
		"name": "RegisterUser",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "UniqueStationId",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "current_time",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "slot_time",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "time_operation",
				"type": "uint256"
			}
		],
		"name": "StartCharging",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "UniqueStationId",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "current_time",
				"type": "uint256"
			}
		],
		"name": "StopCharging",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "Owner",
				"type": "address"
			},
			{
				"internalType": "uint8",
				"name": "pricerate",
				"type": "uint8"
			}
		],
		"name": "UpdatePriceRate",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "Charging_Station_owner_Details",
		"outputs": [
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "uint8",
				"name": "Age",
				"type": "uint8"
			},
			{
				"internalType": "string",
				"name": "Gender",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "Contact_number",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "Email",
				"type": "string"
			},
			{
				"internalType": "bool",
				"name": "Status_of_Registration",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "EV_Users_Details",
		"outputs": [
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "uint8",
				"name": "Age",
				"type": "uint8"
			},
			{
				"internalType": "string",
				"name": "Gender",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "Contact_number",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "Email",
				"type": "string"
			},
			{
				"internalType": "bool",
				"name": "Status_of_Registration",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "UniqueStationId",
				"type": "uint256"
			}
		],
		"name": "PriceRate",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "Station_Registration_Details",
		"outputs": [
			{
				"internalType": "uint64",
				"name": "UniqueStationId",
				"type": "uint64"
			},
			{
				"components": [
					{
						"internalType": "string",
						"name": "name",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "location",
						"type": "string"
					},
					{
						"internalType": "uint8",
						"name": "PowerSupply",
						"type": "uint8"
					},
					{
						"internalType": "string",
						"name": "chargingType",
						"type": "string"
					}
				],
				"internalType": "struct EVcharging.StationDetails",
				"name": "Station_details",
				"type": "tuple"
			},
			{
				"internalType": "enum EVcharging.availability",
				"name": "Availability",
				"type": "uint8"
			},
			{
				"internalType": "uint256",
				"name": "PriceRate",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "slotTime",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "FeeCollected",
				"type": "uint256"
			},
			{
				"internalType": "address payable",
				"name": "Owner",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "TimeOperation",
				"type": "uint256"
			},
			{
				"internalType": "address payable",
				"name": "CurrentUser",
				"type": "address"
			},
			{
				"internalType": "bool",
				"name": "StatusOfRegistration",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "Station_Registration_DetailsID",
		"outputs": [
			{
				"internalType": "uint64",
				"name": "UniqueStationId",
				"type": "uint64"
			},
			{
				"components": [
					{
						"internalType": "string",
						"name": "name",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "location",
						"type": "string"
					},
					{
						"internalType": "uint8",
						"name": "PowerSupply",
						"type": "uint8"
					},
					{
						"internalType": "string",
						"name": "chargingType",
						"type": "string"
					}
				],
				"internalType": "struct EVcharging.StationDetails",
				"name": "Station_details",
				"type": "tuple"
			},
			{
				"internalType": "enum EVcharging.availability",
				"name": "Availability",
				"type": "uint8"
			},
			{
				"internalType": "uint256",
				"name": "PriceRate",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "slotTime",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "FeeCollected",
				"type": "uint256"
			},
			{
				"internalType": "address payable",
				"name": "Owner",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "TimeOperation",
				"type": "uint256"
			},
			{
				"internalType": "address payable",
				"name": "CurrentUser",
				"type": "address"
			},
			{
				"internalType": "bool",
				"name": "StatusOfRegistration",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]
'''