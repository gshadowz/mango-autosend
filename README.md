# Mango Network Autoclaim Discord

## Feature
- Support multi discord account and wallet

## How to use
- Register to Mango Network first, consider to use my [Referral Link](https://task.testnet.mangonetwork.io/?invite=NfWtDM) 

- Join Mango Network discord server [by clicking this Link](https://discord.gg/mangonetwork)

- Get your discord account auth token, tutorial [Click this](https://www.androidauthority.com/get-discord-token-3149920/)

- If all the steps above is done, make tokens.txt and store your discord auth token
    ```bash
    nano tokens.txt
    ```

- After that make wallets.txt and copy your Mango wallet address, store it in wallets.txt
    ```bash
    nano wallets.txt
    ```

- Run the program by typing
    - For linux
        ```bash
        python3 send_discord.py
        ```
    - For windows and termux
        ```bash
        python send_discord.py
        ```

- Done, interval for each message is automaticaly set at 6 hours 1 minutes (Following the slow mode applied in the channel)
