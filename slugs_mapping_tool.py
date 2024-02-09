crypto_mapping_top50 = {
    "bitcoin": "BTC-USD",
    "ethereum": "ETH-USD",
    "tether": "USDT-USD",
    "bnb": "BNB-USD",
    "solana": "SOL-USD",
    "xrp": "XRP-USD",
    "usd-coin": "USDC-USD",
    "steth": "STETH-USD",
    "cardano": "ADA-USD",
    "dogecoin": "DOGE-USD",
    "avalanche": "AVAX-USD",
    "metagamz": "BRIT-USD",
    "tron": "TRX-USD",
    "wrapped-tron": "WTRX-USD",
    "chainlink": "LINK-USD",
    "polkadot-new": "DOT-USD",
    "toncoin": "TON11419-USD",
    "polygon": "MATIC-USD",
    "wrapped-bitcoin": "WBTC-USD",
    "shiba-inu": "SHIB-USD",
    "multi-collateral-dai": "DAI-USD",
    "litecoin": "LTC-USD",
    "internet-computer": "ICT-USD",
    "bitcoin-cash": "BCH-USD",
    "unus-sed-leo": "LEO-USD",
    "uniswap": "UNI7083-USD",
    "cosmos": "ATOM-USD",
    "ethereum-classic": "ETC-USD",
    "stellar": "XLM-USD",
    "okb": "OKB-USD",
    "injective": "INJ-USD",
    "optimism-ethereum": "OP-USD",
    "monero": "XMR-USD",
    "near-protocol": "NEAR-USD",
    "aptos": "APT21794-USD",
    "first-digital-usd": "FDUSD-USD",
    "filecoin": "FIL-USD",
    "wrapped-eos": "WEOS-USD",
    "celestia": "TIA22861-USD",
    "lido-dao": "LDO-USD",
    "hedera": "HBAR-USD",
    "wrapped-hedera": "WHBAR-USD",
    "immutable": "IMX10603-USD",
    "kaspa": "KAS-USD",
    "arbitrum": "ARB11841-USD",
    "bitcoin-bep2": "BTCB-USD",
    "mantle": "MNT27075-USD",
    "stacks": "STX4847-USD",
    "cronos": "CRO-USD",
    "vechain": "VET-USD"
}

#Function to convert user input (e.g. bitcoin) to ticker symbols (e.g. BTC-USD)
def convert_to_tickers(user_input, mapping):
    return [mapping[currency.lower()] for currency in user_input if currency.lower() in mapping]


#Inverse function to the function above (e.g. BTC-USD -> bitcoin)
def convert_to_names(mapping):
    return {v: k for k, v in mapping.items()}


#Control process to check if all keys are in list of slugs
if __name__ == "__main__":
    from api_functions import get_crypto_slugs
    #Get all CMC API slugs
    slugs = get_crypto_slugs()

    #Control function to check if key is in list of slugs
    def print_keys_not_in_list(dictionary, list_to_check):
       keys_not_in_list = [key for key in dictionary.keys() if key not in list_to_check]
       return keys_not_in_list

    #Print keys missing in list of slugs
    keys_not_in_slugs = print_keys_not_in_list(crypto_mapping_top50, slugs)
    print("Keys not in slugs list:", keys_not_in_slugs)