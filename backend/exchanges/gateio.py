def execute_gate_trade(symbol, amount):

    return {
        "exchange": "gateio",
        "symbol": symbol,
        "amount": amount,
        "status": "paper_mode"
    }