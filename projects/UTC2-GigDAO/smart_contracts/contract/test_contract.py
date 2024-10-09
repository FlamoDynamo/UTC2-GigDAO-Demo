# test_contract.py
import pytest
from smart_contracts.contract.contract import GigDAOContract
from smart_contracts.contract.nft_contract import NFTMintingContract
from smart_contracts.contract.nft_contract import create_nft_contract
from algosdk.v2client import algod
from algosdk.mnemonic import to_private_key
from algosdk.encoding import decode_address

class MockAlgodClient:
    def __init__(self):
        pass

@pytest.fixture
def gig_dao():
    # Tạo một phiên bản mới của GigDAOContract cho mỗi bài kiểm tra
    mock_algod = MockAlgodClient()
    aes_key = "GByT3lmFRnLg68bm6oq5is6v4j42kxyniHJRg+sqw40="
    return GigDAOContract(mock_algod, aes_key)

def test_initialize_dao(gig_dao):
    gig_dao.create_dao("Test DAO", "This is a test DAO.")
    assert gig_dao.is_dao_initialized() is True

def test_add_member(gig_dao):
    gig_dao.add_member("user_1", "user_1_address", "user_1_private_key")
    assert "user_1" in gig_dao.dao_members

def test_get_account_address(gig_dao):
    gig_dao.add_member("user_1", "user_1_address", "user_1_private_key")
    account_address = gig_dao.get_account_address("user_1")
    assert account_address == "user_1_address"

def test_get_private_key(gig_dao):
    gig_dao.add_member("user_1", "user_1_address", "user_1_private_key")
    private_key = gig_dao.get_private_key("user_1")
    assert private_key == "user_1_private_key"

def test_join_dao(gig_dao):
    gig_dao.join_dao("user_1")
    assert "user_1" in gig_dao.dao_members

def test_create_proposal(gig_dao):
    gig_dao.add_member("user_1", "user_1_address", "user_1_private_key")
    gig_dao.create_proposal("user_1", "Proposal details")
    assert len(gig_dao.proposals) == 1

def test_vote(gig_dao):
    gig_dao.add_member("user_1", "user_1_address", "user_1_private_key")
    gig_dao.create_proposal("user_1", "Proposal details")
    gig_dao.vote(1, "user_1", "yes")
    assert gig_dao.proposals[1]['votes']['yes'] == 1

def test_finalize_proposal(gig_dao):
    gig_dao.add_member("user_1", "user_1_address", "user_1_private_key")
    gig_dao.create_proposal("user_1", "Proposal details")
    gig_dao.vote(1, "user_1", "yes")
    gig_dao.finalize_proposal(1)
    assert gig_dao.proposals[1]['status'] == 'passed'

def test_deposit_funds(gig_dao):
    gig_dao.add_member("user_1", "user_1_address", "user_1_private_key")
    gig_dao.deposit_funds("user_1", 100)
    assert gig_dao.get_fund_balance() == 100

def test_distribute_funds(gig_dao):
    gig_dao.add_member("user_1", "user_1_address", "user_1_private_key")
    gig_dao.deposit_funds("user_1", 100)
    gig_dao.create_proposal("user_1", "Proposal details")
    gig_dao.vote(1, "user_1", "yes")
    gig_dao.finalize_proposal(1)
    gig_dao.distribute_funds(1, "recipient_address")

def test_issue_nft():
    # Sử dụng mnemonic từ tài khoản testnet của ví Pera
    creator_mnemonic = "tree river prefer carry lift together charge priority cloud oxygen model twin hockey citizen deputy baby flip security bullet dry seat concert special about pride"  # Thay thế bằng mnemonic thực từ tài khoản testnet của bạn

    # Sử dụng AlgoExplorer public API cho testnet
    algod_address = "https://testnet-api.algoexplorer.io"
    algod_token = ""  # Không cần token cho AlgoExplorer public API
    algod_client = algod.AlgodClient(algod_token, algod_address)

    # Kiểm tra kết nối
    try:
        status = algod_client.status()
        print(f"Connected to Algorand testnet. Status: {status}")
    except Exception as e:
        print(f"Failed to connect to Algorand testnet: {e}")
        return  # Kết thúc test nếu không thể kết nối

    # Lấy địa chỉ từ mnemonic
    creator_private_key = mnemonic.to_private_key(creator_mnemonic)
    creator_address = account.address_from_private_key(creator_private_key)
    print(f"Creator address: {creator_address}")

    # Kiểm tra số dư
    try:
        account_info = algod_client.account_info(creator_address)
        balance = account_info.get('amount')
        print(f"Account balance: {balance} microAlgos")
        if balance < 1000000:  # 1 Algo
            print("Warning: Account balance might be too low for transactions")
    except Exception as e:
        print(f"Failed to get account info: {e}")

    # Khởi tạo đối tượng NFTMintingContract
    nft_contract = NFTMintingContract(algod_client, creator_mnemonic)

    # Thực hiện mint NFT với các tham số cần thiết
    nft_name = "My Test NFT"
    nft_description = "This is a test NFT on Algorand testnet."
    nft_image_url = "https://i.imgur.com/FaP7k26.png"  # Sử dụng HTTPS URL

    try:
        print("Attempting to mint NFT...")
        result = nft_contract.mint_nft("member_1", nft_name, nft_image_url, nft_description)
        print(f"Minting result: {result}")
    except Exception as e:
        print(f"Exception occurred while minting NFT: {e}")
        raise  # Re-raise the exception to fail the test

    # Kiểm tra kết quả
    assert result is not None, f"Minting NFT failed. Result: {result}"
    print("NFT minting successful!")