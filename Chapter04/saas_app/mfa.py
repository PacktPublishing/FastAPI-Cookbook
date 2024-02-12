import pyotp


def generate_totp_secret():
    return pyotp.random_base32()


def generate_totp_uri(secret, user_email):
    return pyotp.totp.TOTP(secret).provisioning_uri(
        name=user_email, issuer_name="YourAppName"
    )
