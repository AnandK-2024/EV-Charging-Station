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

# import all the relevant classes
# from logging.config import _LoggerConfiguration
import uuid
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from web3 import Web3, HTTPProvider

# Infineon blocksec2go library to communicate with Infineon's Security2Go Starterkit R1 for Blockchain
from blocksec2go import open_pyscard, CardError
import handle_Transaction
import Config

# method to check the connection to Rinkeby Blockchain network and Security 2Go Starterkit R1
def check_Connection():

    try:
        reader = open_pyscard(None)
    except Exception as err:
        print("Exception : ", err)
        raise Exception("Security2Go Starterkit R1 Connection Error",'No Reader detected with Security2Go Starterkit R1 Card on it.')

    if(w3.isConnected()):
        print("Rinkeby Network is Connected")
    else:
        raise Exception("NETWORK CONNECTION FAILURE","Rinkeby Network is not Connected")
    return reader

# function that displays the pop-up message
def popFun(title_msg = "Error", content_msg = ""):
    window = Popup(title = title_msg, content = Label(text=content_msg),size_hint = (None, None), size = (700, 300))
    window.open()

# class to accept station info and validate it
class loginWindow(Screen):
    ethereumAddress = ObjectProperty(None)
    password = ObjectProperty(None)

    def validate(self):
        if self.ethereumAddress.text == "" or self.password.text == "":
            popFun("Incorrect Data","Please Provide Required Values")
            return


        try:
            result = contract.functions.verifyCredentials(self.ethereumAddress.text, self.password.text).call()
            print('Invoke get()={}'.format(result))
            sm.current = 'detailsstation'
            # reset TextInput widget
            self.ethereumAddress.text = ""
            self.password.text = ""
            station_details = sm.get_screen(name = "detailsstation")
            station_details.fname.text = result[1]
            station_details.location.text = result[2]
            station_details.power.text = result[3]
            station_details.charging.text = result[4]
            station_details.price.text = result[5]
            station_details.slot.text = result[6]
            station_details.time.text = result[7]
            station_details.ethereumAddress.text = result[7]

        except Exception as err:
            print("Exception Occured: ",err)
            popFun("SIGN IN Failed", "Incorrect station Name/Password \nor station Not Registered")
            return

    # method to get Ethereum Address from Public key at given index in Security 2Go Starterkit R1
    def getAddress(self):
        try:
            account_from_key_Index = 0x01

            reader = check_Connection()
            inf_card_addr, key_id = handle_Transaction.getAddressAtIndex(reader, w3, account_from_key_Index)
            self.ethereumAddress.text = inf_card_addr

        except Exception as err:
            if(len(err.args) >= 2):
                popFun(err.args[0], err.args[1])
            else:
                popFun("Exception Occured", str(err))

            return

# class to accept sign up info
class signupWindow(Screen):
    password_reg = ObjectProperty(None)
    fname_reg = ObjectProperty(None)
    age_reg = ObjectProperty(None)
    gender_reg = ObjectProperty(None)
    email_reg = ObjectProperty(None)
    contact_number= ObjectProperty(None)
    status_reg = ObjectProperty(None)


    def signupbtn(self):
        if self.password_reg.text == "" or self.fname_reg.text == "" :
            popFun("Incorrect Data","Please Provide Required Values")
            return
        
        print(self.fname_reg.text,self.location_reg, self.power_reg,self.charging_reg,self.price_reg)
        
        
        id = uuid.uuid1()
        unique_id=id.node
        
        # unique_id = int(str(uuid.uuid4())[:10])
        
        
        #storeCredentials(s)tring memory  pwd,string memory f_Name, string memory l_Name, string memory dob, string memory Gender)
        contract_func = contract.functions.RegisterChargingStation(unique_id,self.fname_reg.text,self.location_reg.text,
           int(self.power_reg.text), self.charging_reg.text,int(self.price_reg.text))
        try:
            reader = check_Connection()

            #print(transaction)
            inf_card_addr, key_id = handle_Transaction.getAddressAtIndex(reader, w3, 0x01)
            nonce = w3.eth.getTransactionCount(inf_card_addr)

            transaction = contract_func.buildTransaction(transaction = {'nonce' : nonce,'gas' : stationGas,'gasPrice': w3.eth.gas_price})
            signed_Transaction = handle_Transaction.getSignedTransaction(reader, w3, transaction, key_id, inf_card_addr)

            txn_hash = w3.eth.sendRawTransaction(signed_Transaction)
            print('txn_hash={} waiting for receipt..'.format(txn_hash.hex()))

            tx_receipt = w3.eth.waitForTransactionReceipt(txn_hash, timeout=120)
            print("Receipt accepted. gasUsed={gasUsed} blockNumber={blockNumber}". format(**tx_receipt))

            # self.password_reg.text = ""
            # self.fname_reg.text = ""
            # self.location_reg.text = ""
            # self.power_reg.text = ""
            # self.contact_number.text = ""
            

            tx_details = sm.get_screen(name = "txDetails")
            print("Transaction details:-", tx_details)
            tx_details.txn_from.text = inf_card_addr
            tx_details.txn_to.text = tx_receipt.to
            tx_details.txn_contract.text = Config.contract_address
            tx_details.txn_hash.text = tx_receipt.transactionHash.hex()
            tx_details.txn_gas.text = str(tx_receipt.gasUsed)
            tx_details.txn_nonce.text = str(nonce)
            accountBalance = w3.fromWei(w3.eth.getBalance(inf_card_addr),'ether')
            tx_details.eth_bal.text = str(accountBalance)
            sm.current = 'txDetails'

        except Exception as err:
            print("Exception Occured: ",err)
            if(len(err.args) >= 2):
                popFun(err.args[0], err.args[1])
            else:
                popFun("Exception Occured", str(err))
            return



# class to display voting result
class stationDetailsWindow(Screen):
    fname = ObjectProperty(None)
    location =ObjectProperty(None)  
    power =ObjectProperty(None)  
    charging =ObjectProperty(None)   
    price =ObjectProperty(None)   
    slot = ObjectProperty  (None)
    time= ObjectProperty(None)
    ethereumAddress = ObjectProperty(None)

    def LOGOUT(self):
        sm.current = 'login'


# class to display voting result
class txnDetailsWindow(Screen):
    txn_from = ObjectProperty(None)
    txn_to = ObjectProperty(None)
    txn_contract = ObjectProperty(None)
    txn_hash = ObjectProperty(None)
    txn_gas = ObjectProperty(None)
    txn_nonce = ObjectProperty(None)
    eth_bal = ObjectProperty(None)

    def Close(self):
        sm.current = 'login'



# class for managing screens
class windowManager(ScreenManager):
	pass


# class that builds gui
class Demo_station_Login_Blockchain(App):
    def on_stop(self):
        print("Stop")
        Window.close()
    def build(self):
        return sm


if __name__=="__main__":

    # ################### Initialize Rinkeyby Network parameters ################

    # instantiate web3 object
    w3 = Web3(HTTPProvider(Config.RPC_ADDRESS, request_kwargs={'timeout': 120}))
    # create contract object
    contract = w3.eth.contract(address=Config.contract_address, abi= Config.abi)

    stationGas = 554321


    # ############# Initialize GUI parameters ############################
    # kv file
    kv = Builder.load_file('station.kv')
    sm = windowManager()


    # adding screens
    sm.add_widget(loginWindow(name='login'))
    sm.add_widget(signupWindow(name='signup'))
    sm.add_widget(loginWindow(name='station'))
    sm.add_widget(stationDetailsWindow(name='detailsstation'))
    sm.add_widget(txnDetailsWindow(name='txDetails'))

    ###########################################################

    Demo_station_Login_Blockchain().run()
