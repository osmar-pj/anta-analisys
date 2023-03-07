from datetime import datetime
# pip install wialon
from wialon.sdk import WialonSdk, WialonError, SdkException
import pandas as pd
"""
WialonSDK example usage
"""
# Initialize Wialon instance


def login():
    sdk = WialonSdk(
        is_development=True,
        scheme='https',
        host='hst-api.wialon.com'
    )

    try:
        # If you haven't a token, you should use our token generator
        token = ''
        # https://goldenmcorp.com/resources/token-generator
        sdk.login(token)
        return sdk
        # sdk.logout()
    except SdkException as e:
        print(f'Sdk related error: {e}')
    except WialonError as e:
        print(f'Wialon related error: {e}')
    except Exception as e:
        print(f'Python error: {e}')