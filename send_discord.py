import requests
import os
import datetime
import time
import json
from threading import Timer

class DiscordAutomaticSender:
    def __init__(self):
        self.tokens = []
        self.token_status = {}
        self.wallet_address = []
        self.channel_id = 1322383092153057311
        self.is_running = True
        self.current_token_index = 0
        self.token_file = "tokens.txt"
        self.wallet_file = "wallets.txt"

    def banner(self):
        logo = r"""
    __  ___                      
   /  |/  /___ _____  ____ _____ 
  / /|_/ / __ `/ __ \/ __ `/ __ \
 / /  / / /_/ / / / / /_/ / /_/ /
/_/  /_/\__,_/_/ /_/\__, /\____/ 
                   /____/        
"""
        print(logo)

    def load_tokens(self):
        try:
            if not os.path.exists(self.token_file):
                raise FileNotFoundError(f"Token file '{self.token_file}' not found.")
            
            with open(self.token_file, "r") as file:
                tokens = [line.strip() for line in file if line.strip()]

            if not tokens:
                raise ValueError("No tokens found in the token file.")
            
            print(f"Loaded {len(tokens)} tokens from {self.token_file}")

            return tokens

        except Exception as e:
            print(f"Error loading tokens: {str(e)}")
            return []
        
    def load_wallets(self):
        try:
            if not os.path.exists(self.wallet_file):
                raise FileNotFoundError(f"Wallet file '{self.wallet_file}' not found.")
            
            with open(self.wallet_file, "r") as file:
                wallets = [line.strip() for line in file if line.strip()]

            if not wallets:
                raise ValueError("No wallets found in the wallet file.")
            
            print(f"Loaded {len(wallets)} wallets from {self.wallet_file}")

            return wallets

        except Exception as e:
            print(f"Error loading wallets: {str(e)}")
            return []
        
    def verify_token(self, token):
        headers = {
            'Authorization': f'{token}',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.207.132.170 Safari/537.36'
        }

        try:
            response = requests.get(
                'https://discord.com/api/v9/users/@me',
                headers=headers
            )

            if response.status_code == 200:
                user_data = response.json()
                return True, user_data.get('username'), user_data.get('discriminator')
            
            return False, None, None

        except Exception as e:
            print(f"Error verifying token: {str(e)}")
            return False, None, None
    
    def setup(self):
        
        self.banner()
        print("Mango Faucet Multi-Token & Address Automatic Claimer")
        print("\n")

        print("=" * 80)
        self.tokens = self.load_tokens()
        self.wallet_address = self.load_wallets()
        print("=" * 80)
        print('Verifying tokens...')
        valid_tokens = []
        for token in self.tokens:
            is_valid, username, discriminator = self.verify_token(token)
            if is_valid:
                valid_tokens.append(token)
                self.token_status[token] = {
                    'username': username,
                    'discriminator': discriminator,
                    'current_wallet_index': 0,
                    'message_sent': 0
                }

                print(f"Token {token[:5]}***{token[-5:]} is valid. Username: {username}#{discriminator}")
            else:
                print(f"Token {token[:5]}***{token[-5:]} is invalid., Skipping...")
        self.tokens = valid_tokens
        if not self.tokens:
            print("No valid tokens found. Exiting...")
            return False
        
        if not self.wallet_address:
            print("No wallet addresses found. Exiting...")
            return False

        return True
    
    def send_message(self, token, wallet):
        headers = {
            'Authorization': f'{token}',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.207.132.170 Safari/537.36'
        }

        try:
            message = f"<@1322128247550640130> {wallet}"

            payload = {
                'content': message
            }

            response = requests.post(
                f"https://discord.com/api/v9/channels/{self.channel_id}/messages",
                headers=headers,
                json=payload
            )

            if response.status_code == 200:
                self.token_status[token]['message_sent'] += 1
                return True
            else:
                print(f"Failed to send message for token {self.token_status[token]['username']} and wallet {wallet}")
                print(f"Response status code: {response.status_code}, Response text: {response.text}")
                return False
            
        except Exception as e:
            print(f"Error sending message: {str(e)}")
            return False
        
    def process_token(self, token):
        status = self.token_status[token]
        username = status['username']

        for wallet in self.wallet_address:
            if not self.is_running:
                return False

            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"Discord username: {username}")
            print(f"Wallet: {wallet}")
            print(f"Time: {current_time}")

            if self.send_message(token, wallet):
                print("Message sent successfully.")
            else:
                print("Failed to send message, trying next wallet in 30 seconds...")
                time.sleep(30)

        return True

    def display_countdown(self, seconds):
        start_time = time.time()
        while time.time() - start_time < seconds and self.is_running:
            time_left = seconds - int(time.time() - start_time)
            hours = time_left // 3600
            minutes = (time_left % 3600) // 60
            second = time_left % 60

            countdown_text = "Waiting for next cycle | "
            countdown_text += f"{hours:02d}:{minutes:02d}:{second:02d}"

            print(f"\r{countdown_text:<80}", end="", flush=True)
            
            time.sleep(1)

        print("\r" + " " * 80, end="", flush=True)

    def process_all_tokens(self):
        for token in self.tokens:
            if not self.is_running:
                return False
            if not self.process_token(token):
                return False

        return True

    def run(self):
        if not self.setup():
            return
        
        print("=" * 80)
        print(f"Total valid tokens: {len(self.tokens)}")
        print(f"Total wallets: {len(self.wallet_address)}")
        print("Interval: 6 hours and 1 minutes")
        print("=" * 80)

        while self.is_running:
            print("Starting cycle..., sending messages...")

            if self.process_all_tokens():
                print("=" * 80)
                print("All tokens was processed successfully.")
                print("Starting countdown and wait for next cycle...")
                self.display_countdown(6 * 3600 + 1 * 60)
            else:
                print("=" * 80)
                print("Error processing tokens, stopping program...")
                break

    def stop(self):
        self.is_running = False
        print('\n')
        print("=" * 80)
        print("Program has stopped.")
        print("Statistic: ")
        print(f'Accounts: {len(self.token_status)}')
        print(f"Message sent: {sum(status['message_sent'] for status in self.token_status.values())}")

if __name__ == "__main__":
    sender = DiscordAutomaticSender()
    try:
        sender.run()
    except KeyboardInterrupt:
        sender.stop()
    except Exception as e:
        print(f"Error: {str(e)}")
        sender.stop()