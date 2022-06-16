import os
from hashlib import sha256
from ecdsa import SigningKey, SECP256k1, VerifyingKey
from Crypto.Hash import RIPEMD160
import bitcoinlib


def generate():
    # Generating a Private/Public Key Pair
    privkey = SigningKey.generate(curve=SECP256k1)
    pubkey = privkey.verifying_key

    pubkeyToAddr(pubkey)

    directory = os.getcwd()
    directory1 = f'{directory}\\Keys'
    os.mkdir(directory1)

    with open("Keys\\PrivateKey.pem", "wb") as f:
        f.write(privkey.to_pem())
    with open("Keys\\PublicKey.pem", "wb") as f:
        f.write(pubkey.to_pem())


def pubkeyToAddr(pubkey):
    # SHA-256 hash of the Public Key
    pubkey_hash = sha256(pubkey.to_string()).hexdigest()

    # RIPEMD-160 hashing on the result of SHA-256 public key
    h = RIPEMD160.new()
    h.update(pubkey_hash.encode())
    # Adding version byte (00)
    res = "00" + h.hexdigest()

    # 2 times SHA-256 hash for RIPEMD-160 hash with version byte
    res2 = sha256(sha256(res.encode()).hexdigest().encode()).hexdigest()

    # Adding CheckSum
    res3 = res + res2[:8]

    # Base58 encoding to obtain a P2PKH address
    addr = bitcoinlib.keys.Address(res3, encoding='base58', script_type='p2pkh')
    return addr.address


def getAddress():
    pubkey = VerifyingKey.from_pem(open("Keys\\PublicKey.pem").read())
    return pubkeyToAddr(pubkey)
