# contract.py
import time
import uuid
from smart_contracts._helpers.crypto_utils import CryptoUtils
from smart_contracts.contract.nft_contract import NFTMintingContract
from algosdk.v2client import algod
from algosdk import transaction
from algosdk import mnemonic
import os

class GigDAOContract:
    def __init__(self, algod_client, aes_key):
        self.algod_client = algod_client
        self.crypto_utils = CryptoUtils(aes_key)  # Đảm bảo rằng aes_key là mã hóa Base64
        self.dao_members = {}
        self.proposals = {}
        self.pooled_funds = 0.0
        self.reputation_scores = {}
        self.dao_initialized = False
        self.dao_name = ""
        self.dao_description = ""
        self.voting_quorum = 0.5

    def add_member(self, user_id, account_address, private_key):
        encrypted_address = self.crypto_utils.encrypt(account_address)
        encrypted_key = self.crypto_utils.encrypt(private_key)

        self.dao_members[user_id] = {
            'encrypted_address': encrypted_address,
            'encrypted_key': encrypted_key,
            'contributions': 0,
            'reputation': 0
        }
        print(f"Added member {user_id} with encrypted credentials.")

    def get_account_address(self, user_id):
        if user_id not in self.dao_members:
            raise Exception("User not found.")
        encrypted_address = self.dao_members[user_id]['encrypted_address']
        return self.crypto_utils.decrypt(encrypted_address)  # Bỏ decode()
    
    def get_private_key(self, user_id):
        if user_id not in self.dao_members:
            raise Exception("User not found.")
        encrypted_key = self.dao_members[user_id]['encrypted_key']
        return self.crypto_utils.decrypt(encrypted_key)  # Bỏ decode()

    def create_dao(self, name: str, description: str, voting_quorum: float = 0.5):
        if self.dao_initialized:
            raise Exception("DAO is already initialized.")

        if not name or not description:
            raise ValueError("DAO name and description cannot be empty.")
        
        self.dao_name = name
        self.dao_description = description
        self.voting_quorum = voting_quorum
        self.dao_initialized = True

        print(f"DAO '{self.dao_name}' initialized with description: '{self.dao_description}' and voting quorum: {self.voting_quorum * 100}%.")
    
    def is_dao_initialized(self):
        return self.dao_initialized

    def join_dao(self, user_id):
        if user_id not in self.dao_members:
            self.dao_members[user_id] = {'contributions': 0, 'reputation': 0}
            print(f"{user_id} joined the DAO.")
        else:
            print(f"{user_id} is already a member.")

    def create_proposal(self, user_id, proposal_details):
        if user_id not in self.dao_members:
            raise Exception("User must be a member to create a proposal.")
        proposal_id = len(self.proposals) + 1
        self.proposals[proposal_id] = {
            'details': proposal_details,
            'votes': {'yes': 0, 'no': 0},
            'status': 'active'
        }
        print(f"Proposal {proposal_id} created.")

    def vote(self, proposal_id, user_id, vote_option):
        if proposal_id not in self.proposals:
            raise Exception("Proposal does not exist.")
        if user_id not in self.dao_members:
            raise Exception("User must be a member to vote.")
        if self.proposals[proposal_id]['status'] != 'active':
            raise Exception("Voting is closed for this proposal.")

        if vote_option.lower() not in ['yes', 'no']:
            raise Exception("Invalid vote option.")
        
        self.proposals[proposal_id]['votes'][vote_option] += 1
        print(f"{user_id} voted {vote_option} on Proposal {proposal_id}.")

    def finalize_proposal(self, proposal_id):
        if proposal_id not in self.proposals:
            raise Exception("Proposal does not exist.")
        if self.proposals[proposal_id]['status'] != 'active':
            raise Exception("Proposal already finalized.")

        total_votes = self.proposals[proposal_id]['votes']['yes'] + self.proposals[proposal_id]['votes']['no']
        if total_votes == 0:
            print("No votes were cast.")
            return

        if self.proposals[proposal_id]['votes']['yes'] > self.proposals[proposal_id]['votes']['no']:
            self.proposals[proposal_id]['status'] = 'passed'
            print(f"Proposal {proposal_id} passed.")
        else:
            self.proposals[proposal_id]['status'] = 'failed'
            print(f"Proposal {proposal_id} failed.")

    def deposit_funds(self, user_id, amount):
        if user_id not in self.dao_members:
            raise Exception("User must be a member to deposit funds.")
        self.pooled_funds += amount
        self.dao_members[user_id]['contributions'] += amount
        print(f"{user_id} deposited {amount} ALGO.")

    def get_fund_balance(self):
        return self.pooled_funds

    def distribute_funds(self, proposal_id, recipient_address):
        if proposal_id not in self.proposals:
            raise Exception("Proposal does not exist.")
        
        if self.proposals[proposal_id]['status'] != 'passed':
            raise Exception("Proposal must be passed to distribute funds.")

        if self.proposals[proposal_id].get('funds_distributed', False):
            raise Exception("Funds have already been distributed for this proposal.")

        amount_to_distribute = self.calculate_funds_to_distribute(proposal_id)

        if amount_to_distribute > 0:
            print(f"Distributing {amount_to_distribute} ALGO to {recipient_address} for Proposal {proposal_id}.")
            self.proposals[proposal_id]['funds_distributed'] = True
        else:
            print("No funds available to distribute.")

    def calculate_funds_to_distribute(self, proposal_id):
        total_votes = self.proposals[proposal_id]['votes']['yes'] + self.proposals[proposal_id]['votes']['no']
        
        if total_votes == 0:
            print("No votes have been cast for this proposal.")
            return 0

        yes_votes = self.proposals[proposal_id]['votes']['yes']
        percentage_approved = (yes_votes / total_votes) * 100
        
        allocation_percentage = 0.0
        
        if percentage_approved > 75:
            allocation_percentage = 0.75
        elif percentage_approved > 50:
            allocation_percentage = 0.50
        else:
            allocation_percentage = 0.25

        funds_to_distribute = self.pooled_funds * allocation_percentage
        print(f"Calculated funds to distribute for Proposal {proposal_id}: {funds_to_distribute} ALGO.")
        return funds_to_distribute

    def issue_nft(self, member_id):
        if member_id not in self.dao_members:
            raise Exception("User must be a member to issue an NFT.")
        
        # Tạo một phiên bản mock của Algod client
        nft_contract = NFTMintingContract(self.algod_client)
        nft_contract.mint_nft(member_id)