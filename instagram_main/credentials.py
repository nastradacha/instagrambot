from instagram_main.modules import last_login
from lastpass import (
    Vault,
    LastPassIncorrectGoogleAuthenticatorCodeError,
    LastPassIncorrectYubikeyPasswordError,
)

DEVICE_ID = "credentials.py"
credentials = last_login(
    r"C:\Users\Nastracha\OneDrive\Documents\lastpass\credential.json"
)


def get_cred_from_lasspass(app_name):
    list_of_login_items = ["user", "pass"]
    list_from_vault = []
    username = credentials["lasspass"]["username"]
    password = credentials["lasspass"]["password"]
    try:
        # First try login without multi factor password
        vault = Vault.open_remote(username, password, None, client_id=DEVICE_ID)
    except LastPassIncorrectGoogleAuthenticatorCodeError:
        # Get the code
        multifactor_password = input("Enter Google Authenticator code:")
        # And now retry with the code
        vault = Vault.open_remote(
            username, password, multifactor_password, client_id=DEVICE_ID
        )
    except LastPassIncorrectYubikeyPasswordError:
        # Get the code
        multifactor_password = input("Enter Yubikey password:")
        # And now retry with the code
        vault = Vault.open_remote(
            username, password, multifactor_password, client_id=DEVICE_ID
        )
    for i in vault.accounts:
        # b'Instagram'
        if i.name.decode("UTF-8") == f"{app_name}":
            list_from_vault.append(i.username.decode("UTF-8"))
            list_from_vault.append(i.password.decode("UTF-8"))
    zipped_credentials = dict(zip(list_of_login_items, list_from_vault))
    return zipped_credentials


# print(get_cred_from_lasspass('Instagram'))
# passing = 'instagram'
# bingo = f"b'{passing}'"
# print(bingo)
