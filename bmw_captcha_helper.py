#!/usr/bin/env python3
"""
BMW ConnectedDrive hCaptcha Token Generator

This script helps you generate the hCaptcha token needed for BMW ConnectedDrive authentication.
"""

import asyncio
from bimmer_connected.account import MyBMWAccount
from bimmer_connected.api.regions import Regions

async def get_captcha_token():
    """
    Instructions for getting BMW hCaptcha token:

    1. Open your web browser (Chrome/Firefox with Developer Tools)
    2. Open Developer Tools (F12) and go to the Network tab
    3. Navigate to: https://customer.bmwgroup.com/gcdm/oauth/authenticate
    4. Enter your BMW credentials (ianwilliams / Ktmexc300)
    5. Complete the hCaptcha challenge
    6. In the Network tab, look for a request containing 'hcaptcha'
    7. Find the 'h-captcha-response' value in the request
    8. Copy that token value

    Once you have the token, you can use it with the BMW API.
    """

    print("=" * 70)
    print("BMW ConnectedDrive hCaptcha Token Instructions")
    print("=" * 70)
    print()
    print("STEP 1: Open Chrome or Firefox with Developer Tools")
    print("  - Press F12 to open Developer Tools")
    print("  - Go to the 'Network' tab")
    print()
    print("STEP 2: Navigate to BMW login page")
    print("  URL: https://customer.bmwgroup.com/gcdm/oauth/authenticate")
    print()
    print("STEP 3: Enter your credentials")
    print("  Username: <your-bmw-username>")
    print("  Password: <your-bmw-password>")
    print()
    print("STEP 4: Complete the hCaptcha challenge")
    print("  - Check the hCaptcha box")
    print("  - Complete any image challenges")
    print()
    print("STEP 5: Extract the token")
    print("  - In the Network tab, filter by 'hcaptcha' or 'oauth'")
    print("  - Look for the 'h-captcha-response' parameter")
    print("  - Copy the long token string")
    print()
    print("STEP 6: Save the token")
    print("  - Store it in a secure location")
    print("  - You'll need to provide this token to the BMW API")
    print()
    print("=" * 70)
    print()
    print("Alternative Method: Use the bimmer_connected library's built-in auth:")
    print()
    print("  export HCAPTCHA_TOKEN='your-token-here'")
    print("  python3 -m bimmer_connected.cli status <your-username> --region rest_of_world")
    print()
    print("=" * 70)

if __name__ == '__main__':
    asyncio.run(get_captcha_token())
