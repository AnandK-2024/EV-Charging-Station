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

# class to accept user info and validate it
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
            sm.current = 'detailsUser'
            # reset TextInput widget
            self.ethereumAddress.text = ""
            self.password.text = ""
            user_details = sm.get_screen(name = "detailsUser")
            user_details.fname.text = result[1]
            user_details.lname.text = result[2]
            user_details.age.text = result[3]
            user_details.gender.text = result[4]
            user_details.email.text = result[5]