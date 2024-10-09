from algosdk.v2client import algod
from smart_contracts.contract.main_contract import MainContract
from smart_contracts.contract.contract import GigDAOContract
from smart_contracts.contract.nft_contract import NFTMintingContract
from crypto_utils import generate_account, get_mnemonic

def main():
    # Khởi tạo Algod client
    algod_address = "http://127.0.0.1:8101"
    algod_token = "4ae95cae3a5203e9e484d92a58697170c47c1422417102ed52a885fdf224bbb5"
    algod_client = algod.AlgodClient(algod_token, algod_address)

    # Tạo tài khoản cho người triển khai
    private_key, address = generate_account()
    print(f"Địa chỉ người triển khai: {address}")
    print(f"Mnemonic của người triển khai: {get_mnemonic(private_key)}")

    # Triển khai Main Contract
    main_contract = MainContract(algod_client)
    main_app_id = main_contract.create_main_contract(address, private_key)
    print(f"Main Contract đã được triển khai với app_id: {main_app_id}")

    # Triển khai GigDAO Contract
    gig_dao_contract = GigDAOContract(algod_client)
    gig_dao_app_id = gig_dao_contract.create_gig_dao(address, private_key)
    print(f"GigDAO Contract đã được triển khai với app_id: {gig_dao_app_id}")

    # Triển khai NFT Minting Contract
    nft_minting_contract = NFTMintingContract(algod_client)
    nft_minting_app_id = nft_minting_contract.create_nft_minting_contract(address, private_key)
    print(f"NFT Minting Contract đã được triển khai với app_id: {nft_minting_app_id}")

    print("Tất cả các contract đã được triển khai thành công!")

if __name__ == "__main__":
    main()