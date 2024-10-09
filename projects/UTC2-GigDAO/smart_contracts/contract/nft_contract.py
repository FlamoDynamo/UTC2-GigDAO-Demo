
from algosdk.mnemonic import to_private_key
from algosdk.v2client import algod
from algosdk.encoding import decode_address
from algosdk import transaction
from algosdk import encoding, account, mnemonic

class NFTMintingContract:
    def __init__(self, algod_client, creator_mnemonic):
        self.algod_client = algod_client
        self.creator_mnemonic = creator_mnemonic
        self.creator_private_key = to_private_key(creator_mnemonic)
        # Lấy địa chỉ công khai từ khóa riêng tư
        self.creator_address = account.address_from_private_key(self.creator_private_key)

    def mint_nft(self, member_id, nft_name, nft_url, nft_description):
        # 1. Xác định các thuộc tính của NFT
        asset_params = {
            "total": 1,
            "default_frozen": False,
            "unit_name": "NFT",
            "asset_name": nft_name,
            "manager": self.creator_address,
            "reserve": self.creator_address,
            "clawback": self.creator_address,
            "url": nft_url,
            "metadata_hash": None,  # Có thể băm metadata nếu cần
            "decimals": 0,
            "strict_empty_address_check": False,
        }

        # 2. Tạo giao dịch minting NFT
        try:
            # Lấy thông tin về tài khoản và trạng thái mạng
            suggested_params = self.algod_client.suggested_params()

            # Tạo giao dịch tạo tài sản mới (NFT)
            txn = transaction.AssetCreateTxn(
                sender=self.creator_address,
                sp=suggested_params,
                total=asset_params["total"],
                default_frozen=asset_params["default_frozen"],
                unit_name=asset_params["unit_name"],
                asset_name=asset_params["asset_name"],
                manager=asset_params["manager"],
                reserve=asset_params["reserve"],
                clawback=asset_params["clawback"],
                url=asset_params["url"],
                metadata_hash=asset_params["metadata_hash"],
                decimals=asset_params["decimals"],
            )

            # 3. Ký và gửi giao dịch
            signed_txn = txn.sign(self.creator_private_key)
            txid = self.algod_client.send_transaction(signed_txn)
            print(f"Transaction ID: {txid}")

            # 4. Xác nhận giao dịch
            print(f"Transaction sent with ID: {txid}")
            transaction.wait_for_confirmation(self.algod_client, txid)
            print("NFT minted successfully!")
            return txid
        except Exception as e:
            print(f"Error minting NFT: {e}")
            return None

# def create_nft_contract(algod_token, algod_address, creator_mnemonic):
#     # Khởi tạo `algod_client`
#     algod_client = algod.AlgodClient(algod_token, algod_address)

#     # Tạo đối tượng NFTMintingContract
#     nft_contract = NFTMintingContract(algod_client, creator_mnemonic)

#     return nft_contract

# # Sử dụng hàm
# algod_token = "4ae95cae3a5203e9e484d92a58697170c47c1422417102ed52a885fdf224bbb5"
# algod_address = "http://127.0.0.1:8101"
# creator_mnemonic = "tree river prefer carry lift together charge priority cloud oxygen model twin hockey citizen deputy baby flip security bullet dry seat concert special about pride"

# nft_contract = create_nft_contract(algod_token, algod_address, creator_mnemonic)

def create_nft_contract(creator_mnemonic):
    # Sử dụng AlgoExplorer public API cho testnet
    algod_address = "https://testnet-api.algoexplorer.io"
    algod_token = ""  # Không cần token cho AlgoExplorer public API

    # Khởi tạo `algod_client`
    algod_client = algod.AlgodClient(algod_token, algod_address)

    # Kiểm tra kết nối
    try:
        status = algod_client.status()
        print(f"Connected to Algorand testnet. Status: {status}")
    except Exception as e:
        print(f"Failed to connect to Algorand testnet: {e}")
        return None

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

    # Tạo đối tượng NFTMintingContract
    nft_contract = NFTMintingContract(algod_client, creator_mnemonic)

    return nft_contract

# Sử dụng hàm
creator_mnemonic = "tree river prefer carry lift together charge priority cloud oxygen model twin hockey citizen deputy baby flip security bullet dry seat concert special about pride"  # Thay thế bằng mnemonic thực từ tài khoản testnet của bạn

nft_contract = create_nft_contract(creator_mnemonic)

if nft_contract:
    print("NFT contract created successfully!")
else:
    print("Failed to create NFT contract.")