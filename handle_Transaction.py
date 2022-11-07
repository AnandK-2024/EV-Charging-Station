'''
* \copyright
* MIT License
*
* Copyright (c) 2022 Infineon Technologies AG
*
* Permission is hereby granted, free of charge, to any person obtaining a copy
* of this software and associated documentation files (the "Software"), to deal
* in the Software without restriction, including without limitation the rights
* to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
* copies of the Software, and to permit persons to whom the Software is
* furnished to do so, subject to the following conditions:
*
* The above copyright notice and this permission notice shall be included in all
* copies or substantial portions of the Software.
*
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
* IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
* FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
* AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
* LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
* OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
* SOFTWARE
*
* \endcopyright
'''

from blocksec2go import select_app, verify_pin, generate_signature, get_key_info, generate_keypair
from eth_account._utils.legacy_transactions import serializable_unsigned_transaction_from_dict, encode_transaction
from blocksec2go import open_pyscard, CardError


# method to derive and return signature prefix, which is used to encode signed transaction
def get_signature_prefix( signature_rs, address, transaction_hash, chainId, web3 ):
    try:
        r, s = signature_rs
    except:
        print( "Invalid signature argument!" )
        raise SystemExit()


    s = Canonicalise(s)

    v = chainId * 2 + 35
    if web3.eth.account._recover_hash( bytes( transaction_hash ), vrs=( v, r, s ) ) != address:
        v = chainId * 2 + 36
        if web3.eth.account._recover_hash( bytes( transaction_hash ), vrs=( v, r, s ) ) != address:
            print( "Could not verify the signature" )
            raise SystemExit()

    print("v : ", v)
    print("r : ", r)
    print("s : ", s)

    return v,s

# EIP-2 https://eips.ethereum.org/EIPS/eip-2
# All transaction signatures whose s-value is greater than secp256k1n/2 are now considered invalid.
# This Method will Canonicalise the s value of signature
def Canonicalise(s_value):
  n = 115792089237316195423570985008687907852837564279074904382605163141518161494337
  nHalf = n//2

  if s_value > nHalf:
    s_value = n - s_value

  return s_value

# method to get r and s components from signature returned from card
def get_signature_components( der_encoded_signature ):
    # check signature lengthl
    if len( der_encoded_signature ) < 2:
        print( "Invalid signature!" )
        raise SystemExit
    # if does not start with signature DER TAG
    if not der_encoded_signature.startswith( b'\x30' ):
        print( "Invalid signature!" )
        raise SystemExit
    # get signature length
    sig_len = der_encoded_signature[1]
    if sig_len != len( der_encoded_signature[2:] ):
        print( "Signature length incorrect" )
        raise SystemExit

    pos = 2
    components = []
    while sig_len > 0:
        # if does not start with component DER TAG
        if der_encoded_signature[pos] != 0x02:
            print( "Expecting component DER TAG" )
            raise SystemExit
        pos += 1
        # get the component length
        component_len = der_encoded_signature[pos]
        pos += 1
        # get the component
        components.append( int.from_bytes( der_encoded_signature[pos:pos+component_len], byteorder='big' ) )
        pos += component_len
        sig_len = sig_len - component_len - 2

    return components

# method to derive Ethereum address from public key at given index
def getAddressAtIndex(reader, web3, account_from_key_Index):

    reader.connection.connect()

    # Proprietary Command of ACS Reader :  command sets the timeout parameter of the contactless chip response time, P2 = FF [Wait until the contactless chip responds]
    r = reader.transceive(b'\xFF\x00\x41\xFF').check()
    print("Set ACS Reader Time Out Parameter Response : ", r)

    select_app(reader)
    global_counter, counter, public_key_sec1 = get_key_info( reader, account_from_key_Index)
    inf_card_addr = ""
    key_id = ""
    if(public_key_sec1 != b""):
        inf_card_addr = web3.toChecksumAddress( web3.keccak( public_key_sec1[1:] )[-20:].hex() )
        key_id = account_from_key_Index
    else:
        key_id = generate_keypair(reader)
        global_counter, counter, public_key_sec1 = get_key_info( reader, key_id)

        if(public_key_sec1 != b""):
            inf_card_addr = web3.toChecksumAddress( web3.keccak( public_key_sec1[1:] )[-20:].hex() )
        else:
            raise Exception("KEY GENERATION FAILURE",'Failed to Generate Key on Security2Go Starterkit R1.')

    reader.connection.disconnect()
    return inf_card_addr, key_id

# method to generate signature on transaction dict and return encoded signed transaction, and account from address
def getSignedTransaction(reader, web3, transaction, keyIndex, inf_card_addr):

    reader.connection.connect()

    # Proprietary Command of ACS Reader :  command sets the timeout parameter of the contactless chip response time, P2 = FF [Wait until the contactless chip responds]
    r = reader.transceive(b'\xFF\x00\x41\xFF').check()
    print("Set ACS Reader Time Out Parameter Response : ", r)

    select_app(reader)

    # serialize the transaction with the RLP encoding scheme
    unsigned_encoded_transaction = serializable_unsigned_transaction_from_dict( transaction )

    # sign the hash of the serialized transaction
    global_counter, counter, signature2 = generate_signature( reader, keyIndex, bytes( unsigned_encoded_transaction.hash() ) ) # reader object, Key ID and unsigned transaction hash
    print("Data for Signature : ", unsigned_encoded_transaction.hash().hex())
    print("Signature from Card : ", signature2.hex())
    reader.connection.disconnect()

    #print("signature2: ",signature2)
    transaction_hash=unsigned_encoded_transaction.hash()

    r,s=get_signature_components(signature2)

    v , s= get_signature_prefix( ( r, s ), web3.toChecksumAddress(inf_card_addr), bytes( transaction_hash ), web3.eth.chainId, web3 )

    signed_encoded_transaction = encode_transaction( unsigned_encoded_transaction, vrs=( v, r, s ) )

    return signed_encoded_transaction

def check_Connection():

    try:
        reader = open_pyscard(None)
        reader.connection.disconnect()
    except Exception as err:
        print("Exception : ", err)
        raise Exception("Security2Go Starterkit R1 Connection Error",'No Reader detected with Security2Go Starterkit R1 Card on it.')

    return reader
