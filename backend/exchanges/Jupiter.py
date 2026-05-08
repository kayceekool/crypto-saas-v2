import requests

JUPITER_QUOTE_API = "https://quote-api.jup.ag/v6/quote"

SOL_MINT = "So11111111111111111111111111111111111111112"

USDC_MINT = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"

def get_jupiter_quote(
    input_mint=USDC_MINT,
    output_mint=SOL_MINT,
    amount=1000000
):

    try:

        params = {
            "inputMint": input_mint,
            "outputMint": output_mint,
            "amount": amount,
            "slippageBps": 50
        }

        response = requests.get(
            JUPITER_QUOTE_API,
            params=params,
            timeout=10
        )

        return response.json()

    except Exception as e:

        return {
            "error": str(e)
        }