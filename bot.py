from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
from web3 import Web3

# Replace these with your own bot token and Web3 provider
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
WEB3_PROVIDER = "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"
CONTRACT_ADDRESS = "0xYourTokenContractAddress"

# Connect to Web3
web3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER))
if not web3.isConnected():
    print("Web3 connection failed")
    exit()

# Function to check wallet balance
def get_token_balance(wallet_address: str) -> int:
    try:
        contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=[
            {"constant": True, "inputs": [{"name": "_owner", "type": "address"}], "name": "balanceOf", "outputs": [{"name": "balance", "type": "uint256"}], "type": "function"}
        ])
        balance = contract.functions.balanceOf(wallet_address).call()
        return web3.fromWei(balance, 'ether')
    except Exception as e:
        print(f"Error getting balance: {e}")
        return 0

# Command handlers
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome to the Web3 Community Bot! Use /verify <wallet_address> to get started.")

def verify(update: Update, context: CallbackContext):
    if len(context.args) != 1:
        update.message.reply_text("Usage: /verify <wallet_address>")
        return

    wallet_address = context.args[0]
    if not web3.isAddress(wallet_address):
        update.message.reply_text("Invalid wallet address. Please try again.")
        return

    balance = get_token_balance(wallet_address)
    if balance > 0:
        update.message.reply_text(f"Verification successful! Your balance: {balance} tokens.")
        # Grant access or add user to a group (can be extended)
    else:
        update.message.reply_text("Verification failed. You need at least 1 token to access this community.")

def balance(update: Update, context: CallbackContext):
    if len(context.args) != 1:
        update.message.reply_text("Usage: /balance <wallet_address>")
        return

    wallet_address = context.args[0]
    if not web3.isAddress(wallet_address):
        update.message.reply_text("Invalid wallet address. Please try again.")
        return

    balance = get_token_balance(wallet_address)
    update.message.reply_text(f"Your balance: {balance} tokens.")

def help_command(update: Update, context: CallbackContext):
    update.message.reply_text("Commands:\n/verify <wallet_address> - Verify your wallet\n/balance <wallet_address> - Check your token balance\n/help - List available commands")

# Main function to start the bot
def main():
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("verify", verify))
    dispatcher.add_handler(CommandHandler("balance", balance))
    dispatcher.add_handler(CommandHandler("help", help_command))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
