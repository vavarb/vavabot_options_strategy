
from PyQt5.QtWidgets import QInputDialog, QLineEdit
from configparser import ConfigParser

from gui_spread import *
from connection_spread import *
from websocket import create_connection
from datetime import datetime, timedelta
import json
import hmac
import hashlib
import time

global index_greeks_print_on_off
global list_monitor_log
global list_thread_when_open_app
global trading_on_off
global run_trade_option_on_off
global run_trade_future_on_off
global run_target_on_off
global trading_on_off_for_msg
global send_future_orders_while
global sender_rate_dict
global password_dict
global counter_send_order_for_function
global dont_stop_trading_and_update_amount_adjusted


class Sinais(QtCore.QObject):
    textEdit_monitor_signal = QtCore.pyqtSignal(str)
    led_color_green_signal = QtCore.pyqtSignal()
    led_color_red_signal = QtCore.pyqtSignal()
    error_in_list_monitor_signal = QtCore.pyqtSignal(str)
    index_btc_print_signal = QtCore.pyqtSignal(str)
    greeks_signal = QtCore.pyqtSignal(dict)
    greeks_signal1 = QtCore.pyqtSignal(dict)
    chronometer_signal = QtCore.pyqtSignal(str)
    btc_index_print_gui_adjusts_signal = QtCore.pyqtSignal()
    start_thread_trade_signal = QtCore.pyqtSignal()
    start_signal_1 = QtCore.pyqtSignal(str)
    start_signal_2 = QtCore.pyqtSignal()
    start_signal_3 = QtCore.pyqtSignal()
    start_signal_4 = QtCore.pyqtSignal()
    btc_index_print_start_thread_signal = QtCore.pyqtSignal()
    structure_cost_for_tab_run_trading_and_btc_index_and_greeks_when_started_trading_signal_0 = QtCore.pyqtSignal(dict)
    structure_cost_for_tab_run_trading_and_btc_index_and_greeks_when_started_trading_signal_1 = QtCore.pyqtSignal()
    structure_cost_for_tab_run_trading_and_btc_index_and_greeks_when_started_trading_signal_2 = QtCore.pyqtSignal(str)
    structure_mark_greek_cost_signal = QtCore.pyqtSignal(dict)
    quote_new_structure_cost_for_print_when_stopped_trading_signal1 = QtCore.pyqtSignal(dict)
    position_now_signal = QtCore.pyqtSignal(dict)
    msg_box_for_position_now_signal = QtCore.pyqtSignal()
    print_greeks_by_instrument_signal = QtCore.pyqtSignal(dict)
    textedit_instruments_saved_settext_signal = QtCore.pyqtSignal(str)
    msg_box_for_thread_when_open_app1_signal = QtCore.pyqtSignal(list)
    textedit_balance_settext_signal = QtCore.pyqtSignal(str)
    quote_new_when_open_app_signal1 = QtCore.pyqtSignal(dict)
    last_trade_instrument_conditions_quote_signal = QtCore.pyqtSignal(dict)
    position_now_when_open_app_signal = QtCore.pyqtSignal(str)
    textedit_balance_after_signal = QtCore.pyqtSignal(dict)
    pushbutton_2_click_signal = QtCore.pyqtSignal()
    set_version_and_icon_and_texts_and_dates_signal = QtCore.pyqtSignal()
    target_saved_check_signal = QtCore.pyqtSignal()
    strategy_name_update_signal = QtCore.pyqtSignal()
    date_time_signal = QtCore.pyqtSignal(dict)
    reduce_only_signal = QtCore.pyqtSignal(dict)
    date_time_enabled_signal = QtCore.pyqtSignal()
    date_time_disabled_signal = QtCore.pyqtSignal()
    instruments_saved_print_and_check_available_signal = QtCore.pyqtSignal()
    msg_box_for_thread_when_open_app3_signal = QtCore.pyqtSignal()
    position_now_signal_2 = QtCore.pyqtSignal()
    pushButton_request_options_structure_cost_signal = QtCore.pyqtSignal()

    def __init__(self):
        QtCore.QObject.__init__(self)


sinal = Sinais()
delay_delay = 0
delay = 0


class Deribit:
    def __init__(self, client_id=None, client_secret=None, wss_url=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.wss_url = wss_url

        self._auth(client_id=client_id, wss_url=wss_url, client_secret=client_secret)

    # noinspection PyMethodMayBeStatic
    def logwriter(self, msg):
        from lists import list_monitor_log

        filename = 'log_strategy.log'

        try:
            out = datetime.now().strftime("\n[%Y/%m/%d, %H:%M:%S] ") + str(msg)
            list_monitor_log.append(str(msg))
            with open(filename, 'a') as logwriter_file:
                logwriter_file.write(str(out))

        except Exception as er:
            from connection_spread import connect
            from lists import list_monitor_log
            global counter_send_order_for_function

            with open(filename, 'a') as logwriter_file:
                logwriter_file.write(str(datetime.now().strftime("\n[%Y/%m/%d, %H:%M:%S] ")) +
                                     '***** ERROR except in logwriter: ' +
                                     str(er) + str(msg) +
                                     '_' + str(counter_send_order_for_function) + ' *****')
            list_monitor_log.append('***** ERROR except in logwriter: ' + str(er) + ' *****')
        finally:
            pass

    def _auth(self, client_id=None, wss_url=None, client_secret=None):
        self.client_id = client_id
        self.wss_url = wss_url
        self.client_secret = client_secret

        from lists import list_monitor_log
        global sender_rate_dict
        global delay_delay
        global counter_send_order_for_function

        counter_send_order_for_function = 0

        sender_rate_dict = dict()
        sender_rate_dict['time_1'] = time.time()
        sender_rate_dict['counter_send_order_for_sender_rate'] = 1

        timestamp = round(datetime.now().timestamp() * 1000)
        nonce = "abcd"
        data = ""
        signature = hmac.new(
            bytes(client_secret, "latin-1"),
            msg=bytes('{}\n{}\n{}'.format(timestamp, nonce, data), "latin-1"),
            digestmod=hashlib.sha256
        ).hexdigest().lower()

        try:
            self._WSS = create_connection(wss_url, enable_multithread=True)
            msg = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "public/auth",
                "params": {
                    "grant_type": "client_signature",
                    "client_id": client_id,
                    "timestamp": timestamp,
                    "signature": signature,
                    "nonce": nonce,
                    "data": data
                }
            }
            self.logwriter('Auth OK\n############')
            list_monitor_log.append('Auth OK\n############')
            list_monitor_log.append('identified')
            return self._sender(msg)

        except Exception as er:
            from lists import list_monitor_log
            list_monitor_log.append('***** auth ERROR:' + ' error: ' + str(er) + ' *****')
            self.logwriter('***** auth ERROR:' + ' error: ' + str(er) + ' *****')

    # noinspection PyMethodMayBeStatic
    def sender_rate(self, counter_send_order_for_sender_rate, time_now):
        global sender_rate_dict

        if float(time_now - sender_rate_dict['time_1']) >= 120:
            delta_counter_send_order = float(
                counter_send_order_for_sender_rate) - float(sender_rate_dict['counter_send_order_for_sender_rate'])
            delta_time_for_sender_rate = float(time_now - sender_rate_dict['time_1'])
            rate_sender_orders = float(delta_counter_send_order) / float(delta_time_for_sender_rate)

            sender_rate_dict['time_1'] = time_now
            sender_rate_dict['counter_send_order_for_sender_rate'] = float(counter_send_order_for_sender_rate)

            return round(rate_sender_orders, 2)
        else:
            return False

    def _delay(self, sender_rate_rate_):
        global delay_delay
        from lists import list_monitor_log

        if sender_rate_rate_ is not False:
            orders_per_second_ = float(ConfigSaved().orders_rate_saved())

            list_monitor_log.append('*** Check Sent Orders Rate ***')
            self.logwriter(
                '*** Sent Orders Rate: ' + str(sender_rate_rate_) + ' Orders/Second ***')
            if float(sender_rate_rate_) > float(orders_per_second_):
                delay_delay = round(delay_delay + ((1 / orders_per_second_) - (1 / sender_rate_rate_)), 2)
                list_monitor_log.append('*** Sent Orders Rate Checked: > ' + str(orders_per_second_) +
                                        ' Orders/second ***')
                self.logwriter('*** Setup New Delay to send order: ' + str(delay_delay) + ' seconds ***')
            else:
                list_monitor_log.append('*** Sent Orders Rate Checked: < ' + str(orders_per_second_) +
                                        ' Orders/second ***')
                if delay_delay == 0:
                    self.logwriter('*** Setup Delay to send order Unmodified ***')
                else:
                    if round(delay_delay - ((1 / sender_rate_rate_) - (1 / orders_per_second_)), 2) > 0:
                        delay_delay = round(delay_delay - ((1 / sender_rate_rate_) - (1 / orders_per_second_)), 2)
                        self.logwriter('*** Setup New Delay to send order: ' + str(delay_delay) + ' seconds ***')
                    else:
                        delay_delay = 0
                        self.logwriter('*** Setup New Delay to send order: ' + str(delay_delay) + ' seconds ***')
            if delay_delay < 0:
                return 0
            else:
                return float(delay_delay)
        else:
            if delay_delay < 0:
                return 0
            else:
                return float(delay_delay)

    @staticmethod
    def counter_send_order_function():
        global counter_send_order_for_function

        counter_send_order_for_function = counter_send_order_for_function + 1
        return counter_send_order_for_function

    def _sender(self, msg):
        global delay
        from connection_spread import led_color

        counter_send_order = self.counter_send_order_function()
        msg_id_before_counter = msg['id']
        msg['id'] = int(str(msg['id']) + str(counter_send_order))

        try:
            if str(msg['method']) == 'private/buy' or str(msg['method']) == 'private/sell':
                if str(msg_id_before_counter) == "8" or str(msg_id_before_counter) == "9":
                    instrument_name = str(msg['params']['instrument_name'])
                    instrument_direction = str(msg['method']) + ' ' + str(msg['params']['type'])
                    order_amount_instrument = str(msg['params']['amount'])
                    instrument_price = str(msg['params']['price'])
                    self.logwriter(str(instrument_name) +
                                   ': ' + str(instrument_direction) +
                                   ' ' + str(order_amount_instrument) +
                                   ' at ' + str(instrument_price) +
                                   ' ID: ' + str(msg['id']) +
                                   '_' + str(counter_send_order))
                else:
                    pass
            else:
                self.logwriter(str(msg['method']) + ' ID: ' + str(msg['id']) + '_' + str(counter_send_order))

            self._WSS.send(json.dumps(msg))
            out = json.loads(self._WSS.recv())

            delay = self._delay(sender_rate_rate_=self.sender_rate(
                counter_send_order_for_sender_rate=counter_send_order, time_now=time.time()))

            if delay > 0 and (msg_id_before_counter != 8 and msg_id_before_counter != 9 and
                              msg_id_before_counter != 14):
                time.sleep(delay)
            else:
                pass

            if 'error' in str(out) or \
                    (msg['id'] != out['id'] and msg_id_before_counter != 1 and led_color() == 'green' and
                     msg_id_before_counter != 8 and msg_id_before_counter != 9):
                if msg['id'] != out['id']:
                    self.logwriter(' ***** ERROR: msgSentID != msgOutID *****\n***** msgSent: ' + str(msg) +
                                   ' *****\n***** msgOut: ' + str(out) + ' *****\n*** msgSent ID: ' + str(msg['id']) +
                                   '_' + str(counter_send_order) + ' ***''\n*** msgOut ID: ' + str(out['id']) + ' ***')
                    time.sleep(10)
                    out = {'error': {'code': 'error'}}
                else:
                    self.logwriter(' ***** _sender ERROR: msgOut: ' + str(out) + '*****\n ***msgSent ID: ' +
                                   str(msg['id']) + '_' + str(counter_send_order) + ' ***')

                if str(out['error']['code']) == '13009' or str(out['error']['code']) == '13004':
                    self.logwriter('***** _sender msg - VERIFY CREDENTIALS - Type your Deribit API and Secret Keys '
                                   '*****')
                    if str(msg_id_before_counter) == '19':
                        return float(0)
                    elif str(msg_id_before_counter) == '25':
                        return 0
                    else:
                        return out['error']

                elif str(msg_id_before_counter) == '19':
                    return float(0)

                elif str(msg_id_before_counter) == '25':
                    return 0

                else:
                    return out['error']

            elif str(msg_id_before_counter) == '18':
                return out['result']['trades'][0]['price']

            elif str(msg_id_before_counter) == '19':
                if str(out['result']['size']) == 'None' or str(out['result']['size']) == 'none':
                    return float(0)
                else:
                    return out['result']['size']

            elif str(msg_id_before_counter) == '20':
                if str(out['result']['best_ask_price']) == 'null' or str(out['result']['best_ask_price']) == 'None':
                    return 0
                else:
                    return out['result']['best_ask_price']

            elif str(msg_id_before_counter) == '21':
                if str(out['result']['best_bid_price']) == 'null' or str(out['result']['best_bid_price']) == 'None':
                    return 0
                else:
                    return out['result']['best_bid_price']

            elif str(msg_id_before_counter) == '22':
                return out['result'][0]['mark_price']

            elif str(msg_id_before_counter) == '23':
                if str(out['result']['best_bid_amount']) == 'null' or str(out['result']['best_bid_amount']) == 'None':
                    return 0
                else:
                    return out['result']['best_bid_amount']

            elif str(msg_id_before_counter) == '24':
                if str(out['result']['best_ask_amount']) == 'null' or str(out['result']['best_ask_amount']) == 'None':
                    return 0
                else:
                    return out['result']['best_ask_amount']

            elif str(msg_id_before_counter) == '25':
                if len(out['result']['data']) == 0 or out['result']['data'] == 'ok' or out[
                    'result']['data'] == 'OK' or out['result']['data'] == 'Ok' or out[
                        'result'] == 'ok' or out['result'] == 'Ok' or out['result'] == 'OK':
                    return 0
                elif 'error' in str(out):
                    return 0
                elif len(out['result']['data']) != 0:
                    return out['result']['data'][-1][-1]
                else:
                    return 0

            else:
                return out['result']

        except Exception as er:
            from connection_spread import connection_thread, run_thread
            import threading

            self.logwriter('***** _sender ERROR: ' + str(er) + ' msgSent ID: ' + str(msg['id']) +
                           '_' + str(counter_send_order) + ' *****')
            if run_thread.is_alive() is True:
                pass
            else:
                connection_thread()
        finally:
            pass

    def get_instruments(self, currency):
        msg = \
            {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "public/get_instruments",
                "params": {
                    "currency": currency,
                    "expired": False
                }
            }
        return self._sender(msg)

    def index_price(self, currency):
        msg = \
            {
                "jsonrpc": "2.0",
                "method": "public/get_index_price",
                "id": 3,
                "params": {
                    "index_name": currency
                }
            }
        return self._sender(msg)

    def test(self):
        global delay

        counter_send_order1 = self.counter_send_order_function()

        if delay > 0:
            time.sleep(delay)
        else:
            pass

        msg1 = \
            {
                "jsonrpc": "2.0",
                "id": 4,
                "method": "public/test",
                "params": {
                }
            }
        try:
            self._WSS.send(json.dumps(msg1))
            out1 = json.loads(self._WSS.recv())
        except AttributeError as er1:
            self.logwriter(
                str('********** Connection Test Error: ' + str(er1) + ' **********\n msgSent ID: ' +
                    str(msg1['id']) + '_' + str(counter_send_order1)))
            return 'error'

        self.logwriter(
            str(msg1['method']) + '(* Connection Test *)' + ' ID: ' + str(msg1['id']) + '_' + str(
                counter_send_order1))

        if 'error' in str(out1):
            self.logwriter('**************** Connection Test ERROR *****************\n*** msgOUT: ' + str(out1) +
                           '*** \n*** msgOut ID: ' + str(out1['id']) + '_' + str(counter_send_order1) + ' ***')
            return 'error'
        else:
            if out1['id'] == 4:
                return out1['result']
            elif (isinstance(out1['id'], int) or isinstance(out1['id'], float)) and out1['id'] != 4:
                return 'version'
            else:
                return out1['result']

    def get_order_book(self, instrument_name=None):
        msg = \
            {
                "jsonrpc": "2.0",
                "id": 7,
                "method": "public/get_order_book",
                "params": {
                    "instrument_name": instrument_name
                }
            }
        return self._sender(msg)

    def buy_limit(self, currency, amount, price):
        msg = \
            {
                "jsonrpc": "2.0",
                "id": 8,
                "method": "private/buy",
                "params": {
                    "instrument_name": currency,
                    "amount": amount,
                    "type": "limit",
                    "price": price
                }
            }
        return self._sender(msg)

    def sell_limit(self, currency, amount, price):
        msg = \
            {
                "jsonrpc": "2.0",
                "id": 9,
                "method": "private/sell",
                "params": {
                    "instrument_name": currency,
                    "amount": amount,
                    "type": "limit",
                    "price": price
                }
            }
        return self._sender(msg)

    def cancel_all(self):
        msg = \
            {
                "jsonrpc": "2.0",
                "id": 14,
                "method": "private/cancel_all",
                "params": {

                }
            }
        return self._sender(msg)

    def get_book_summary_by_instrument(self, instrument_name):
        msg = \
            {
                "jsonrpc": "2.0",
                "id": 16,
                "method": "public/get_book_summary_by_instrument",
                "params": {
                    "instrument_name": instrument_name
                }
            }
        return self._sender(msg)

    def get_last_trades_by_instrument_price(self, instrument_name):
        msg = \
            {
                "jsonrpc": "2.0",
                "id": 18,
                "method": "public/get_last_trades_by_instrument",
                "params": {
                    "instrument_name": instrument_name
                }
            }
        return self._sender(msg)

    def get_position_size(self, instrument_name):
        msg = \
            {
                "jsonrpc": "2.0",
                "id": 19,
                "method": "private/get_position",
                "params": {
                    "instrument_name": instrument_name
                }
            }
        return self._sender(msg)

    def ask_price(self, instrument_name=None):
        msg = \
            {
                "jsonrpc": "2.0",
                "id": 20,
                "method": "public/get_order_book",
                "params": {
                    "instrument_name": instrument_name
                }
            }
        return self._sender(msg)

    def bid_price(self, instrument_name=None):
        msg = \
            {
                "jsonrpc": "2.0",
                "id": 21,
                "method": "public/get_order_book",
                "params": {
                    "instrument_name": instrument_name
                }
            }
        return self._sender(msg)

    def mark_price(self, instrument_name=None):
        msg = \
            {
                "jsonrpc": "2.0",
                "id": 22,
                "method": "public/get_book_summary_by_instrument",
                "params": {
                    "instrument_name": instrument_name
                }
            }
        return self._sender(msg)

    def best_bid_amount(self, instrument_name=None):
        msg = \
            {
                "jsonrpc": "2.0",
                "id": 23,
                "method": "public/get_order_book",
                "params": {
                    "instrument_name": instrument_name
                }
            }
        return self._sender(msg)

    def best_ask_amount(self, instrument_name=None):
        msg = \
            {
                "jsonrpc": "2.0",
                "id": 24,
                "method": "public/get_order_book",
                "params": {
                    "instrument_name": instrument_name
                }
            }
        return self._sender(msg)

    def volatility_index_data(self, currency):
        timestamp_end = float(round(datetime.now().timestamp()) * 1000)
        timestamp_start = timestamp_end - 10000
        msg = \
            {
                "jsonrpc": "2.0",
                "id": 25,
                "method": "public/get_volatility_index_data",
                "params": {
                    "currency": currency,
                    "start_timestamp": timestamp_start,
                    "end_timestamp": timestamp_end,
                    "resolution": "1"
                }
            }
        return self._sender(msg)

    def hello(self):
        setup = ConfigParser(
            allow_no_value=True,
            strict=False
        )
        setup.read('setup.ini')
        default_setup = dict(setup['DEFAULT'])
        name = default_setup['name']
        version = default_setup['version']
        msg = \
            {
                "jsonrpc": "2.0",
                "id": 26,
                "method": "public/hello",
                "params": {
                    "client_name": str(name),
                    "client_version": str(version)
                }
            }
        return self._sender(msg)


class CredentialsSaved:
    def __init__(self):
        self.self = self

    @staticmethod
    def api_secret_saved():
        import os
        import base64
        from cryptography.fernet import Fernet, InvalidToken, InvalidSignature
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        from lists import password_dict
        global password_dict

        password1 = str(password_dict['pwd'])

        if os.path.isfile('api-key_spread.txt') is False:
            with open('api-key_spread.txt', 'a') as api_key_save_file:
                api_key_save_file.write(str('<Type your Deribit Key>'))
            api_secret_saved_file_read = str('<Type your Deribit Key>')
        else:
            with open('api-key_spread.txt', 'r') as file:
                if '<Type your Deribit Key>' in str(file.read()):
                    file_read = str('<Type your Deribit Key>')
                else:
                    file_read = 'True'
            if file_read == 'True':
                salt = b'\x90"\x90J\r\xa6\x08\xb6_\xbdfEd\x1cDE'
                kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=salt,
                    iterations=390000,
                )

                key = base64.urlsafe_b64encode(kdf.derive(str(password1).encode('utf-8')))
                f = Fernet(key)

                with open('api-key_spread.txt', 'rb') as enc_file:
                    encrypted = enc_file.read()
                try:
                    decrypted = f.decrypt(encrypted).decode('utf-8')
                    api_secret_saved_file_read = str(decrypted)
                except InvalidToken or InvalidSignature:
                    api_secret_saved_file_read = str('<Type your Deribit Key>')
                finally:
                    pass
            else:
                api_secret_saved_file_read = str('<Type your Deribit Key>')

        return api_secret_saved_file_read

    @staticmethod
    def secret_key_saved():
        import os
        import base64
        from cryptography.fernet import Fernet, InvalidToken, InvalidSignature
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        from lists import password_dict
        global password_dict

        password2 = str(password_dict['pwd'])

        if os.path.isfile('secret-key_spread.txt') is False:
            with open('secret-key_spread.txt', 'a') as secret_key_saved_file:
                secret_key_saved_file.write(str('<Type your Deribit Secret Key>'))
            secret_key_saved_file_read = str('<Type your Deribit Secret Key>')
        else:
            with open('secret-key_spread.txt', 'r') as file:
                if '<Type your Deribit Secret Key>' in str(file.read()):
                    file_read = str('<Type your Deribit Secret Key>')
                else:
                    file_read = 'True'
            if file_read == 'True':
                salt = b'\x90"\x90J\r\xa6\x08\xb6_\xbdfEd\x1cDE'
                kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=salt,
                    iterations=390000,
                )

                key = base64.urlsafe_b64encode(kdf.derive(str(password2).encode('utf-8')))
                f = Fernet(key)

                with open('secret-key_spread.txt', 'rb') as enc_file:
                    encrypted = enc_file.read()
                try:
                    decrypted = f.decrypt(encrypted).decode('utf-8')
                    secret_key_saved_file_read = str(decrypted)
                except InvalidToken or InvalidSignature:
                    secret_key_saved_file_read = str('<Type your Deribit Secret Key>')
                finally:
                    pass
            else:
                secret_key_saved_file_read = str('<Type your Deribit Secret Key>')

        return secret_key_saved_file_read

    @staticmethod
    def testnet_saved_true_or_false():
        from lists import list_monitor_log

        setup = ConfigParser(
            allow_no_value=True,
            inline_comment_prefixes='#',
            strict=False
        )
        setup.read('setup.ini')
        credentials_setup = setup['credentials']

        testnet_saved_true_or_false = credentials_setup.getboolean('test_net')

        if testnet_saved_true_or_false is True:
            list_monitor_log.append('*** TEST Account Selected ***')
            return True
        elif testnet_saved_true_or_false is False:
            list_monitor_log.append('*** REAL Account Selected ***')
            return False
        else:
            list_monitor_log.append('***** ERROR in testnet_saved_true_or_false - Error Code: 732 *****')
            connect.logwriter('***** ERROR in testnet_saved_true_or_false - Error Code: 733 *****')

    @staticmethod
    def url():
        from lists import list_monitor_log
        if CredentialsSaved.testnet_saved_true_or_false() is True:
            list_monitor_log.append('*** URL: ' + 'wss://test.deribit.com/ws/api/v2' + ' Selected ***')
            return 'wss://test.deribit.com/ws/api/v2'
        elif CredentialsSaved.testnet_saved_true_or_false() is False:
            list_monitor_log.append('*** URL: ' + 'wss://www.deribit.com/ws/api/v2' + ' Selected ***')
            return 'wss://www.deribit.com/ws/api/v2'
        else:
            list_monitor_log.append('***** URL ERROR in testnet True or False - Error Code: 630 *****')


class InstrumentsSaved:
    def __init__(self):
        self.self = self
        self.instrument_number = None

    @staticmethod
    def instruments_check():
        with open('instruments_spread.txt', 'r') as instruments_check_file:
            return str(instruments_check_file.read())

    def instrument_name_construction_from_file(self, instrument_number=None):
        self.instrument_number = instrument_number
        file_open = 'instruments_spread.txt'

        instrument_number_adjusted_to_list = (int(instrument_number) - 1)

        # open file instruments
        with open(file_open, 'r') as file_instruments:
            lines_file_instruments = file_instruments.readlines()  # file instruments_spread.txt ==> lines
            # Instrument
            list_line_instrument = lines_file_instruments[instrument_number_adjusted_to_list].split()  # line ==> list
            if 'Unassigned' in list_line_instrument:
                return 'Unassigned'
            else:
                instrument_name = str(list_line_instrument[5])
                return str(instrument_name)

    def instrument_available(self, instrument_number=None):
        from lists import list_monitor_log
        from connection_spread import connect

        self.instrument_number = instrument_number

        instrument_name = InstrumentsSaved().instrument_name_construction_from_file(
            instrument_number=instrument_number)

        if instrument_name == 'Unassigned':
            return 'Unassigned'
        else:
            currency = str
            if 'BTC' in instrument_name:
                currency = 'BTC'
            elif 'ETH' in instrument_name:
                currency = 'ETH'
            else:
                connect.logwriter(str('********** Instrument currency ERROR Error Code:: 678 *********'))
                list_monitor_log.append('********** Instrument currency ERROR Error Code:: 679 *********')
            a10 = connect.get_instruments(currency=currency)
            list_instrument_name = []
            for i in a10:
                list_instrument_name.append(i['instrument_name'])
            if instrument_name in list_instrument_name:
                list_instrument_name.clear()
                return 'instrument available'
            else:
                list_instrument_name.clear()
                return 'instrument NO available'

    def instrument_buy_or_sell(self, instrument_number=None):
        file_open = 'instruments_spread.txt'
        self.instrument_number = instrument_number
        instrument_number_adjusted_to_list = (int(instrument_number) - 1)
        if InstrumentsSaved().instrument_name_construction_from_file(
                instrument_number=instrument_number) == 'Unassigned':
            return 'Unassigned'
        else:
            with open(file_open, 'r') as file_instruments:
                lines_file_instruments = file_instruments.readlines()  # file instruments.txt ==> lines
                # Instrument
                list_line_instrument = \
                    lines_file_instruments[instrument_number_adjusted_to_list].split()  # line ==> list
                instrument_buy_or_sell = str(list_line_instrument[3])
                return str(instrument_buy_or_sell)

    def instrument_position_saved(self, instrument_number=None):
        self.instrument_number = instrument_number
        from lists import list_monitor_log

        setup = ConfigParser(
            allow_no_value=True,
            inline_comment_prefixes='#',
            strict=False
        )
        setup.read('setup.ini')
        position_saved_setup = setup['position_saved']
        position_saved = str(
            position_saved_setup['Instrument' + str(instrument_number) + '_position_saved']
        )

        if 'Unassigned' in position_saved:
            return 0
        elif 'None' in position_saved:
            list_monitor_log.append('********** ERROR **********\nSyntax ERROR or there is not \n'
                                    'Instrument ' + instrument_number)
            pass
            return '***** Syntax ERROR or there is not Instrument *****'
        else:
            return float(position_saved)

    def instrument_amount_saved(self, instrument_number=None):
        self.instrument_number = instrument_number
        from lists import list_monitor_log

        setup = ConfigParser(
            allow_no_value=True,
            inline_comment_prefixes='#',
            strict=False
        )
        setup.read('setup.ini')

        instrument_amount_setup = setup['amount']
        instrument_amount_saved = instrument_amount_setup['instrument' + str(instrument_number) + '_amount']

        amount_adjusted_setup = setup['amount_adjusted']
        rate_amount = float(amount_adjusted_setup['rate_amount'])
        
        kind_setup = setup['kind']
        instrument_kind = str(kind_setup['kind_instrument' + str(instrument_number)])

        if instrument_amount_saved == 'Unassigned':
            return 'Unassigned'
        elif rate_amount < 1 and instrument_amount_saved != 'Unassigned' and (
                instrument_kind == 'option' or instrument_kind == 'future'):
            if instrument_kind == 'option':
                return str(round(float(instrument_amount_saved) * rate_amount, 1))
            else:
                return str(
                    ConditionsCheck().number_multiple_0_1_and_round_1_digits(
                        number=float(instrument_amount_saved) * rate_amount
                    )
                )
        elif rate_amount == 1 and instrument_amount_saved != 'Unassigned':
            return str(instrument_amount_saved)
        else:
            list_monitor_log.append(
                '********** ERROR code 869 - instrument amount saved error' + ' - Instrument ' + str(instrument_number)
            )
            return str(0.0)

    def instrument_kind_saved(self, instrument_number=None):
        self.instrument_number = instrument_number
        from connection_spread import connect
        
        setup = ConfigParser(
            allow_no_value=True,
            inline_comment_prefixes='#',
            strict=False
        )
        setup.read('setup.ini')
        kind_setup = setup['kind']

        kind_instrument = str(kind_setup['kind_instrument' + str(instrument_number)])
        if 'Unassigned' in kind_instrument:
            return 'Unassigned'
        elif 'future' in kind_instrument:
            return 'future'
        elif 'option' in kind_instrument:
            return 'option'
        else:
            connect.logwriter('*** Instrument ' + str(instrument_number) + ' kind ERROR Error Code:: 746 ***')
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText('Instrument ' + str(instrument_number) + ' kind ERROR Error Code:: 749')
            msg.setWindowTitle('***** ERROR *****')
            msg.exec_()
            pass

    def instrument_direction_construction_from_instrument_file(self, instrument_number=None):
        self.instrument_number = instrument_number
        from connection_spread import connect

        file_open = 'instruments_spread.txt'
        instrument_number_adjusted_to_list = (int(instrument_number) - 1)

        # open file instruments

        with open(file_open, 'r') as file_instruments:
            lines_file_instruments = file_instruments.readlines()  # file instruments_spread.txt ==> lines
            # Instrument
            list_line_instrument = lines_file_instruments[instrument_number_adjusted_to_list].split()  # line ==> list
            if 'Unassigned' in list_line_instrument:
                return 'Unassigned'
            elif 'buy' in list_line_instrument:
                return 'buy'
            elif 'sell' in list_line_instrument:
                return 'sell'
            else:
                connect.logwriter(str(
                    '*** Instrument ' + str(instrument_number) + ' direction ERROR Error Code:: 775 ***'))
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Instrument ' + str(instrument_number) + ' direction ERROR Error Code:: 778')
                msg.setWindowTitle('***** ERROR *****')
                msg.exec_()
                pass


class Instruments:
    def __init__(self):
        self.self = self
        self.instrument_number = None
        self.instrument_name = None
        self.instrument_name1 = None
        self.instrument_name2 = None
        self.instrument_name3 = None
        self.instrument_name4 = None

    def instrument_available_before_save(self, instrument_name=None):  # Não tem UI
        from lists import list_monitor_log
        from connection_spread import connect

        self.instrument_name = instrument_name

        if instrument_name == 'Unassigned':
            return 'Unassigned'
        else:
            currency = str
            if 'BTC' in instrument_name:
                currency = 'BTC'
            elif 'ETH' in instrument_name:
                currency = 'ETH'
            else:
                connect.logwriter(str('********** Instrument currency ERROR Error Code:: 809 *********'))
                list_monitor_log.append('********** Instrument currency ERROR Error Code:: 810 *********')
            a10 = connect.get_instruments(currency=currency)
            list_instrument_name = []
            for i in a10:
                list_instrument_name.append(i['instrument_name'])
            if instrument_name in list_instrument_name:
                list_instrument_name.clear()
                return 'instrument available'
            else:
                list_instrument_name.clear()
                return 'instrument NO available'

    def instrument_check_available_before_save(self,
                                               instrument_name1=None,
                                               instrument_name2=None,
                                               instrument_name3=None,
                                               instrument_name4=None):  # Não tem UI
        self.instrument_name1 = instrument_name1
        self.instrument_name2 = instrument_name2
        self.instrument_name3 = instrument_name3
        self.instrument_name4 = instrument_name4
        from connection_spread import connect

        try:
            if (Instruments().instrument_available_before_save(instrument_name=instrument_name1) ==
                'instrument available' or
                Instruments().instrument_available_before_save(instrument_name=instrument_name1) == 'Unassigned') and \
                    (Instruments().instrument_available_before_save(instrument_name=instrument_name2) ==
                     'instrument available' or
                     Instruments().instrument_available_before_save(instrument_name=instrument_name2) ==
                     'Unassigned') and \
                    (Instruments().instrument_available_before_save(instrument_name=instrument_name3) ==
                     'instrument available' or
                     Instruments().instrument_available_before_save(instrument_name=instrument_name3) ==
                     'Unassigned') and \
                    (Instruments().instrument_available_before_save(instrument_name=instrument_name4) ==
                     'instrument available' or
                     Instruments().instrument_available_before_save(instrument_name=instrument_name4) == 'Unassigned'):
                return 'instrument_check_available_before_save_OK'
                pass
            else:
                pass

            if Instruments().instrument_available_before_save(instrument_name=instrument_name1) == \
                    'instrument NO available':
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Instrument 1 Syntax ERROR')
                msg.setWindowTitle('***** ERROR *****')
                msg.exec_()
                pass
            else:
                pass

            if Instruments().instrument_available_before_save(instrument_name=instrument_name2) == \
                    'instrument NO available':
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Instrument 2 Syntax ERROR')
                msg.setWindowTitle('***** ERROR *****')
                msg.exec_()
                pass
            else:
                pass

            if Instruments().instrument_available_before_save(instrument_name=instrument_name3) == \
                    'instrument NO available':
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Instrument 3 Syntax ERROR')
                msg.setWindowTitle('***** ERROR *****')
                msg.exec_()
                pass
            else:
                pass

            if Instruments().instrument_available_before_save(instrument_name=instrument_name4) == \
                    'instrument NO available':
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Instrument 4 Syntax ERROR')
                msg.setWindowTitle('***** ERROR *****')
                msg.exec_()
                pass
            else:
                pass

        except Exception as er:
            connect.logwriter(str(er) + ' Error Code:: 898')
            list_monitor_log.append(str(er) + ' Error Code:: 899')
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText('Instruments Checking before save\n Syntax ERROR')
            msg.setWindowTitle('***** ERROR *****')
            msg.exec_()
            pass
        finally:
            pass

    def greeks_by_instruments(self, instrument_number=None):
        self.instrument_number = instrument_number
        # import time
        from connection_spread import connect

        instrument_kind_greeks = InstrumentsSaved().instrument_kind_saved(instrument_number=instrument_number)
        if 'option' in instrument_kind_greeks:
            instrument_name_greeks = InstrumentsSaved().instrument_name_construction_from_file(
                instrument_number=instrument_number)
            book_instrument_greeks = connect.get_order_book(instrument_name=instrument_name_greeks)
            return book_instrument_greeks['greeks']
        elif 'future' in instrument_kind_greeks:
            delta_future_instrument_name = InstrumentsSaved().instrument_name_construction_from_file(
                instrument_number=instrument_number)
            last_trade_future = connect.get_last_trades_by_instrument_price(
                instrument_name=delta_future_instrument_name)
            delta_future = 1 / last_trade_future
            return {'vega': 0, 'theta': 0, 'rho': 0, 'gamma': 0, 'delta': delta_future}
        elif 'Unassigned' in instrument_kind_greeks:
            return {'vega': 0, 'theta': 0, 'rho': 0, 'gamma': 0, 'delta': 0}
    
    @staticmethod
    def adjust_rate_trade_by_reduce_only_save_to_run():
        from connection_spread import connect

        setup = ConfigParser(
            allow_no_value=True,
            inline_comment_prefixes='#',
            strict=False
        )
        setup.read('setup.ini')
        amount_setup = setup['amount']

        instrument1_amount_saved_to_adjust_rate = amount_setup['instrument1_amount']
        if instrument1_amount_saved_to_adjust_rate == 'Unassigned':
            instrument1_amount_saved_to_adjust_rate = 0
        else:
            instrument1_amount_saved_to_adjust_rate = float(instrument1_amount_saved_to_adjust_rate)
        instrument2_amount_saved_to_adjust_rate = amount_setup['instrument2_amount']
        if instrument2_amount_saved_to_adjust_rate == 'Unassigned':
            instrument2_amount_saved_to_adjust_rate = 0
        else:
            instrument2_amount_saved_to_adjust_rate = float(instrument2_amount_saved_to_adjust_rate)
        instrument3_amount_saved_to_adjust_rate = amount_setup['instrument3_amount']
        if instrument3_amount_saved_to_adjust_rate == 'Unassigned':
            instrument3_amount_saved_to_adjust_rate = 0
        else:
            instrument3_amount_saved_to_adjust_rate = float(instrument3_amount_saved_to_adjust_rate)
        instrument4_amount_saved_to_adjust_rate = amount_setup['instrument4_amount']
        if instrument4_amount_saved_to_adjust_rate == 'Unassigned':
            instrument4_amount_saved_to_adjust_rate = 0
        else:
            instrument4_amount_saved_to_adjust_rate = float(instrument4_amount_saved_to_adjust_rate)

        amount_adjusted_setup = setup['amount_adjusted']

        instrument1_amount_saved_and_reduce_only_to_adjust_rate = amount_adjusted_setup['instrument1_amount_adjusted']
        if instrument1_amount_saved_and_reduce_only_to_adjust_rate == 'Unassigned':
            instrument1_amount_saved_and_reduce_only_to_adjust_rate = 0
        else:
            instrument1_amount_saved_and_reduce_only_to_adjust_rate = float(
                instrument1_amount_saved_and_reduce_only_to_adjust_rate)
        instrument2_amount_saved_and_reduce_only_to_adjust_rate = amount_adjusted_setup['instrument2_amount_adjusted']
        if instrument2_amount_saved_and_reduce_only_to_adjust_rate == 'Unassigned':
            instrument2_amount_saved_and_reduce_only_to_adjust_rate = 0
        else:
            instrument2_amount_saved_and_reduce_only_to_adjust_rate = float(
                instrument2_amount_saved_and_reduce_only_to_adjust_rate)
        instrument3_amount_saved_and_reduce_only_to_adjust_rate = amount_adjusted_setup['instrument3_amount_adjusted']
        if instrument3_amount_saved_and_reduce_only_to_adjust_rate == 'Unassigned':
            instrument3_amount_saved_and_reduce_only_to_adjust_rate = 0
        else:
            instrument3_amount_saved_and_reduce_only_to_adjust_rate = float(
                instrument3_amount_saved_and_reduce_only_to_adjust_rate)
        instrument4_amount_saved_and_reduce_only_to_adjust_rate = amount_adjusted_setup['instrument4_amount_adjusted']
        if instrument4_amount_saved_and_reduce_only_to_adjust_rate == 'Unassigned':
            instrument4_amount_saved_and_reduce_only_to_adjust_rate = 0
        else:
            instrument4_amount_saved_and_reduce_only_to_adjust_rate = float(
                instrument4_amount_saved_and_reduce_only_to_adjust_rate)

        if instrument1_amount_saved_and_reduce_only_to_adjust_rate == 0 and \
                instrument1_amount_saved_to_adjust_rate == 0:
            instrument1_rate = 1
        elif instrument1_amount_saved_and_reduce_only_to_adjust_rate != 0 and \
                instrument1_amount_saved_to_adjust_rate == 0:
            instrument1_rate = 0
        else:
            instrument1_rate = float(
                instrument1_amount_saved_and_reduce_only_to_adjust_rate / instrument1_amount_saved_to_adjust_rate
            )
        if instrument2_amount_saved_and_reduce_only_to_adjust_rate == 0 and \
                instrument2_amount_saved_to_adjust_rate == 0:
            instrument2_rate = 1
        elif instrument2_amount_saved_and_reduce_only_to_adjust_rate != 0 and \
                instrument2_amount_saved_to_adjust_rate == 0:
            instrument2_rate = 0
        else:
            instrument2_rate = float(
                instrument2_amount_saved_and_reduce_only_to_adjust_rate / instrument2_amount_saved_to_adjust_rate
            )
        if instrument3_amount_saved_and_reduce_only_to_adjust_rate == 0 and \
                instrument3_amount_saved_to_adjust_rate == 0:
            instrument3_rate = 1
        elif instrument3_amount_saved_and_reduce_only_to_adjust_rate != 0 and \
                instrument3_amount_saved_to_adjust_rate == 0:
            instrument3_rate = 0
        else:
            instrument3_rate = float(
                instrument3_amount_saved_and_reduce_only_to_adjust_rate / instrument3_amount_saved_to_adjust_rate
            )
        if instrument4_amount_saved_and_reduce_only_to_adjust_rate == 0 and \
                instrument4_amount_saved_to_adjust_rate == 0:
            instrument4_rate = 1
        elif instrument4_amount_saved_and_reduce_only_to_adjust_rate != 0 and \
                instrument4_amount_saved_to_adjust_rate == 0:
            instrument4_rate = 0
        else:
            instrument4_rate = float(
                instrument4_amount_saved_and_reduce_only_to_adjust_rate / instrument4_amount_saved_to_adjust_rate
            )

        adjust_rate_trade_by_reduce_only = dict()
        adjust_rate_trade_by_reduce_only.clear()
        adjust_rate_trade_by_reduce_only_dict = {
            'instrument1_rate': abs(instrument1_rate),
            'instrument2_rate': abs(instrument2_rate),
            'instrument3_rate': abs(instrument3_rate),
            'instrument4_rate': abs(instrument4_rate)
        }
        smaller_adjust_rate_trade_by_reduce_only = min(
            adjust_rate_trade_by_reduce_only_dict, key=adjust_rate_trade_by_reduce_only_dict.get)  # instrument number
        smaller_adjust_rate_trade_by_reduce_only_value = abs(adjust_rate_trade_by_reduce_only_dict.get(
            smaller_adjust_rate_trade_by_reduce_only, 0))  # Valor

        amount_adjusted_setup['rate_amount'] = str(smaller_adjust_rate_trade_by_reduce_only_value)

        with open('setup.ini', 'w') as configfile:
            setup.write(configfile)
        connect.logwriter('*** Rate Trades Saved ***')
        return float(smaller_adjust_rate_trade_by_reduce_only_value)

    @staticmethod
    def adjust_rate_trade_by_reduce_only_save():
        from connection_spread import connect

        setup = ConfigParser(
            allow_no_value=True,
            inline_comment_prefixes='#',
            strict=False
        )
        setup.read('setup.ini')
        amount_setup = setup['amount']

        instrument1_amount_saved_to_adjust_rate = amount_setup['instrument1_amount']
        if instrument1_amount_saved_to_adjust_rate == 'Unassigned':
            instrument1_amount_saved_to_adjust_rate = 0
        else:
            instrument1_amount_saved_to_adjust_rate = float(instrument1_amount_saved_to_adjust_rate)
        instrument2_amount_saved_to_adjust_rate = amount_setup['instrument2_amount']
        if instrument2_amount_saved_to_adjust_rate == 'Unassigned':
            instrument2_amount_saved_to_adjust_rate = 0
        else:
            instrument2_amount_saved_to_adjust_rate = float(instrument2_amount_saved_to_adjust_rate)
        instrument3_amount_saved_to_adjust_rate = amount_setup['instrument3_amount']
        if instrument3_amount_saved_to_adjust_rate == 'Unassigned':
            instrument3_amount_saved_to_adjust_rate = 0
        else:
            instrument3_amount_saved_to_adjust_rate = float(instrument3_amount_saved_to_adjust_rate)
        instrument4_amount_saved_to_adjust_rate = amount_setup['instrument4_amount']
        if instrument4_amount_saved_to_adjust_rate == 'Unassigned':
            instrument4_amount_saved_to_adjust_rate = 0
        else:
            instrument4_amount_saved_to_adjust_rate = float(instrument4_amount_saved_to_adjust_rate)

        amount_adjusted_setup = setup['amount_adjusted']

        instrument1_amount_saved_and_reduce_only_to_adjust_rate = amount_adjusted_setup['instrument1_amount_adjusted']
        if instrument1_amount_saved_and_reduce_only_to_adjust_rate == 'Unassigned':
            instrument1_amount_saved_and_reduce_only_to_adjust_rate = 0
        else:
            instrument1_amount_saved_and_reduce_only_to_adjust_rate = float(
                instrument1_amount_saved_and_reduce_only_to_adjust_rate)
        instrument2_amount_saved_and_reduce_only_to_adjust_rate = amount_adjusted_setup['instrument2_amount_adjusted']
        if instrument2_amount_saved_and_reduce_only_to_adjust_rate == 'Unassigned':
            instrument2_amount_saved_and_reduce_only_to_adjust_rate = 0
        else:
            instrument2_amount_saved_and_reduce_only_to_adjust_rate = float(
                instrument2_amount_saved_and_reduce_only_to_adjust_rate)
        instrument3_amount_saved_and_reduce_only_to_adjust_rate = amount_adjusted_setup['instrument3_amount_adjusted']
        if instrument3_amount_saved_and_reduce_only_to_adjust_rate == 'Unassigned':
            instrument3_amount_saved_and_reduce_only_to_adjust_rate = 0
        else:
            instrument3_amount_saved_and_reduce_only_to_adjust_rate = float(
                instrument3_amount_saved_and_reduce_only_to_adjust_rate)
        instrument4_amount_saved_and_reduce_only_to_adjust_rate = amount_adjusted_setup['instrument4_amount_adjusted']
        if instrument4_amount_saved_and_reduce_only_to_adjust_rate == 'Unassigned':
            instrument4_amount_saved_and_reduce_only_to_adjust_rate = 0
        else:
            instrument4_amount_saved_and_reduce_only_to_adjust_rate = float(
                instrument4_amount_saved_and_reduce_only_to_adjust_rate)

        if instrument1_amount_saved_and_reduce_only_to_adjust_rate == 0 and\
                instrument1_amount_saved_to_adjust_rate == 0:
            instrument1_rate = 1
        elif instrument1_amount_saved_and_reduce_only_to_adjust_rate != 0 and\
                instrument1_amount_saved_to_adjust_rate == 0:
            instrument1_rate = 0
        else:
            instrument1_rate = float(
                instrument1_amount_saved_and_reduce_only_to_adjust_rate / instrument1_amount_saved_to_adjust_rate
            )
        if instrument2_amount_saved_and_reduce_only_to_adjust_rate == 0 and\
                instrument2_amount_saved_to_adjust_rate == 0:
            instrument2_rate = 1
        elif instrument2_amount_saved_and_reduce_only_to_adjust_rate != 0 and\
                instrument2_amount_saved_to_adjust_rate == 0:
            instrument2_rate = 0
        else:
            instrument2_rate = float(
                instrument2_amount_saved_and_reduce_only_to_adjust_rate / instrument2_amount_saved_to_adjust_rate
            )
        if instrument3_amount_saved_and_reduce_only_to_adjust_rate == 0 and\
                instrument3_amount_saved_to_adjust_rate == 0:
            instrument3_rate = 1
        elif instrument3_amount_saved_and_reduce_only_to_adjust_rate != 0 and\
                instrument3_amount_saved_to_adjust_rate == 0:
            instrument3_rate = 0
        else:
            instrument3_rate = float(
                instrument3_amount_saved_and_reduce_only_to_adjust_rate / instrument3_amount_saved_to_adjust_rate
            )
        if instrument4_amount_saved_and_reduce_only_to_adjust_rate == 0 and\
                instrument4_amount_saved_to_adjust_rate == 0:
            instrument4_rate = 1
        elif instrument4_amount_saved_and_reduce_only_to_adjust_rate != 0 and\
                instrument4_amount_saved_to_adjust_rate == 0:
            instrument4_rate = 0
        else:
            instrument4_rate = float(
                instrument4_amount_saved_and_reduce_only_to_adjust_rate / instrument4_amount_saved_to_adjust_rate
            )

        adjust_rate_trade_by_reduce_only = dict()
        adjust_rate_trade_by_reduce_only.clear()
        adjust_rate_trade_by_reduce_only_dict = {
            'instrument1_rate': abs(instrument1_rate),
            'instrument2_rate': abs(instrument2_rate),
            'instrument3_rate': abs(instrument3_rate),
            'instrument4_rate': abs(instrument4_rate)
        }
        smaller_adjust_rate_trade_by_reduce_only = min(
            adjust_rate_trade_by_reduce_only_dict, key=adjust_rate_trade_by_reduce_only_dict.get)  # instrument number
        smaller_adjust_rate_trade_by_reduce_only_value = abs(adjust_rate_trade_by_reduce_only_dict.get(
            smaller_adjust_rate_trade_by_reduce_only, 0))  # Valor

        amount_adjusted_setup['rate_amount'] = str(smaller_adjust_rate_trade_by_reduce_only_value)

        with open('setup.ini', 'w') as configfile:
            setup.write(configfile)
        connect.logwriter('*** Rate Trades Saved ***')

    @staticmethod
    def amount_adjusted_save():
        Instruments().amount_adjusted_save_before_rate(instrument_number=1)
        Instruments().amount_adjusted_save_before_rate(instrument_number=2)
        Instruments().amount_adjusted_save_before_rate(instrument_number=3)
        Instruments().amount_adjusted_save_before_rate(instrument_number=4)

    def amount_adjusted_save_before_rate(self, instrument_number=None):
        self.instrument_number = instrument_number
        from connection_spread import connect

        setup = ConfigParser(
            allow_no_value=True,
            inline_comment_prefixes='#',
            strict=False
        )
        setup.read('setup.ini')

        reduce_only_setup = setup['reduce_only']
        instrument_reduce_only_setup = reduce_only_setup.getboolean('instrument' + str(instrument_number))

        amount_adjusted_setup = setup['amount_adjusted']

        instrument_name_construction_from_file = InstrumentsSaved().instrument_name_construction_from_file(
                instrument_number=instrument_number)

        if instrument_name_construction_from_file == 'Unassigned':
            amount_adjusted_setup[str('instrument' + str(instrument_number) + '_amount_adjusted')] = 'Unassigned'
        elif instrument_reduce_only_setup is True and instrument_name_construction_from_file != 'Unassigned':

            instrument_direction = str(
                InstrumentsSaved().instrument_direction_construction_from_instrument_file(
                    instrument_number=instrument_number))

            amount_setup = setup['amount']
            instrument_amount_saved = amount_setup[str('instrument' + str(instrument_number) + '_amount')]

            if 'Unassigned' in instrument_amount_saved:
                instrument_amount_saved = 0
            else:
                instrument_amount_saved = float(instrument_amount_saved)

            if instrument_direction == 'sell':
                instrument_amount_saved = instrument_amount_saved * -1
            else:
                pass

            instrument_position_saved_for_reduce_only = float(
                InstrumentsSaved().instrument_position_saved(instrument_number=instrument_number)
            )

            if instrument_direction == 'buy':
                if instrument_position_saved_for_reduce_only + instrument_amount_saved <= 0:
                    amount_adjusted_setup[str('instrument' + str(instrument_number) + '_amount_adjusted')] = str(
                        instrument_amount_saved)
                else:
                    if instrument_position_saved_for_reduce_only > 0:
                        amount_adjusted_setup[str('instrument' + str(instrument_number) + '_amount_adjusted')] = str(
                            0.0)
                    else:
                        amount_adjusted_setup[str('instrument' + str(instrument_number) + '_amount_adjusted')] = str(
                            abs(instrument_position_saved_for_reduce_only))
            elif instrument_direction == 'sell':
                if instrument_position_saved_for_reduce_only + instrument_amount_saved >= 0:
                    amount_adjusted_setup[str('instrument' + str(instrument_number) + '_amount_adjusted')] = str(
                        instrument_amount_saved)
                else:
                    if instrument_position_saved_for_reduce_only < 0:
                        amount_adjusted_setup[str('instrument' + str(instrument_number) + '_amount_adjusted')] = str(
                            0.0)
                    else:
                        amount_adjusted_setup[str('instrument' + str(instrument_number) + '_amount_adjusted')] = str(
                            abs(instrument_position_saved_for_reduce_only))
            else:
                connect.logwriter('********** ERROR code 1181 - Amount Adjusted Save error')

        else:
            amount_setup = setup['amount']
            instrument_amount_saved = amount_setup[str('instrument' + str(instrument_number) + '_amount')]

            amount_adjusted_setup[str('instrument' + str(instrument_number) + '_amount_adjusted')] = str(
                instrument_amount_saved)
        
        with open('setup.ini', 'w') as configfile:
            setup.write(configfile)
        connect.logwriter('*** Amount Adjusted Saved - ' + 'Instrument ' + str(instrument_number) + ' ***')


class ConfigSaved:
    def __init__(self):
        self.self = self

    @staticmethod
    def orders_rate_saved():
        from lists import list_monitor_log

        setup = ConfigParser(
            allow_no_value=True,
            inline_comment_prefixes='#',
            strict=False
        )
        setup.read('setup.ini')
        default_setup = dict(setup['DEFAULT'])
        send_orders_rate_file_read = default_setup['orders_rate']

        list_monitor_log.append('*** Order/Second Setup: ' + str(send_orders_rate_file_read) + ' ***')

        return round(float(send_orders_rate_file_read), 2)

    @staticmethod
    def orders_rate_saved2():
        from connection_spread import connect

        setup = ConfigParser(
            allow_no_value=True,
            inline_comment_prefixes='#',
            strict=False
        )
        setup.read('setup.ini')
        default_setup = dict(setup['DEFAULT'])
        send_orders_rate_file_read = default_setup['orders_rate']

        ui.lineEdit_orders_rate.setText(str(send_orders_rate_file_read))
        connect.logwriter('*** Order/Second Setup: ' + str(send_orders_rate_file_read) + ' ***')

    @staticmethod
    def remove_log_spread_log_if_bigger_500kb_when_open_app():
        import os
        from lists import list_monitor_log

        try:
            if os.path.isfile('log_strategy_backup.log') is True:
                if float(os.path.getsize('log_strategy_backup.log')) > 8000000:
                    os.unlink('log_strategy_backup.log')
                    list_monitor_log.append('*** Deleted log_strategy_backup.log (>8MB). ***')
                else:
                    list_monitor_log.append('*** log_strategy_backup.log Size < 8MB. ***')
            else:
                pass

            if os.path.isfile('log_strategy.log') is True:
                if float(os.path.getsize('log_strategy.log')) > 500000:
                    with open('log_strategy_backup.log', 'a') as file_backup:
                        with open('log_strategy.log', 'r') as log_file:
                            file_backup.writelines(log_file)
                            list_monitor_log.append('*** Appended log_strategy.log into log_strategy_backup.log ***')
                    os.unlink('log_strategy.log')
                    list_monitor_log.append('*** Deleted and Created log_strategy.log ***')
                else:
                    list_monitor_log.append('*** log_strategy.log Size < 0.5MB. ***')
            else:
                list_monitor_log.append('*** Created log_strategy.log ***')

        except Exception as er:
            from connection_spread import connect
            connect.logwriter('***** ERROR in remove_log_spread_log_if_bigger_500kb_when_open_app(): ' +
                              str(er) + '. Error Code 1050 *****')

    @staticmethod
    def targets_saved():
        file_open = 'targets_spread.txt'
        with open(file_open, 'r') as f1:
            f2 = str(f1.read())
            f3 = str.replace(f2, 'for target setting', 'for conditions')
            return f3

    @staticmethod
    def target_saved_check():
        sinal.target_saved_check_signal.emit()

    @staticmethod
    def position_saved():
        setup = ConfigParser(
            allow_no_value=True,
            inline_comment_prefixes='#',
            strict=False
        )
        setup.read('setup.ini')
        position_saved_setup = setup['position_saved']
        position_saved = str(
            'Instrument 1: ' + str(position_saved_setup['instrument1_position_saved']) + '\n' +
            'Instrument 2: ' + str(position_saved_setup['instrument2_position_saved']) + '\n' +
            'Instrument 3: ' + str(position_saved_setup['instrument3_position_saved']) + '\n' +
            'Instrument 4: ' + str(position_saved_setup['instrument4_position_saved'])
        )
        return position_saved

    @staticmethod
    def currency_exchange_rate_for_upper_and_lower():
        with open('targets_spread.txt', 'r') as file:
            lines_file = file.readlines()  # file instruments_spread.txt ==> lines
            list_line_file = lines_file[4].split()  # line ==> list
            return str(list_line_file[7])

    @staticmethod
    def exchange_rate_lower_then():
        with open('targets_spread.txt', 'r') as file:
            lines_file = file.readlines()  # file instruments_spread.txt ==> lines
            list_line_file = lines_file[1].split()  # line ==> list
            return float(list_line_file[7])

    @staticmethod
    def exchange_rate_upper_then():
        with open('targets_spread.txt', 'r') as file:
            lines_file = file.readlines()  # file instruments_spread.txt ==> lines
            list_line_file = lines_file[0].split()  # line ==> list
            return float(list_line_file[7])

    @staticmethod
    def buy_or_sell_structure():
        with open('targets_spread.txt', 'r') as file:
            lines_file = file.readlines()  # file instruments_spread.txt ==> lines
            list_line_file = lines_file[2].split()  # line ==> list
            return list_line_file[5]

    @staticmethod
    def target_cost_structure_in_btc():
        with open('targets_spread.txt', 'r') as file:
            lines_file = file.readlines()  # file instruments_spread.txt ==> lines
            list_line_file = lines_file[3].split()  # line ==> list
            return float(list_line_file[6])

    @staticmethod
    def setup_ini_check():
        from lists import list_monitor_log
        import os

        if os.path.isfile('setup.ini') is False:
            Config().setup_ini_creator()
        else:
            list_monitor_log.append('***** There is a setup.ini file *****')


class Config:
    def __init__(self):
        self.self = self
        self.currency_exchange_rate_for_upper_and_lower1 = None
        self.currency_exchange_rate_upper1 = None
        self.currency_exchange_rate_lower1 = None
        self.buy_or_sell_structure1 = None
        self.spread_structure1 = None
        self.instrument_number = None

    def save_targets(self, currency_exchange_rate_for_upper_and_lower1=None, currency_exchange_rate_upper1=None,
                     currency_exchange_rate_lower1=None, buy_or_sell_structure1=None, spread_structure1=None):
        self.currency_exchange_rate_for_upper_and_lower1 = currency_exchange_rate_for_upper_and_lower1
        self.currency_exchange_rate_upper1 = currency_exchange_rate_upper1
        self.currency_exchange_rate_lower1 = currency_exchange_rate_lower1
        self.buy_or_sell_structure1 = buy_or_sell_structure1
        self.spread_structure1 = spread_structure1

        from connection_spread import connect
        from lists import list_monitor_log

        if float(str.replace(ui.lineEdit_currency_exchange_rate_upper1.text(), ',', '.')) > \
                float(str.replace(ui.lineEdit_currency_exchange_rate_lower1.text(), ',', '.')):
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText('\'Trade if currency quote UPPER\'\nmust be LOWER then\n\'Trade if currency quote LOWER\'')
            msg.setWindowTitle('***** ERROR *****')
            msg.exec_()
            pass
        else:
            with open('targets_spread.txt', 'w') as ft1:
                file_targets = ft1
                if buy_or_sell_structure1 == 'buy':
                    spread_structure1_adjusted = str.replace(spread_structure1, ',', '.')
                    mark_price_percentage_yes_or_no = ui.comboBox_value_given.currentText()
                    mppyon = mark_price_percentage_yes_or_no

                    if spread_structure1_adjusted != ' ':
                        if 'Mark Price %' in mppyon:
                            pass
                        elif 'USD' in mppyon or 'BTC' in mppyon:
                            spread_structure1_adjusted = str(abs(float(spread_structure1_adjusted)) * -1)
                        else:
                            connect.logwriter("Code Error 1133")
                            list_monitor_log.append("Code Error 1134")
                    else:
                        pass

                    spread_structure1_higher_or_less1 = '<'
                    file_targets.write(
                        'Trade if exchange rate upper then: ' + '> ' + currency_exchange_rate_upper1 + ' USD' +
                        '\n' +
                        'Trade if exchange rate lower then: ' + '< ' + currency_exchange_rate_lower1 + ' USD' +
                        '\n' +
                        'buy or sell the structure: ' + buy_or_sell_structure1 + '\n' +
                        'Structure cost should be higher/less: ' + spread_structure1_higher_or_less1 + ' ' +
                        spread_structure1_adjusted + ' BTC' + '\n' +
                        'instrument name to consider for target setting: ' +
                        currency_exchange_rate_for_upper_and_lower1.upper()
                    )
                    pass

                elif buy_or_sell_structure1 == 'sell':
                    spread_structure1_adjusted = str.replace(spread_structure1, ',', '.')
                    spread_structure1_higher_or_less1 = '>'
                    file_targets.write(
                        'Trade if exchange rate upper then: ' + '> ' + currency_exchange_rate_upper1 + ' USD' +
                        '\n' +
                        'Trade if exchange rate lower then: ' + '< ' + currency_exchange_rate_lower1 + ' USD' +
                        '\n' +
                        'buy or sell the structure: ' + buy_or_sell_structure1 + '\n' +
                        'Structure cost should be higher/less: ' + spread_structure1_higher_or_less1 + ' ' +
                        spread_structure1_adjusted + ' BTC' + '\n' +
                        'instrument name to consider for target setting: ' +
                        currency_exchange_rate_for_upper_and_lower1.upper()
                    )
                    pass

                else:
                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Information)
                    msg.setText('Set Strategy BUY or SELL')
                    msg.setWindowTitle('***** ERROR *****')
                    msg.exec_()
                    pass

                if str(ui.comboBox_value_given_2.currentText()) != \
                        'Set Option Strategy Cost as TRIGGER (optional)':
                    lcerl1_2 = str(ui.lineEdit_currency_exchange_rate_lower1_2.text())
                    lcerl1_2_adjusted_dot = str.replace(lcerl1_2, ',', '.')
                    file_targets.write('\n' + str(ui.comboBox_value_given_2.currentText()) +
                                       str(lcerl1_2_adjusted_dot))
                    pass
                else:
                    file_targets.write('\n' + str('Set the cost of the Options Structure as trigger (optional)'))
                    pass

            with open('value_given_in.txt', 'w') as file_value_given_in:
                write_in_value_given_in = ui.comboBox_value_given.currentText()
                file_value_given_in.write(str(write_in_value_given_in))
            pass

        ConfigSaved().target_saved_check()

    @staticmethod
    def position_before_trade_save():
        # import time
        from connection_spread import connect
        from lists import list_monitor_log

        instrument1_name = InstrumentsSaved().instrument_name_construction_from_file(instrument_number=1)
        instrument2_name = InstrumentsSaved().instrument_name_construction_from_file(instrument_number=2)
        instrument3_name = InstrumentsSaved().instrument_name_construction_from_file(instrument_number=3)
        instrument4_name = InstrumentsSaved().instrument_name_construction_from_file(instrument_number=4)

        a = instrument1_name
        b = instrument2_name
        c = instrument3_name
        d = instrument4_name

        try:
            setup = ConfigParser(
                allow_no_value=True,
                inline_comment_prefixes='#',
                strict=False
            )
            setup.read('setup.ini')
            position_saved_setup = setup['position_saved']

            if a != 'Unassigned':
                a1 = connect.get_position_size(instrument_name=a)
                if str(a1) == 'None':
                    aa = '0'
                    position_saved_setup['instrument1_position_saved'] = str(aa)
                else:
                    position_saved_setup['instrument1_position_saved'] = str(a1)
            else:
                pass

            if b != 'Unassigned':
                b1 = connect.get_position_size(instrument_name=b)
                if str(b1) == 'None':
                    aa = '0'
                    position_saved_setup['instrument2_position_saved'] = str(aa)
                else:
                    position_saved_setup['instrument2_position_saved'] = str(b1)
            else:
                pass

            if c != 'Unassigned':
                c1 = connect.get_position_size(instrument_name=c)
                if str(c1) == 'None':
                    aa = '0'
                    position_saved_setup['instrument3_position_saved'] = str(aa)
                else:
                    position_saved_setup['instrument3_position_saved'] = str(c1)
            else:
                pass

            if d != 'Unassigned':
                d1 = connect.get_position_size(instrument_name=d)
                if str(d1) == 'None':
                    aa = '0'
                    position_saved_setup['instrument4_position_saved'] = str(aa)
                else:
                    position_saved_setup['instrument4_position_saved'] = str(d1)
            else:
                pass

            if a == 'Unassigned':
                a1 = 'Unassigned'
                position_saved_setup['instrument1_position_saved'] = str(a1)
            else:
                pass

            if b == 'Unassigned':
                b1 = 'Unassigned'
                position_saved_setup['instrument2_position_saved'] = str(b1)
            else:
                pass

            if c == 'Unassigned':
                c1 = 'Unassigned'
                position_saved_setup['instrument3_position_saved'] = str(c1)
            else:
                pass

            if d == 'Unassigned':
                d1 = 'Unassigned'
                position_saved_setup['instrument4_position_saved'] = str(d1)
            else:
                pass

            with open('setup.ini', 'w') as configfile:
                setup.write(configfile)
            connect.logwriter('***  Position Saved ***')

        except Exception as er:
            connect.logwriter(str(er) + ' Error Code:: 1458')
            list_monitor_log.append(str(er) + ' Error Code:: 1451')

            list_for_signal = list()
            list_for_signal.clear()
            list_for_signal.append('Positions preview don´t saved')
            list_for_signal.append('***** ERROR *****')
            sinal.msg_box_for_thread_when_open_app1_signal.emit(list_for_signal)
            pass
        finally:
            pass

    def max_position_from_position_saved_and_instrument_amount(self, instrument_number=None):
        self.instrument_number = instrument_number
        from lists import list_monitor_log

        setup = ConfigParser(
            allow_no_value=True,
            inline_comment_prefixes='#',
            strict=False
        )
        setup.read('setup.ini')
        position_saved_setup = setup['position_saved']
        position_saved = str(
            position_saved_setup['Instrument' + str(instrument_number) + '_position_saved']
        )
        if 'Unassigned' in position_saved:
            if InstrumentsSaved().instrument_direction_construction_from_instrument_file(
                    instrument_number=instrument_number) == 'buy':
                return float(InstrumentsSaved().instrument_amount_saved(
                    instrument_number=instrument_number))
            elif InstrumentsSaved().instrument_direction_construction_from_instrument_file(
                    instrument_number=instrument_number) == 'sell':
                return float(InstrumentsSaved().instrument_amount_saved(
                    instrument_number=instrument_number)) * -1
            else:
                return 'Unassigned'
        elif 'None' in position_saved:
            list_monitor_log.append('********** ERROR **********\nSyntax ERROR or there is not \n'
                                    'Instrument ' + str(instrument_number))
            pass
            return '***** Syntax ERROR or there is not Instrument *****'
        else:
            instrument_position_preview = float(position_saved)
            if InstrumentsSaved().instrument_direction_construction_from_instrument_file(
                    instrument_number=instrument_number) == 'buy':
                return float(instrument_position_preview) + \
                        float(InstrumentsSaved().instrument_amount_saved(
                            instrument_number=instrument_number))
            elif InstrumentsSaved().instrument_direction_construction_from_instrument_file(
                    instrument_number=instrument_number) == 'sell':
                return float(instrument_position_preview) + \
                        (float(InstrumentsSaved().instrument_amount_saved(
                            instrument_number=instrument_number)) * -1)
            else:
                pass

    @staticmethod
    def setup_ini_creator():
        from lists import list_monitor_log

        now = datetime.now()
        now10 = now + timedelta(days=10)
        now_10_text = now10.strftime('%d/%m/%Y %H:%M')
        now_text = now.strftime('%d/%m/%Y %H:%M')

        setup = ConfigParser()

        dict_setup_default = {
            'name': 'VavaBot - Options Strategy',
            'version': '7.7',
            'date': '2022',
            'strategy_name': 'None',
            'orders_rate': '20.0'
        }
        setup['DEFAULT'] = dict_setup_default

        setup['credentials'] = {}
        credentials_ = setup['credentials']
        credentials_['test_net'] = 'True'

        setup['reduce_only'] = {}
        reduce_only = setup['reduce_only']
        reduce_only['instrument1'] = 'False'
        reduce_only['instrument2'] = 'False'
        reduce_only['instrument3'] = 'False'
        reduce_only['instrument4'] = 'False'
        reduce_only['dont_stop_trading_and_update_amount_adjusted'] = 'False'

        setup['amount'] = {}
        amount = setup['amount']
        amount['instrument1_amount'] = 'Unassigned'
        amount['instrument2_amount'] = 'Unassigned'
        amount['instrument3_amount'] = 'Unassigned'
        amount['instrument4_amount'] = 'Unassigned'

        setup['amount_adjusted'] = {}
        amount_adjusted = setup['amount_adjusted']
        amount_adjusted['rate_amount'] = '1'
        amount_adjusted['instrument1_amount_adjusted'] = 'Unassigned'
        amount_adjusted['instrument2_amount_adjusted'] = 'Unassigned'
        amount_adjusted['instrument3_amount_adjusted'] = 'Unassigned'
        amount_adjusted['instrument4_amount_adjusted'] = 'Unassigned'

        setup['position_saved'] = {}
        position_saved = setup['position_saved']
        position_saved['instrument1_position_saved'] = 'Unassigned'
        position_saved['instrument2_position_saved'] = 'Unassigned'
        position_saved['instrument3_position_saved'] = 'Unassigned'
        position_saved['instrument4_position_saved'] = 'Unassigned'

        setup['kind'] = {}
        kind = setup['kind']
        kind['kind_instrument1'] = 'Unassigned'
        kind['kind_instrument2'] = 'Unassigned'
        kind['kind_instrument3'] = 'Unassigned'
        kind['kind_instrument4'] = 'Unassigned'

        setup['date_time'] = {}
        date_time = setup['date_time']
        date_time['start_ischecked'] = 'False'
        date_time['start'] = now_text
        date_time['end_ischecked'] = 'False'
        date_time['end'] = now_10_text
        date_time['date_time_enabled'] = 'True'

        with open('setup.ini', 'w') as setupfile:
            setup.write(setupfile)
        list_monitor_log.append('***** Setup.ini file created *****')
        Config().date_time_saved()
        Config().reduce_only_saved()

    @staticmethod
    def date_time_saved():
        from lists import list_monitor_log
        try:
            from connection_spread import connect
            connect.logwriter('*** Date and time saved - connect ***')
        except ImportError:
            pass

        setup = ConfigParser(
            allow_no_value=True,
            inline_comment_prefixes='#',
            strict=False
        )
        setup.read('setup.ini')

        date_time_setup = setup['date_time']

        date_time_start_str = date_time_setup['start']
        date_time_start_datetime = datetime.strptime(date_time_start_str, "%d/%m/%Y %H:%M")
        date_time_start_stamp = date_time_start_datetime.timestamp()

        date_time_end_str = date_time_setup['end']
        date_time_end_datetime = datetime.strptime(date_time_end_str, "%d/%m/%Y %H:%M")
        date_time_end_stamp = date_time_end_datetime.timestamp()

        if date_time_start_stamp >= date_time_end_stamp:
            if ui.checkbox_date_time_start.isChecked() is True:
                date_time_setup['start_ischecked'] = 'True'
                true_or_false_start_ischecked = True
            else:
                date_time_setup['start_ischecked'] = 'False'
                true_or_false_start_ischecked = False

            if ui.checkbox_date_time_end.isChecked() is True:
                date_time_setup['end_ischecked'] = 'True'
                true_or_false_end_ischecked = True
            else:
                date_time_setup['end_ischecked'] = 'False'
                true_or_false_end_ischecked = False

            now = datetime.now()
            now10 = now + timedelta(days=10)
            now_10_text = now10.strftime('%d/%m/%Y %H:%M')
            now_text = now.strftime('%d/%m/%Y %H:%M')

            date_time_setup['start'] = now_text
            date_time_setup['end'] = now_10_text

            with open('setup.ini', 'w') as configfile:
                setup.write(configfile)

            list_monitor_log.append('*** Date and time saved - list ***')

            date_time_dict = dict()
            date_time_dict['text_date_time_start'] = now_text
            date_time_dict['text_date_time_end'] = now_10_text
            date_time_dict['true_or_false_start_ischecked'] = true_or_false_start_ischecked
            date_time_dict['true_or_false_end_ischecked'] = true_or_false_end_ischecked

            sinal.date_time_signal.emit(date_time_dict)
        else:
            text_date_time_start = date_time_setup['start']
            text_date_time_end = date_time_setup['end']
            true_or_false_start_ischecked = date_time_setup.getboolean('start_ischecked')
            true_or_false_end_ischecked = date_time_setup.getboolean('end_ischecked')

            date_time_dict = dict()
            date_time_dict['text_date_time_start'] = text_date_time_start
            date_time_dict['text_date_time_end'] = text_date_time_end
            date_time_dict['true_or_false_start_ischecked'] = true_or_false_start_ischecked
            date_time_dict['true_or_false_end_ischecked'] = true_or_false_end_ischecked

            sinal.date_time_signal.emit(date_time_dict)
        
    @staticmethod
    def reduce_only_saved():
        setup = ConfigParser(
            allow_no_value=True,
            inline_comment_prefixes='#',
            strict=False
        )
        setup.read('setup.ini')

        reduce_only_setup = setup['reduce_only']
        
        reduce_only_dict = dict()
        
        true_or_false_reduce_only1 = reduce_only_setup.getboolean('instrument1')        
        reduce_only_dict['true_or_false_reduce_only1'] = true_or_false_reduce_only1

        true_or_false_reduce_only2 = reduce_only_setup.getboolean('instrument2')
        reduce_only_dict['true_or_false_reduce_only2'] = true_or_false_reduce_only2

        true_or_false_reduce_only3 = reduce_only_setup.getboolean('instrument3')
        reduce_only_dict['true_or_false_reduce_only3'] = true_or_false_reduce_only3

        true_or_false_reduce_only4 = reduce_only_setup.getboolean('instrument4')
        reduce_only_dict['true_or_false_reduce_only4'] = true_or_false_reduce_only4

        sinal.reduce_only_signal.emit(reduce_only_dict)


class Quote:
    def __init__(self):
        self.self = self
        self.instrument_number = None
        self.quote_dict = None

    def instrument_market_cost(self, instrument_number):
        self.instrument_number = instrument_number

        from connection_spread import connect

        instrument_kind = InstrumentsSaved().instrument_kind_saved(
            instrument_number=instrument_number)
        instrument_name = InstrumentsSaved().instrument_name_construction_from_file(
            instrument_number=instrument_number)
        instrument_amount = InstrumentsSaved().instrument_amount_saved(
            instrument_number=instrument_number)
        instrument_direction = InstrumentsSaved().instrument_direction_construction_from_instrument_file(
            instrument_number=instrument_number)

        if instrument_kind == 'future':
            return 0
        elif instrument_name == "Unassigned":
            return 0
        elif instrument_kind == 'option':
            if instrument_direction == 'buy':
                x = connect.ask_price(instrument_name=instrument_name)

                return x * float(instrument_amount) * -1

            elif instrument_direction == 'sell':
                x = connect.bid_price(instrument_name=instrument_name)

                return x * float(instrument_amount) * 1

            else:
                pass
        else:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText('instrument market price ERROR')
            msg.setWindowTitle('***** ERROR *****')
            msg.exec_()
            pass
            return '***** ERROR in instrument market price'

    def instrument_mark_price_cost(self, instrument_number):
        self.instrument_number = instrument_number

        from connection_spread import connect

        instrument_kind = InstrumentsSaved().instrument_kind_saved(
            instrument_number=instrument_number)
        instrument_name = InstrumentsSaved().instrument_name_construction_from_file(
            instrument_number=instrument_number)
        instrument_amount = InstrumentsSaved().instrument_amount_saved(
            instrument_number=instrument_number)
        instrument_direction = InstrumentsSaved().instrument_direction_construction_from_instrument_file(
            instrument_number=instrument_number)

        if instrument_kind == 'option':
            if instrument_direction == 'buy':
                a = float(connect.mark_price(instrument_name=instrument_name))
                return a * float(instrument_amount) * -1
            elif instrument_direction == 'sell':
                a = float(connect.mark_price(instrument_name=instrument_name))
                return a * float(instrument_amount) * 1
            else:
                pass
        else:
            return 0

    @staticmethod
    def bid_ask_offer():
        from lists import list_monitor_log
        instrument1_kind = InstrumentsSaved().instrument_kind_saved(instrument_number=1)
        instrument2_kind = InstrumentsSaved().instrument_kind_saved(instrument_number=2)
        instrument3_kind = InstrumentsSaved().instrument_kind_saved(instrument_number=3)
        instrument4_kind = InstrumentsSaved().instrument_kind_saved(instrument_number=4)
        if (str(Quote().instrument_market_cost(instrument_number=1)) == '0' and instrument1_kind == 'option') or \
                (str(abs(Quote().instrument_market_cost(instrument_number=1))) ==
                 '0.0' and instrument1_kind == 'option') or \
                (str(Quote().instrument_market_cost(instrument_number=2)) == '0' and instrument2_kind == 'option') or \
                (str(abs(Quote().instrument_market_cost(instrument_number=2))) ==
                 '0.0' and instrument2_kind == 'option') or \
                (str(Quote().instrument_market_cost(instrument_number=3)) == '0' and instrument3_kind == 'option') or \
                (str(abs(Quote().instrument_market_cost(instrument_number=3))) ==
                 '0.0' and instrument3_kind == 'option') or \
                (str(Quote().instrument_market_cost(instrument_number=4)) == '0' and instrument4_kind == 'option') or \
                (str(abs(Quote().instrument_market_cost(instrument_number=4))) ==
                 '0.0' and instrument4_kind == 'option'):
            list_monitor_log.append('*** WAITING BID/ASK OFFER - There are NOT Bid/Ask offer ***')
            return 'waiting bid/ask offer'
        else:
            return 'bid/ask offer ok'

    @staticmethod
    def structure_option_mark_price_cost():
        instrument1_mark_price_cost = float(Quote().instrument_mark_price_cost(instrument_number=1))
        instrument2_mark_price_cost = float(Quote().instrument_mark_price_cost(instrument_number=2))
        instrument3_mark_price_cost = float(Quote().instrument_mark_price_cost(instrument_number=3))
        instrument4_mark_price_cost = float(Quote().instrument_mark_price_cost(instrument_number=4))
        return (instrument1_mark_price_cost + instrument2_mark_price_cost + instrument3_mark_price_cost +
                instrument4_mark_price_cost)

    @staticmethod
    def structure_option_market_cost():
        instrument1_market_cost = Quote().instrument_market_cost(instrument_number=1)
        instrument2_market_cost = Quote().instrument_market_cost(instrument_number=2)
        instrument3_market_cost = Quote().instrument_market_cost(instrument_number=3)
        instrument4_market_cost = Quote().instrument_market_cost(instrument_number=4)
        return (
            instrument1_market_cost + instrument2_market_cost + instrument3_market_cost + instrument4_market_cost)

    def instrument_mark_greek_cost(self, instrument_number):
        self.instrument_number = instrument_number

        from connection_spread import connect

        instrument_kind_greeks = InstrumentsSaved().instrument_kind_saved(
            instrument_number=instrument_number)

        if 'option' in instrument_kind_greeks:
            instrument_name_greeks = InstrumentsSaved().instrument_name_construction_from_file(
                instrument_number=instrument_number)
            book_instrument_greeks = connect.get_order_book(instrument_name=instrument_name_greeks)
            return book_instrument_greeks['greeks']
        elif 'future' in instrument_kind_greeks:
            delta_future_instrument_name = InstrumentsSaved().instrument_name_construction_from_file(
                instrument_number=instrument_number)
            last_trade_future = connect.get_last_trades_by_instrument_price(delta_future_instrument_name)
            delta_future = 1 / last_trade_future
            return {'vega': 0, 'theta': 0, 'rho': 0, 'gamma': 0, 'delta': delta_future}
        elif 'Unassigned' in instrument_kind_greeks:
            return {'vega': 0, 'theta': 0, 'rho': 0, 'gamma': 0, 'delta': 0}

    @staticmethod
    def structure_mark_greek_cost():
        import decimal
        instrument1_mark_greek_cost = Quote().instrument_mark_greek_cost(
            instrument_number=1)
        instrument1_vega = instrument1_mark_greek_cost['vega']
        instrument1_theta = instrument1_mark_greek_cost['theta']
        instrument1_rho = instrument1_mark_greek_cost['rho']
        instrument1_gamma = instrument1_mark_greek_cost['gamma']
        instrument1_delta = instrument1_mark_greek_cost['delta']

        instrument2_mark_greek_cost = Quote().instrument_mark_greek_cost(
            instrument_number=2)
        instrument2_vega = instrument2_mark_greek_cost['vega']
        instrument2_theta = instrument2_mark_greek_cost['theta']
        instrument2_rho = instrument2_mark_greek_cost['rho']
        instrument2_gamma = instrument2_mark_greek_cost['gamma']
        instrument2_delta = instrument2_mark_greek_cost['delta']

        instrument3_mark_greek_cost = Quote().instrument_mark_greek_cost(
            instrument_number=3)
        instrument3_vega = instrument3_mark_greek_cost['vega']
        instrument3_theta = instrument3_mark_greek_cost['theta']
        instrument3_rho = instrument3_mark_greek_cost['rho']
        instrument3_gamma = instrument3_mark_greek_cost['gamma']
        instrument3_delta = instrument3_mark_greek_cost['delta']

        instrument4_mark_greek_cost = Quote().instrument_mark_greek_cost(
            instrument_number=4)
        instrument4_vega = instrument4_mark_greek_cost['vega']
        instrument4_theta = instrument4_mark_greek_cost['theta']
        instrument4_rho = instrument4_mark_greek_cost['rho']
        instrument4_gamma = instrument4_mark_greek_cost['gamma']
        instrument4_delta = instrument4_mark_greek_cost['delta']

        idg1 = InstrumentsSaved().instrument_direction_construction_from_instrument_file(
            instrument_number=1)
        if idg1 == 'Unassigned':
            instrument1_amount_greeks = 0
        else:
            if idg1 == 'buy':
                instrument1_amount_greeks = abs(float(InstrumentsSaved().instrument_amount_saved(
                    instrument_number=1)))
            elif idg1 == 'sell':
                instrument1_amount_greeks = abs(float(InstrumentsSaved().instrument_amount_saved(
                    instrument_number=1))) * -1
            else:
                instrument1_amount_greeks = 0

        idg2 = InstrumentsSaved().instrument_direction_construction_from_instrument_file(
            instrument_number=2)
        if idg2 == 'Unassigned':
            instrument2_amount_greeks = 0
        else:
            if idg2 == 'buy':
                instrument2_amount_greeks = abs(float(InstrumentsSaved().instrument_amount_saved(
                    instrument_number=2)))
            elif idg2 == 'sell':
                instrument2_amount_greeks = abs(float(InstrumentsSaved().instrument_amount_saved(
                    instrument_number=2))) * -1
            else:
                instrument2_amount_greeks = 0

        idg3 = InstrumentsSaved().instrument_direction_construction_from_instrument_file(
            instrument_number=3)
        if idg3 == 'Unassigned':
            instrument3_amount_greeks = 0
        else:
            if idg3 == 'buy':
                instrument3_amount_greeks = abs(float(InstrumentsSaved().instrument_amount_saved(
                    instrument_number=3)))
            elif idg3 == 'sell':
                instrument3_amount_greeks = abs(float(InstrumentsSaved().instrument_amount_saved(
                    instrument_number=3))) * -1
            else:
                instrument3_amount_greeks = 0

        idg4 = InstrumentsSaved().instrument_direction_construction_from_instrument_file(
            instrument_number=4)
        if idg4 == 'Unassigned':
            instrument4_amount_greeks = 0
        else:
            if idg4 == 'buy':
                instrument4_amount_greeks = abs(float(InstrumentsSaved().instrument_amount_saved(
                    instrument_number=4)))
            elif idg4 == 'sell':
                instrument4_amount_greeks = abs(float(InstrumentsSaved().instrument_amount_saved(
                    instrument_number=4))) * -1
            else:
                instrument4_amount_greeks = 0

        instrument1_vega_total = float(instrument1_vega) * float(instrument1_amount_greeks)
        instrument2_vega_total = float(instrument2_vega) * float(instrument2_amount_greeks)
        instrument3_vega_total = float(instrument3_vega) * float(instrument3_amount_greeks)
        instrument4_vega_total = float(instrument4_vega) * float(instrument4_amount_greeks)

        instrument1_theta_total = float(instrument1_theta) * float(instrument1_amount_greeks)
        instrument2_theta_total = float(instrument2_theta) * float(instrument2_amount_greeks)
        instrument3_theta_total = float(instrument3_theta) * float(instrument3_amount_greeks)
        instrument4_theta_total = float(instrument4_theta) * float(instrument4_amount_greeks)

        instrument1_rho_total = float(instrument1_rho) * float(instrument1_amount_greeks)
        instrument2_rho_total = float(instrument2_rho) * float(instrument2_amount_greeks)
        instrument3_rho_total = float(instrument3_rho) * float(instrument3_amount_greeks)
        instrument4_rho_total = float(instrument4_rho) * float(instrument4_amount_greeks)

        instrument1_gamma_total = round(decimal.Context().create_decimal_from_float(
            instrument1_gamma * instrument1_amount_greeks), 5)
        instrument2_gamma_total = round(decimal.Context().create_decimal_from_float(
            instrument2_gamma * instrument2_amount_greeks), 5)
        instrument3_gamma_total = round(decimal.Context().create_decimal_from_float(
            instrument3_gamma * instrument3_amount_greeks), 5)
        instrument4_gamma_total = round(decimal.Context().create_decimal_from_float(
            instrument4_gamma * instrument4_amount_greeks), 5)

        instrument1_delta_total = float(instrument1_delta) * float(instrument1_amount_greeks)
        instrument2_delta_total = float(instrument2_delta) * float(instrument2_amount_greeks)
        instrument3_delta_total = float(instrument3_delta) * float(instrument3_amount_greeks)
        instrument4_delta_total = float(instrument4_delta) * float(instrument4_amount_greeks)

        structure_vega = round(float(instrument1_vega_total + instrument2_vega_total +
                                     instrument3_vega_total + instrument4_vega_total), 5)
        structure_theta = round(float(instrument1_theta_total + instrument2_theta_total +
                                      instrument3_theta_total + instrument4_theta_total), 5)
        structure_rho = round(float(instrument1_rho_total + instrument2_rho_total +
                                    instrument3_rho_total + instrument4_rho_total), 5)

        structure_gamma_d = \
            instrument1_gamma_total + instrument2_gamma_total + instrument3_gamma_total + instrument4_gamma_total
        structure_gamma_s = str(structure_gamma_d)

        structure_delta = round(float(instrument1_delta_total + instrument2_delta_total +
                                      instrument3_delta_total + instrument4_delta_total), 5)

        return {'vega': structure_vega,
                'theta': structure_theta,
                'rho': structure_rho,
                'gamma': structure_gamma_s,
                'delta': structure_delta
                }

    @staticmethod
    def structure_option_greeks_quote():
        c = dict()
        c.clear()
        c = Quote().structure_mark_greek_cost()
        sinal.greeks_signal1.emit(c)  # manda dados para a tabela de greeks na aba Instruments

    @staticmethod
    def last_trade_instrument_conditions_quote():
        from connection_spread import connect

        instrument_conditions_name = ui.lineEdit_currency_exchange_rate_for_upper_and_lower1.text()

        last_trade_instrument_conditions_quote_request = connect.get_last_trades_by_instrument_price(
            instrument_name=instrument_conditions_name)
        last_trade_instrument_conditions_quote_signal_dict = dict()
        last_trade_instrument_conditions_quote_signal_dict.clear()

        last_trade_instrument_conditions_quote_signal_dict['lineEdit_24_btc_index_2'] = str(
            last_trade_instrument_conditions_quote_request)
        last_trade_instrument_conditions_quote_signal_dict['lineEdit_24_btc_index_3'] = str(
            instrument_conditions_name) + ' (last trade):'

        sinal.last_trade_instrument_conditions_quote_signal.emit(last_trade_instrument_conditions_quote_signal_dict)
        # ui.lineEdit_24_btc_index_2.setText(str(last_trade_instrument_conditions_quote_request))
        # ui.lineEdit_24_btc_index_3.setText(str(instrument_conditions_name) + ' (last trade):')

    @staticmethod
    def quote_new():
        from connection_spread import connect, led_color
        from lists import list_monitor_log

        if led_color() == 'red':
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText(' Connection Offline ')
            msg.setWindowTitle('***** ERROR *****')
            msg.exec_()
            pass
        else:
            try:
                quote_new_when_open_app_signal1_dict = dict()
                quote_new_when_open_app_signal1_dict.clear()

                f9 = InstrumentsSaved().instrument_direction_construction_from_instrument_file(instrument_number=1)
                quote_new_when_open_app_signal1_dict['f9'] = str(f9)  # ui.lineEdit.setText(f9)
                f10 = InstrumentsSaved().instrument_direction_construction_from_instrument_file(instrument_number=2)
                quote_new_when_open_app_signal1_dict['f10'] = str(f10)  # ui.lineEdit_2.setText(f10)
                f11 = InstrumentsSaved().instrument_direction_construction_from_instrument_file(instrument_number=3)
                quote_new_when_open_app_signal1_dict['f11'] = str(f11)  # ui.lineEdit_3.setText(f11)
                f12 = InstrumentsSaved().instrument_direction_construction_from_instrument_file(instrument_number=4)
                quote_new_when_open_app_signal1_dict['f12'] = str(f12)  # ui.lineEdit_4.setText(f12)
                f13 = str(InstrumentsSaved().instrument_amount_saved(instrument_number=1))
                quote_new_when_open_app_signal1_dict['f13'] = str(f13)  # ui.lineEdit_7.setText(f13)
                f13_k = str(InstrumentsSaved().instrument_kind_saved(instrument_number=1))
                f14 = str(InstrumentsSaved().instrument_amount_saved(instrument_number=2))
                quote_new_when_open_app_signal1_dict['f14'] = str(f14)  # ui.lineEdit_5.setText(f14)
                f14_k = str(InstrumentsSaved().instrument_kind_saved(instrument_number=2))
                f15 = str(InstrumentsSaved().instrument_amount_saved(instrument_number=3))
                quote_new_when_open_app_signal1_dict['f15'] = str(f15)  # ui.lineEdit_8.setText(f15)
                f15_k = str(InstrumentsSaved().instrument_kind_saved(instrument_number=3))
                f16 = str(InstrumentsSaved().instrument_amount_saved(instrument_number=4))
                quote_new_when_open_app_signal1_dict['f16'] = str(f16)  # ui.lineEdit_6.setText(f16)
                f16_k = str(InstrumentsSaved().instrument_kind_saved(instrument_number=4))
                f17 = InstrumentsSaved().instrument_name_construction_from_file(instrument_number=1)
                quote_new_when_open_app_signal1_dict['f17'] = str(f17)  # ui.lineEdit_10.setText(f17)
                f18 = InstrumentsSaved().instrument_name_construction_from_file(instrument_number=2)
                quote_new_when_open_app_signal1_dict['f18'] = str(f18)  # ui.lineEdit_11.setText(f18)
                f19 = InstrumentsSaved().instrument_name_construction_from_file(instrument_number=3)
                quote_new_when_open_app_signal1_dict['f19'] = str(f19)  # ui.lineEdit_9.setText(f19)
                f20 = InstrumentsSaved().instrument_name_construction_from_file(instrument_number=4)
                quote_new_when_open_app_signal1_dict['f20'] = str(f20)  # ui.lineEdit_12.setText(f20)
                f21 = round(Quote().instrument_mark_price_cost(instrument_number=1), 4)
                f25 = str(f21)
                quote_new_when_open_app_signal1_dict['f25'] = str(f25)  # ui.lineEdit_14.setText(f25)
                f22 = round(Quote().instrument_mark_price_cost(instrument_number=2), 4)
                f26 = str(f22)
                quote_new_when_open_app_signal1_dict['f26'] = str(f26)  # ui.lineEdit_15.setText(f26)
                f23 = round(Quote().instrument_mark_price_cost(instrument_number=3), 4)
                f27 = str(f23)
                quote_new_when_open_app_signal1_dict['f27'] = str(f27)  # ui.lineEdit_13.setText(f27)
                f24 = round(Quote().instrument_mark_price_cost(instrument_number=4), 4)
                f28 = str(f24)
                quote_new_when_open_app_signal1_dict['f28'] = str(f28)  # ui.lineEdit_16.setText(f28)
                f25 = round(Quote().instrument_market_cost(instrument_number=1), 4)
                f29 = str(f25)
                quote_new_when_open_app_signal1_dict['f29'] = str(f29)  # ui.lineEdit_17.setText(f29)
                f26 = round(Quote().instrument_market_cost(instrument_number=2), 4)
                f30 = str(f26)
                quote_new_when_open_app_signal1_dict['f30'] = str(f30)  # ui.lineEdit_18.setText(f30)
                f27 = round(Quote().instrument_market_cost(instrument_number=3), 4)
                f31 = str(f27)
                quote_new_when_open_app_signal1_dict['f31'] = str(f31)  # ui.lineEdit_19.setText(f31)
                f28 = round(Quote().instrument_market_cost(instrument_number=4), 4)
                f32 = str(f28)
                quote_new_when_open_app_signal1_dict['f32'] = str(f32)  # ui.lineEdit_20.setText(f32)

                instrument_name_currency_exchange_rate = ConfigSaved().currency_exchange_rate_for_upper_and_lower()

                if Quote().bid_ask_offer() == 'waiting bid/ask offer':
                    f = float(
                        connect.get_last_trades_by_instrument_price(
                            instrument_name=instrument_name_currency_exchange_rate))
                    a = round(float(Quote().structure_option_mark_price_cost()), 5)
                    a_usd = round(float(a) * f, 2)
                    a1 = 'None - NO OPTION BID/ASK OFFER'
                    a1_a = 'None - NO BID/ASK OFFER'
                    g = ''
                    h = ''

                elif (f13 == 'Unassigned' or f13_k == 'future') and \
                        (f14 == 'Unassigned' or f14_k == 'future') and \
                        (f15 == 'Unassigned' or f15_k == 'future') and \
                        (f16 == 'Unassigned' or f16_k == 'future'):
                    a = 'All instruments Unassigned '
                    a_usd = ''
                    a1 = a
                    g = ''
                    a1_a = a
                    h = ''
                else:
                    f = float(
                        connect.get_last_trades_by_instrument_price(
                            instrument_name=instrument_name_currency_exchange_rate))

                    a = round(float(Quote().structure_option_mark_price_cost()), 5)
                    a_usd = round(float(a) * f, 2)

                    a1 = round(float(Quote().structure_option_market_cost()), 5)
                    a1_usd = round(float(a1) * f, 2)
                    if float(a) == 0:
                        a1_a = 'Strategy MARK Price = 0'
                        h = ''
                    else:
                        a1_a = round(abs(float(a1) / float(a)) * 100, 2)
                        h = '% of the Strategy MARK Price'
                    g = ' (' + str(a1_usd) + 'USD)'

                quote_new_when_open_app_signal1_dict['lineEdit_22'] = str(
                    'Strategy MARK Price: ' + str(a) + ' (' + str(a_usd) + 'USD)')
                quote_new_when_open_app_signal1_dict['lineEdit_23'] = str(
                    'Strategy MARKET Price: ' + str(a1) + g)
                quote_new_when_open_app_signal1_dict['lineEdit_21'] = str(
                    'Strategy MARKET Price cost ' + str(a1_a) + h)

                sinal.quote_new_when_open_app_signal1.emit(quote_new_when_open_app_signal1_dict)

                Quote().structure_option_greeks_quote()  # já chama signal (crei ter erro aqui)
                Quote().last_trade_instrument_conditions_quote()  # já chama signal (creir ter erro aqui)
            except Exception as er:
                connect.logwriter(str(er) + ' Error Code:: 2430')
                list_monitor_log.append(str(er) + ' Error Code:: 2430')
                list_monitor_log.append('********* Quote new ERROR Error Code:: 2430 *********')
                pass
            finally:
                pass

    @staticmethod
    def quote_new_structure_cost_for_print_when_stopped_trading():
        from connection_spread import connect, led_color
        from lists import list_monitor_log

        if led_color() == 'red':
            pass
        else:
            try:
                f13 = str(InstrumentsSaved().instrument_amount_saved(instrument_number=1))
                f13_k = str(InstrumentsSaved().instrument_kind_saved(instrument_number=1))
                f14 = str(InstrumentsSaved().instrument_amount_saved(instrument_number=2))
                f14_k = str(InstrumentsSaved().instrument_kind_saved(instrument_number=2))
                f15 = str(InstrumentsSaved().instrument_amount_saved(instrument_number=3))
                f15_k = str(InstrumentsSaved().instrument_kind_saved(instrument_number=3))
                f16 = str(InstrumentsSaved().instrument_amount_saved(instrument_number=4))
                f16_k = str(InstrumentsSaved().instrument_kind_saved(instrument_number=4))

                instrument_name_currency_exchange_rate = ConfigSaved().currency_exchange_rate_for_upper_and_lower()

                if Quote().bid_ask_offer() == 'waiting bid/ask offer':
                    f = float(
                        connect.get_last_trades_by_instrument_price(
                            instrument_name=instrument_name_currency_exchange_rate))
                    a = round(float(Quote().structure_option_mark_price_cost()), 5)
                    a_usd = round(float(a) * f, 2)
                    a1 = 'None - NO OPTION OPTION BID/ASK OFFER'
                    a1_a = 'None - NO BID/ASK OFFER'
                    g = ''
                    h = ''

                elif (f13 == 'Unassigned' or f13_k == 'future') and \
                        (f14 == 'Unassigned' or f14_k == 'future') and \
                        (f15 == 'Unassigned' or f15_k == 'future') and \
                        (f16 == 'Unassigned' or f16_k == 'future'):
                    a = 'All instruments Unassigned '
                    a_usd = ''
                    a1 = a
                    g = ''
                    a1_a = a
                    h = ''
                else:
                    f = float(
                        connect.get_last_trades_by_instrument_price(
                            instrument_name=instrument_name_currency_exchange_rate))

                    a = round(float(Quote().structure_option_mark_price_cost()), 5)
                    a_usd = round(float(a) * f, 2)

                    a1 = round(float(Quote().structure_option_market_cost()), 5)
                    a1_usd = round(float(a1) * f, 2)
                    if float(a) == 0:
                        a1_a = 'Strategy MARK Price = 0'
                        h = ''
                    else:
                        a1_a = round(abs(float(a1) / float(a)) * 100, 2)
                        h = '% of the Strategy MARK Price'
                    g = ' (' + str(a1_usd) + 'USD)'

                quote_dict = dict()
                quote_dict['text59'] = str('Strategy MARK Price: ' + str(a) + ' (' + str(a_usd) + 'USD)')
                quote_dict['text61'] = str('Strategy MARKET Price: ' + str(a1) + g)
                quote_dict['text60'] = str('Strategy MARKET Price cost: ' + str(a1_a) + h)
                quote_dict_for_signal = quote_dict
                sinal.quote_new_structure_cost_for_print_when_stopped_trading_signal1.emit(quote_dict_for_signal)

            except Exception as er:
                connect.logwriter(str(er) + ' Error Code:: 1768')
                list_monitor_log.append(str(er) + ' Error Code:: 1769')
                list_monitor_log.append('********** Quote new Strategy cost for print in tab run'
                                        ' ERROR Error Code:: 1771 **********')
                pass
            finally:
                pass


class ConditionsCheck:
    def __init__(self):
        self.self = self
        self.instrument_number = None
        self.number = None
        self.index = None
        self.greeks = None

    @staticmethod
    def structure_market_cost_trigger():  # E´de configuração opcional
        from lists import list_monitor_log
        from connection_spread import connect

        with open('targets_spread.txt', 'r') as file_structure_market_cost_trigger:
            lines_file_structure_market_cost_trigger = file_structure_market_cost_trigger.readlines()
            list_lines_file_structure_market_cost_trigger = lines_file_structure_market_cost_trigger[5].split()

        if 'Set' in str(lines_file_structure_market_cost_trigger):
            list_monitor_log.append('*** STRATEGY COST TRIGGER NO SET (optional) ***')
            return True

        elif 'in BTC >' in str(lines_file_structure_market_cost_trigger):
            # arg fixed
            value_in_btc_list_lines_file_structure_market_cost_trigger = float(
                list_lines_file_structure_market_cost_trigger[3])
            list_monitor_log.append('*** STRATEGY COST TRIGGER SELECTED IN BTC > ' +
                                    str(value_in_btc_list_lines_file_structure_market_cost_trigger) + ' ***')
            if Quote().structure_option_market_cost() > value_in_btc_list_lines_file_structure_market_cost_trigger:
                list_monitor_log.append('*** STRATEGY COST TRIGGER FILLED ***')
                return True
            else:
                list_monitor_log.append('*** WAITING STRATEGY COST TRIGGER ***')
                return False

        elif 'in BTC < ' in str(lines_file_structure_market_cost_trigger):
            value_in_btc_list_lines_file_structure_market_cost_trigger = float(
                list_lines_file_structure_market_cost_trigger[3])
            list_monitor_log.append('*** STRATEGY COST TRIGGER SELECTED IN BTC < ' +
                                    str(value_in_btc_list_lines_file_structure_market_cost_trigger) + ' ***')

            if Quote().structure_option_market_cost() < value_in_btc_list_lines_file_structure_market_cost_trigger:
                list_monitor_log.append('*** STRATEGY COST TRIGGER FILLED ***')
                return True
            else:
                list_monitor_log.append('*** WAITING STRATEGY COST TRIGGER ***')
                return False

        elif 'in Mark Price % > ' in str(lines_file_structure_market_cost_trigger):  # aqui tem ERRO
            value_in_mark_price_list_lines_file_structure_market_cost_trigger = float(
                list_lines_file_structure_market_cost_trigger[5])
            list_monitor_log.append('*** STRATEGY COST TRIGGER SELECTED IN Mark Price % > *** \n')
            list_monitor_log.append('*** Mark Price selected: Strategy MARKET Price will be >' +
                                    str(value_in_mark_price_list_lines_file_structure_market_cost_trigger) +
                                    '% of de Strategy MARK Price ***')
            # args modify
            structure_option_market_cost = float(Quote().structure_option_market_cost())
            structure_option_mark_price_cost = float(Quote().structure_option_mark_price_cost())
            if float(structure_option_mark_price_cost) != 0:
                trigger_percentage = abs(structure_option_market_cost / float(
                    structure_option_mark_price_cost)) * 100
                if trigger_percentage > float(
                        value_in_mark_price_list_lines_file_structure_market_cost_trigger):
                    list_monitor_log.append('*** Strategy MARKET price = ' +
                                            str(trigger_percentage) +
                                            '% of the Strategy MARK Price ***')
                    list_monitor_log.append('*** STRATEGY COST TRIGGER FILLED ***')
                    return True
                else:
                    list_monitor_log.append('*** Strategy MARKET price = ' +
                                            str(trigger_percentage) +
                                            '% of the Strategy MARK Price ***')
                    list_monitor_log.append('*** WAITING STRATEGY COST TRIGGER ***')
                    return False
            elif float(structure_option_mark_price_cost) == 0:
                list_monitor_log.append('*** MARK Price is 0 (ZERO) ***')
                list_monitor_log.append('*** WAITING STRATEGY COST TRIGGER ***')
                return False
            else:
                connect.logwriter(str('***** ERROR in structure_market_cost_trigger() Error Code:: 1855 *****'))
                list_monitor_log.append('***** ERROR in structure_market_cost_trigger() Error Code:: 1856 *****')
                return False

        elif 'in Mark Price % < ' in str(lines_file_structure_market_cost_trigger):
            value_in_mark_price_list_lines_file_structure_market_cost_trigger = float(
                list_lines_file_structure_market_cost_trigger[5])
            list_monitor_log.append('*** STRATEGY COST TRIGGER SELECTED IN Mark Price % < *** \n')
            list_monitor_log.append('*** Mark Price selected: Strategy MARKET Price will be <' +
                                    str(value_in_mark_price_list_lines_file_structure_market_cost_trigger) +
                                    '% of de Strategy MARK Price ***')
            # args modify
            structure_option_market_cost = float(Quote().structure_option_market_cost())
            structure_option_mark_price_cost = float(Quote().structure_option_mark_price_cost())
            if float(structure_option_mark_price_cost) != 0:
                trigger_percentage = abs(structure_option_market_cost / float(
                    structure_option_mark_price_cost)) * 100
                if trigger_percentage < float(
                        value_in_mark_price_list_lines_file_structure_market_cost_trigger):
                    list_monitor_log.append('*** Strategy MARKET price = ' +
                                            str(trigger_percentage) +
                                            '% of the Strategy MARK Price ***')
                    list_monitor_log.append('**** STRATEGY COST TRIGGER FILLED ***')
                    return True
                else:
                    list_monitor_log.append('*** Strategy MARKET price = ' +
                                            str(trigger_percentage) +
                                            '% of the Strategy MARK Price ***')
                    list_monitor_log.append('*** WAITING STRATEGY COST TRIGGER ***')
                    return False
            elif float(structure_option_mark_price_cost) == 0:
                list_monitor_log.append('*** MARK Price is 0 (ZERO) ***')
                list_monitor_log.append('*** WAITING STRATEGY COST TRIGGER ***')
                return False
            else:
                connect.logwriter(str('***** ERROR in structure_market_cost_trigger() Error Code:: 1890 *****'))
                list_monitor_log.append('***** ERROR in structure_market_cost_trigger() Error Code:: 1891 *****')
                return False

        elif 'in USD > ' in str(lines_file_structure_market_cost_trigger):
            # args fixes
            instrument_name_currency_exchange_rate = ConfigSaved().currency_exchange_rate_for_upper_and_lower()
            value_in_usd_list_lines_file_structure_market_cost_trigger = float(
                list_lines_file_structure_market_cost_trigger[3])
            list_monitor_log.append('*** STRATEGY COST TRIGGER SELECTED IN USD > ' +
                                    str(value_in_usd_list_lines_file_structure_market_cost_trigger) + ' ***')

            # args modify
            structure_option_market_cost = float(Quote().structure_option_market_cost())
            currency_exchange_rate_mark_price = float(connect.get_book_summary_by_instrument(
                instrument_name=instrument_name_currency_exchange_rate)[0]['mark_price'])
            structure_option_market_cost_usd = structure_option_market_cost * currency_exchange_rate_mark_price

            if structure_option_market_cost_usd > value_in_usd_list_lines_file_structure_market_cost_trigger:
                list_monitor_log.append('*** STRATEGY COST TRIGGER FILLED ***')
                return True
            else:
                list_monitor_log.append('*** WAITING STRATEGY COST TRIGGER ***')
                return False

        elif 'in USD < ' in str(lines_file_structure_market_cost_trigger):
            # args fixes
            instrument_name_currency_exchange_rate = ConfigSaved().currency_exchange_rate_for_upper_and_lower()
            value_in_usd_list_lines_file_structure_market_cost_trigger = float(
                list_lines_file_structure_market_cost_trigger[3])
            list_monitor_log.append('*** STRATEGY COST TRIGGER IN USD < ' +
                                    str(value_in_usd_list_lines_file_structure_market_cost_trigger) + ' ***')

            # args modify
            structure_option_market_cost = float(Quote().structure_option_market_cost())
            currency_exchange_rate_mark_price = float(connect.get_book_summary_by_instrument(
                instrument_name=instrument_name_currency_exchange_rate)[0]['mark_price'])
            structure_option_market_cost_usd = structure_option_market_cost * currency_exchange_rate_mark_price

            if structure_option_market_cost_usd < value_in_usd_list_lines_file_structure_market_cost_trigger:
                list_monitor_log.append('*** STRATEGY COST TRIGGER FILLED ***')
                return True
            else:
                list_monitor_log.append('*** WAITING STRATEGY COST TRIGGER ***')
                return False

        elif 'in Vega > ' in str(lines_file_structure_market_cost_trigger):
            structure_option_market_cost_vega = float(Quote().structure_mark_greek_cost()['vega'])
            value_in_vega_list_lines_file_structure_market_cost_trigger = float(
                list_lines_file_structure_market_cost_trigger[3])
            list_monitor_log.append('*** STRATEGY COST TRIGGER SELECTED IN VEGA > ' +
                                    str(value_in_vega_list_lines_file_structure_market_cost_trigger) + ' ***')
            if structure_option_market_cost_vega > value_in_vega_list_lines_file_structure_market_cost_trigger:
                list_monitor_log.append('*** STRATEGY COST TRIGGER FILLED ***')
                return True
            else:
                list_monitor_log.append('*** WAITING STRATEGY COST TRIGGER ***')
                return False

        elif 'in Vega < ' in str(lines_file_structure_market_cost_trigger):
            structure_option_market_cost_vega = float(Quote().structure_mark_greek_cost()['vega'])
            value_in_vega_list_lines_file_structure_market_cost_trigger = float(
                list_lines_file_structure_market_cost_trigger[3])
            list_monitor_log.append('*** STRATEGY COST TRIGGER SELECTED IN VEGA < ' +
                                    str(value_in_vega_list_lines_file_structure_market_cost_trigger) + ' ***')
            if structure_option_market_cost_vega < value_in_vega_list_lines_file_structure_market_cost_trigger:
                list_monitor_log.append('*** STRATEGY COST TRIGGER FILLED ***')
                return True
            else:
                list_monitor_log.append('*** WAITING STRATEGY COST TRIGGER ***')
                return False

        elif 'in Delta > ' in str(lines_file_structure_market_cost_trigger):
            structure_option_market_cost_delta = float(Quote().structure_mark_greek_cost()['delta'])
            value_in_delta_list_lines_file_structure_market_cost_trigger = float(
                list_lines_file_structure_market_cost_trigger[3])
            list_monitor_log.append('*** STRATEGY COST TRIGGER SELECTED IN DELTA > ' +
                                    str(value_in_delta_list_lines_file_structure_market_cost_trigger) + ' ***')
            if structure_option_market_cost_delta > value_in_delta_list_lines_file_structure_market_cost_trigger:
                list_monitor_log.append('*** STRATEGY COST TRIGGER FILLED ***')
                return True
            else:
                list_monitor_log.append('*** WAITING STRATEGY COST TRIGGER ***')
                return False

        elif 'in Delta < ' in str(lines_file_structure_market_cost_trigger):
            structure_option_market_cost_delta = float(Quote().structure_mark_greek_cost()['delta'])
            value_in_delta_list_lines_file_structure_market_cost_trigger = float(
                list_lines_file_structure_market_cost_trigger[3])
            list_monitor_log.append('*** STRATEGY COST TRIGGER SELECTED IN DELTA < ' +
                                    str(value_in_delta_list_lines_file_structure_market_cost_trigger) + ' ***')
            if structure_option_market_cost_delta < value_in_delta_list_lines_file_structure_market_cost_trigger:
                list_monitor_log.append('*** STRATEGY COST TRIGGER FILLED ***')
                return True
            else:
                list_monitor_log.append('*** WAITING STRATEGY COST TRIGGER ***')
                return False

        elif 'in Theta > ' in str(lines_file_structure_market_cost_trigger):
            structure_option_market_cost_theta = float(Quote().structure_mark_greek_cost()['theta'])
            value_in_theta_list_lines_file_structure_market_cost_trigger = float(
                list_lines_file_structure_market_cost_trigger[3])
            list_monitor_log.append('*** STRATEGY COST TRIGGER SELECTED IN THETA > ' +
                                    str(value_in_theta_list_lines_file_structure_market_cost_trigger) + ' ***')
            if structure_option_market_cost_theta > value_in_theta_list_lines_file_structure_market_cost_trigger:
                list_monitor_log.append('*** STRATEGY COST TRIGGER FILLED ***')
                return True
            else:
                list_monitor_log.append('*** WAITING STRATEGY COST TRIGGER ***')
                return False

        elif 'in Theta < ' in str(lines_file_structure_market_cost_trigger):
            structure_option_market_cost_theta = float(Quote().structure_mark_greek_cost()['theta'])
            value_in_theta_list_lines_file_structure_market_cost_trigger = float(
                list_lines_file_structure_market_cost_trigger[3])
            list_monitor_log.append('*** STRATEGY COST TRIGGER SELECTED IN THETA < ' +
                                    str(value_in_theta_list_lines_file_structure_market_cost_trigger) + ' ***')
            if structure_option_market_cost_theta < value_in_theta_list_lines_file_structure_market_cost_trigger:
                list_monitor_log.append('*** STRATEGY COST TRIGGER FILLED ***')
                return True
            else:
                list_monitor_log.append('*** WAITING STRATEGY COST TRIGGER ***')
                return False

        elif 'in Gamma > ' in str(lines_file_structure_market_cost_trigger):
            structure_option_market_cost_gamma = float(Quote().structure_mark_greek_cost()['gamma'])
            value_in_gamma_list_lines_file_structure_market_cost_trigger = float(
                list_lines_file_structure_market_cost_trigger[3])
            list_monitor_log.append('*** STRATEGY COST TRIGGER SELECTED IN GAMMA > ' +
                                    str(value_in_gamma_list_lines_file_structure_market_cost_trigger) + ' ***')
            if structure_option_market_cost_gamma > value_in_gamma_list_lines_file_structure_market_cost_trigger:
                list_monitor_log.append('*** STRATEGY COST TRIGGER FILLED ***')
                return True
            else:
                list_monitor_log.append('*** WAITING STRATEGY COST TRIGGER ***')
                return False

        elif 'in Gamma < ' in str(lines_file_structure_market_cost_trigger):
            structure_option_market_cost_gamma = float(Quote().structure_mark_greek_cost()['gamma'])
            value_in_gamma_list_lines_file_structure_market_cost_trigger = float(
                list_lines_file_structure_market_cost_trigger[3])
            list_monitor_log.append('*** STRATEGY COST TRIGGER SELECTED IN GAMMA < ' +
                                    str(value_in_gamma_list_lines_file_structure_market_cost_trigger) + ' ***')
            if structure_option_market_cost_gamma < value_in_gamma_list_lines_file_structure_market_cost_trigger:
                list_monitor_log.append('*** STRATEGY COST TRIGGER FILLED ***')
                return True
            else:
                list_monitor_log.append('*** WAITING STRATEGY COST TRIGGER ***')
                return False

        elif 'in Rho > ' in str(lines_file_structure_market_cost_trigger):
            structure_option_market_cost_rho = float(Quote().structure_mark_greek_cost()['rho'])
            value_in_rho_list_lines_file_structure_market_cost_trigger = float(
                list_lines_file_structure_market_cost_trigger[3])
            list_monitor_log.append('*** STRATEGY COST TRIGGER SELECTED IN RHO > ' +
                                    str(value_in_rho_list_lines_file_structure_market_cost_trigger) + ' ***')
            if structure_option_market_cost_rho > value_in_rho_list_lines_file_structure_market_cost_trigger:
                list_monitor_log.append('*** STRATEGY COST TRIGGER FILLED ***')
                return True
            else:
                list_monitor_log.append('*** WAITING STRATEGY COST TRIGGER ***')
                return False

        elif 'in Rho < ' in str(lines_file_structure_market_cost_trigger):
            structure_option_market_cost_rho = float(Quote().structure_mark_greek_cost()['rho'])
            value_in_rho_list_lines_file_structure_market_cost_trigger = float(
                list_lines_file_structure_market_cost_trigger[3])
            list_monitor_log.append('*** STRATEGY COST TRIGGER SELECTED IN RHO < ' +
                                    str(value_in_rho_list_lines_file_structure_market_cost_trigger) + ' ***')
            if structure_option_market_cost_rho < value_in_rho_list_lines_file_structure_market_cost_trigger:
                list_monitor_log.append('*** STRATEGY COST TRIGGER FILLED ***')
                return True
            else:
                list_monitor_log.append('*** WAITING STRATEGY COST TRIGGER ***')
                return False

        elif 'in Vol >' in str(lines_file_structure_market_cost_trigger):
            value_in_btc_vol_list_lines_file_structure_market_cost_trigger = float(
                list_lines_file_structure_market_cost_trigger[3])

            currency_exchange_rate_for_upper_and_lower_for_btc_vol = str(
                ConfigSaved().currency_exchange_rate_for_upper_and_lower())

            if 'BTC' in currency_exchange_rate_for_upper_and_lower_for_btc_vol:
                currency = 'BTC'
            elif 'ETH' in currency_exchange_rate_for_upper_and_lower_for_btc_vol:
                currency = 'ETH'
            elif 'SOL' in currency_exchange_rate_for_upper_and_lower_for_btc_vol:
                currency = 'SOL'
            elif 'USDC' in currency_exchange_rate_for_upper_and_lower_for_btc_vol:
                currency = 'USDC'
            else:
                currency = 'BTC'
                connect.logwriter(str('***** ERROR in structure_market_cost_trigger() Error Code:: 2085 *****'))
                list_monitor_log.append('*** ERROR in structure_market_cost_trigger Error Code:: 2086 ***')

            list_monitor_log.append('*** STRATEGY COST TRIGGER SELECTED IN ' + str(currency) + ' VOL > ' +
                                    str(value_in_btc_vol_list_lines_file_structure_market_cost_trigger) + ' ***')

            vol = float(connect.volatility_index_data(currency=currency))

            if vol == 0:
                connect.logwriter(str('***** ERROR in structure_market_cost_trigger() Error Code:: 2094 *****'))
                list_monitor_log.append('*** ERROR in structure_market_cost_trigger Error Code:: 2095. '
                                        'connect.volatility_index_data Returned 0 (zero) ***')
                return False
            elif vol > float(value_in_btc_vol_list_lines_file_structure_market_cost_trigger):
                list_monitor_log.append('*** ' + str(currency) + ' Vol = ' +
                                        str(vol) +
                                        ' ***')
                list_monitor_log.append('**** STRATEGY COST TRIGGER FILLED ***')
                return True
            elif vol <= float(value_in_btc_vol_list_lines_file_structure_market_cost_trigger):
                list_monitor_log.append('*** ' + str(currency) + ' Vol = ' +
                                        str(vol) +
                                        ' ***')
                list_monitor_log.append('*** WAITING STRATEGY COST TRIGGER ***')
                return False
            else:
                connect.logwriter(str('***** ERROR in structure_market_cost_trigger() Error Code:: 2111 *****'))
                list_monitor_log.append('*** ERROR in structure_market_cost_trigger Error Code:: 2112 ***')
                return False

        elif 'in Vol <' in str(lines_file_structure_market_cost_trigger):
            value_in_btc_vol_list_lines_file_structure_market_cost_trigger = float(
                list_lines_file_structure_market_cost_trigger[3])

            currency_exchange_rate_for_upper_and_lower_for_btc_vol = str(
                ConfigSaved().currency_exchange_rate_for_upper_and_lower())

            if 'BTC' in currency_exchange_rate_for_upper_and_lower_for_btc_vol:
                currency = 'BTC'
            elif 'ETH' in currency_exchange_rate_for_upper_and_lower_for_btc_vol:
                currency = 'ETH'
            elif 'SOL' in currency_exchange_rate_for_upper_and_lower_for_btc_vol:
                currency = 'SOL'
            elif 'USDC' in currency_exchange_rate_for_upper_and_lower_for_btc_vol:
                currency = 'USDC'
            else:
                currency = 'BTC'
                list_monitor_log.append('*** ERROR in structure_market_cost_trigger Error Code:: 2132 ***')

            list_monitor_log.append('*** STRATEGY COST TRIGGER SELECTED IN ' + str(currency) + ' VOL < ' +
                                    str(value_in_btc_vol_list_lines_file_structure_market_cost_trigger) + ' ***')

            vol = float(connect.volatility_index_data(currency=currency))

            if vol == 0:
                connect.logwriter(str('***** ERROR in structure_market_cost_trigger() Error Code:: 2140 *****'))
                list_monitor_log.append('*** ERROR in structure_market_cost_trigger Error Code:: 2141. '
                                        'connect.volatility_index_data Returned 0 (zero) ***')
                return False
            elif vol < float(value_in_btc_vol_list_lines_file_structure_market_cost_trigger):
                list_monitor_log.append('*** ' + str(currency) + ' Vol = ' +
                                        str(vol) +
                                        ' ***')
                list_monitor_log.append('**** STRATEGY COST TRIGGER FILLED ***')
                return True
            elif vol >= float(value_in_btc_vol_list_lines_file_structure_market_cost_trigger):
                list_monitor_log.append('*** ' + str(currency) + ' Vol = ' +
                                        str(vol) +
                                        ' ***')
                list_monitor_log.append('*** WAITING STRATEGY COST TRIGGER ***')
                return False
            else:
                connect.logwriter(str('***** ERROR in structure_market_cost_trigger() Error Code:: 2157 *****'))
                list_monitor_log.append('*** ERROR in structure_market_cost_trigger Error Code:: 2158 ***')
                return False

        else:
            connect.logwriter(str('***** ERROR in structure_market_cost_trigger() Error Code:: 2162 *****'))
            list_monitor_log.append(
                '*** ERROR IN STRATEGY COST TRIGGER - Error Code:: 2164 ***')
            return False

    def position_option_smaller_max_position_instrument(self, instrument_number=None):
        self.instrument_number = instrument_number
        from connection_spread import connect
        from lists import list_monitor_log

        # Args fixes
        instrument_max_position = Config().max_position_from_position_saved_and_instrument_amount(
            instrument_number=instrument_number)
        instrument_kind = InstrumentsSaved().instrument_kind_saved(instrument_number=instrument_number)
        instrument_name = InstrumentsSaved().instrument_name_construction_from_file(instrument_number=instrument_number)
        instrument_direction = InstrumentsSaved().instrument_direction_construction_from_instrument_file(
            instrument_number=instrument_number)
        if instrument_max_position != 'Unassigned' and instrument_kind == 'option':
            a5a = connect.get_position_size(instrument_name=instrument_name)
            if str(a5a) == 'None':
                a5b = '0'
                a5 = float(a5b)
            else:
                a5 = float(a5a)
            b5 = instrument_max_position
            d5 = instrument_direction
            if a5 < b5 and round(b5 - a5, 1) >= 0.1 and d5 == 'buy':
                return 'instrument_run_trade_ok'
            elif a5 == b5 or round(b5 - a5, 1) < 0.1 and d5 == 'buy':
                return 'instrument_run_trade_no'
            elif a5 > b5 and d5 == 'buy':
                connect.logwriter('****************** ERROR: Instrument ' + str(
                    instrument_number) + ' position > max position Error Code:: 2195 ******************')
                list_monitor_log.append(
                    '****************** ERROR: Instrument ' + str(instrument_number) +
                    ' position > max position ****************** Error Code:: 2198')
                return 'instrument_run_trade_no'
            elif a5 > b5 and abs(round(b5 - a5, 1)) >= 0.1 and d5 == 'sell':
                return 'instrument_run_trade_ok'
            elif a5 == b5 or abs(round(b5 - a5, 1)) < 0.1 and d5 == 'sell':
                return 'instrument_run_trade_no'
            elif a5 < b5 and d5 == 'sell':
                connect.logwriter(
                    '****************** ERROR: Instrument ' + str(instrument_number) +
                    ' position > max position Error Code:: 2207 ******************')
                list_monitor_log.append(
                    '****************** ERROR: Instrument ' + str(instrument_number) +
                    ' position > max position Error Code:: 2210 ******************')
                return 'instrument_run_trade_no'
            else:
                pass
        elif instrument_max_position == 'Unassigned' or instrument_kind == 'future':
            return 'instrument_run_trade_no'
        else:
            connect.logwriter(
                '****************** ERROR: position_option_smaller_max_position_instrument '
                'vavabot_spread.py Error Code:: 2219 ******************')
            list_monitor_log.append('****************** ERROR: position_option_smaller_max_position_instrument '
                                    'vavabot_spread.py Error Code:: 2221 ******************')
            return 'instrument_run_trade_no'

    @staticmethod
    def position_option_smaller_max_position_instruments_():
        from lists import list_monitor_log
        from connection_spread import connect
        # args modify
        position_option_smaller_max_position_instrument1 = \
            ConditionsCheck().position_option_smaller_max_position_instrument(instrument_number=1)
        position_option_smaller_max_position_instrument2 = \
            ConditionsCheck().position_option_smaller_max_position_instrument(instrument_number=2)
        position_option_smaller_max_position_instrument3 = \
            ConditionsCheck().position_option_smaller_max_position_instrument(instrument_number=3)
        position_option_smaller_max_position_instrument4 = \
            ConditionsCheck().position_option_smaller_max_position_instrument(instrument_number=4)
        if position_option_smaller_max_position_instrument1 == 'instrument_run_trade_no' and \
                position_option_smaller_max_position_instrument2 == 'instrument_run_trade_no' and \
                position_option_smaller_max_position_instrument3 == 'instrument_run_trade_no' and \
                position_option_smaller_max_position_instrument4 == 'instrument_run_trade_no':
            list_monitor_log.append('***** NO OPTIONS FOR TRADING *****')
            return 'position_option_smaller_max_position_instruments_no'
        elif position_option_smaller_max_position_instrument1 == 'instrument_run_trade_ok' or \
                position_option_smaller_max_position_instrument2 == 'instrument_run_trade_ok' or \
                position_option_smaller_max_position_instrument3 == 'instrument_run_trade_ok' or \
                position_option_smaller_max_position_instrument4 == 'instrument_run_trade_ok':
            list_monitor_log.append('***** WAITING FOR TRADING OPTIONS SETTINGS')
            return 'position_option_smaller_max_position_instruments_ok'
        else:
            connect.logwriter('********** ERROR IN OPTION POSITION SMALLER MAX POSITION INSTRUMENTS '
                              'Error Code:: 2252 **********')
            list_monitor_log.append('********** ERROR IN OPTION POSITION SMALLER MAX POSITION INSTRUMENTS '
                                    'Error Code:: 2254 **********')
            return 'position_option_smaller_max_position_instruments_ERROR'

    @staticmethod
    def min_max_price_option_buy_or_sell_order_by_mark_price():
        from lists import list_monitor_log

        # args modify
        a1 = abs(float(Quote().instrument_mark_price_cost(instrument_number=1)))
        a2 = abs(float(Quote().instrument_mark_price_cost(instrument_number=2)))
        a3 = abs(float(Quote().instrument_mark_price_cost(instrument_number=3)))
        a4 = abs(float(Quote().instrument_mark_price_cost(instrument_number=4)))

        b1 = abs(float(Quote().instrument_market_cost(instrument_number=1)))
        b2 = abs(float(Quote().instrument_market_cost(instrument_number=2)))
        b3 = abs(float(Quote().instrument_market_cost(instrument_number=3)))
        b4 = abs(float(Quote().instrument_market_cost(instrument_number=4)))

        # args fixes
        instrument1_direction = \
            InstrumentsSaved().instrument_direction_construction_from_instrument_file(instrument_number=1)
        instrument2_direction = \
            InstrumentsSaved().instrument_direction_construction_from_instrument_file(instrument_number=2)
        instrument3_direction = \
            InstrumentsSaved().instrument_direction_construction_from_instrument_file(instrument_number=3)
        instrument4_direction = \
            InstrumentsSaved().instrument_direction_construction_from_instrument_file(instrument_number=4)

        if (b1 == 0 and InstrumentsSaved().instrument_kind_saved(instrument_number=1) == 'option') or \
                (b2 == 0 and InstrumentsSaved().instrument_kind_saved(instrument_number=2) == 'option') or \
                (b3 == 0 and InstrumentsSaved().instrument_kind_saved(instrument_number=3) == 'option') or \
                (b4 == 0 and InstrumentsSaved().instrument_kind_saved(instrument_number=4) == 'option'):
            list_monitor_log.append('*** WAITING FOR BID/ASK OFFER - There are NOT Bid/Ask Offer ***')
            return 'waiting trade'
        elif b1 > (a1 + (30 * a1 / 100)) and instrument1_direction == 'buy':
            list_monitor_log.append('*** Market price > 30% Mark Price ***')
            list_monitor_log.append('*** WAITING REDUCE OPTION MARKET PRICE INSTRUMENT 1 ***')
            return 'waiting trade'
        elif b2 > (a2 + (30 * a2 / 100)) and instrument2_direction == 'buy':
            list_monitor_log.append('*** Market price > 30% Mark Price ***')
            list_monitor_log.append('*** WAITING REDUCE OPTION MARKET PRICE INSTRUMENT 2 ***')
            return 'waiting trade'
        elif b3 > (a3 + (30 * a3 / 100)) and instrument3_direction == 'buy':
            list_monitor_log.append('*** Market price > 30% Mark Price ***')
            list_monitor_log.append('*** WAITING REDUCE OPTION MARKET PRICE INSTRUMENT 3 ***')
            return 'waiting trade'
        elif b4 > (a4 + (30 * a4 / 100)) and instrument4_direction == 'buy':
            list_monitor_log.append('*** Market price > 30% Mark Price ***')
            list_monitor_log.append('WAITING REDUCE OPTION MARKET PRICE INSTRUMENT 4')
            return 'waiting trade'
        elif b1 < (a1 - (30 * a1 / 100)) and instrument1_direction == 'sell':
            list_monitor_log.append('*** Market price < 30% Mark Price ***')
            list_monitor_log.append('*** WAITING INCREASE OPTION MARKET PRICE INSTRUMENT 1 ***')
            return 'waiting trade'
        elif b2 < (a2 - (30 * a2 / 100)) and instrument2_direction == 'sell':
            list_monitor_log.append('*** Market price < 30% Mark Price ***')
            list_monitor_log.append('*** WAITING INCREASE OPTION MARKET PRICE INSTRUMENT 2 ***')
            return 'waiting trade'
        elif b3 < (a3 - (30 * a3 / 100)) and instrument3_direction == 'sell':
            list_monitor_log.append('*** Market price < 30% Mark Price ***')
            list_monitor_log.append('*** WAITING INCREASE OPTION MARKET PRICE INSTRUMENT 3 ***')
            return 'waiting trade'
        elif b4 < (a4 - (30 * a4 / 100)) and instrument4_direction == 'sell':
            list_monitor_log.append('*** Market price < 30% Mark Price ***')
            list_monitor_log.append('*** WAITING INCREASE OPTION MARKET PRICE INSTRUMENT 4 ***')
            return 'waiting trade'

        else:
            return 'ok'

    @staticmethod
    def value_give_in_achieved():
        from lists import list_monitor_log
        from connection_spread import connect

        with open('value_given_in.txt', 'r') as file_vgi:
            read_file_vgi = str(file_vgi.read())
        try:
            if 'BTC' not in read_file_vgi:
                with open('targets_spread.txt', 'r') as ft:
                    lines_ft = ft.readlines()  # file targets_spread.txt ==> lines
                    list_line_target_cost_structure_in = lines_ft[3].split()
                    target_cost_structure_in = float(list_line_target_cost_structure_in[6])

                if 'Mark' in read_file_vgi:
                    list_monitor_log.append('*** STRATEGY COST SETTED:  MARK PRICE % ***')
                    buy_or_sell_structure = ConfigSaved().buy_or_sell_structure()

                    if buy_or_sell_structure == 'buy':
                        structure_option_market_cost = Quote().structure_option_market_cost()
                        structure_option_mark_price_cost = Quote().structure_option_mark_price_cost()

                        if float(structure_option_mark_price_cost) != 0:
                            mark_percentage = abs(float(
                                structure_option_market_cost) / float(structure_option_mark_price_cost)) * 100
                            if mark_percentage <= abs(float(target_cost_structure_in)):
                                list_monitor_log.append('*** Strategy option MARKET price: ' +
                                                        str(mark_percentage) +
                                                        '% of the Strategy option MARK price - CONDITION FILLED - ***')
                                list_monitor_log.append('*** value_give_in_achieved Mark % is TRUE ***')
                                return True
                            else:
                                list_monitor_log.append('Waiting Strategy option market cost <= ' +
                                                        str(target_cost_structure_in) +
                                                        '% of the Mark cost')

                                mark_percentage = abs(float(
                                    structure_option_market_cost) / float(structure_option_mark_price_cost)) * 100

                                list_monitor_log.append('Strategy option MARKET price is: ' +
                                                        str(mark_percentage) +
                                                        '% of the MARK cost.')
                                list_monitor_log.append('*** WAITING  STRATEGY COST TO BE FILLED ***')
                                return False
                        elif float(structure_option_mark_price_cost) == 0:
                            connect.logwriter('*** MARK price is 0 (ZERO) Error Code:: 2369 ***')
                            list_monitor_log.append('*** MARK price is 0 (ZERO) Error Code:: 2370 ***')
                            return False
                        else:
                            connect.logwriter('***** ERROR in value_give_in_achieved() Error Code:: 2373 *****')
                            list_monitor_log.append('***** ERROR in value_give_in_achieved() Error Code:: 2374 *****')
                            return False

                    elif buy_or_sell_structure == 'sell':
                        structure_option_market_cost = Quote().structure_option_market_cost()
                        structure_option_mark_price_cost = Quote().structure_option_mark_price_cost()

                        if float(structure_option_mark_price_cost) != 0:
                            mark_percentage = abs(float(
                                structure_option_market_cost) / float(structure_option_mark_price_cost)) * 100
                            if mark_percentage >= abs(float(target_cost_structure_in)):
                                list_monitor_log.append('*** Strategy option MARKET price: ' +
                                                        str(mark_percentage) +
                                                        '% of the Strategy option MARK price - CONDITION FILLED - ***')
                                list_monitor_log.append('*** value_give_in_achieved Mark % is TRUE ***')
                                return True
                            else:
                                list_monitor_log.append('Waiting Strategy option market cost >= ' +
                                                        str(target_cost_structure_in) +
                                                        '% of the Mark cost')

                                mark_percentage = abs(float(
                                    structure_option_market_cost) / float(structure_option_mark_price_cost)) * 100

                                list_monitor_log.append('Strategy option MARKET price is: ' +
                                                        str(mark_percentage) +
                                                        '% of the MARK cost.')
                                list_monitor_log.append('*** WAITING  STRATEGY COST TO BE FILLED ***')
                                return False
                        elif float(structure_option_mark_price_cost) == 0:
                            connect.logwriter('*** MARK price is 0 (ZERO) Error Code:: 2404 ***')
                            list_monitor_log.append('*** MARK price is 0 (ZERO) Error Code:: 2405 ***')
                            return False
                        else:
                            connect.logwriter('***** ERROR in value_give_in_achieved() Error Code:: 2408 *****')
                            list_monitor_log.append('***** ERROR in value_give_in_achieved() Error Code:: 2409 *****')
                            return False
                    else:
                        connect.logwriter('***** ERROR in value_give_in_achieved() Error Code:: 2412 *****')
                        list_monitor_log.append('**** ERRORR - value_give_in_achieved - Error Code:: 2413 *****')
                        return False

                elif 'USD' in read_file_vgi:
                    list_monitor_log.append('*** STRATEGY COST SETTED:  USD ***')
                    buy_or_sell_structure = ConfigSaved().buy_or_sell_structure()

                    if buy_or_sell_structure == 'buy':
                        instrument_name_currency_exchange_rate = \
                            ConfigSaved().currency_exchange_rate_for_upper_and_lower()
                        structure_option_market_cost = float(Quote().structure_option_market_cost())
                        currency_exchange_rate_mark_price = float(connect.get_book_summary_by_instrument(
                            instrument_name=instrument_name_currency_exchange_rate)[0]['mark_price'])
                        structure_option_market_cost_usd = structure_option_market_cost * \
                            currency_exchange_rate_mark_price
                        if float(structure_option_market_cost_usd) >= float(target_cost_structure_in):
                            list_monitor_log.append('*** Strategy option market cost current (' +
                                                    str(structure_option_market_cost_usd) +
                                                    'USD >= ' +
                                                    str(target_cost_structure_in) +
                                                    'USD) Strategy MARKET cost target - Condition Filled - ***')
                            list_monitor_log.append('*** value_give_in_achieved USD is TRUE ***')
                            return True
                        else:
                            list_monitor_log.append('Waiting Strategy option market cost >= ' +
                                                    str(target_cost_structure_in) +
                                                    'USD')
                            list_monitor_log.append('Strategy option market cost current: ' +
                                                    str(structure_option_market_cost_usd) +
                                                    'USD')
                            list_monitor_log.append('\n*** WAITING  STRATEGY COST TO BE FILLED ***')
                            return False

                    elif buy_or_sell_structure == 'sell':
                        instrument_name_currency_exchange_rate = \
                            ConfigSaved().currency_exchange_rate_for_upper_and_lower()
                        structure_option_market_cost = float(Quote().structure_option_market_cost())
                        currency_exchange_rate_mark_price = float(connect.get_book_summary_by_instrument(
                            instrument_name=instrument_name_currency_exchange_rate)[0]['mark_price'])
                        structure_option_market_cost_usd = structure_option_market_cost * \
                            currency_exchange_rate_mark_price
                        if float(structure_option_market_cost_usd) >= float(target_cost_structure_in):
                            list_monitor_log.append('*** Strategy option market cost current (' +
                                                    str(structure_option_market_cost_usd) +
                                                    'USD > ' +
                                                    str(target_cost_structure_in) +
                                                    'USD) Strategy MARKET cost targe - Condition Filled - ***')
                            list_monitor_log.append('*** value_give_in_achieved USD is TRUE ***')
                            return True
                        else:
                            list_monitor_log.append('Waiting Strategy option market cost > ' +
                                                    str(target_cost_structure_in) +
                                                    'USD')
                            list_monitor_log.append('Strategy option market cost now: ' +
                                                    str(structure_option_market_cost_usd) +
                                                    'USD')
                            list_monitor_log.append('\n*** WAITING  STRATEGY COST TO BE FILLED ***')
                            return False
                    else:
                        connect.logwriter('***** ERROR in value_give_in_achieved() Error Code:: 2474 *****')
                        list_monitor_log.append(
                            '********** ERROR in value_give_in_achieved Error Code:: 2476 **********')
                        return False

                else:
                    connect.logwriter('***** ERROR in value_give_in_achieved() Error Code:: 2480 *****')
                    list_monitor_log.append('********* ERRORR - value_give_in_achieved Error Code:: 2481 ***********')

            elif 'BTC' in read_file_vgi:
                with open('targets_spread.txt', 'r') as ft:
                    lines_ft = ft.readlines()  # file targets_spread.txt ==> lines
                    list_line_target_cost_structure_in = lines_ft[3].split()
                    target_cost_structure_in = float(list_line_target_cost_structure_in[6])

                list_monitor_log.append('*** STRATEGY COST SETTED:  BTC ***')
                buy_or_sell_structure = ConfigSaved().buy_or_sell_structure()

                if buy_or_sell_structure == 'buy':
                    structure_option_market_cost = float(Quote().structure_option_market_cost())
                    if float(structure_option_market_cost) >= float(target_cost_structure_in):
                        list_monitor_log.append('*** Strategy option market cost current (' +
                                                str(structure_option_market_cost) + ' >= ' +
                                                str(target_cost_structure_in) +
                                                ') Strategy MARKET cost target - '
                                                'Strategy option market cost - Condition Filled - ***')
                        list_monitor_log.append('*** value_give_in_achieved BTC is TRUE ***')
                        return True
                    else:
                        list_monitor_log.append('Waiting Strategy option market cost >= ' +
                                                str(target_cost_structure_in) + 'BTC')
                        list_monitor_log.append('Strategy option market cost current: ' +
                                                str(structure_option_market_cost) + 'BTC')
                        list_monitor_log.append('\n*** WAITING  STRATEGY COST TO BE FILLED ***')
                        return False

                elif buy_or_sell_structure == 'sell':
                    structure_option_market_cost = float(Quote().structure_option_market_cost())
                    if float(structure_option_market_cost) >= float(target_cost_structure_in):
                        list_monitor_log.append('*** Strategy option market cost current (' +
                                                str(structure_option_market_cost) + ' > ' +
                                                str(target_cost_structure_in) +
                                                ') Strategy MARKET cost target - '
                                                'Strategy option market cost - Condition Filled - ***')
                        list_monitor_log.append('*** value_give_in_achieved BTC is TRUE ***')
                        return True
                    else:
                        list_monitor_log.append('Waiting Strategy option market cost > ' +
                                                str(target_cost_structure_in) + 'BTC')
                        list_monitor_log.append('Strategy option market cost now: ' +
                                                str(structure_option_market_cost) + 'BTC')
                        list_monitor_log.append('\n*** WAITING STRATEGY COST TO BE FILLED ***')
                        return False
                else:
                    connect.logwriter('***** ERROR in value_give_in_achieved() Error Code:: 2530 *****')
                    list_monitor_log.append('********* ERROR in def value_give_in_achieved Error Code:: 2531 *********')
                    return False
            else:
                connect.logwriter('***** ERROR in value_give_in_achieved() Error Code:: 2534 *****')
                list_monitor_log.append('********** ERROR in def value_give_in_achieved Error Code:: 2535 **********')
                return False
        except Exception as er:
            connect.logwriter(str(er) + ' Error Code:: 2538')
            list_monitor_log.append('target_cost_structure_in_btc Error Code:: 2539' + str(er))
            return False
        finally:
            pass

    def number_multiple_0_1_and_round_1_digits(self, number=None):
        self.number = number

        # a3 = round(number - number % 0.1, 1)  # Creio que seria somente round.
        return round(number, 1)

    @staticmethod
    def send_options_orders_like_first_time():
        from connection_spread import connect
        from lists import list_monitor_log
        try:
            # ABAIXO PRIMEIRAS ORDENS ENVIADAS SE ACIMA NÃO HOUVER AJUSTES
            # Args fixes
            instrument1_amount = InstrumentsSaved().instrument_amount_saved(instrument_number=1)
            instrument2_amount = InstrumentsSaved().instrument_amount_saved(instrument_number=2)
            instrument3_amount = InstrumentsSaved().instrument_amount_saved(instrument_number=3)
            instrument4_amount = InstrumentsSaved().instrument_amount_saved(instrument_number=4)

            instrument1_kind = InstrumentsSaved().instrument_kind_saved(instrument_number=1)
            instrument2_kind = InstrumentsSaved().instrument_kind_saved(instrument_number=2)
            instrument3_kind = InstrumentsSaved().instrument_kind_saved(instrument_number=3)
            instrument4_kind = InstrumentsSaved().instrument_kind_saved(instrument_number=4)

            instrument1_name = InstrumentsSaved().instrument_name_construction_from_file(instrument_number=1)
            instrument2_name = InstrumentsSaved().instrument_name_construction_from_file(instrument_number=2)
            instrument3_name = InstrumentsSaved().instrument_name_construction_from_file(instrument_number=3)
            instrument4_name = InstrumentsSaved().instrument_name_construction_from_file(instrument_number=4)

            instrument1_max_position_return = Config().max_position_from_position_saved_and_instrument_amount(
                instrument_number=1)
            if type(instrument1_max_position_return) is float or type(instrument1_max_position_return) is int:
                instrument1_max_position = float(instrument1_max_position_return)
            else:
                instrument1_max_position = 0
            instrument2_max_position_return = Config().max_position_from_position_saved_and_instrument_amount(
                instrument_number=2)
            if type(instrument2_max_position_return) is float or type(instrument2_max_position_return) is int:
                instrument2_max_position = float(instrument2_max_position_return)
            else:
                instrument2_max_position = 0
            instrument3_max_position_return = Config().max_position_from_position_saved_and_instrument_amount(
                instrument_number=3)
            if type(instrument3_max_position_return) is float or type(instrument3_max_position_return) is int:
                instrument3_max_position = float(instrument3_max_position_return)
            else:
                instrument3_max_position = 0
            instrument4_max_position_return = Config().max_position_from_position_saved_and_instrument_amount(
                instrument_number=4)
            if type(instrument4_max_position_return) is float or type(instrument4_max_position_return) is int:
                instrument4_max_position = float(instrument4_max_position_return)
            else:
                instrument4_max_position = 0

            instrument1_direction = InstrumentsSaved().instrument_direction_construction_from_instrument_file(
                instrument_number=1)
            instrument2_direction = InstrumentsSaved().instrument_direction_construction_from_instrument_file(
                instrument_number=2)
            instrument3_direction = InstrumentsSaved().instrument_direction_construction_from_instrument_file(
                instrument_number=3)
            instrument4_direction = InstrumentsSaved().instrument_direction_construction_from_instrument_file(
                instrument_number=4)

            # Args modify
            position_option_smaller_max_position_instrument1 = \
                ConditionsCheck().position_option_smaller_max_position_instrument(instrument_number=1)
            position_option_smaller_max_position_instrument2 = \
                ConditionsCheck().position_option_smaller_max_position_instrument(instrument_number=2)
            position_option_smaller_max_position_instrument3 = \
                ConditionsCheck().position_option_smaller_max_position_instrument(instrument_number=3)
            position_option_smaller_max_position_instrument4 = \
                ConditionsCheck().position_option_smaller_max_position_instrument(instrument_number=4)

            instrument1_position = 0
            instrument2_position = 0
            instrument3_position = 0
            instrument4_position = 0
            if instrument1_amount != 'Unassigned' and instrument1_kind == 'option':
                instrument1_position = float(connect.get_position_size(instrument_name=instrument1_name))
            if instrument2_amount != 'Unassigned' and instrument2_kind == 'option':
                instrument2_position = float(connect.get_position_size(instrument_name=instrument2_name))
            if instrument3_amount != 'Unassigned' and instrument3_kind == 'option':
                instrument3_position = float(connect.get_position_size(instrument_name=instrument3_name))
            if instrument4_amount != 'Unassigned' and instrument4_kind == 'option':
                instrument4_position = float(connect.get_position_size(instrument_name=instrument4_name))

            # old def smaller_bid_ask_amount_book
            smaller_bid_ask_amount_book_dict = dict()
            smaller_bid_ask_amount_book_dict.clear()

            xx1 = float  # o que falta negociar
            xx2 = float
            xx3 = float
            xx4 = float

            yy1 = float
            yy2 = float
            yy3 = float
            yy4 = float

            if instrument1_direction == 'buy' and instrument1_kind == 'option':
                instrument_position = float(instrument1_position)
                y1 = connect.best_ask_amount(instrument_name=instrument1_name)
                yy1 = connect.ask_price(instrument_name=instrument1_name)

                x1 = float(instrument1_max_position)
                xx1a = float(x1) - float(instrument_position)
                xx1 = round(xx1a, 1)
                if xx1a == 0:
                    smaller_bid_ask_amount_book_dict[1] = 1
                else:
                    yy = float(y1) / xx1a
                    smaller_bid_ask_amount_book_dict[1] = abs(yy)
            elif instrument1_direction == 'sell' and instrument1_kind == 'option':
                instrument_position = float(instrument1_position)
                y1 = connect.best_bid_amount(instrument_name=instrument1_name)
                yy1 = connect.bid_price(instrument_name=instrument1_name)

                x1 = float(instrument1_max_position)
                xx1a = float(x1) - float(instrument_position)  # É o que falta negociar
                xx1 = round(xx1a, 1)
                if xx1a == 0:
                    smaller_bid_ask_amount_book_dict[1] = 1
                else:
                    yy = float(y1) / xx1a
                    smaller_bid_ask_amount_book_dict[1] = abs(yy)
            else:
                pass

            if instrument2_direction == 'buy' and instrument2_kind == 'option':
                instrument_position = float(instrument2_position)
                y2 = connect.best_ask_amount(instrument_name=instrument2_name)
                yy2 = connect.ask_price(instrument_name=instrument2_name)

                x2 = float(instrument2_max_position)
                xx2a = float(x2) - float(instrument_position)
                xx2 = round(xx2a, 1)
                if xx2a == 0:
                    smaller_bid_ask_amount_book_dict[2] = 1
                else:
                    yy = float(y2) / xx2a
                    smaller_bid_ask_amount_book_dict[2] = abs(yy)
            elif instrument2_direction == 'sell' and instrument2_kind == 'option':
                instrument_position = float(instrument2_position)
                y2 = connect.best_bid_amount(instrument_name=instrument2_name)
                yy2 = connect.bid_price(instrument_name=instrument2_name)

                x2 = float(instrument2_max_position)
                xx2a = float(x2) - float(instrument_position)
                xx2 = round(xx2a, 1)
                if xx2a == 0:
                    smaller_bid_ask_amount_book_dict[2] = 1
                else:
                    yy = float(y2) / xx2a
                    smaller_bid_ask_amount_book_dict[2] = abs(yy)
            else:
                pass

            if instrument3_direction == 'buy' and instrument3_kind == 'option':
                instrument_position = float(instrument3_position)
                y3 = connect.best_ask_amount(instrument_name=instrument3_name)
                yy3 = connect.ask_price(instrument_name=instrument3_name)

                x3 = float(instrument3_max_position)
                xx3a = float(x3) - float(instrument_position)
                xx3 = round(xx3a, 1)
                if xx3a == 0:
                    smaller_bid_ask_amount_book_dict[3] = 1
                else:
                    yy = float(y3) / xx3a
                    smaller_bid_ask_amount_book_dict[3] = abs(yy)
            elif instrument3_direction == 'sell' and instrument3_kind == 'option':
                instrument_position = float(instrument3_position)
                y3 = connect.best_bid_amount(instrument_name=instrument3_name)
                yy3 = connect.bid_price(instrument_name=instrument3_name)

                x3 = float(instrument3_max_position)
                xx3a = float(x3) - float(instrument_position)
                xx3 = round(xx3a, 1)
                if xx3a == 0:
                    smaller_bid_ask_amount_book_dict[3] = 1
                else:
                    yy = float(y3) / xx3a
                    smaller_bid_ask_amount_book_dict[3] = abs(yy)
            else:
                pass

            if instrument4_direction == 'buy' and instrument4_kind == 'option':
                instrument_position = float(instrument4_position)
                y4 = connect.best_ask_amount(instrument_name=instrument4_name)
                yy4 = connect.ask_price(instrument_name=instrument4_name)

                x4 = float(instrument4_max_position)
                xx4a = float(x4) - float(instrument_position)
                xx4 = round(xx4a, 1)
                if xx4a == 0:
                    smaller_bid_ask_amount_book_dict[4] = 1
                else:
                    yy = float(y4) / xx4a
                    smaller_bid_ask_amount_book_dict[4] = abs(yy)
            elif instrument4_direction == 'sell' and instrument4_kind == 'option':
                instrument_position = float(instrument4_position)
                y4 = connect.best_bid_amount(instrument_name=instrument4_name)
                yy4 = connect.bid_price(instrument_name=instrument4_name)

                x4 = float(instrument4_max_position)
                xx4a = float(x4) - float(instrument_position)
                xx4 = round(xx4a, 1)
                if xx4a == 0:
                    smaller_bid_ask_amount_book_dict[4] = 1
                else:
                    yy = float(y4) / xx4a
                    smaller_bid_ask_amount_book_dict[4] = abs(yy)
            else:
                pass

            if len(smaller_bid_ask_amount_book_dict) > 0:
                smaller_bid_ask_amount_book_instrument_number = min(
                    smaller_bid_ask_amount_book_dict, key=smaller_bid_ask_amount_book_dict.get)  # instrument number
                smaller_bid_ask_amount_book_ratio = abs(smaller_bid_ask_amount_book_dict.get(
                    smaller_bid_ask_amount_book_instrument_number, 0))  # Valor
            else:
                smaller_bid_ask_amount_book_ratio = 0  # valor

            # ********************************************************************************
            # Send Orders:
            # Para criar a variável para depois informar no list_monitor_log_append após informar 'ORDERS SENT'
            list_monitor_log_append_for_msg_after_orders_sent1 = 'Instrument 1: NO ORDER SENT'
            list_monitor_log_append_for_msg_after_orders_sent2 = 'Instrument 2: NO ORDER SENT'
            list_monitor_log_append_for_msg_after_orders_sent3 = 'Instrument 3: NO ORDER SENT'
            list_monitor_log_append_for_msg_after_orders_sent4 = 'Instrument 4: NO ORDER SENT'

            # instrument1:
            if instrument1_amount != 'Unassigned' and instrument1_kind == 'option' and \
                    position_option_smaller_max_position_instrument1 == 'instrument_run_trade_ok':

                instrument1_price = yy1  # market price
                # xx1 é o que falta comprar
                if 0 < smaller_bid_ask_amount_book_ratio < 1:
                    b = xx1 * smaller_bid_ask_amount_book_ratio
                    order_amount_instrument1 = ConditionsCheck().number_multiple_0_1_and_round_1_digits(
                        number=b)
                    if instrument1_direction == 'buy':
                        if float(instrument1_position) + abs(float(order_amount_instrument1)) > float(
                                instrument1_max_position):
                            order_amount_instrument1 = abs(float(xx1))
                        else:
                            pass
                        connect.buy_limit(currency=instrument1_name, amount=abs(order_amount_instrument1),
                                          price=instrument1_price)
                        list_monitor_log_append_for_msg_after_orders_sent1 = str((str(instrument1_name) +
                                                                                  ': ' + str(instrument1_direction) +
                                                                                  ' ' + str(order_amount_instrument1) +
                                                                                  ' at ' + str(instrument1_price)))
                    elif instrument1_direction == 'sell':
                        if float(instrument1_position) - abs(float(order_amount_instrument1)) < float(
                                instrument1_max_position):
                            order_amount_instrument1 = abs(float(xx1))
                        else:
                            pass
                        connect.sell_limit(currency=instrument1_name, amount=abs(order_amount_instrument1),
                                           price=instrument1_price)
                        list_monitor_log_append_for_msg_after_orders_sent1 = str((str(instrument1_name) +
                                                                                  ': ' + str(instrument1_direction) +
                                                                                  ' ' + str(order_amount_instrument1) +
                                                                                  ' at ' + str(instrument1_price)))
                    else:
                        pass
                elif smaller_bid_ask_amount_book_ratio >= 1:
                    a = abs(xx1)
                    order_amount_instrument1 = ConditionsCheck().number_multiple_0_1_and_round_1_digits(number=a)
                    if instrument1_direction == 'buy':
                        connect.buy_limit(currency=instrument1_name, amount=abs(order_amount_instrument1),
                                          price=instrument1_price)
                        list_monitor_log_append_for_msg_after_orders_sent1 = str((str(instrument1_name) +
                                                                                  ': ' + str(instrument1_direction) +
                                                                                  ' ' + str(order_amount_instrument1) +
                                                                                  ' at ' + str(instrument1_price)))
                    elif instrument1_direction == 'sell':
                        connect.sell_limit(currency=instrument1_name, amount=abs(order_amount_instrument1),
                                           price=instrument1_price)
                        list_monitor_log_append_for_msg_after_orders_sent1 = str((str(instrument1_name) +
                                                                                  ': ' + str(instrument1_direction) +
                                                                                  ' ' + str(order_amount_instrument1) +
                                                                                  ' at ' + str(instrument1_price)))
                    else:
                        pass
                else:
                    pass
            else:
                pass

            # instrument2:
            if instrument2_amount != 'Unassigned' and instrument2_kind == 'option' and \
                    position_option_smaller_max_position_instrument2 == 'instrument_run_trade_ok':

                instrument2_price = yy2
                if 0 < smaller_bid_ask_amount_book_ratio < 1:
                    b = xx2 * smaller_bid_ask_amount_book_ratio
                    order_amount_instrument2 = ConditionsCheck().number_multiple_0_1_and_round_1_digits(
                        number=b)
                    if instrument2_direction == 'buy':
                        if float(instrument2_position) + abs(float(order_amount_instrument2)) > float(
                                instrument2_max_position):
                            order_amount_instrument2 = abs(float(xx2))
                        else:
                            pass
                        connect.buy_limit(currency=instrument2_name, amount=abs(order_amount_instrument2),
                                          price=instrument2_price)
                        list_monitor_log_append_for_msg_after_orders_sent2 = str((str(instrument2_name) +
                                                                                  ': ' + str(instrument2_direction) +
                                                                                  ' ' + str(order_amount_instrument2) +
                                                                                  ' at ' + str(instrument2_price)))
                    elif instrument2_direction == 'sell':
                        if float(instrument2_position) - abs(float(order_amount_instrument2)) < float(
                                instrument2_max_position):
                            order_amount_instrument2 = abs(float(xx2))
                        else:
                            pass
                        connect.sell_limit(currency=instrument2_name, amount=abs(order_amount_instrument2),
                                           price=instrument2_price)
                        list_monitor_log_append_for_msg_after_orders_sent2 = str((str(instrument2_name) +
                                                                                  ': ' + str(instrument2_direction) +
                                                                                  ' ' + str(order_amount_instrument2) +
                                                                                  ' at ' + str(instrument2_price)))
                    else:
                        pass
                elif smaller_bid_ask_amount_book_ratio >= 1:
                    a = abs(xx2)
                    order_amount_instrument2 = ConditionsCheck().number_multiple_0_1_and_round_1_digits(number=a)
                    if instrument2_direction == 'buy':
                        connect.buy_limit(currency=instrument2_name, amount=abs(order_amount_instrument2),
                                          price=instrument2_price)
                        list_monitor_log_append_for_msg_after_orders_sent2 = str((str(instrument2_name) +
                                                                                  ': ' + str(instrument2_direction) +
                                                                                  ' ' + str(order_amount_instrument2) +
                                                                                  ' at ' + str(instrument2_price)))
                    elif instrument2_direction == 'sell':
                        connect.sell_limit(currency=instrument2_name, amount=abs(order_amount_instrument2),
                                           price=instrument2_price)
                        list_monitor_log_append_for_msg_after_orders_sent2 = str((str(instrument2_name) +
                                                                                  ': ' + str(instrument2_direction) +
                                                                                  ' ' + str(order_amount_instrument2) +
                                                                                  ' at ' + str(instrument2_price)))
                    else:
                        pass
                else:
                    pass
            else:
                pass

            # instrument3:
            if instrument3_amount != 'Unassigned' and instrument3_kind == 'option' and \
                    position_option_smaller_max_position_instrument3 == 'instrument_run_trade_ok':

                instrument3_price = yy3  # market price

                if 0 < smaller_bid_ask_amount_book_ratio < 1:
                    b = xx3 * smaller_bid_ask_amount_book_ratio
                    order_amount_instrument3 = ConditionsCheck().number_multiple_0_1_and_round_1_digits(
                        number=b)
                    if instrument3_direction == 'buy':
                        if float(instrument3_position) + abs(float(order_amount_instrument3)) > float(
                                instrument3_max_position):
                            order_amount_instrument3 = abs(float(xx3))
                        else:
                            pass
                        connect.buy_limit(currency=instrument3_name, amount=abs(order_amount_instrument3),
                                          price=instrument3_price)
                        list_monitor_log_append_for_msg_after_orders_sent3 = str((str(instrument3_name) +
                                                                                  ': ' + str(instrument3_direction) +
                                                                                  ' ' + str(order_amount_instrument3) +
                                                                                  ' at ' + str(instrument3_price)))
                    elif instrument3_direction == 'sell':
                        if float(instrument3_position) - abs(float(order_amount_instrument3)) < float(
                                instrument3_max_position):
                            order_amount_instrument3 = abs(float(xx3))
                        else:
                            pass
                        connect.sell_limit(currency=instrument3_name, amount=abs(order_amount_instrument3),
                                           price=instrument3_price)
                        list_monitor_log_append_for_msg_after_orders_sent3 = str((str(instrument3_name) +
                                                                                  ': ' + str(instrument3_direction) +
                                                                                  ' ' + str(order_amount_instrument3) +
                                                                                  ' at ' + str(instrument3_price)))
                    else:
                        pass
                elif smaller_bid_ask_amount_book_ratio >= 1:
                    a = abs(xx3)
                    order_amount_instrument3 = ConditionsCheck().number_multiple_0_1_and_round_1_digits(number=a)
                    if instrument3_direction == 'buy':
                        connect.buy_limit(currency=instrument3_name, amount=abs(order_amount_instrument3),
                                          price=instrument3_price)
                        list_monitor_log_append_for_msg_after_orders_sent3 = str((str(instrument3_name) +
                                                                                  ': ' + str(instrument3_direction) +
                                                                                  ' ' + str(order_amount_instrument3) +
                                                                                  ' at ' + str(instrument3_price)))
                    elif instrument3_direction == 'sell':
                        connect.sell_limit(currency=instrument3_name, amount=abs(order_amount_instrument3),
                                           price=instrument3_price)
                        list_monitor_log_append_for_msg_after_orders_sent3 = str((str(instrument3_name) +
                                                                                  ': ' + str(instrument3_direction) +
                                                                                  ' ' + str(order_amount_instrument3) +
                                                                                  ' at ' + str(instrument3_price)))
                    else:
                        pass
                else:
                    pass
            else:
                pass

            # instrument4:
            if instrument4_amount != 'Unassigned' and instrument4_kind == 'option' and \
                    position_option_smaller_max_position_instrument4 == 'instrument_run_trade_ok':

                instrument4_price = yy4  # market price

                if 0 < smaller_bid_ask_amount_book_ratio < 1:
                    b = xx4 * smaller_bid_ask_amount_book_ratio
                    order_amount_instrument4 = ConditionsCheck().number_multiple_0_1_and_round_1_digits(
                        number=b)
                    if instrument4_direction == 'buy':
                        if float(instrument4_position) + abs(float(order_amount_instrument4)) > float(
                                instrument4_max_position):
                            order_amount_instrument4 = abs(float(xx4))
                        else:
                            pass
                        connect.buy_limit(currency=instrument4_name, amount=abs(order_amount_instrument4),
                                          price=instrument4_price)
                        list_monitor_log_append_for_msg_after_orders_sent4 = str((str(instrument4_name) +
                                                                                  ': ' + str(instrument4_direction) +
                                                                                  ' ' + str(order_amount_instrument4) +
                                                                                  ' at ' + str(instrument4_price)))
                    elif instrument4_direction == 'sell':
                        if float(instrument4_position) - abs(float(order_amount_instrument4)) < float(
                                instrument4_max_position):
                            order_amount_instrument4 = abs(float(xx4))
                        else:
                            pass
                        connect.sell_limit(currency=instrument4_name, amount=abs(order_amount_instrument4),
                                           price=instrument4_price)
                        list_monitor_log_append_for_msg_after_orders_sent4 = str((str(instrument4_name) +
                                                                                  ': ' + str(instrument4_direction) +
                                                                                  ' ' + str(order_amount_instrument4) +
                                                                                  ' at ' + str(instrument4_price)))
                    else:
                        pass
                elif smaller_bid_ask_amount_book_ratio >= 1:
                    a = abs(xx4)
                    order_amount_instrument4 = ConditionsCheck().number_multiple_0_1_and_round_1_digits(number=a)
                    if instrument4_direction == 'buy':
                        connect.buy_limit(currency=instrument4_name, amount=abs(order_amount_instrument4),
                                          price=instrument4_price)
                        list_monitor_log_append_for_msg_after_orders_sent4 = str((str(instrument4_name) +
                                                                                  ': ' + str(instrument4_direction) +
                                                                                  ' ' + str(order_amount_instrument4) +
                                                                                  ' at ' + str(instrument4_price)))
                    elif instrument4_direction == 'sell':
                        connect.sell_limit(currency=instrument4_name, amount=abs(order_amount_instrument4),
                                           price=instrument4_price)
                        list_monitor_log_append_for_msg_after_orders_sent4 = str((str(instrument4_name) +
                                                                                  ': ' + str(instrument4_direction) +
                                                                                  ' ' + str(order_amount_instrument4) +
                                                                                  ' at ' + str(instrument4_price)))
                    else:
                        pass
                else:
                    pass
            else:
                pass

            list_monitor_log.append('********** SENT ORDERS AFTER ADJUSTMENTS **********')
            connect.logwriter('********** SENT ORDERS AFTER ADJUSTMENTS **********')
            # Para informar quais ordens foram enviadas
            list_monitor_log.append(str(list_monitor_log_append_for_msg_after_orders_sent1))
            list_monitor_log.append(str(list_monitor_log_append_for_msg_after_orders_sent2))
            list_monitor_log.append(str(list_monitor_log_append_for_msg_after_orders_sent3))
            list_monitor_log.append(str(list_monitor_log_append_for_msg_after_orders_sent4))

            time.sleep(10)
            connect.cancel_all()

        except Exception as er:
            list_monitor_log.append('ERROR in send_options_orders_like_first_time(). Error Code 3031 ' + str(er))
            connect.logwriter('ERROR in send_options_orders_like_first_time(). Error Code 3032 ' + str(er))
        finally:
            pass

    @staticmethod
    def send_options_orders():
        from connection_spread import connect
        from lists import list_monitor_log
        try:
            # Args fixes
            instrument1_amount = InstrumentsSaved().instrument_amount_saved(instrument_number=1)
            instrument2_amount = InstrumentsSaved().instrument_amount_saved(instrument_number=2)
            instrument3_amount = InstrumentsSaved().instrument_amount_saved(instrument_number=3)
            instrument4_amount = InstrumentsSaved().instrument_amount_saved(instrument_number=4)

            instrument1_kind = InstrumentsSaved().instrument_kind_saved(instrument_number=1)
            instrument2_kind = InstrumentsSaved().instrument_kind_saved(instrument_number=2)
            instrument3_kind = InstrumentsSaved().instrument_kind_saved(instrument_number=3)
            instrument4_kind = InstrumentsSaved().instrument_kind_saved(instrument_number=4)

            instrument1_direction = InstrumentsSaved().instrument_direction_construction_from_instrument_file(
                instrument_number=1)
            instrument2_direction = InstrumentsSaved().instrument_direction_construction_from_instrument_file(
                instrument_number=2)
            instrument3_direction = InstrumentsSaved().instrument_direction_construction_from_instrument_file(
                instrument_number=3)
            instrument4_direction = InstrumentsSaved().instrument_direction_construction_from_instrument_file(
                instrument_number=4)

            instrument_amount1_for_bigger_rate_options_now = InstrumentsSaved().instrument_amount_saved(
                instrument_number=1)
            instrument_amount2_for_bigger_rate_options_now = InstrumentsSaved().instrument_amount_saved(
                instrument_number=2)
            instrument_amount3_for_bigger_rate_options_now = InstrumentsSaved().instrument_amount_saved(
                instrument_number=3)
            instrument_amount4_for_bigger_rate_options_now = InstrumentsSaved().instrument_amount_saved(
                instrument_number=4)
            if instrument1_direction == 'sell' and instrument1_kind == 'option' and \
                    instrument_amount1_for_bigger_rate_options_now != 0:
                instrument_amount1_for_bigger_rate_options_now = float(
                    instrument_amount1_for_bigger_rate_options_now) * -1
            else:
                pass
            if instrument2_direction == 'sell' and instrument2_kind == 'option' and \
                    instrument_amount2_for_bigger_rate_options_now != 0:
                instrument_amount2_for_bigger_rate_options_now = float(
                    instrument_amount2_for_bigger_rate_options_now) * -1
            else:
                pass
            if instrument3_direction == 'sell' and instrument3_kind == 'option' and \
                    instrument_amount3_for_bigger_rate_options_now != 0:
                instrument_amount3_for_bigger_rate_options_now = float(
                    instrument_amount3_for_bigger_rate_options_now) * -1
            else:
                pass
            if instrument4_direction == 'sell' and instrument4_kind == 'option' and \
                    instrument_amount4_for_bigger_rate_options_now != 0:
                instrument_amount4_for_bigger_rate_options_now = float(
                    instrument_amount4_for_bigger_rate_options_now) * -1
            else:
                pass

            instrument1_name = InstrumentsSaved().instrument_name_construction_from_file(instrument_number=1)
            instrument2_name = InstrumentsSaved().instrument_name_construction_from_file(instrument_number=2)
            instrument3_name = InstrumentsSaved().instrument_name_construction_from_file(instrument_number=3)
            instrument4_name = InstrumentsSaved().instrument_name_construction_from_file(instrument_number=4)

            instrument1_max_position_return = Config().max_position_from_position_saved_and_instrument_amount(
                instrument_number=1)
            if type(instrument1_max_position_return) is float or type(instrument1_max_position_return) is int:
                instrument1_max_position = float(instrument1_max_position_return)
            else:
                instrument1_max_position = 0
            instrument2_max_position_return = Config().max_position_from_position_saved_and_instrument_amount(
                instrument_number=2)
            if type(instrument2_max_position_return) is float or type(instrument2_max_position_return) is int:
                instrument2_max_position = float(instrument2_max_position_return)
            else:
                instrument2_max_position = 0
            instrument3_max_position_return = Config().max_position_from_position_saved_and_instrument_amount(
                instrument_number=3)
            if type(instrument3_max_position_return) is float or type(instrument3_max_position_return) is int:
                instrument3_max_position = float(instrument3_max_position_return)
            else:
                instrument3_max_position = 0
            instrument4_max_position_return = Config().max_position_from_position_saved_and_instrument_amount(
                instrument_number=4)
            if type(instrument4_max_position_return) is float or type(instrument4_max_position_return) is int:
                instrument4_max_position = float(instrument4_max_position_return)
            else:
                instrument4_max_position = 0

            # Args modify
            position_option_smaller_max_position_instrument1 = \
                ConditionsCheck().position_option_smaller_max_position_instrument(instrument_number=1)
            position_option_smaller_max_position_instrument2 = \
                ConditionsCheck().position_option_smaller_max_position_instrument(instrument_number=2)
            position_option_smaller_max_position_instrument3 = \
                ConditionsCheck().position_option_smaller_max_position_instrument(instrument_number=3)
            position_option_smaller_max_position_instrument4 = \
                ConditionsCheck().position_option_smaller_max_position_instrument(instrument_number=4)

            instrument1_position = 0
            instrument2_position = 0
            instrument3_position = 0
            instrument4_position = 0
            if instrument_amount1_for_bigger_rate_options_now != 'Unassigned' and instrument1_kind == 'option':
                instrument1_position = float(connect.get_position_size(instrument_name=instrument1_name))
            if instrument_amount2_for_bigger_rate_options_now != 'Unassigned' and instrument2_kind == 'option':
                instrument2_position = float(connect.get_position_size(instrument_name=instrument2_name))
            if instrument_amount3_for_bigger_rate_options_now != 'Unassigned' and instrument3_kind == 'option':
                instrument3_position = float(connect.get_position_size(instrument_name=instrument3_name))
            if instrument_amount4_for_bigger_rate_options_now != 'Unassigned' and instrument4_kind == 'option':
                instrument4_position = float(connect.get_position_size(instrument_name=instrument4_name))

            # Para criar a variável para depois informar no list_monitor_log_append após informar 'ORDERS SENT'
            list_monitor_log_append_for_msg_after_orders_sent1 = 'Instrument 1: NO ORDER SENT'
            list_monitor_log_append_for_msg_after_orders_sent2 = 'Instrument 2: NO ORDER SENT'
            list_monitor_log_append_for_msg_after_orders_sent3 = 'Instrument 3: NO ORDER SENT'
            list_monitor_log_append_for_msg_after_orders_sent4 = 'Instrument 4: NO ORDER SENT'

            # Para criar a variável para depois ver o que enviar no list_monitor_log_append
            sent_options_adjusts_instrument1 = False
            sent_options_adjusts_instrument2 = False
            sent_options_adjusts_instrument3 = False
            sent_options_adjusts_instrument4 = False

            # old bigger_rate_options_now
            bigger_rate_options_now_dict = dict()
            bigger_rate_options_now_dict.clear()

            instrument1_rate_options_now = 0
            instrument2_rate_options_now = 0
            instrument3_rate_options_now = 0
            instrument4_rate_options_now = 0

            # instrument 1
            if instrument_amount1_for_bigger_rate_options_now != 'Unassigned' and instrument1_kind == 'option':
                instrument_position = instrument1_position
                x = instrument1_max_position
                # float(x) - float(instrument_position)) é o que falta negociar
                # (float(instrument_amount1) - (float(x) - float(instrument_position))) é o que foi executado/negociado
                instrument1_rate_options_now = abs(
                    (float(instrument_amount1_for_bigger_rate_options_now) - (float(x) - float(
                        instrument_position))) / float(instrument_amount1_for_bigger_rate_options_now))
                bigger_rate_options_now_dict[instrument1_name] = instrument1_rate_options_now
            else:
                pass

            # instrument 2
            if instrument_amount2_for_bigger_rate_options_now != 'Unassigned' and instrument2_kind == 'option':
                instrument_position = instrument2_position
                x = instrument2_max_position
                instrument2_rate_options_now = abs(
                    (float(instrument_amount2_for_bigger_rate_options_now) - (float(x) - float(
                        instrument_position))) / float(instrument_amount2_for_bigger_rate_options_now))
                bigger_rate_options_now_dict[instrument2_name] = instrument2_rate_options_now
            else:
                pass

            # instrument 3
            if instrument_amount3_for_bigger_rate_options_now != 'Unassigned' and instrument3_kind == 'option':
                instrument_position = instrument3_position
                x = instrument3_max_position
                instrument3_rate_options_now = abs(
                    (float(instrument_amount3_for_bigger_rate_options_now) - (float(x) - float(
                        instrument_position))) / float(instrument_amount3_for_bigger_rate_options_now))
                bigger_rate_options_now_dict[instrument3_name] = instrument3_rate_options_now
            else:
                pass

            # instrument 4
            if instrument_amount4_for_bigger_rate_options_now != 'Unassigned' and instrument4_kind == 'option':
                instrument_position = instrument4_position
                x = instrument4_max_position
                instrument4_rate_options_now = abs(
                    (float(instrument_amount4_for_bigger_rate_options_now) - (float(x) - float(
                        instrument_position))) / float(instrument_amount4_for_bigger_rate_options_now))
                bigger_rate_options_now_dict[instrument4_name] = instrument4_rate_options_now
            else:
                pass

            if len(bigger_rate_options_now_dict) == 0:
                bigger_rate_options_now = 0
            else:
                bigger_rate_options_now_dict_min_instrument_name = max(
                    bigger_rate_options_now_dict, key=bigger_rate_options_now_dict.get)  # min instrument name
                bigger_rate_options_now_dict_min = bigger_rate_options_now_dict.get(
                    bigger_rate_options_now_dict_min_instrument_name, 0)  # valor
                if float(bigger_rate_options_now_dict_min) >= 1:
                    bigger_rate_options_now = 1
                elif 0 < float(bigger_rate_options_now_dict_min) < 1:
                    bigger_rate_options_now = float(bigger_rate_options_now_dict_min)
                else:
                    bigger_rate_options_now = 0

            # old def smaller_bid_ask_amount_book
            smaller_bid_ask_amount_book_dict = dict()
            smaller_bid_ask_amount_book_dict.clear()

            y1 = float()  # best bid/ask amount
            y2 = float()
            y3 = float()
            y4 = float()

            xx1 = float  # o que falta negociar
            xx2 = float
            xx3 = float
            xx4 = float

            yy1 = float
            yy2 = float
            yy3 = float
            yy4 = float

            if instrument1_direction == 'buy' and instrument1_kind == 'option':
                instrument_position = float(instrument1_position)
                y1 = connect.best_ask_amount(instrument_name=instrument1_name)
                yy1 = connect.ask_price(instrument_name=instrument1_name)

                x1 = float(instrument1_max_position)
                xx1a = float(x1) - float(instrument_position)
                xx1 = round(xx1a, 1)
                if xx1a == 0:
                    smaller_bid_ask_amount_book_dict[1] = 1
                else:
                    yy = float(y1) / xx1a
                    smaller_bid_ask_amount_book_dict[1] = abs(yy)
            elif instrument1_direction == 'sell' and instrument1_kind == 'option':
                instrument_position = float(instrument1_position)
                y1 = connect.best_bid_amount(instrument_name=instrument1_name)
                yy1 = connect.bid_price(instrument_name=instrument1_name)

                x1 = float(instrument1_max_position)
                xx1a = float(x1) - float(instrument_position)
                xx1 = round(xx1a, 1)
                if xx1a == 0:
                    smaller_bid_ask_amount_book_dict[1] = 1
                else:
                    yy = float(y1) / xx1a
                    smaller_bid_ask_amount_book_dict[1] = abs(yy)
            else:
                pass

            if instrument2_direction == 'buy' and instrument2_kind == 'option':
                instrument_position = float(instrument2_position)
                y2 = connect.best_ask_amount(instrument_name=instrument2_name)
                yy2 = connect.ask_price(instrument_name=instrument2_name)

                x2 = float(instrument2_max_position)
                xx2a = float(x2) - float(instrument_position)
                xx2 = round(xx2a, 1)
                if xx2a == 0:
                    smaller_bid_ask_amount_book_dict[2] = 1
                else:
                    yy = float(y2) / xx2a
                    smaller_bid_ask_amount_book_dict[2] = abs(yy)
            elif instrument2_direction == 'sell' and instrument2_kind == 'option':
                instrument_position = float(instrument2_position)
                y2 = connect.best_bid_amount(instrument_name=instrument2_name)
                yy2 = connect.bid_price(instrument_name=instrument2_name)

                x2 = float(instrument2_max_position)
                xx2a = float(x2) - float(instrument_position)
                xx2 = round(xx2a, 1)
                if xx2a == 0:
                    smaller_bid_ask_amount_book_dict[2] = 1
                else:
                    yy = float(y2) / xx2a
                    smaller_bid_ask_amount_book_dict[2] = abs(yy)
            else:
                pass

            if instrument3_direction == 'buy' and instrument3_kind == 'option':
                instrument_position = float(instrument3_position)
                y3 = connect.best_ask_amount(instrument_name=instrument3_name)
                yy3 = connect.ask_price(instrument_name=instrument3_name)

                x3 = float(instrument3_max_position)
                xx3a = float(x3) - float(instrument_position)
                xx3 = round(xx3a, 1)
                if xx3a == 0:
                    smaller_bid_ask_amount_book_dict[3] = 1
                else:
                    yy = float(y3) / xx3a
                    smaller_bid_ask_amount_book_dict[3] = abs(yy)
            elif instrument3_direction == 'sell' and instrument3_kind == 'option':
                instrument_position = float(instrument3_position)
                y3 = connect.best_bid_amount(instrument_name=instrument3_name)
                yy3 = connect.bid_price(instrument_name=instrument3_name)

                x3 = float(instrument3_max_position)
                xx3a = float(x3) - float(instrument_position)
                xx3 = round(xx3a, 1)
                if xx3a == 0:
                    smaller_bid_ask_amount_book_dict[3] = 1
                else:
                    yy = float(y3) / xx3a
                    smaller_bid_ask_amount_book_dict[3] = abs(yy)
            else:
                pass

            if instrument4_direction == 'buy' and instrument4_kind == 'option':
                instrument_position = float(instrument4_position)
                y4 = connect.best_ask_amount(instrument_name=instrument4_name)
                yy4 = connect.ask_price(instrument_name=instrument4_name)

                x4 = float(instrument4_max_position)
                xx4a = float(x4) - float(instrument_position)
                xx4 = round(xx4a, 1)
                if xx4a == 0:
                    smaller_bid_ask_amount_book_dict[4] = 1
                else:
                    yy = float(y4) / xx4a
                    smaller_bid_ask_amount_book_dict[4] = abs(yy)
            elif instrument4_direction == 'sell' and instrument4_kind == 'option':
                instrument_position = float(instrument4_position)
                y4 = connect.best_bid_amount(instrument_name=instrument4_name)
                yy4 = connect.bid_price(instrument_name=instrument4_name)

                x4 = float(instrument4_max_position)
                xx4a = float(x4) - float(instrument_position)
                xx4 = round(xx4a, 1)
                if xx4a == 0:
                    smaller_bid_ask_amount_book_dict[4] = 1
                else:
                    yy = float(y4) / xx4a
                    smaller_bid_ask_amount_book_dict[4] = abs(yy)
            else:
                pass

            if len(smaller_bid_ask_amount_book_dict) > 0:
                smaller_bid_ask_amount_book_instrument_number = min(
                    smaller_bid_ask_amount_book_dict, key=smaller_bid_ask_amount_book_dict.get)  # instrument number
                smaller_bid_ask_amount_book_ratio = abs(smaller_bid_ask_amount_book_dict.get(
                    smaller_bid_ask_amount_book_instrument_number, 0))  # Valor
            else:
                smaller_bid_ask_amount_book_ratio = 0  # valor

            # ********************************************************************************

            # Se já houver alguma compra de options, conferir se está com relação que deveria
            #   * Primerio: descobrir qual a maior relação atual das opcões já negociadas
            #       * # retorna 0 se nenhuma opção tiver sido negociada ou não tiver options nos instruments
            #           retorna 1 se 100% já tiver sido negociado
            #           caso contrário, retorna a menor relação já negociada
            bigger_rate_option_now = bigger_rate_options_now

            #   * Segundo: descobrir qual a relação já negociada de cada instrument
            #       Já calculado acima como instrument1_rate_options_now, instrument2_rate_options_now,...

            #   * Terceiro: descobrir a menor relação entre o amount do ajuste e o best bid/ask amount
            #       Só calcular se houver alguma negociação, a relação entre bigger_rate_option_now e
            #           instrumentx_rate_options_now diferirem
            smaller_bid_ask_amount_adjust_book_ratio_now_dict = dict()
            smaller_bid_ask_amount_adjust_book_ratio_now_dict.clear()
            #           Instrument 1
            if float(bigger_rate_option_now) != 0 and instrument1_kind == 'option' and \
                    instrument1_amount != 'Unassigned' and abs(float(bigger_rate_option_now)) > abs(
                        float(instrument1_rate_options_now)):
                # xx1 é o que falta negociar
                b = abs(float(xx1)) * abs(abs(float(bigger_rate_option_now)) - abs(float(instrument1_rate_options_now)))
                order_amount_instrument1 = ConditionsCheck().number_multiple_0_1_and_round_1_digits(
                    number=b)
                if order_amount_instrument1 >= 0.1:
                    smaller_bid_ask_amount_adjust_book_ratio_now_dict[1]: abs(float(y1) / float(
                        order_amount_instrument1))
                else:
                    smaller_bid_ask_amount_adjust_book_ratio_now_dict[1]: float(0)
            else:
                pass
            #           Instrument 2
            if float(bigger_rate_option_now) != 0 and instrument2_kind == 'option' and \
                    instrument2_amount != 'Unassigned' and abs(float(bigger_rate_option_now)) > abs(
                        float(instrument2_rate_options_now)):
                # xx2 é o que falta negociar
                b = abs(float(xx2)) * abs(abs(float(bigger_rate_option_now)) - abs(float(instrument2_rate_options_now)))
                order_amount_instrument2 = ConditionsCheck().number_multiple_0_1_and_round_1_digits(
                    number=b)
                if order_amount_instrument2 >= 0.1:
                    smaller_bid_ask_amount_adjust_book_ratio_now_dict[2]: abs(float(y2) / float(
                        order_amount_instrument2))
                else:
                    smaller_bid_ask_amount_adjust_book_ratio_now_dict[2]: float(0)
            else:
                pass
            #           Instrument 3
            if float(bigger_rate_option_now) != 0 and instrument3_kind == 'option' and \
                    instrument3_amount != 'Unassigned' and abs(float(bigger_rate_option_now)) > abs(
                        float(instrument3_rate_options_now)):
                # xx3 é o que falta negociar
                b = abs(float(xx3)) * abs(abs(float(bigger_rate_option_now)) - abs(float(instrument3_rate_options_now)))
                order_amount_instrument3 = ConditionsCheck().number_multiple_0_1_and_round_1_digits(
                    number=b)
                if order_amount_instrument3 >= 0.1:
                    smaller_bid_ask_amount_adjust_book_ratio_now_dict[3]: abs(float(y3) / float(
                        order_amount_instrument3))
                else:
                    smaller_bid_ask_amount_adjust_book_ratio_now_dict[3]: float(0)
            else:
                pass
            #           Instrument 4
            if float(bigger_rate_option_now) != 0 and instrument4_kind == 'option' and \
                    instrument4_amount != 'Unassigned' and abs(float(bigger_rate_option_now)) > abs(
                        float(instrument4_rate_options_now)):
                # xx4 é o que falta negociar
                b = abs(float(xx4)) * abs(abs(float(bigger_rate_option_now)) - abs(float(instrument4_rate_options_now)))
                order_amount_instrument4 = ConditionsCheck().number_multiple_0_1_and_round_1_digits(
                    number=b)
                if order_amount_instrument4 >= 0.1:
                    smaller_bid_ask_amount_adjust_book_ratio_now_dict[4]: abs(float(y4) / float(
                        order_amount_instrument4))
                else:
                    smaller_bid_ask_amount_adjust_book_ratio_now_dict[4]: float(0)
            else:
                pass
            if len(smaller_bid_ask_amount_adjust_book_ratio_now_dict) == 0:
                smaller_bid_ask_amount_adjust_book_ratio_now_dict_min = 0
                pass
            else:
                smaller_bid_ask_amount_adjust_book_ratio_now_dict_min_instrument_number = min(
                    smaller_bid_ask_amount_adjust_book_ratio_now_dict,
                    key=smaller_bid_ask_amount_adjust_book_ratio_now_dict.get)  # Min instrument number
                smaller_bid_ask_amount_adjust_book_ratio_now_dict_min = float(
                    smaller_bid_ask_amount_adjust_book_ratio_now_dict.get(
                        smaller_bid_ask_amount_adjust_book_ratio_now_dict_min_instrument_number, 0))  # Valor

            #   * Quarto: se já houver opção negociada bigger_rate_option_now é != 0

            #       Se já houver negociação feita, conferir e ajustar s.n. cada instrument
            #           Instrument 1
            if float(bigger_rate_option_now) != 0 and instrument1_kind == 'option' and \
                    instrument1_amount != 'Unassigned':
                #           houve negociação, relação igual, send orders igual à primeira negocialção
                if abs(float(instrument1_rate_options_now)) == abs(float(bigger_rate_option_now)):
                    sent_options_adjusts_instrument1 = False
                    #           send orders igual à primeira negocialção
                    pass
                #        se houve alguma negociação, a relação diferir e o amount p/ enviar ordem for >= 0.1, send order
                elif abs(float(instrument1_rate_options_now)) < abs(float(bigger_rate_option_now)):
                    # xx1 é o que falta negociar
                    b = abs(float(xx1)) * abs(abs(float(bigger_rate_option_now)) - abs(float(
                        instrument1_rate_options_now)))
                    if 0 < smaller_bid_ask_amount_adjust_book_ratio_now_dict_min < 1:
                        order_amount_instrument1 = ConditionsCheck().number_multiple_0_1_and_round_1_digits(
                            number=abs(b * abs(float(smaller_bid_ask_amount_adjust_book_ratio_now_dict_min))))
                        if order_amount_instrument1 >= 0.1:
                            instrument1_price = abs(float(yy1))  # market price
                            if instrument1_direction == 'buy':
                                if float(instrument1_position) + abs(float(order_amount_instrument1)) > float(
                                        instrument1_max_position):
                                    order_amount_instrument1 = abs(float(xx1))
                                else:
                                    pass
                                connect.buy_limit(currency=instrument1_name, amount=abs(order_amount_instrument1),
                                                  price=instrument1_price)
                                list_monitor_log_append_for_msg_after_orders_sent1 = str(
                                    (str(instrument1_name) + ': ' + str(instrument1_direction) + ' ' +
                                     str(order_amount_instrument1) + ' at ' + str(instrument1_price)))
                                sent_options_adjusts_instrument1 = True
                            elif instrument1_direction == 'sell':
                                if float(instrument1_position) - abs(float(order_amount_instrument1)) < float(
                                        instrument1_max_position):
                                    order_amount_instrument1 = abs(float(xx1))
                                else:
                                    pass
                                connect.sell_limit(currency=instrument1_name, amount=abs(order_amount_instrument1),
                                                   price=instrument1_price)
                                list_monitor_log_append_for_msg_after_orders_sent1 = str(
                                    (str(instrument1_name) + ': ' + str(instrument1_direction) + ' ' +
                                     str(order_amount_instrument1) + ' at ' + str(instrument1_price)))
                                sent_options_adjusts_instrument1 = True
                            else:
                                sent_options_adjusts_instrument1 = False
                                list_monitor_log.append(
                                    '***** ERROR in option adjusts orders - Error Code:: 3507 *****')
                                connect.logwriter(msg=str(
                                    '***** ERROR in option adjusts orders - Error Code:: 3509 *****'))
                        else:
                            sent_options_adjusts_instrument1 = False
                            pass
                    elif smaller_bid_ask_amount_adjust_book_ratio_now_dict_min >= 1:
                        order_amount_instrument1 = ConditionsCheck().number_multiple_0_1_and_round_1_digits(
                            number=abs(b))
                        if order_amount_instrument1 >= 0.1:
                            instrument1_price = yy1  # market price
                            if instrument1_direction == 'buy':
                                if float(instrument1_position) + abs(float(order_amount_instrument1)) > float(
                                        instrument1_max_position):
                                    order_amount_instrument1 = abs(float(xx1))
                                else:
                                    pass
                                connect.buy_limit(currency=instrument1_name, amount=abs(order_amount_instrument1),
                                                  price=instrument1_price)
                                list_monitor_log_append_for_msg_after_orders_sent1 = str(
                                    (str(instrument1_name) + ': ' + str(instrument1_direction) + ' ' +
                                     str(order_amount_instrument1) + ' at ' + str(instrument1_price)))
                                sent_options_adjusts_instrument1 = True
                            elif instrument1_direction == 'sell':
                                if float(instrument1_position) - abs(float(order_amount_instrument1)) < float(
                                        instrument1_max_position):
                                    order_amount_instrument1 = abs(float(xx1))
                                else:
                                    pass
                                connect.sell_limit(currency=instrument1_name, amount=abs(order_amount_instrument1),
                                                   price=instrument1_price)
                                list_monitor_log_append_for_msg_after_orders_sent1 = str(
                                    (str(instrument1_name) + ': ' + str(instrument1_direction) + ' ' +
                                     str(order_amount_instrument1) + ' at ' + str(instrument1_price)))
                                sent_options_adjusts_instrument1 = True
                            else:
                                sent_options_adjusts_instrument1 = False
                                list_monitor_log.append(
                                    '***** ERROR in option adjusts orders - Error Code:: 3545 *****')
                                connect.logwriter(msg=str(
                                    '***** ERROR in option adjusts orders - Error Code:: 3547 *****'))
                        else:
                            sent_options_adjusts_instrument1 = False
                            pass
                    else:
                        sent_options_adjusts_instrument1 = False
                        pass
                else:
                    sent_options_adjusts_instrument1 = False
                    list_monitor_log.append('***** ERROR in option adjusts orders - Error Code:: 3556 *****')
                    connect.logwriter(msg=str('***** ERROR in option adjusts orders - Error Code:: 3557 *****'))

            #           Instrument 2
            if float(bigger_rate_option_now) != 0 and instrument2_kind == 'option' and \
                    instrument2_amount != 'Unassigned':
                #           houve negociação, relação igual, send orders igual à primeira negocialção
                if abs(float(instrument2_rate_options_now)) == abs(float(bigger_rate_option_now)):
                    sent_options_adjusts_instrument2 = False
                    #        send orders igual à primeira negocialção
                    pass
                #        se houve alguma negociação, a relação diferir e o amount p/ enviar ordem for >= 0.1, send order
                elif abs(float(instrument2_rate_options_now)) < abs(float(bigger_rate_option_now)):
                    # xx2 é o que falta negociar
                    b = abs(float(xx2)) * abs(abs(float(bigger_rate_option_now)) - abs(
                        float(instrument2_rate_options_now)))
                    if 0 < smaller_bid_ask_amount_adjust_book_ratio_now_dict_min < 1:
                        order_amount_instrument2 = ConditionsCheck().number_multiple_0_1_and_round_1_digits(
                            number=abs(b * abs(float(smaller_bid_ask_amount_adjust_book_ratio_now_dict_min))))
                        if order_amount_instrument2 >= 0.1:
                            instrument2_price = abs(float(yy2))  # market price
                            if instrument2_direction == 'buy':
                                if float(instrument2_position) + abs(float(order_amount_instrument2)) > float(
                                        instrument2_max_position):
                                    order_amount_instrument2 = abs(float(xx2))
                                else:
                                    pass
                                connect.buy_limit(currency=instrument2_name, amount=abs(order_amount_instrument2),
                                                  price=instrument2_price)
                                list_monitor_log_append_for_msg_after_orders_sent2 = str(
                                    (str(instrument2_name) + ': ' + str(instrument2_direction) + ' ' +
                                     str(order_amount_instrument2) + ' at ' + str(instrument2_price)))
                                sent_options_adjusts_instrument2 = True
                            elif instrument2_direction == 'sell':
                                if float(instrument2_position) - abs(float(order_amount_instrument2)) < float(
                                        instrument2_max_position):
                                    order_amount_instrument2 = abs(float(xx2))
                                else:
                                    pass
                                connect.sell_limit(currency=instrument2_name, amount=abs(order_amount_instrument2),
                                                   price=instrument2_price)
                                list_monitor_log_append_for_msg_after_orders_sent2 = str(
                                    (str(instrument2_name) + ': ' + str(instrument2_direction) + ' ' +
                                     str(order_amount_instrument2) + ' at ' + str(instrument2_price)))
                                sent_options_adjusts_instrument2 = True
                            else:
                                sent_options_adjusts_instrument2 = False
                                list_monitor_log.append(
                                    '***** ERROR in option adjusts orders - Error Code:: 3604 *****')
                                connect.logwriter(msg=str(
                                    '***** ERROR in option adjusts orders - Error Code:: 3606 *****'))
                        else:
                            sent_options_adjusts_instrument2 = False
                            pass
                    elif smaller_bid_ask_amount_adjust_book_ratio_now_dict_min >= 1:
                        order_amount_instrument2 = ConditionsCheck().number_multiple_0_1_and_round_1_digits(
                            number=abs(b))
                        if order_amount_instrument2 >= 0.1:
                            instrument2_price = yy2  # market price
                            if instrument2_direction == 'buy':
                                if float(instrument2_position) + abs(float(order_amount_instrument2)) > float(
                                        instrument2_max_position):
                                    order_amount_instrument2 = abs(float(xx2))
                                else:
                                    pass
                                connect.buy_limit(currency=instrument2_name, amount=abs(order_amount_instrument2),
                                                  price=instrument2_price)
                                list_monitor_log_append_for_msg_after_orders_sent2 = str(
                                    (str(instrument2_name) + ': ' + str(instrument2_direction) + ' ' +
                                     str(order_amount_instrument2) + ' at ' + str(instrument2_price)))
                                sent_options_adjusts_instrument2 = True
                            elif instrument2_direction == 'sell':
                                if float(instrument2_position) - abs(float(order_amount_instrument2)) < float(
                                        instrument2_max_position):
                                    order_amount_instrument2 = abs(float(xx2))
                                else:
                                    pass
                                connect.sell_limit(currency=instrument2_name, amount=abs(order_amount_instrument2),
                                                   price=instrument2_price)
                                list_monitor_log_append_for_msg_after_orders_sent2 = str(
                                    (str(instrument2_name) + ': ' + str(instrument2_direction) + ' ' +
                                     str(order_amount_instrument2) + ' at ' + str(instrument2_price)))
                                sent_options_adjusts_instrument2 = True
                            else:
                                sent_options_adjusts_instrument2 = False
                                list_monitor_log.append(
                                    '***** ERROR in option adjusts orders - Error Code:: 3642 *****')
                                connect.logwriter(msg=str(
                                    '***** ERROR in option adjusts orders - Error Code:: 3644 *****'))
                        else:
                            sent_options_adjusts_instrument2 = False
                            pass
                    else:
                        sent_options_adjusts_instrument2 = False
                        pass
                else:
                    sent_options_adjusts_instrument2 = False
                    list_monitor_log.append('***** ERROR in option adjusts orders - Error Code:: 3653 *****')
                    connect.logwriter(msg=str('***** ERROR in option adjusts orders - Error Code:: 3654 *****'))

            #           Instrument 3
            if float(bigger_rate_option_now) != 0 and instrument3_kind == 'option' and \
                    instrument3_amount != 'Unassigned':
                #           houve negociação, relação igual, send orders igual à primeira negocialção
                if abs(float(instrument3_rate_options_now)) == abs(float(bigger_rate_option_now)):
                    sent_options_adjusts_instrument3 = False
                    #         send orders igual à primeira negocialção
                    pass
                #        se houve alguma negociação, a relação diferir e o amount p/ enviar ordem for >= 0.1, send order
                elif abs(float(instrument3_rate_options_now)) < abs(float(bigger_rate_option_now)):
                    # xx3 é o que falta negociar
                    b = abs(float(xx3)) * abs(abs(float(bigger_rate_option_now)) - abs(
                        float(instrument3_rate_options_now)))
                    if 0 < smaller_bid_ask_amount_adjust_book_ratio_now_dict_min < 1:
                        order_amount_instrument3 = ConditionsCheck().number_multiple_0_1_and_round_1_digits(
                            number=abs(b * abs(float(smaller_bid_ask_amount_adjust_book_ratio_now_dict_min))))
                        if order_amount_instrument3 >= 0.1:
                            instrument3_price = abs(float(yy3))  # market price
                            if instrument3_direction == 'buy':
                                if float(instrument3_position) + abs(float(order_amount_instrument3)) > float(
                                        instrument3_max_position):
                                    order_amount_instrument3 = abs(float(xx3))
                                else:
                                    pass
                                connect.buy_limit(currency=instrument3_name, amount=abs(order_amount_instrument3),
                                                  price=instrument3_price)
                                list_monitor_log_append_for_msg_after_orders_sent3 = str(
                                    (str(instrument3_name) + ': ' + str(instrument3_direction) + ' ' +
                                     str(order_amount_instrument3) + ' at ' + str(instrument3_price)))
                                sent_options_adjusts_instrument3 = True
                            elif instrument3_direction == 'sell':
                                if float(instrument3_position) - abs(float(order_amount_instrument3)) < float(
                                        instrument3_max_position):
                                    order_amount_instrument3 = abs(float(xx3))
                                else:
                                    pass
                                connect.sell_limit(currency=instrument3_name, amount=abs(order_amount_instrument3),
                                                   price=instrument3_price)
                                list_monitor_log_append_for_msg_after_orders_sent3 = str(
                                    (str(instrument3_name) + ': ' + str(instrument3_direction) + ' ' +
                                     str(order_amount_instrument3) + ' at ' + str(instrument3_price)))
                                sent_options_adjusts_instrument3 = True
                            else:
                                sent_options_adjusts_instrument3 = False
                                list_monitor_log.append(
                                    '***** ERROR in option adjusts orders - Error Code:: 3701 *****')
                                connect.logwriter(msg=str(
                                    '***** ERROR in option adjusts orders - Error Code:: 3703 *****'))
                        else:
                            sent_options_adjusts_instrument3 = False
                            pass
                    elif smaller_bid_ask_amount_adjust_book_ratio_now_dict_min >= 1:
                        order_amount_instrument3 = ConditionsCheck().number_multiple_0_1_and_round_1_digits(
                            number=abs(b))
                        if order_amount_instrument3 >= 0.1:
                            instrument3_price = yy3  # market price
                            if instrument3_direction == 'buy':
                                if float(instrument3_position) + abs(float(order_amount_instrument3)) > float(
                                        instrument3_max_position):
                                    order_amount_instrument3 = abs(float(xx3))
                                else:
                                    pass
                                connect.buy_limit(currency=instrument3_name, amount=abs(order_amount_instrument3),
                                                  price=instrument3_price)
                                list_monitor_log_append_for_msg_after_orders_sent3 = str(
                                    (str(instrument3_name) + ': ' + str(instrument3_direction) + ' ' +
                                     str(order_amount_instrument3) + ' at ' + str(instrument3_price)))
                                sent_options_adjusts_instrument3 = True
                            elif instrument3_direction == 'sell':
                                if float(instrument3_position) - abs(float(order_amount_instrument3)) < float(
                                        instrument3_max_position):
                                    order_amount_instrument3 = abs(float(xx3))
                                else:
                                    pass
                                connect.sell_limit(currency=instrument3_name, amount=abs(order_amount_instrument3),
                                                   price=instrument3_price)
                                list_monitor_log_append_for_msg_after_orders_sent3 = str(
                                    (str(instrument3_name) + ': ' + str(instrument3_direction) + ' ' +
                                     str(order_amount_instrument3) + ' at ' + str(instrument3_price)))
                                sent_options_adjusts_instrument3 = True
                            else:
                                sent_options_adjusts_instrument3 = False
                                list_monitor_log.append(
                                    '***** ERROR in option adjusts orders - Error Code:: 3739 *****')
                                connect.logwriter(msg=str(
                                    '***** ERROR in option adjusts orders - Error Code:: 3741 *****'))
                        else:
                            sent_options_adjusts_instrument3 = False
                            pass
                    else:
                        sent_options_adjusts_instrument3 = False
                        pass
                else:
                    sent_options_adjusts_instrument3 = False
                    list_monitor_log.append('***** ERROR in option adjusts orders - Error Code:: 3750 *****')
                    connect.logwriter(msg=str('***** ERROR in option adjusts orders - Error Code:: 3751 *****'))

            #           Instrument 4
            if float(bigger_rate_option_now) != 0 and instrument4_kind == 'option' and \
                    instrument4_amount != 'Unassigned':
                #           houve negociação, relação igual, send orders igual à primeira negocialção
                if abs(float(instrument4_rate_options_now)) == abs(float(bigger_rate_option_now)):
                    sent_options_adjusts_instrument4 = False
                    #       send orders igual à primeira negocialção
                    pass
                #       se houve alguma negociação, a relação diferir e o amount p/ enviar ordem for >= 0.1, send order
                elif abs(float(instrument4_rate_options_now)) < abs(float(bigger_rate_option_now)):
                    # xx4 é o que falta negociar
                    b = abs(float(xx4)) * abs(abs(float(bigger_rate_option_now)) - abs(
                        float(instrument4_rate_options_now)))
                    if 0 < smaller_bid_ask_amount_adjust_book_ratio_now_dict_min < 1:
                        order_amount_instrument4 = ConditionsCheck().number_multiple_0_1_and_round_1_digits(
                            number=abs(b * abs(float(smaller_bid_ask_amount_adjust_book_ratio_now_dict_min))))
                        if order_amount_instrument4 >= 0.1:
                            instrument4_price = abs(float(yy4))  # market price
                            if instrument4_direction == 'buy':
                                if float(instrument4_position) + abs(float(order_amount_instrument4)) > float(
                                        instrument4_max_position):
                                    order_amount_instrument4 = abs(float(xx4))
                                else:
                                    pass
                                connect.buy_limit(currency=instrument4_name, amount=abs(order_amount_instrument4),
                                                  price=instrument4_price)
                                list_monitor_log_append_for_msg_after_orders_sent4 = str(
                                    (str(instrument4_name) + ': ' + str(instrument4_direction) + ' ' +
                                     str(order_amount_instrument4) + ' at ' + str(instrument4_price)))
                                sent_options_adjusts_instrument4 = True
                            elif instrument4_direction == 'sell':
                                if float(instrument4_position) - abs(float(order_amount_instrument4)) < float(
                                        instrument4_max_position):
                                    order_amount_instrument4 = abs(float(xx4))
                                else:
                                    pass
                                connect.sell_limit(currency=instrument4_name, amount=abs(order_amount_instrument4),
                                                   price=instrument4_price)
                                list_monitor_log_append_for_msg_after_orders_sent4 = str(
                                    (str(instrument4_name) + ': ' + str(instrument4_direction) + ' ' +
                                     str(order_amount_instrument4) + ' at ' + str(instrument4_price)))
                                sent_options_adjusts_instrument4 = True
                            else:
                                sent_options_adjusts_instrument4 = False
                                list_monitor_log.append(
                                    '***** ERROR in option adjusts orders - Error Code:: 3798 *****')
                                connect.logwriter(msg=str(
                                    '***** ERROR in option adjusts orders - Error Code:: 3800 *****'))
                        else:
                            sent_options_adjusts_instrument4 = False
                            pass
                    elif smaller_bid_ask_amount_adjust_book_ratio_now_dict_min >= 1:
                        order_amount_instrument4 = ConditionsCheck().number_multiple_0_1_and_round_1_digits(
                            number=abs(b))
                        if order_amount_instrument4 >= 0.1:
                            instrument4_price = yy4  # market price
                            if instrument4_direction == 'buy':
                                if float(instrument4_position) + abs(float(order_amount_instrument4)) > float(
                                        instrument4_max_position):
                                    order_amount_instrument4 = abs(float(xx4))
                                else:
                                    pass
                                connect.buy_limit(currency=instrument4_name, amount=abs(order_amount_instrument4),
                                                  price=instrument4_price)
                                list_monitor_log_append_for_msg_after_orders_sent4 = str(
                                    (str(instrument4_name) + ': ' + str(instrument4_direction) + ' ' +
                                     str(order_amount_instrument4) + ' at ' + str(instrument4_price)))
                                sent_options_adjusts_instrument4 = True
                            elif instrument4_direction == 'sell':
                                if float(instrument4_position) - abs(float(order_amount_instrument4)) < float(
                                        instrument4_max_position):
                                    order_amount_instrument4 = abs(float(xx4))
                                else:
                                    pass
                                connect.sell_limit(currency=instrument4_name, amount=abs(order_amount_instrument4),
                                                   price=instrument4_price)
                                list_monitor_log_append_for_msg_after_orders_sent4 = str(
                                    (str(instrument4_name) + ': ' + str(instrument4_direction) + ' ' +
                                     str(order_amount_instrument4) + ' at ' + str(instrument4_price)))
                                sent_options_adjusts_instrument4 = True
                            else:
                                sent_options_adjusts_instrument4 = False
                                list_monitor_log.append(
                                    '***** ERROR in option adjusts orders - Error Code:: 3836 *****')
                                connect.logwriter(msg=str(
                                    '***** ERROR in option adjusts orders - Error Code:: 3838 *****'))
                        else:
                            sent_options_adjusts_instrument4 = False
                            pass
                    else:
                        sent_options_adjusts_instrument4 = False
                        pass
                else:
                    sent_options_adjusts_instrument4 = False
                    list_monitor_log.append('***** ERROR in option adjusts orders - Error Code:: 3847 *****')
                    connect.logwriter(msg=str('***** ERROR in option adjusts orders - Error Code:: 3848 *****'))

            # se não houver negociação de ajuste feita, ordem igual à primeira ordem
            if float(bigger_rate_option_now) == 0 or (
                    sent_options_adjusts_instrument1 is False and sent_options_adjusts_instrument2 is False and
                    sent_options_adjusts_instrument3 is False and sent_options_adjusts_instrument4 is False):
                list_monitor_log.append('*** NO SENT ORDERS ADJUSTMENTS ***')
                # colar aqui a primeira ordem de negociação
                # *************************************************************************************************************
                # ABAIXO PRIMEIRAS ORDENS ENVIADAS SE ACIMA NÃO HOUVER AJUSTES
                # Para criar a variável para depois informar no list_monitor_log_append após informar 'ORDERS SENT'
                list_monitor_log_append_for_msg_after_orders_sent1 = 'Instrument 1: NO ORDER SENT'
                list_monitor_log_append_for_msg_after_orders_sent2 = 'Instrument 2: NO ORDER SENT'
                list_monitor_log_append_for_msg_after_orders_sent3 = 'Instrument 3: NO ORDER SENT'
                list_monitor_log_append_for_msg_after_orders_sent4 = 'Instrument 4: NO ORDER SENT'

                # instrument1:
                if instrument1_amount != 'Unassigned' and instrument1_kind == 'option' and \
                        position_option_smaller_max_position_instrument1 == 'instrument_run_trade_ok':

                    instrument1_price = yy1  # market price
                    # xx1 é o que falta comprar
                    if 0 < smaller_bid_ask_amount_book_ratio < 1:
                        b = xx1 * smaller_bid_ask_amount_book_ratio
                        order_amount_instrument1 = ConditionsCheck().number_multiple_0_1_and_round_1_digits(
                            number=b)
                        if instrument1_direction == 'buy':
                            if float(instrument1_position) + abs(float(order_amount_instrument1)) > float(
                                    instrument1_max_position):
                                order_amount_instrument1 = abs(float(xx1))
                            else:
                                pass
                            connect.buy_limit(currency=instrument1_name, amount=abs(order_amount_instrument1),
                                              price=instrument1_price)
                            list_monitor_log_append_for_msg_after_orders_sent1 = str(
                                (str(instrument1_name) + ': ' + str(instrument1_direction) + ' ' + str(
                                    order_amount_instrument1) + ' at ' + str(instrument1_price)))
                        elif instrument1_direction == 'sell':
                            if float(instrument1_position) - abs(float(order_amount_instrument1)) < float(
                                    instrument1_max_position):
                                order_amount_instrument1 = abs(float(xx1))
                            else:
                                pass
                            connect.sell_limit(currency=instrument1_name, amount=abs(order_amount_instrument1),
                                               price=instrument1_price)
                            list_monitor_log_append_for_msg_after_orders_sent1 = str(
                                (str(instrument1_name) + ': ' + str(instrument1_direction) + ' ' + str(
                                    order_amount_instrument1) + ' at ' + str(instrument1_price)))
                        else:
                            pass
                    elif smaller_bid_ask_amount_book_ratio >= 1:
                        a = abs(xx1)
                        order_amount_instrument1 = ConditionsCheck().number_multiple_0_1_and_round_1_digits(number=a)
                        if instrument1_direction == 'buy':
                            connect.buy_limit(currency=instrument1_name, amount=abs(order_amount_instrument1),
                                              price=instrument1_price)
                            list_monitor_log_append_for_msg_after_orders_sent1 = str(
                                (str(instrument1_name) + ': ' + str(instrument1_direction) + ' ' + str(
                                    order_amount_instrument1) + ' at ' + str(instrument1_price)))
                        elif instrument1_direction == 'sell':
                            connect.sell_limit(currency=instrument1_name, amount=abs(order_amount_instrument1),
                                               price=instrument1_price)
                            list_monitor_log_append_for_msg_after_orders_sent1 = str(
                                (str(instrument1_name) + ': ' + str(instrument1_direction) + ' ' + str(
                                    order_amount_instrument1) + ' at ' + str(instrument1_price)))
                        else:
                            pass
                    else:
                        pass
                else:
                    pass

                # instrument2:
                if instrument2_amount != 'Unassigned' and instrument2_kind == 'option' and \
                        position_option_smaller_max_position_instrument2 == 'instrument_run_trade_ok':

                    instrument2_price = yy2
                    if 0 < smaller_bid_ask_amount_book_ratio < 1:
                        b = xx2 * smaller_bid_ask_amount_book_ratio
                        order_amount_instrument2 = ConditionsCheck().number_multiple_0_1_and_round_1_digits(
                            number=b)
                        if instrument2_direction == 'buy':
                            if float(instrument2_position) + abs(float(order_amount_instrument2)) > float(
                                    instrument2_max_position):
                                order_amount_instrument2 = abs(float(xx2))
                            else:
                                pass
                            connect.buy_limit(currency=instrument2_name, amount=abs(order_amount_instrument2),
                                              price=instrument2_price)
                            list_monitor_log_append_for_msg_after_orders_sent2 = str(
                                (str(instrument2_name) + ': ' + str(instrument2_direction) + ' ' + str(
                                    order_amount_instrument2) + ' at ' + str(instrument2_price)))
                        elif instrument2_direction == 'sell':
                            if float(instrument2_position) - abs(float(order_amount_instrument2)) < float(
                                    instrument2_max_position):
                                order_amount_instrument2 = abs(float(xx2))
                            else:
                                pass
                            connect.sell_limit(currency=instrument2_name, amount=abs(order_amount_instrument2),
                                               price=instrument2_price)
                            list_monitor_log_append_for_msg_after_orders_sent2 = str(
                                (str(instrument2_name) + ': ' + str(instrument2_direction) + ' ' + str(
                                    order_amount_instrument2) + ' at ' + str(instrument2_price)))
                        else:
                            pass
                    elif smaller_bid_ask_amount_book_ratio >= 1:
                        a = abs(xx2)
                        order_amount_instrument2 = ConditionsCheck().number_multiple_0_1_and_round_1_digits(number=a)
                        if instrument2_direction == 'buy':
                            connect.buy_limit(currency=instrument2_name, amount=abs(order_amount_instrument2),
                                              price=instrument2_price)
                            list_monitor_log_append_for_msg_after_orders_sent2 = str(
                                (str(instrument2_name) + ': ' + str(instrument2_direction) + ' ' + str(
                                    order_amount_instrument2) + ' at ' + str(instrument2_price)))
                        elif instrument2_direction == 'sell':
                            connect.sell_limit(currency=instrument2_name, amount=abs(order_amount_instrument2),
                                               price=instrument2_price)
                            list_monitor_log_append_for_msg_after_orders_sent2 = str(
                                (str(instrument2_name) + ': ' + str(instrument2_direction) + ' ' + str(
                                    order_amount_instrument2) + ' at ' + str(instrument2_price)))
                        else:
                            pass
                    else:
                        pass
                else:
                    pass

                # instrument3:
                if instrument3_amount != 'Unassigned' and instrument3_kind == 'option' and \
                        position_option_smaller_max_position_instrument3 == 'instrument_run_trade_ok':

                    instrument3_price = yy3  # market price

                    if 0 < smaller_bid_ask_amount_book_ratio < 1:
                        b = xx3 * smaller_bid_ask_amount_book_ratio
                        order_amount_instrument3 = ConditionsCheck().number_multiple_0_1_and_round_1_digits(
                            number=b)
                        if instrument3_direction == 'buy':
                            if float(instrument3_position) + abs(float(order_amount_instrument3)) > float(
                                    instrument3_max_position):
                                order_amount_instrument3 = abs(float(xx3))
                            else:
                                pass
                            connect.buy_limit(currency=instrument3_name, amount=abs(order_amount_instrument3),
                                              price=instrument3_price)
                            list_monitor_log_append_for_msg_after_orders_sent3 = str(
                                (str(instrument3_name) + ': ' + str(instrument3_direction) + ' ' + str(
                                    order_amount_instrument3) + ' at ' + str(instrument3_price)))
                        elif instrument3_direction == 'sell':
                            if float(instrument3_position) - abs(float(order_amount_instrument3)) < float(
                                    instrument3_max_position):
                                order_amount_instrument3 = abs(float(xx3))
                            else:
                                pass
                            connect.sell_limit(currency=instrument3_name, amount=abs(order_amount_instrument3),
                                               price=instrument3_price)
                            list_monitor_log_append_for_msg_after_orders_sent3 = str(
                                (str(instrument3_name) + ': ' + str(instrument3_direction) + ' ' + str(
                                    order_amount_instrument3) + ' at ' + str(instrument3_price)))
                        else:
                            pass
                    elif smaller_bid_ask_amount_book_ratio >= 1:
                        a = abs(xx3)
                        order_amount_instrument3 = ConditionsCheck().number_multiple_0_1_and_round_1_digits(number=a)
                        if instrument3_direction == 'buy':
                            connect.buy_limit(currency=instrument3_name, amount=abs(order_amount_instrument3),
                                              price=instrument3_price)
                            list_monitor_log_append_for_msg_after_orders_sent3 = str(
                                (str(instrument3_name) + ': ' + str(instrument3_direction) + ' ' + str(
                                    order_amount_instrument3) + ' at ' + str(instrument3_price)))
                        elif instrument3_direction == 'sell':
                            connect.sell_limit(currency=instrument3_name, amount=abs(order_amount_instrument3),
                                               price=instrument3_price)
                            list_monitor_log_append_for_msg_after_orders_sent3 = str(
                                (str(instrument3_name) + ': ' + str(instrument3_direction) + ' ' + str(
                                    order_amount_instrument3) + ' at ' + str(instrument3_price)))
                        else:
                            pass
                    else:
                        pass
                else:
                    pass

                # instrument4:
                if instrument4_amount != 'Unassigned' and instrument4_kind == 'option' and \
                        position_option_smaller_max_position_instrument4 == 'instrument_run_trade_ok':

                    instrument4_price = yy4  # market price

                    if 0 < smaller_bid_ask_amount_book_ratio < 1:
                        b = xx4 * smaller_bid_ask_amount_book_ratio
                        order_amount_instrument4 = ConditionsCheck().number_multiple_0_1_and_round_1_digits(
                            number=b)
                        if instrument4_direction == 'buy':
                            if float(instrument4_position) + abs(float(order_amount_instrument4)) > float(
                                    instrument4_max_position):
                                order_amount_instrument4 = abs(float(xx4))
                            else:
                                pass
                            connect.buy_limit(currency=instrument4_name, amount=abs(order_amount_instrument4),
                                              price=instrument4_price)
                            list_monitor_log_append_for_msg_after_orders_sent4 = str(
                                (str(instrument4_name) + ': ' + str(instrument4_direction) + ' ' + str(
                                    order_amount_instrument4) + ' at ' + str(instrument4_price)))
                        elif instrument4_direction == 'sell':
                            if float(instrument4_position) - abs(float(order_amount_instrument4)) < float(
                                    instrument4_max_position):
                                order_amount_instrument4 = abs(float(xx4))
                            else:
                                pass
                            connect.sell_limit(currency=instrument4_name, amount=abs(order_amount_instrument4),
                                               price=instrument4_price)
                            list_monitor_log_append_for_msg_after_orders_sent4 = str(
                                (str(instrument4_name) + ': ' + str(instrument4_direction) + ' ' + str(
                                    order_amount_instrument4) + ' at ' + str(instrument4_price)))
                        else:
                            pass
                    elif smaller_bid_ask_amount_book_ratio >= 1:
                        a = abs(xx4)
                        order_amount_instrument4 = ConditionsCheck().number_multiple_0_1_and_round_1_digits(number=a)
                        if instrument4_direction == 'buy':
                            connect.buy_limit(currency=instrument4_name, amount=abs(order_amount_instrument4),
                                              price=instrument4_price)
                            list_monitor_log_append_for_msg_after_orders_sent4 = str(
                                (str(instrument4_name) + ': ' + str(instrument4_direction) + ' ' + str(
                                    order_amount_instrument4) + ' at ' + str(instrument4_price)))
                        elif instrument4_direction == 'sell':
                            connect.sell_limit(currency=instrument4_name, amount=abs(order_amount_instrument4),
                                               price=instrument4_price)
                            list_monitor_log_append_for_msg_after_orders_sent4 = str(
                                (str(instrument4_name) + ': ' + str(instrument4_direction) + ' ' + str(
                                    order_amount_instrument4) + ' at ' + str(instrument4_price)))
                        else:
                            pass
                    else:
                        pass
                else:
                    pass

                list_monitor_log.append('********** SENT ORDERS **********')
                connect.logwriter('********** SENT ORDERS **********')
                # Para informar quais ordens foram enviadas
                list_monitor_log.append(str(list_monitor_log_append_for_msg_after_orders_sent1))
                list_monitor_log.append(str(list_monitor_log_append_for_msg_after_orders_sent2))
                list_monitor_log.append(str(list_monitor_log_append_for_msg_after_orders_sent3))
                list_monitor_log.append(str(list_monitor_log_append_for_msg_after_orders_sent4))

                time.sleep(10)
                connect.cancel_all()
            # *************************************************************************************************************
            # se houver negociação de ajuste, chamar uma funçao para recalcular as variáveis com dados de mercado
            elif float(bigger_rate_option_now) != 0 and (
                    sent_options_adjusts_instrument1 is True or sent_options_adjusts_instrument2 is True or
                    sent_options_adjusts_instrument3 is True or sent_options_adjusts_instrument4 is True):
                list_monitor_log.append('*** SENT ORDERS ADJUSTMENTS ***')
                connect.logwriter(msg=str('*** SENT ORDERS ADJUSTMENTS ***'))

                # Para informar quais ordens foram enviadas
                list_monitor_log.append(str(list_monitor_log_append_for_msg_after_orders_sent1))
                list_monitor_log.append(str(list_monitor_log_append_for_msg_after_orders_sent2))
                list_monitor_log.append(str(list_monitor_log_append_for_msg_after_orders_sent3))
                list_monitor_log.append(str(list_monitor_log_append_for_msg_after_orders_sent4))

                time.sleep(10)
                connect.cancel_all()
                ConditionsCheck().send_options_orders_like_first_time()
                pass  # chamar uma funçao para recalcular as variáveis com dados do mercado
            else:
                list_monitor_log.append('***** ERROR in option adjusts orders - Error Code:: 4125 *****')
                connect.logwriter(msg=str('***** ERROR in option adjusts orders - Error Code:: 4126 *****'))
                pass

        except Exception as er:
            list_monitor_log.append('ERROR in send_options_orders(). Error Code 4130 ' + str(er))
            connect.logwriter('ERROR in send_options_orders(). Error Code 4131 ' + str(er))
        finally:
            pass

    def position_future_smaller_max_position_instrument(self, instrument_number=None):
        self.instrument_number = instrument_number
        from connection_spread import connect
        from lists import list_monitor_log

        try:
            instrument_max_position = Config().max_position_from_position_saved_and_instrument_amount(
                instrument_number=instrument_number)
            instrument_kind = InstrumentsSaved().instrument_kind_saved(instrument_number=instrument_number)

            if instrument_max_position != 'Unassigned' and instrument_kind == 'future':
                instrument_name = InstrumentsSaved().instrument_name_construction_from_file(
                    instrument_number=instrument_number)
                instrument_direction = InstrumentsSaved().instrument_direction_construction_from_instrument_file(
                    instrument_number=instrument_number)

                a9 = float(connect.get_position_size(instrument_name=instrument_name))
                b9 = float(instrument_max_position)
                d9 = instrument_direction
                if a9 < b9 and round(b9 - a9, 0) >= 10 and d9 == 'buy':
                    return 'instrument_run_trade_ok'
                elif a9 == b9 or round(b9 - a9, 0) < 10 and d9 == 'buy':
                    return 'instrument_run_trade_no'
                elif a9 > b9 and d9 == 'buy':
                    connect.logwriter(
                        '****************** ERROR: Instrument ' + str(instrument_number) +
                        ' position > max position Error Code:: 4162 ******************')
                    list_monitor_log.append(
                        '****************** ERROR: Instrument ' + str(instrument_number) +
                        ' position > max position Error Code:: 4165 ******************')
                    return 'instrument_run_trade_no'
                elif a9 > b9 and abs(round(b9 - a9, 0)) >= 10 and d9 == 'sell':
                    return 'instrument_run_trade_ok'
                elif a9 == b9 or abs(round(b9 - a9, 0)) < 10 and d9 == 'sell':
                    return 'instrument_run_trade_no'
                elif a9 < b9 and d9 == 'sell':
                    connect.logwriter(
                        '****************** ERROR: Instrument ' + str(instrument_number) +
                        ' position > max position Error Code:: 4174 ******************')
                    list_monitor_log.append(
                        '****************** ERROR: Instrument ' + str(instrument_number) +
                        ' position > max position Error Code:: 4177 ******************')
                    return 'instrument_run_trade_no'
                else:
                    pass
            elif instrument_max_position == 'Unassigned' or instrument_kind == 'option':
                return 'instrument_run_trade_no'
            else:
                connect.logwriter('****************** ERROR: Instrument  position vavabot_spread.py Error Code:: '
                                  '4185 ******************')
                list_monitor_log.append('****************** ERROR: Instrument  position vavabot_spread.py Error Code:: '
                                        '4187 ******************')
                return 'instrument_run_trade_no'
        except Exception as er:
            connect.logwriter(str(er) + ' Error Code:: 4190')
            list_monitor_log.append(str(er) + ' Error Code:: 4191')
            pass
        finally:
            pass

    @staticmethod
    def targets_achieved_future():
        return 'targets_future_ok'

    # noinspection PyMethodMayBeStatic
    def number_multiple_10_and_round_0_digits(self, number=None):
        a3 = round(number - (number % 10), 0)
        return a3

    @staticmethod
    def rate_options_now():
        from connection_spread import connect
        instrument_kind1 = InstrumentsSaved().instrument_kind_saved(instrument_number=1)
        instrument_kind2 = InstrumentsSaved().instrument_kind_saved(instrument_number=2)
        instrument_kind3 = InstrumentsSaved().instrument_kind_saved(instrument_number=3)
        instrument_kind4 = InstrumentsSaved().instrument_kind_saved(instrument_number=4)

        instrument_direction1 = InstrumentsSaved().instrument_direction_construction_from_instrument_file(
            instrument_number=1)
        instrument_direction2 = InstrumentsSaved().instrument_direction_construction_from_instrument_file(
            instrument_number=2)
        instrument_direction3 = InstrumentsSaved().instrument_direction_construction_from_instrument_file(
            instrument_number=3)
        instrument_direction4 = InstrumentsSaved().instrument_direction_construction_from_instrument_file(
            instrument_number=4)
        instrument_amount1 = InstrumentsSaved().instrument_amount_saved(instrument_number=1)
        instrument_amount2 = InstrumentsSaved().instrument_amount_saved(instrument_number=2)
        instrument_amount3 = InstrumentsSaved().instrument_amount_saved(instrument_number=3)
        instrument_amount4 = InstrumentsSaved().instrument_amount_saved(instrument_number=4)

        if instrument_direction1 == 'sell' and instrument_kind1 == 'option' and instrument_amount1 != 0:
            instrument_amount1 = float(instrument_amount1) * -1
        else:
            pass
        if instrument_direction2 == 'sell' and instrument_kind2 == 'option' and instrument_amount2 != 0:
            instrument_amount2 = float(instrument_amount2) * -1
        else:
            pass
        if instrument_direction3 == 'sell' and instrument_kind3 == 'option' and instrument_amount3 != 0:
            instrument_amount3 = float(instrument_amount3) * -1
        else:
            pass
        if instrument_direction4 == 'sell' and instrument_kind4 == 'option' and instrument_amount4 != 0:
            instrument_amount4 = float(instrument_amount4) * -1
        else:
            pass

        rate_options_now_dict = dict()
        rate_options_now_dict.clear()
        # instrument 1
        if instrument_amount1 != 'Unassigned' and instrument_kind1 == 'option':
            instrument_name = InstrumentsSaved().instrument_name_construction_from_file(
                instrument_number=1)
            instrument_position = float(connect.get_position_size(instrument_name=instrument_name))
            x = Config().max_position_from_position_saved_and_instrument_amount(
                instrument_number=1)
            # float(x) - float(instrument_position)) é o que falta negociar
            # (float(instrument_amount1) - (float(x) - float(instrument_position))) é o que foi executado/negociado
            rate_options_now_dict[instrument_name] = abs(
                (float(instrument_amount1) - (float(x) - float(instrument_position))) / float(instrument_amount1))
        else:
            pass

        # instrument 2
        if instrument_amount2 != 'Unassigned' and instrument_kind2 == 'option':
            instrument_name = InstrumentsSaved().instrument_name_construction_from_file(
                instrument_number=2)
            instrument_position = float(connect.get_position_size(instrument_name=instrument_name))
            x = Config().max_position_from_position_saved_and_instrument_amount(
                instrument_number=2)
            rate_options_now_dict[instrument_name] = abs(
                (float(instrument_amount2) - (float(x) - float(instrument_position))) / float(instrument_amount2))
        else:
            pass

        # instrument 3
        if instrument_amount3 != 'Unassigned' and instrument_kind3 == 'option':
            instrument_name = InstrumentsSaved().instrument_name_construction_from_file(
                instrument_number=3)
            instrument_position = float(connect.get_position_size(instrument_name=instrument_name))
            x = Config().max_position_from_position_saved_and_instrument_amount(
                instrument_number=3)
            rate_options_now_dict[instrument_name] = abs(
                (float(instrument_amount3) - (float(x) - float(instrument_position))) / float(instrument_amount3))
        else:
            pass

        # instrument 4
        if instrument_amount4 != 'Unassigned' and instrument_kind4 == 'option':
            instrument_name = InstrumentsSaved().instrument_name_construction_from_file(
                instrument_number=4)
            instrument_position = float(connect.get_position_size(instrument_name=instrument_name))
            x = Config().max_position_from_position_saved_and_instrument_amount(
                instrument_number=4)
            rate_options_now_dict[instrument_name] = abs(
                (float(instrument_amount4) - (float(x) - float(instrument_position))) / float(instrument_amount4))
        else:
            pass

        if len(rate_options_now_dict) == 0:
            return 0
        else:
            rate_options_now_dict_min_instrument_name = min(
                rate_options_now_dict, key=rate_options_now_dict.get)  # min instrument name
            rate_options_now_dict_min = rate_options_now_dict.get(rate_options_now_dict_min_instrument_name, 0)  # valor
            if float(rate_options_now_dict_min) >= 1:
                return 1
            elif 0 < float(rate_options_now_dict_min) < 1:
                return float(rate_options_now_dict_min)
            else:
                return 0

    def send_future_orders(self, instrument_number=None):
        self.instrument_number = instrument_number
        from connection_spread import connect, led_color
        from lists import list_monitor_log
        global send_future_orders_while

        send_future_orders_while = True
        while send_future_orders_while is True:
            from connection_spread import connect
            from lists import list_monitor_log

            try:
                if led_color() == 'red':
                    time.sleep(3)
                    pass

                else:
                    connect.cancel_all()
                    time.sleep(0.3)
                    instrument_amount = InstrumentsSaved().instrument_amount_saved(instrument_number=instrument_number)
                    instrument_kind = InstrumentsSaved().instrument_kind_saved(instrument_number=instrument_number)
                    position_future_smaller_max_position_instrument = \
                        ConditionsCheck().position_future_smaller_max_position_instrument(
                            instrument_number=instrument_number)
                    if instrument_amount != 'Unassigned' and instrument_kind == 'future' and \
                            position_future_smaller_max_position_instrument == 'instrument_run_trade_ok':
                        instrument_direction = \
                            InstrumentsSaved().instrument_direction_construction_from_instrument_file(
                                instrument_number=instrument_number)
                        instrument_name = InstrumentsSaved().instrument_name_construction_from_file(
                            instrument_number=instrument_number)
                        instrument_max_position = Config().max_position_from_position_saved_and_instrument_amount(
                            instrument_number=instrument_number)
                        instrument_position = float(connect.get_position_size(instrument_name=instrument_name))
                        if instrument_direction == 'buy':
                            y = connect.ask_price(instrument_name=instrument_name)
                            instrument_price = float(y)
                            x = float(instrument_max_position)
                            xx = float(ConditionsCheck().number_multiple_10_and_round_0_digits(
                                number=(x - instrument_position)))
                            rate_option_now_for_here = float(ConditionsCheck().rate_options_now())
                            if 0 < rate_option_now_for_here < 1:
                                rate_future_for_trade = rate_option_now_for_here
                                rate_future_now = abs((float(
                                    instrument_amount) - (float(x) - float(instrument_position))) / float(
                                    instrument_amount))
                                if rate_future_now >= rate_future_for_trade:
                                    send_future_orders_while = False
                                    break
                                    pass
                                elif rate_future_now < rate_future_for_trade:
                                    order_amount_instrument = float(
                                        ConditionsCheck().number_multiple_10_and_round_0_digits(
                                            number=abs(abs(xx) * (abs(rate_future_for_trade) - abs(
                                                rate_future_now)))))
                                    if order_amount_instrument >= 10:
                                        connect.buy_limit(currency=instrument_name, amount=abs(
                                            order_amount_instrument), price=instrument_price)
                                        list_monitor_log.append('Send ' + str(
                                            instrument_name) + ' Order Buy, at price: ' + str(
                                            instrument_price) + '. Amount: ' + str(order_amount_instrument))
                                        time.sleep(7)
                                        connect.cancel_all()
                                        time.sleep(3)
                                    else:
                                        send_future_orders_while = False
                                        break
                                        pass
                                else:
                                    send_future_orders_while = False
                                    break
                                    pass
                            elif rate_option_now_for_here >= 1:
                                order_amount_instrument = abs(xx)
                                if order_amount_instrument >= 10:
                                    connect.buy_limit(currency=instrument_name, amount=abs(
                                        order_amount_instrument), price=instrument_price)
                                    list_monitor_log.append('Send ' + str(
                                        instrument_name) + ' Order Buy, at price: ' + str(
                                        instrument_price) + '. Amount: ' + str(order_amount_instrument))
                                    time.sleep(7)
                                    connect.cancel_all()
                                    time.sleep(3)
                                else:
                                    send_future_orders_while = False
                                    break
                                    pass
                            else:
                                if InstrumentsSaved().instrument_kind_saved(instrument_number=1) != 'option' and \
                                        InstrumentsSaved().instrument_kind_saved(instrument_number=2) != 'option' and \
                                        InstrumentsSaved().instrument_kind_saved(instrument_number=3) != 'option' and \
                                        InstrumentsSaved().instrument_kind_saved(instrument_number=4) != 'option':
                                    order_amount_instrument = abs(xx)
                                    if order_amount_instrument >= 10:
                                        connect.buy_limit(currency=instrument_name, amount=abs(
                                            order_amount_instrument), price=instrument_price)
                                        list_monitor_log.append('Send ' + str(
                                            instrument_name) + ' Order Buy, at price: ' + str(
                                            instrument_price) + '. Amount: ' + str(order_amount_instrument))
                                        time.sleep(7)
                                        connect.cancel_all()
                                        time.sleep(3)
                                    else:
                                        send_future_orders_while = False
                                        break
                                        pass
                                else:
                                    send_future_orders_while = False
                                    break
                                    pass
                        elif instrument_direction == 'sell':
                            instrument_amount = float(instrument_amount) * 1
                            y = connect.bid_price(instrument_name=instrument_name)
                            instrument_price = abs(float(y))
                            x = float(instrument_max_position)
                            xx = abs(float(ConditionsCheck().number_multiple_10_and_round_0_digits(
                                number=(x - instrument_position))))
                            rate_option_now_for_here = abs(float(ConditionsCheck().rate_options_now()))
                            if 0 < rate_option_now_for_here < 1:
                                rate_future_for_trade = rate_option_now_for_here
                                rate_future_now = abs((float(
                                    instrument_amount) - (float(x) - float(instrument_position))) / float(
                                    instrument_amount))
                                if rate_future_now >= rate_future_for_trade:
                                    send_future_orders_while = False
                                    break
                                    pass
                                elif rate_future_now < rate_future_for_trade:
                                    order_amount_instrument = float(
                                        ConditionsCheck().number_multiple_10_and_round_0_digits(
                                            number=abs(abs(xx) * (abs(rate_future_for_trade) - abs(
                                                rate_future_now)))))
                                    if order_amount_instrument >= 10:
                                        connect.sell_limit(currency=instrument_name, amount=abs(
                                            order_amount_instrument), price=instrument_price)
                                        list_monitor_log.append('Send ' + str(
                                            instrument_name) + ' Order Sell, at price: ' + str(
                                            instrument_price) + '. Amount: ' + str(order_amount_instrument))
                                        time.sleep(7)
                                        connect.cancel_all()
                                        time.sleep(3)
                                    else:
                                        send_future_orders_while = False
                                        break
                                        pass
                                else:
                                    send_future_orders_while = False
                                    break
                                    pass
                            elif rate_option_now_for_here >= 1:
                                order_amount_instrument = abs(xx)
                                if order_amount_instrument >= 10:
                                    connect.sell_limit(currency=instrument_name, amount=abs(
                                        order_amount_instrument), price=instrument_price)
                                    list_monitor_log.append('Send ' + str(
                                        instrument_name) + ' Order Sell, at price: ' + str(
                                        instrument_price) + '. Amount: ' + str(order_amount_instrument))
                                    time.sleep(7)
                                    connect.cancel_all()
                                    time.sleep(3)
                                else:
                                    send_future_orders_while = False
                                    break
                                    pass
                            else:
                                if InstrumentsSaved().instrument_kind_saved(instrument_number=1) != 'option' and \
                                        InstrumentsSaved().instrument_kind_saved(instrument_number=2) != 'option' and \
                                        InstrumentsSaved().instrument_kind_saved(instrument_number=3) != 'option' and \
                                        InstrumentsSaved().instrument_kind_saved(instrument_number=4) != 'option':
                                    order_amount_instrument = abs(xx)
                                    if order_amount_instrument >= 10:
                                        connect.sell_limit(currency=instrument_name, amount=abs(
                                            order_amount_instrument), price=instrument_price)
                                        list_monitor_log.append('Send ' + str(
                                            instrument_name) + ' Order Sell, at price: ' + str(
                                            instrument_price) + '. Amount: ' + str(order_amount_instrument))
                                        time.sleep(7)
                                        connect.cancel_all()
                                        time.sleep(3)
                                    else:
                                        send_future_orders_while = False
                                        break
                                        pass
                                else:
                                    send_future_orders_while = False
                                    break
                                    pass

                        else:
                            connect.logwriter('********** ERROR in def send_future_orders in vavabot_spread.py '
                                              'Error Code:: 4493 **********')
                            list_monitor_log.append('********** ERROR in def send_future_orders in vavabot_spread.py '
                                                    'Error Code:: 4495 **********')
                            time.sleep(3)
                            pass
                    else:
                        break
            except Exception as er:
                connect.logwriter(str(er) + ' Error Code:: 4501')
                list_monitor_log.append(str(er) + ' Error Code:: 4502')
                time.sleep(10)
                pass
            finally:
                pass
        time.sleep(7)
        connect.cancel_all()
        time.sleep(3)
        list_monitor_log.append('There are NOT Future Orders to Send')
        connect.logwriter('There are NOT Future Orders to Send')

    @staticmethod
    def targets_achieved():
        from lists import list_monitor_log
        from connection_spread import led_color
        import time
        global run_target_on_off
        global trading_on_off_for_msg

        # Args Fixes
        instrument_name_currency_exchange_rate = ConfigSaved().currency_exchange_rate_for_upper_and_lower()
        exchange_rate_lower_then = float(ConfigSaved().exchange_rate_lower_then())
        exchange_rate_upper_then = float(ConfigSaved().exchange_rate_upper_then())

        try:
            from connection_spread import connect
            if led_color() == 'red':
                list_monitor_log.append('********** Connection Offline - '
                                        'Waiting connection online for check '
                                        'if Conditions are Filled **********')
                time.sleep(3)
                pass
            else:
                if run_target_on_off == 'on':
                    list_monitor_log.append('*** Checking if Targets are filled ***')

                    # Args modify
                    currency_exchange_rate_mark_price = float(connect.get_book_summary_by_instrument(
                        instrument_name=instrument_name_currency_exchange_rate)[0]['mark_price'])

                    # Targets check
                    if float(currency_exchange_rate_mark_price) < float(exchange_rate_lower_then):
                        list_monitor_log.append('*** Mark Price < ' + str(
                            exchange_rate_lower_then) + 'USD - ''LOWER then Condition Filled ***')
                        if float(currency_exchange_rate_mark_price) > float(exchange_rate_upper_then):
                            list_monitor_log.append('*** Mark Price > ' + str(
                                exchange_rate_upper_then) + 'USD - '' UPPER then Condition Filled ***')
                            structure_market_cost_trigger_check = ConditionsCheck().structure_market_cost_trigger()
                            if structure_market_cost_trigger_check is True:  # Opcional a configuração
                                value_give_in_achieved_check = ConditionsCheck().value_give_in_achieved()
                                if value_give_in_achieved_check is True:
                                    run_target_on_off = 'off'
                                    list_monitor_log.append('*** ALL CONDITIONS FILLED ***')
                                elif value_give_in_achieved_check is False:
                                    run_target_on_off = 'on'
                                else:
                                    connect.logwriter(
                                        '********** ERROR -  Strategy cost unassigned Error Code:: 4561 **********')
                                    list_monitor_log.append(
                                        '********** ERROR -  Strategy cost unassigned Error Code:: 4563 **********')
                                    pass
                            elif structure_market_cost_trigger_check is False:  # Opcional a configuração
                                run_target_on_off = 'on'
                            else:
                                run_target_on_off = 'on'
                                connect.logwriter(
                                    '********** ERROR - structure_market_cost_trigger Error Code:: 4571 - **********')
                                list_monitor_log.append(
                                    '********** ERROR - structure_market_cost_trigger Error Code:: 4573 - **********')
                                time.sleep(5)
                                pass
                        else:
                            run_target_on_off = 'on'
                            list_monitor_log.append('Waiting Mark Price  > ' +
                                                    str(exchange_rate_upper_then) +
                                                    ' - UPPER then Condition')
                    else:
                        run_target_on_off = 'on'
                        list_monitor_log.append('Waiting Mark Price < ' +
                                                str(exchange_rate_lower_then) +
                                                ' - LOWER then Condition')
                        pass
                elif trading_on_off_for_msg == 'off':
                    run_target_on_off = 'off'
                    pass
                else:
                    list_monitor_log.append('****** ERROR targets_achieved Error Code:: 4593 *****')
                    connect.logwriter(msg='****** ERROR targets_achieved Error Code:: 4594 *****')
                    pass
        except Exception as er:
            from connection_spread import connect
            connect.logwriter(str(er) + ' Error Code:: 4598')
            list_monitor_log.append(str(er) + ' Error Code:: 4599')
        finally:
            pass

        if trading_on_off_for_msg == 'off':
            return 'trading_on_off_off'
        elif run_target_on_off == 'on':
            return 'targets_no'
        elif run_target_on_off == 'off':
            return 'targets_ok'
        else:
            from connection_spread import connect
            connect.logwriter('*********** Error Error Code:: 4611 - targets_achieved ************')
            list_monitor_log.append('*********** Error Error Code:: 4612 - targets_achieved ************')
            return 'targets_ok'

    @staticmethod
    def structure_cost_for_tab_run_trading_and_btc_index_and_greeks_when_started_trading():
        import time
        from connection_spread import led_color
        from lists import list_monitor_log

        if led_color() == 'red':
            list_monitor_log.append('********** Connection Offline - Waiting for BTC index and Strategy Cost')
            time.sleep(3)
            pass
        else:
            try:
                from connection_spread import connect
                sinal.structure_cost_for_tab_run_trading_and_btc_index_and_greeks_when_started_trading_signal_1.emit()

                a = connect.index_price('btc_usd')
                b = str(a['index_price'])
                sinal.structure_cost_for_tab_run_trading_and_btc_index_and_greeks_when_started_trading_signal_2.emit(
                    str(b))

                c = Quote().structure_mark_greek_cost()
                sinal.structure_mark_greek_cost_signal.emit(c)

                f13 = str(InstrumentsSaved().instrument_amount_saved(instrument_number=1))
                f13_k = str(InstrumentsSaved().instrument_kind_saved(instrument_number=1))
                f14 = str(InstrumentsSaved().instrument_amount_saved(instrument_number=2))
                f14_k = str(InstrumentsSaved().instrument_kind_saved(instrument_number=2))
                f15 = str(InstrumentsSaved().instrument_amount_saved(instrument_number=3))
                f15_k = str(InstrumentsSaved().instrument_kind_saved(instrument_number=3))
                f16 = str(InstrumentsSaved().instrument_amount_saved(instrument_number=4))
                f16_k = str(InstrumentsSaved().instrument_kind_saved(instrument_number=4))

                instrument_name_currency_exchange_rate = ConfigSaved().currency_exchange_rate_for_upper_and_lower()

                if Quote().bid_ask_offer() == 'waiting bid/ask offer':
                    f = float(
                        connect.get_last_trades_by_instrument_price(
                            instrument_name=instrument_name_currency_exchange_rate))
                    a = round(float(Quote().structure_option_mark_price_cost()), 5)
                    a_usd = round(float(a) * f, 2)
                    a1 = 'None - NO OPTION OPTION BID/ASK OFFER'
                    a1_a = 'None - NO BID/ASK OFFER'
                    g = ''
                    h = ''

                elif (f13 == 'Unassigned' or f13_k == 'future') and \
                        (f14 == 'Unassigned' or f14_k == 'future') and \
                        (f15 == 'Unassigned' or f15_k == 'future') and \
                        (f16 == 'Unassigned' or f16_k == 'future'):
                    a = 'All instruments Unassigned or NO option assigned'
                    a_usd = ''
                    a1 = a
                    g = ''
                    a1_a = a
                    h = ''
                else:
                    f = float(
                        connect.get_last_trades_by_instrument_price(
                            instrument_name=instrument_name_currency_exchange_rate))

                    a = round(float(Quote().structure_option_mark_price_cost()), 5)
                    a_usd = round(float(a) * f, 2)

                    a1 = round(float(Quote().structure_option_market_cost()), 5)
                    a1_usd = round(float(a1) * f, 2)
                    if float(a) == 0:
                        a1_a = 'Strategy MARK Price = 0'
                        h = ''
                    else:
                        a1_a = round(abs(float(a1) / float(a)) * 100, 2)
                        h = '% of the Strategy MARK Price'
                    g = ' (' + str(a1_usd) + 'USD)'

                quote_dict = dict()
                quote_dict.clear()
                quote_dict['text59'] = str('Strategy MARK Price: ' + str(a) + ' (' + str(a_usd) + 'USD)')
                quote_dict['text61'] = str('Strategy MARKET Price: ' + str(a1) + g)
                quote_dict['text60'] = str('Strategy MARKET Price price: ' + str(a1_a) + h)

                sinal.structure_cost_for_tab_run_trading_and_btc_index_and_greeks_when_started_trading_signal_0.emit(
                    quote_dict)

            except Exception as er:
                from connection_spread import connect
                connect.logwriter(str(er) + ' Error Code:: 4698')
                list_monitor_log.append(str(er) + ' Error Code:: 4699')
                list_monitor_log.append('********* ERROR - Strategy cost for tab run trade when started run trading'
                                        ' Error Code:: 4701 **********')
                pass
            finally:
                pass


# noinspection PyShadowingNames
def credentials(ui):
    def message_box_reboot():
        import sys
        from lists import password_dict
        global password_dict

        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText('If you update\nAPI key and secret key\nyou will need restart bot')
        msg.setWindowTitle('*** WARNING ***')
        msg.addButton('Ok', msg.AcceptRole)
        msg.addButton('Cancel', msg.RejectRole)
        pass
        if msg.exec_() == msg.Rejected:
            password_dict['pwd'] = str(ui.lineEdit_password.text())
            api_key_save()  # ok clicked
            time.sleep(1)
            sys.exit()
        else:
            pass  # cancel clicked

    def message_box_reboot1():
        if str(ui.lineEdit_password.text()) == '':
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText('You need to create a password\nto recover API credentials')
            msg.setWindowTitle('INFO')
            msg.exec_()
            pass
        else:
            if CredentialsSaved.testnet_saved_true_or_false() == '':
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('You need\nSet Test or Real Account')
                msg.setWindowTitle('INFO')
                msg.exec_()
                pass
            else:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Test or Real Account\nIs Correct?')
                msg.setWindowTitle('*** WARNING ***')
                msg.addButton('Yes', msg.AcceptRole)
                msg.addButton('No', msg.RejectRole)
                pass
                if msg.exec_() == msg.Rejected:
                    message_box_reboot()  # ok clicked
                else:
                    pass  # cancel clicked

    def message_box_reboot2():
        import sys
        if CredentialsSaved.testnet_saved_true_or_false() is True:
            pass
        else:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText('Dou you want\nUpdate Account? ')
            msg.setWindowTitle('*** WARNING ***')
            msg.addButton('Yes', msg.AcceptRole)
            msg.addButton('No', msg.RejectRole)
            pass
            if msg.exec_() == msg.Rejected:
                testnet_true_save()  # ok clicked

                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Dou you want\nUpdate APIs? ')
                msg.setWindowTitle('*** WARNING ***')
                msg.addButton('Yes', msg.AcceptRole)
                msg.addButton('No', msg.RejectRole)
                pass
                if msg.exec_() == msg.Rejected:
                    message_box_reboot()  # ok clicked
                else:
                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Information)
                    msg.setText('You need\nRestart bot')
                    msg.setWindowTitle('INFO')
                    msg.exec_()
                    pass  # cancel clicked
                    sys.exit()
            else:
                if CredentialsSaved.testnet_saved_true_or_false() is True:
                    ui.radioButton_testnet_true.setChecked(True)
                    ui.radioButton_2_testnet_false.setChecked(False)
                elif CredentialsSaved.testnet_saved_true_or_false() is False:
                    ui.radioButton_testnet_true.setChecked(False)
                    ui.radioButton_2_testnet_false.setChecked(True)
                else:
                    ui.radioButton_testnet_true.setChecked(False)
                    ui.radioButton_2_testnet_false.setChecked(False)
                    pass  # cancel clicked

    def message_box_reboot3():
        import sys
        if CredentialsSaved.testnet_saved_true_or_false() is False:
            pass
        else:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText('Dou you want\nUpdate Account? ')
            msg.setWindowTitle('*** WARNING ***')
            msg.addButton('Yes', msg.AcceptRole)
            msg.addButton('No', msg.RejectRole)
            pass
            if msg.exec_() == msg.Rejected:
                testnet_false_save()  # ok clicked

                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Dou you want\nUpdate APIs? ')
                msg.setWindowTitle('*** WARNING ***')
                msg.addButton('Yes', msg.AcceptRole)
                msg.addButton('No', msg.RejectRole)
                pass
                if msg.exec_() == msg.Rejected:
                    message_box_reboot()  # ok clicked
                else:
                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Information)
                    msg.setText('You need\nRestart bot')
                    msg.setWindowTitle('INFO')
                    msg.exec_()
                    pass  # cancel clicked
                    sys.exit()
            else:
                if CredentialsSaved.testnet_saved_true_or_false() is True:
                    ui.radioButton_testnet_true.setChecked(True)
                    ui.radioButton_2_testnet_false.setChecked(False)
                elif CredentialsSaved.testnet_saved_true_or_false() is False:
                    ui.radioButton_testnet_true.setChecked(False)
                    ui.radioButton_2_testnet_false.setChecked(True)
                else:
                    ui.radioButton_testnet_true.setChecked(False)
                    ui.radioButton_2_testnet_false.setChecked(False)
                    pass  # cancel clicked

    def api_key_saved_print():
        text = str(CredentialsSaved.api_secret_saved())

        if text == '<Type your Deribit Key>':
            ui.lineEdit_api_key_saved.setText(text)
        else:
            text1 = text[:3]
            list_text1 = list(text1)
            if len(text) >= 4:
                text2 = text[3:]
                list_text2 = list(text2)
                for i in list_text2:
                    list_text2[list_text2.index(i)] = '*'
                list_text1.extend(list_text2)
                text3 = "".join(list_text1)
                ui.lineEdit_api_key_saved.setText(text3)
            else:
                for i in list_text1:
                    list_text1[list_text1.index(i)] = '*'
                text3 = "".join(list_text1)
                ui.lineEdit_api_key_saved.setText(text3)

    def secret_key_saved_print():
        text = str(CredentialsSaved.secret_key_saved())

        if text == '<Type your Deribit Secret Key>':
            ui.lineEdit_api_secret_saved.setText(text)
        else:
            text1 = text[:3]
            list_text1 = list(text1)
            if len(text) >= 4:
                text2 = text[3:]
                list_text2 = list(text2)
                for i in list_text2:
                    list_text2[list_text2.index(i)] = '*'
                list_text1.extend(list_text2)
                text3 = "".join(list_text1)
                ui.lineEdit_api_secret_saved.setText(text3)
            else:
                for i in list_text1:
                    list_text1[list_text1.index(i)] = '*'
                text3 = "".join(list_text1)
                ui.lineEdit_api_secret_saved.setText(text3)

    def testnet_true_or_false_saved_print():
        testnet_true_or_false_saved_print_file = CredentialsSaved.testnet_saved_true_or_false()
        if testnet_true_or_false_saved_print_file is True:
            ui.lineEdit_testenet_true_or_false_satatus.setText('Test Account')
            ui.radioButton_testnet_true.setChecked(True)
            ui.radioButton_2_testnet_false.setChecked(False)
        elif testnet_true_or_false_saved_print_file is False:
            ui.lineEdit_testenet_true_or_false_satatus.setText('Real Account')
            ui.radioButton_testnet_true.setChecked(False)
            ui.radioButton_2_testnet_false.setChecked(True)
        else:
            ui.lineEdit_testenet_true_or_false_satatus.setText('SET Account')
            ui.radioButton_testnet_true.setChecked(False)
            ui.radioButton_2_testnet_false.setChecked(False)
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText('You need\nSet Test or Real Account')
            msg.setWindowTitle('*** Warning ***')
            msg.exec_()
            pass

    def api_key_save():
        import base64
        from cryptography.fernet import Fernet
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        from lists import password_dict
        global password_dict

        password3 = str(password_dict['pwd'])

        salt = b'\x90"\x90J\r\xa6\x08\xb6_\xbdfEd\x1cDE'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=390000,
        )

        key = base64.urlsafe_b64encode(kdf.derive(str(password3).encode('utf-8')))
        f = Fernet(key)
        original = str(ui.lineEdit_api_key_new.text()).encode('utf-8')
        token = f.encrypt(original)

        with open('api-key_spread.txt', 'wb') as encrypted_file:
            encrypted_file.write(token)

        secret_key_save()
        api_key_saved_print()

    def secret_key_save():
        import base64
        from cryptography.fernet import Fernet
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        from lists import password_dict
        global password_dict

        password4 = str(password_dict['pwd'])

        salt = b'\x90"\x90J\r\xa6\x08\xb6_\xbdfEd\x1cDE'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=390000,
        )

        key = base64.urlsafe_b64encode(kdf.derive(str(password4).encode('utf-8')))
        f = Fernet(key)
        original = str(ui.lineEdit_api_secret_new.text()).encode('utf-8')
        token = f.encrypt(original)

        with open('secret-key_spread.txt', 'wb') as encrypted_file:
            encrypted_file.write(token)

        secret_key_saved_print()

    def testnet_true_save():
        setup = ConfigParser(
            allow_no_value=True,
            inline_comment_prefixes='#',
            strict=False
        )
        setup.read('setup.ini')
        credentials_setup = setup['credentials']

        credentials_setup['test_net'] = 'True'

        with open('setup.ini', 'w') as configfile:
            setup.write(configfile)
        testnet_true_or_false_saved_print()

    def testnet_false_save():
        setup = ConfigParser(
            allow_no_value=True,
            inline_comment_prefixes='#',
            strict=False
        )
        setup.read('setup.ini')
        credentials_setup = setup['credentials']

        credentials_setup['test_net'] = 'False'

        with open('setup.ini', 'w') as configfile:
            setup.write(configfile)
        testnet_true_or_false_saved_print()

    def need_password_counter_smaller_three():
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText('You need to create a password\nto recover API credentials')
        msg.setWindowTitle('WARNING')
        msg.exec_()
        pass
        time.sleep(0.5)

    def invalid_password():
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText('Invalid Password')
        msg.setWindowTitle('INFO')
        msg.exec_()
        pass
        time.sleep(0.5)

    def invalid_password_counter_bigger_three():
        import os
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText('Credentials will be reset\nAnd APP will be close')
        msg.setWindowTitle('INFO')
        msg.exec_()
        pass
        os.unlink('api-key_spread.txt')
        os.unlink('secret-key_spread.txt')
        time.sleep(1)
        sys.exit()

    def message_connection_only_public():
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText('Only public methods\nwill be executed')
        msg.setWindowTitle('INFO')
        msg.exec_()
        pass

    def message_box_password_input():
        from connection_spread import connection1
        import os
        from lists import password_dict
        global password_dict

        if os.path.isfile('secret-key_spread.txt') is True:
            with open('secret-key_spread.txt', 'r') as file1:
                sks = file1.read()
        else:
            sks = '<Type your Deribit Secret Key>'

        if os.path.isfile('api-key_spread.txt') is True:
            with open('api-key_spread.txt', 'r') as file2:
                a_s_saved = file2.read()
        else:
            a_s_saved = '<Type your Deribit Key>'

        if '<Type your Deribit Key>' in str(a_s_saved) or '<Type your Deribit Secret Key>' in str(sks):
            connection1()
            api_key_saved_print()
            secret_key_saved_print()
            testnet_true_or_false_saved_print()
        else:
            password_input = 'User'
            invalid_password_counter = 0
            need_password_counter = 0

            while password_input == 'User':
                le = QLineEdit()
                le.setText('Password')

                text, ok = QInputDialog().getText(le, "WARNING",
                                                  "Password to recovey API Credentials:", le.Password)
                # QDir().home().dirName())
                if ok is False:
                    password_input = str(password_dict['pwd'])
                    message_connection_only_public()
                    connection1()
                    api_key_saved_print()
                    secret_key_saved_print()
                    testnet_true_or_false_saved_print()
                if ok:
                    le.setText(str(text))
                    if str(text) == '':
                        if need_password_counter <= 3:
                            need_password_counter = need_password_counter + 1
                            need_password_counter_smaller_three()
                        else:
                            invalid_password_counter_bigger_three()
                    else:
                        import base64
                        from cryptography.fernet import Fernet, InvalidToken, InvalidSignature
                        from cryptography.hazmat.primitives import hashes
                        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

                        password_dict['pwd'] = str(text)

                        salt = b'\x90"\x90J\r\xa6\x08\xb6_\xbdfEd\x1cDE'
                        kdf = PBKDF2HMAC(
                            algorithm=hashes.SHA256(),
                            length=32,
                            salt=salt,
                            iterations=390000,
                        )

                        key = base64.urlsafe_b64encode(kdf.derive(str(password_dict['pwd']).encode('utf-8')))
                        f = Fernet(key)

                        with open('api-key_spread.txt', 'rb') as enc_file:
                            encrypted1 = enc_file.read()
                        with open('secret-key_spread.txt', 'rb') as enc_file:
                            encrypted2 = enc_file.read()

                        if invalid_password_counter <= 3:
                            try:
                                f.decrypt(encrypted1).decode('utf-8')
                                f.decrypt(encrypted2).decode('utf-8')
                            except InvalidToken or InvalidSignature:
                                invalid_password_counter = invalid_password_counter + 1
                                invalid_password()
                            else:
                                password_input = str(password_dict['pwd'])
                                connection1()
                                api_key_saved_print()
                                secret_key_saved_print()
                                testnet_true_or_false_saved_print()
                            finally:
                                pass
                        else:
                            invalid_password_counter_bigger_three()

    def message_box_wait_when_open_app():
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText('WAIT while Syntax Instruments will be checked')
        msg.setWindowTitle('*** INFO ***')
        msg.exec_()
        pass

    message_box_password_input()
    ui.pushButton_submit_new_credintals.clicked.connect(message_box_reboot1)
    ui.radioButton_testnet_true.clicked.connect(message_box_reboot2)
    ui.radioButton_2_testnet_false.clicked.connect(message_box_reboot3)
    message_box_wait_when_open_app()


# noinspection PyShadowingNames
def instruments(ui):
    def instrument_expiration_construction_from_instrument_file(instrument_number=None):
        file_open = 'instruments_spread.txt'
        instrument_number_adjusted_to_list = int(instrument_number) - 1

        # open file instruments

        with open(file_open, 'r') as file_instruments:
            lines_file_instruments = file_instruments.readlines()  # file instruments_spread.txt ==> lines
            # Instrument
            list_line_instrument = lines_file_instruments[instrument_number_adjusted_to_list].split(
                '-')  # line ==> list
            if 'Unassigned' in list_line_instrument[0]:
                return False
            elif 'option' in list_line_instrument[0]:
                return list_line_instrument[1]
            elif 'future' in list_line_instrument[0]:
                if 'PERPETUAL' in list_line_instrument[1]:
                    return True
                else:
                    return list_line_instrument[1]
            else:
                connect.logwriter(str(
                    '*** Instrument ' + str(instrument_number) + ' Expiration ERROR - Error Code:: 4881 ***'))
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Instrument ' + str(instrument_number) + ' Expiration ERROR Error - Code:: 4884')
                msg.setWindowTitle('***** ERROR *****')
                msg.exec_()

    def _payoff(kind, quantidade, cotacao, strike, premio):
        from connection_spread import connect
        from lists import list_monitor_log

        try:
            if kind == 'call':
                if cotacao > strike:
                    payoff = quantidade * ((cotacao - strike) - premio)
                else:
                    payoff = quantidade * (0 - premio)
            elif kind == 'put':
                if cotacao < strike:
                    payoff = quantidade * ((strike - cotacao) - premio)
                else:
                    payoff = quantidade * (0 - premio)
            elif kind == 'future':
                payoff = quantidade / strike * (cotacao - strike)
                return round(payoff, 8)
            else:
                payoff = 'error'

            if payoff == 'error':
                return 'error'
            else:
                return round(payoff, 2)

        except Exception as er:
            list_monitor_log.append('*** ERROR in _payoff() Error Code: 4920 ***' + str(er))
            connect.logwriter(msg='*** ERROR in _payoff() Error Code: 4921 ***' + str(er))
        finally:
            pass

    def plot_payoff_for_4_instruments():
        import matplotlib.pyplot as plt
        from connection_spread import connect
        from lists import list_monitor_log
        try:
            instrument1_kind = InstrumentsSaved().instrument_kind_saved(instrument_number=1)
            instrument2_kind = InstrumentsSaved().instrument_kind_saved(instrument_number=2)
            instrument3_kind = InstrumentsSaved().instrument_kind_saved(instrument_number=3)
            instrument4_kind = InstrumentsSaved().instrument_kind_saved(instrument_number=4)

            instrument1_amount = InstrumentsSaved().instrument_amount_saved(instrument_number=1)
            instrument2_amount = InstrumentsSaved().instrument_amount_saved(instrument_number=2)
            instrument3_amount = InstrumentsSaved().instrument_amount_saved(instrument_number=3)
            instrument4_amount = InstrumentsSaved().instrument_amount_saved(instrument_number=4)

            instrument1_direction = InstrumentsSaved().instrument_direction_construction_from_instrument_file(
                instrument_number=1)
            instrument2_direction = InstrumentsSaved().instrument_direction_construction_from_instrument_file(
                instrument_number=2)
            instrument3_direction = InstrumentsSaved().instrument_direction_construction_from_instrument_file(
                instrument_number=3)
            instrument4_direction = InstrumentsSaved().instrument_direction_construction_from_instrument_file(
                instrument_number=4)

            instrument1_name = InstrumentsSaved().instrument_name_construction_from_file(instrument_number=1)
            instrument2_name = InstrumentsSaved().instrument_name_construction_from_file(instrument_number=2)
            instrument3_name = InstrumentsSaved().instrument_name_construction_from_file(instrument_number=3)
            instrument4_name = InstrumentsSaved().instrument_name_construction_from_file(instrument_number=4)
            # instrument KIND
            # instrument 1
            if instrument1_kind == 'option':
                if '-P' in instrument1_name:
                    instrument1_kind = 'put'
                elif '-C' in instrument1_name:
                    instrument1_kind = 'call'
                else:
                    instrument1_kind = 'error'
            elif instrument1_kind == 'future':
                instrument1_kind = 'future'
            elif instrument1_kind == 'Unassigned':
                instrument1_kind = 'Unassigned'
            else:
                instrument1_kind = 'error'

            # instrument 2
            if instrument2_kind == 'option':
                if '-P' in instrument2_name:
                    instrument2_kind = 'put'
                elif '-C' in instrument2_name:
                    instrument2_kind = 'call'
                else:
                    instrument2_kind = 'error'
            elif instrument2_kind == 'future':
                instrument2_kind = 'future'
            elif instrument2_kind == 'Unassigned':
                instrument2_kind = 'Unassigned'
            else:
                instrument2_kind = 'error'

            # instrument 3
            if instrument3_kind == 'option':
                if '-P' in instrument3_name:
                    instrument3_kind = 'put'
                elif '-C' in instrument3_name:
                    instrument3_kind = 'call'
                else:
                    instrument3_kind = 'error'
            elif instrument3_kind == 'future':
                instrument3_kind = 'future'
            elif instrument3_kind == 'Unassigned':
                instrument3_kind = 'Unassigned'
            else:
                instrument3_kind = 'error'

            # instrument 4
            if instrument4_kind == 'option':
                if '-P' in instrument4_name:
                    instrument4_kind = 'put'
                elif '-C' in instrument4_name:
                    instrument4_kind = 'call'
                else:
                    instrument4_kind = 'error'
            elif instrument4_kind == 'future':
                instrument4_kind = 'future'
            elif instrument4_kind == 'Unassigned':
                instrument4_kind = 'Unassigned'
            else:
                instrument4_kind = 'error'

            # Instrument AMOUNT
            # Instrument 1
            if instrument1_amount != 'Unassigned' and instrument1_direction == 'sell':
                instrument1_amount = float(instrument1_amount) * -1
            else:
                pass

            # Instrument 2
            if instrument2_amount != 'Unassigned' and instrument2_direction == 'sell':
                instrument2_amount = float(instrument2_amount) * -1
            else:
                pass

            # Instrument 3
            if instrument3_amount != 'Unassigned' and instrument3_direction == 'sell':
                instrument3_amount = float(instrument3_amount) * -1
            else:
                pass

            # Instrument 4
            if instrument4_amount != 'Unassigned' and instrument4_direction == 'sell':
                instrument4_amount = float(instrument4_amount) * -1
            else:
                pass

            # Instrument PREMIO
            bid_ask_offer = Quote().bid_ask_offer()

            currency_exchange_rate_for_premio_for_plot_payoff = \
                ConfigSaved().currency_exchange_rate_for_upper_and_lower()
            if 'BTC' in currency_exchange_rate_for_premio_for_plot_payoff:
                index_name = 'btc_usd'
            elif 'ETH' in currency_exchange_rate_for_premio_for_plot_payoff:
                index_name = 'eth_usd'
            elif 'SOL' in currency_exchange_rate_for_premio_for_plot_payoff:
                index_name = 'sol_usd'
            elif 'USDC' in currency_exchange_rate_for_premio_for_plot_payoff:
                index_name = 'btc_usd'
            else:
                index_name = 'BTC'
                connect.logwriter(str('***** ERROR in plot_payoff_for_4_instruments ' + str(
                    index_name) + ' Error Code:: 5055 *****'))
                list_monitor_log.append(str('***** ERROR in plot_payoff_for_4_instruments ' + str(
                    index_name) + ' Error Code:: 5057 *****'))
                time.sleep(3)
            index_price_a = connect.index_price(currency=str(index_name))
            index_price = float(index_price_a['index_price'])

            # Instrument 1
            if instrument1_kind == 'Unassigned':
                instrument1_premio = 'Unassigned'
            elif instrument1_kind == 'future':
                instrument1_premio = 0
            elif instrument1_kind == 'call' or instrument1_kind == 'put':
                if bid_ask_offer != 'waiting bid/ask offer':
                    instrument1_premio = round(
                        abs(Quote().instrument_market_cost(instrument_number=1) / float(
                            instrument1_amount) * index_price), 2)
                else:
                    instrument1_premio = round(
                        abs(Quote().instrument_mark_price_cost(instrument_number=1) / float(
                            instrument1_amount) * index_price), 2)
            else:
                instrument1_premio = 'error'

            # Instrument 2
            if instrument2_kind == 'Unassigned':
                instrument2_premio = 'Unassigned'
            elif instrument2_kind == 'future':
                instrument2_premio = 0
            elif instrument2_kind == 'call' or instrument2_kind == 'put':
                if bid_ask_offer != 'waiting bid/ask offer':
                    instrument2_premio = round(
                        abs(Quote().instrument_market_cost(instrument_number=2) / float(
                            instrument2_amount) * index_price), 2)
                else:
                    instrument2_premio = round(
                        abs(Quote().instrument_mark_price_cost(instrument_number=2) / float(
                            instrument2_amount) * index_price), 2)
            else:
                instrument2_premio = 'error'

            # Instrument 3
            if instrument3_kind == 'Unassigned':
                instrument3_premio = 'Unassigned'
            elif instrument3_kind == 'future':
                instrument3_premio = 0
            elif instrument3_kind == 'call' or instrument3_kind == 'put':
                if bid_ask_offer != 'waiting bid/ask offer':
                    instrument3_premio = round(
                        abs(Quote().instrument_market_cost(instrument_number=3) / float(
                            instrument3_amount) * index_price), 2)
                else:
                    instrument3_premio = round(
                        abs(Quote().instrument_mark_price_cost(instrument_number=3) / float(
                            instrument3_amount) * index_price), 2)
            else:
                instrument3_premio = 'error'

            # Instrument 4
            if instrument4_kind == 'Unassigned':
                instrument4_premio = 'Unassigned'
            elif instrument4_kind == 'future':
                instrument4_premio = 0
            elif instrument4_kind == 'call' or instrument4_kind == 'put':
                if bid_ask_offer != 'waiting bid/ask offer':
                    instrument4_premio = round(
                        abs(Quote().instrument_market_cost(instrument_number=4) / float(
                            instrument4_amount) * index_price), 2)
                else:
                    instrument4_premio = round(
                        abs(Quote().instrument_mark_price_cost(instrument_number=4) / float(
                            instrument4_amount) * index_price), 2)
            else:
                instrument4_premio = 'error'

            # Instrument Strike
            # Instrument 1
            if instrument1_kind == 'call' or instrument1_kind == 'put':
                instrument1_strike_list = instrument1_name.split('-')
                instrument1_strike = float(instrument1_strike_list[-2])
            elif instrument1_kind == 'future':
                if instrument1_direction == 'buy':
                    instrument1_strike = connect.ask_price(instrument_name=instrument1_name)
                elif instrument1_direction == 'sell':
                    instrument1_strike = connect.bid_price(instrument_name=instrument1_name)
                else:
                    instrument1_strike = 'error'
            else:
                instrument1_strike = 'Unassigned'

            # Instrument 2
            if instrument2_kind == 'call' or instrument2_kind == 'put':
                instrument2_strike_list = instrument2_name.split('-')
                instrument2_strike = float(instrument2_strike_list[-2])
            elif instrument2_kind == 'future':
                if instrument2_direction == 'buy':
                    instrument2_strike = connect.ask_price(instrument_name=instrument2_name)
                elif instrument2_direction == 'sell':
                    instrument2_strike = connect.bid_price(instrument_name=instrument2_name)
                else:
                    instrument2_strike = 'error'
            else:
                instrument2_strike = 'Unassigned'

            # Instrument 3
            if instrument3_kind == 'call' or instrument3_kind == 'put':
                instrument3_strike_list = instrument3_name.split('-')
                instrument3_strike = float(instrument3_strike_list[-2])
            elif instrument3_kind == 'future':
                if instrument3_direction == 'buy':
                    instrument3_strike = connect.ask_price(instrument_name=instrument3_name)
                elif instrument3_direction == 'sell':
                    instrument3_strike = connect.bid_price(instrument_name=instrument3_name)
                else:
                    instrument3_strike = 'error'
            else:
                instrument3_strike = 'Unassigned'

            # Instrument 4
            if instrument4_kind == 'call' or instrument4_kind == 'put':
                instrument4_strike_list = instrument4_name.split('-')
                instrument4_strike = float(instrument4_strike_list[-2])
            elif instrument4_kind == 'future':
                if instrument4_direction == 'buy':
                    instrument4_strike = connect.ask_price(instrument_name=instrument4_name)
                elif instrument4_direction == 'sell':
                    instrument4_strike = connect.bid_price(instrument_name=instrument4_name)
                else:
                    instrument4_strike = 'error'
            else:
                instrument4_strike = 'Unassigned'

            # QUAL MENOR E MAIOR STRIKE
            strike_dict = dict()
            strike_dict.clear()
            if instrument1_strike != 'Unassigned' and instrument1_strike != 'error':
                strike_dict[str(instrument1_name)] = float(instrument1_strike)
            if instrument2_strike != 'Unassigned' and instrument2_strike != 'error':
                strike_dict[str(instrument2_name)] = float(instrument2_strike)
            if instrument3_strike != 'Unassigned' and instrument3_strike != 'error':
                strike_dict[str(instrument3_name)] = float(instrument3_strike)
            if instrument4_strike != 'Unassigned' and instrument4_strike != 'error':
                strike_dict[str(instrument4_name)] = float(instrument4_strike)

            if len(strike_dict) > 0:
                smaller_strike_instrument_name = min(strike_dict, key=strike_dict.get)  # instrument number
                smaller_strike = abs(strike_dict.get(smaller_strike_instrument_name, 0))  # Valor
                bigger_strike_instrument_name = max(strike_dict, key=strike_dict.get)  # instrument number
                bigger_strike = abs(strike_dict.get(bigger_strike_instrument_name, 0))  # Valor
            else:
                smaller_strike = 0  # valor
                bigger_strike = 0  # valor

            # BUILDING X axis
            x_axis_list = list()
            x_axis_list.clear()
            start_range = round(float(smaller_strike) * 0.1, 0)
            stop_range = round(float(bigger_strike) * 2, 0)
            step_range = 100
            x_axis_list = list(
                range(int(start_range), int(stop_range), step_range))  # lista com as cotações para plotar

            # BUILDING Y axis
            y_axis_list = list()
            y_axis_list_instrument1 = list()
            y_axis_list_instrument2 = list()
            y_axis_list_instrument3 = list()
            y_axis_list_instrument4 = list()

            y_axis_list.clear()  # lista com payoff para diferentes cotações
            y_axis_list_instrument1.clear()
            y_axis_list_instrument2.clear()
            y_axis_list_instrument3.clear()
            y_axis_list_instrument4.clear()

            # Cria variáveis utilizadas abaixo
            instrument1_payoff = 0
            instrument2_payoff = 0
            instrument3_payoff = 0
            instrument4_payoff = 0

            if (instrument1_strike == 'Unassigned' or instrument1_strike == 'error') and \
                    (instrument2_strike == 'Unassigned' or instrument2_strike == 'error') and \
                    (instrument3_strike == 'Unassigned' or instrument3_strike == 'error') and \
                    (instrument4_strike == 'Unassigned' or instrument4_strike == 'error'):
                y_axis_list.append(0)
            else:
                for i in x_axis_list:
                    if instrument1_strike != 'Unassigned' and instrument1_strike != 'error':
                        instrument1_payoff = float(_payoff(kind=instrument1_kind, quantidade=float(instrument1_amount),
                                                           cotacao=float(i), strike=float(instrument1_strike),
                                                           premio=float(instrument1_premio)))
                    else:
                        instrument1_payoff = 0

                    if instrument2_strike != 'Unassigned' and instrument2_strike != 'error':
                        instrument2_payoff = float(_payoff(kind=instrument2_kind, quantidade=float(instrument2_amount),
                                                           cotacao=float(i), strike=float(instrument2_strike),
                                                           premio=float(instrument2_premio)))
                    else:
                        instrument2_payoff = 0

                    if instrument3_strike != 'Unassigned' and instrument3_strike != 'error':
                        instrument3_payoff = float(_payoff(kind=instrument3_kind, quantidade=float(instrument3_amount),
                                                           cotacao=float(i), strike=float(instrument3_strike),
                                                           premio=float(instrument3_premio)))
                    else:
                        instrument3_payoff = 0

                    if instrument4_strike != 'Unassigned' and instrument4_strike != 'error':
                        instrument4_payoff = float(_payoff(kind=instrument4_kind, quantidade=float(instrument4_amount),
                                                           cotacao=float(i), strike=float(instrument4_strike),
                                                           premio=float(instrument4_premio)))
                    else:
                        instrument4_payoff = 0

                    if instrument1_strike != 'Unassigned' and instrument1_strike != 'error' and instrument1_payoff != 0:
                        y_axis_list_instrument1.append(round(instrument1_payoff, 2))
                    if instrument2_strike != 'Unassigned' and instrument2_strike != 'error' and instrument2_payoff != 0:
                        y_axis_list_instrument2.append(round(instrument2_payoff, 2))
                    if instrument3_strike != 'Unassigned' and instrument3_strike != 'error' and instrument3_payoff != 0:
                        y_axis_list_instrument3.append(round(instrument3_payoff, 2))
                    if instrument4_strike != 'Unassigned' and instrument4_strike != 'error' and instrument4_payoff != 0:
                        y_axis_list_instrument4.append(round(instrument4_payoff, 2))

                    y_axis_list.append(round(
                        instrument1_payoff + instrument2_payoff + instrument3_payoff + instrument4_payoff, 2))

            #  PLOT
            if instrument1_strike != 'Unassigned' and instrument1_strike != 'error' and instrument1_payoff != 0:
                x_axis_instrument1 = x_axis_list
                y_axis_instrument1 = y_axis_list_instrument1
            else:
                x_axis_instrument1 = 0
                y_axis_instrument1 = 0

            if instrument2_strike != 'Unassigned' and instrument2_strike != 'error' and instrument2_payoff != 0:
                x_axis_instrument2 = x_axis_list
                y_axis_instrument2 = y_axis_list_instrument2
            else:
                x_axis_instrument2 = 0
                y_axis_instrument2 = 0

            if instrument3_strike != 'Unassigned' and instrument3_strike != 'error' and instrument3_payoff != 0:
                x_axis_instrument3 = x_axis_list
                y_axis_instrument3 = y_axis_list_instrument3
            else:
                x_axis_instrument3 = 0
                y_axis_instrument3 = 0

            if instrument4_strike != 'Unassigned' and instrument4_strike != 'error' and instrument4_payoff != 0:
                x_axis_instrument4 = x_axis_list
                y_axis_instrument4 = y_axis_list_instrument4
            else:
                x_axis_instrument4 = 0
                y_axis_instrument4 = 0

            plt.figure(1)
            plt.subplot(221)  # the first subplot in the first figure
            plt.plot(x_axis_instrument1, y_axis_instrument1)
            plt.minorticks_on()
            plt.axhline(y=0.5, color="black", linestyle=":")
            plt.title(instrument1_name)
            plt.xlabel('Expiry Price')
            plt.ylabel('Loss/Gain')

            plt.subplot(222)  # the second subplot in the first figure
            plt.plot(x_axis_instrument2, y_axis_instrument2)
            plt.minorticks_on()
            plt.axhline(y=0.5, color="black", linestyle=":")
            plt.title(instrument2_name)
            plt.xlabel('Expiry Price')
            plt.ylabel('Loss/Gain')

            plt.subplot(223)
            plt.plot(x_axis_instrument3, y_axis_instrument3)
            plt.minorticks_on()
            plt.axhline(y=0.5, color="black", linestyle=":")
            plt.title(instrument3_name)
            plt.xlabel('Expiry Price')
            plt.ylabel('Loss/Gain')

            plt.subplot(224)
            plt.plot(x_axis_instrument4, y_axis_instrument4)
            plt.minorticks_on()
            plt.axhline(y=0.5, color="black", linestyle=":")
            plt.title(instrument4_name)
            plt.xlabel('Expiry Price')
            plt.ylabel('Loss/Gain')

            plt.subplots_adjust(top=0.92, bottom=0.10, left=0.12, right=0.95, hspace=0.5,
                                wspace=0.70)

            instrument1_expiration = instrument_expiration_construction_from_instrument_file(1)
            instrument2_expiration = instrument_expiration_construction_from_instrument_file(2)
            instrument3_expiration = instrument_expiration_construction_from_instrument_file(3)
            instrument4_expiration = instrument_expiration_construction_from_instrument_file(4)

            instrument_expiration_list = []
            instrument_expiration_list2 = []

            instrument_expiration_list.clear()
            instrument_expiration_list2.clear()

            if instrument1_expiration is not False and instrument1_expiration is not True:
                instrument_expiration_list.append(str.replace(str(instrument1_expiration), '\n', ''))
            else:
                instrument_expiration_list.append(instrument1_expiration)
            if instrument2_expiration is not False and instrument2_expiration is not True:
                instrument_expiration_list.append(str.replace(str(instrument2_expiration), '\n', ''))
            else:
                instrument_expiration_list.append(instrument2_expiration)
            if instrument3_expiration is not False and instrument3_expiration is not True:
                instrument_expiration_list.append(str.replace(str(instrument3_expiration), '\n', ''))
            else:
                instrument_expiration_list.append(instrument3_expiration)
            if instrument4_expiration is not False and instrument4_expiration is not True:
                instrument_expiration_list.append(str.replace(str(instrument4_expiration), '\n', ''))
            else:
                instrument_expiration_list.append(instrument4_expiration)

            if len(instrument_expiration_list) >= 2:
                for i in instrument_expiration_list:
                    instrument_expiration_list2.append(i)

                if False in instrument_expiration_list2:
                    try:
                        while True:
                            instrument_expiration_list2.remove(False)
                    except ValueError:
                        pass
                if True in instrument_expiration_list2:
                    try:
                        while True:
                            instrument_expiration_list2.remove(True)
                    except ValueError:
                        pass

                if len(instrument_expiration_list2) >= 1:
                    plot_figure_2 = True
                    for item1 in instrument_expiration_list:
                        if item1 is True or item1 is False:
                            pass
                        else:
                            if item1 != instrument_expiration_list2[0]:
                                plot_figure_2 = False
                            else:
                                pass
                else:
                    plot_figure_2 = True
            else:
                plot_figure_2 = True

            if plot_figure_2 is True:
                plt.figure(2)
                plt.plot(x_axis_list, y_axis_list)
                plt.minorticks_on()
                plt.axhline(y=0.5, color="black", linestyle=":")
                plt.title('STRATEGY PAYOFF')
                plt.xlabel('Expiry Price')
                plt.ylabel('Loss/Gain')
            else:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('STRATEGY PAYOFF IS ONLY AVAILABLE IF ALL EXPIRATIONS ARE THE SAME OR PERPETUAL. '
                            'OTHERWISE, ONLY THE PAYOFF OF EACH SEPARATE INSTRUMENT WILL BE SHOWN.')
                msg.setWindowTitle('***** INFO *****')
                msg.exec_()

            plt.show()

        except Exception as er:
            list_monitor_log.append('*** ERROR in plot_payoff_for_4_instruments() Error Code: 5359 ***' + str(er))
            connect.logwriter(msg='*** ERROR in plot_payoff_for_4_instruments() Error Code: 5360 ***' + str(er))
        finally:
            pass

    def enable_disable_strike_and_c_or_p_and_maturity():
        if ui.lineEdit_o_or_f_instrumet1.currentText() == '':
            ui.lineEdit_buy_or_sell_instrumet1.setEnabled(False)
            ui.lineEdit_amount_instrumet1.setEnabled(False)
            ui.lineEdit_currency_instrumet1.setEnabled(False)
            ui.lineEdit_strike_instrumet1.setEnabled(False)
            ui.lineEdit_maturity_instrumet1.setEnabled(False)
            ui.checkBox_perpetual_1.setEnabled(False)
            ui.lineEdit_c_or_p_instrumet1.setEnabled(False)
            ui.check_box_reduce_only_1.setEnabled(False)
        elif ui.lineEdit_o_or_f_instrumet1.currentText() == 'o' or \
                ui.lineEdit_o_or_f_instrumet1.currentText() == 'f':
            ui.lineEdit_buy_or_sell_instrumet1.setEnabled(True)
            ui.lineEdit_amount_instrumet1.setEnabled(True)
            ui.lineEdit_currency_instrumet1.setEnabled(True)
            ui.check_box_reduce_only_1.setEnabled(True)
            if ui.lineEdit_o_or_f_instrumet1.currentText() == 'o':
                ui.lineEdit_strike_instrumet1.setEnabled(True)
                ui.lineEdit_maturity_instrumet1.setEnabled(True)
                ui.checkBox_perpetual_1.setEnabled(False)
                ui.lineEdit_c_or_p_instrumet1.setEnabled(True)
            elif ui.lineEdit_o_or_f_instrumet1.currentText() == 'f':
                ui.lineEdit_strike_instrumet1.setEnabled(False)
                ui.checkBox_perpetual_1.setEnabled(True)
                ui.lineEdit_c_or_p_instrumet1.setEnabled(False)
                if ui.checkBox_perpetual_1.isChecked() is True:
                    ui.lineEdit_maturity_instrumet1.setEnabled(False)
                elif ui.checkBox_perpetual_1.isChecked() is False:
                    ui.lineEdit_maturity_instrumet1.setEnabled(True)
                else:
                    pass
            else:
                pass
        else:
            pass

        if ui.lineEdit_o_or_f_instrumet2.currentText() == '':
            ui.lineEdit_buy_or_sell_instrumet2.setEnabled(False)
            ui.lineEdit_amount_instrumet2.setEnabled(False)
            ui.lineEdit_currency_instrumet2.setEnabled(False)
            ui.lineEdit_strike_instrumet2.setEnabled(False)
            ui.lineEdit_maturity_instrumet2.setEnabled(False)
            ui.checkBox_perpetual_2.setEnabled(False)
            ui.lineEdit_c_or_p_instrumet2.setEnabled(False)
            ui.check_box_reduce_only_2.setEnabled(False)
        elif ui.lineEdit_o_or_f_instrumet2.currentText() == 'o' or \
                ui.lineEdit_o_or_f_instrumet2.currentText() == 'f':
            ui.lineEdit_buy_or_sell_instrumet2.setEnabled(True)
            ui.lineEdit_amount_instrumet2.setEnabled(True)
            ui.lineEdit_currency_instrumet2.setEnabled(True)
            ui.check_box_reduce_only_2.setEnabled(True)
            if ui.lineEdit_o_or_f_instrumet2.currentText() == 'o':
                ui.lineEdit_strike_instrumet2.setEnabled(True)
                ui.lineEdit_maturity_instrumet2.setEnabled(True)
                ui.checkBox_perpetual_2.setEnabled(False)
                ui.lineEdit_c_or_p_instrumet2.setEnabled(True)
            elif ui.lineEdit_o_or_f_instrumet2.currentText() == 'f':
                ui.lineEdit_strike_instrumet2.setEnabled(False)
                ui.checkBox_perpetual_2.setEnabled(True)
                ui.lineEdit_c_or_p_instrumet2.setEnabled(False)
                if ui.checkBox_perpetual_2.isChecked() is True:
                    ui.lineEdit_maturity_instrumet2.setEnabled(False)
                elif ui.checkBox_perpetual_2.isChecked() is False:
                    ui.lineEdit_maturity_instrumet2.setEnabled(True)
                else:
                    pass
            else:
                pass
        else:
            pass

        if ui.lineEdit_o_or_f_instrumet3.currentText() == '':
            ui.lineEdit_buy_or_sell_instrumet3.setEnabled(False)
            ui.lineEdit_amount_instrumet3.setEnabled(False)
            ui.lineEdit_currency_instrumet3.setEnabled(False)
            ui.lineEdit_strike_instrumet3.setEnabled(False)
            ui.lineEdit_maturity_instrumet3.setEnabled(False)
            ui.checkBox_perpetual_3.setEnabled(False)
            ui.lineEdit_c_or_p_instrumet3.setEnabled(False)
            ui.check_box_reduce_only_3.setEnabled(False)
        elif ui.lineEdit_o_or_f_instrumet3.currentText() == 'o' or \
                ui.lineEdit_o_or_f_instrumet3.currentText() == 'f':
            ui.lineEdit_buy_or_sell_instrumet3.setEnabled(True)
            ui.lineEdit_amount_instrumet3.setEnabled(True)
            ui.lineEdit_currency_instrumet3.setEnabled(True)
            ui.check_box_reduce_only_3.setEnabled(True)
            if ui.lineEdit_o_or_f_instrumet3.currentText() == 'o':
                ui.lineEdit_strike_instrumet3.setEnabled(True)
                ui.lineEdit_maturity_instrumet3.setEnabled(True)
                ui.checkBox_perpetual_3.setEnabled(False)
                ui.lineEdit_c_or_p_instrumet3.setEnabled(True)
            elif ui.lineEdit_o_or_f_instrumet3.currentText() == 'f':
                ui.lineEdit_strike_instrumet3.setEnabled(False)
                ui.checkBox_perpetual_3.setEnabled(True)
                ui.lineEdit_c_or_p_instrumet3.setEnabled(False)
                if ui.checkBox_perpetual_3.isChecked() is True:
                    ui.lineEdit_maturity_instrumet3.setEnabled(False)
                elif ui.checkBox_perpetual_3.isChecked() is False:
                    ui.lineEdit_maturity_instrumet3.setEnabled(True)
                else:
                    pass
            else:
                pass
        else:
            pass

        if ui.lineEdit_o_or_f_instrumet4.currentText() == '':
            ui.lineEdit_buy_or_sell_instrumet4.setEnabled(False)
            ui.lineEdit_amount_instrumet4.setEnabled(False)
            ui.lineEdit_currency_instrumet4.setEnabled(False)
            ui.lineEdit_strike_instrumet4.setEnabled(False)
            ui.lineEdit_maturity_instrumet4.setEnabled(False)
            ui.checkBox_perpetual_4.setEnabled(False)
            ui.lineEdit_c_or_p_instrumet4.setEnabled(False)
            ui.check_box_reduce_only_4.setEnabled(False)
        elif ui.lineEdit_o_or_f_instrumet4.currentText() == 'o' or \
                ui.lineEdit_o_or_f_instrumet4.currentText() == 'f':
            ui.lineEdit_buy_or_sell_instrumet4.setEnabled(True)
            ui.lineEdit_amount_instrumet4.setEnabled(True)
            ui.lineEdit_currency_instrumet4.setEnabled(True)
            ui.check_box_reduce_only_4.setEnabled(True)
            if ui.lineEdit_o_or_f_instrumet4.currentText() == 'o':
                ui.lineEdit_strike_instrumet4.setEnabled(True)
                ui.lineEdit_maturity_instrumet4.setEnabled(True)
                ui.checkBox_perpetual_4.setEnabled(False)
                ui.lineEdit_c_or_p_instrumet4.setEnabled(True)
            elif ui.lineEdit_o_or_f_instrumet4.currentText() == 'f':
                ui.lineEdit_strike_instrumet4.setEnabled(False)
                ui.checkBox_perpetual_4.setEnabled(True)
                ui.lineEdit_c_or_p_instrumet4.setEnabled(False)
                if ui.checkBox_perpetual_4.isChecked() is True:
                    ui.lineEdit_maturity_instrumet4.setEnabled(False)
                elif ui.checkBox_perpetual_4.isChecked() is False:
                    ui.lineEdit_maturity_instrumet4.setEnabled(True)
                else:
                    pass
            else:
                pass
        else:
            pass

    def instruments_saved_print_and_check_available():
        from lists import list_monitor_log
        textedit_instruments_saved_settext_signal_str = str(InstrumentsSaved().instruments_check())
        sinal.textedit_instruments_saved_settext_signal.emit(textedit_instruments_saved_settext_signal_str)

        instrument1_available = InstrumentsSaved().instrument_available(instrument_number=1)
        instrument2_available = InstrumentsSaved().instrument_available(instrument_number=2)
        instrument3_available = InstrumentsSaved().instrument_available(instrument_number=3)
        instrument4_available = InstrumentsSaved().instrument_available(instrument_number=4)
        
        try:
            if (instrument1_available == 'instrument available' or
                instrument1_available == 'Unassigned') and \
                    (instrument2_available == 'instrument available' or
                     instrument2_available == 'Unassigned') and \
                    (instrument3_available == 'instrument available' or
                     instrument3_available == 'Unassigned') and \
                    (instrument4_available == 'instrument available' or
                     instrument4_available == 'Unassigned'):

                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Instruments Syntax OK')
                msg.setWindowTitle('INFO')
                msg.exec_()
                pass
            else:
                pass

            if instrument1_available == 'instrument NO available':
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Instrument 1 Syntax ERROR')
                msg.setWindowTitle('***** ERROR *****')
                msg.exec_()
                pass
            else:
                pass

            if instrument2_available == 'instrument NO available':
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Instrument 2 Syntax ERROR')
                msg.setWindowTitle('***** ERROR *****')
                msg.exec_()
                pass
            else:
                pass

            if instrument3_available == 'instrument NO available':
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Instrument 3 Syntax ERROR')
                msg.setWindowTitle('***** ERROR *****')
                msg.exec_()
                pass
            else:
                pass

            if instrument4_available == 'instrument NO available':
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Instrument 4 Syntax ERROR')
                msg.setWindowTitle('***** ERROR *****')
                msg.exec_()
                pass
            else:
                pass

        except Exception as er:
            from connection_spread import connect
            connect.logwriter(str(er) + ' Error Code:: 5563')
            list_monitor_log.append(str(er) + ' Error Code:: 5564')

            list_for_signal = list()
            list_for_signal.clear()
            list_for_signal.append('Instruments Checking Syntax ERROR')
            list_for_signal.append('***** ERROR *****')
            sinal.msg_box_for_thread_when_open_app1_signal.emit(list_for_signal)
            pass
        finally:
            pass

    def position_now_when_open_app():
        global list_thread_when_open_app
        from connection_spread import connect, led_color
        from lists import list_monitor_log

        instrument1_name = instrument_name_construction_from_file_when_open_app(instrument_number=1)
        instrument2_name = instrument_name_construction_from_file_when_open_app(instrument_number=2)
        instrument3_name = instrument_name_construction_from_file_when_open_app(instrument_number=3)
        instrument4_name = instrument_name_construction_from_file_when_open_app(instrument_number=4)

        a = instrument1_name
        b = instrument2_name
        c = instrument3_name
        d = instrument4_name

        if led_color() == 'red':
            list_for_signal = list()
            list_for_signal.clear()
            list_for_signal.append('Connection Offline - Current Positions don´t updated')
            list_for_signal.append('***** ERROR *****')
            sinal.msg_box_for_thread_when_open_app1_signal.emit(list_for_signal)
            time.sleep(3)
            pass
        else:
            try:
                if a != 'Unassigned':
                    a1 = connect.get_position_size(instrument_name=a)
                else:
                    a1 = 'Unassigned'

                if b != 'Unassigned':
                    b1 = connect.get_position_size(instrument_name=b)
                else:
                    b1 = 'Unassigned'

                if c != 'Unassigned':
                    c1 = connect.get_position_size(instrument_name=c)
                else:
                    c1 = 'Unassigned'

                if d != 'Unassigned':
                    d1 = connect.get_position_size(instrument_name=d)
                else:
                    d1 = 'Unassigned'

                sinal.position_now_when_open_app_signal.emit(str('Instrument 1: ' + str(a1) + '\n' +
                                                                 'Instrument 2: ' + str(b1) + '\n' +
                                                                 'Instrument 3: ' + str(c1) + '\n' +
                                                                 'Instrument 4: ' + str(d1)))

            except Exception as er:
                connect.logwriter(str(er) + ' Error Code:: 5628')
                list_monitor_log.append(str(er) + ' Error Code:: 5629')
                ui.textEdit_balance_2.clear()
                ui.textEdit_balance_2.setText(str(er) + ' Error Code:: 5631')

                list_for_signal = list()
                list_for_signal.clear()
                list_for_signal.append('Current Positions don´t checked')
                list_for_signal.append('***** ERROR *****')
                sinal.msg_box_for_thread_when_open_app1_signal.emit(list_for_signal)
                pass
            finally:
                pass

    def msg_box_for_thread_when_open_app2():
        instruments_saved_print_and_check_available_when_open_app2()

    def msg_box_for_thread_when_open_app3():
        sinal.textedit_balance_settext_signal.emit(str(ConfigSaved().position_saved()))  # Sbustitui o abaixo
        # ui.textEdit_balance.setText(str(ConfigSaved().position_saved()))
        position_now_when_open_app()

    def quote_new_when_open_app():
        from connection_spread import connect, led_color
        global list_thread_when_open_app

        if led_color() == 'red':
            list_for_signal = list()
            list_for_signal.clear()
            list_for_signal.append('Connectioin Off line')
            list_for_signal.append('***** ERROR *****')
            sinal.msg_box_for_thread_when_open_app1_signal.emit(list_for_signal)
            time.sleep(3)
            pass
        else:
            quote_new_when_open_app_signal1_dict = dict()
            quote_new_when_open_app_signal1_dict.clear()

            f9 = InstrumentsSaved().instrument_direction_construction_from_instrument_file(instrument_number=1)
            quote_new_when_open_app_signal1_dict['f9'] = str(f9)  # ui.lineEdit.setText(f9)
            f10 = InstrumentsSaved().instrument_direction_construction_from_instrument_file(instrument_number=2)
            quote_new_when_open_app_signal1_dict['f10'] = str(f10)  # ui.lineEdit_2.setText(f10)
            f11 = InstrumentsSaved().instrument_direction_construction_from_instrument_file(instrument_number=3)
            quote_new_when_open_app_signal1_dict['f11'] = str(f11)  # ui.lineEdit_3.setText(f11)
            f12 = InstrumentsSaved().instrument_direction_construction_from_instrument_file(instrument_number=4)
            quote_new_when_open_app_signal1_dict['f12'] = str(f12)  # ui.lineEdit_4.setText(f12)
            f13 = str(InstrumentsSaved().instrument_amount_saved(instrument_number=1))
            quote_new_when_open_app_signal1_dict['f13'] = str(f13)  # ui.lineEdit_7.setText(f13)
            f13_k = str(InstrumentsSaved().instrument_kind_saved(instrument_number=1))
            f14 = str(InstrumentsSaved().instrument_amount_saved(instrument_number=2))
            quote_new_when_open_app_signal1_dict['f14'] = str(f14)  # ui.lineEdit_5.setText(f14)
            f14_k = str(InstrumentsSaved().instrument_kind_saved(instrument_number=2))
            f15 = str(InstrumentsSaved().instrument_amount_saved(instrument_number=3))
            quote_new_when_open_app_signal1_dict['f15'] = str(f15)  # ui.lineEdit_8.setText(f15)
            f15_k = str(InstrumentsSaved().instrument_kind_saved(instrument_number=3))
            f16 = str(InstrumentsSaved().instrument_amount_saved(instrument_number=4))
            quote_new_when_open_app_signal1_dict['f16'] = str(f16)  # ui.lineEdit_6.setText(f16)
            f16_k = str(InstrumentsSaved().instrument_kind_saved(instrument_number=4))
            f17 = InstrumentsSaved().instrument_name_construction_from_file(instrument_number=1)
            quote_new_when_open_app_signal1_dict['f17'] = str(f17)  # ui.lineEdit_10.setText(f17)
            f18 = InstrumentsSaved().instrument_name_construction_from_file(instrument_number=2)
            quote_new_when_open_app_signal1_dict['f18'] = str(f18)  # ui.lineEdit_11.setText(f18)
            f19 = InstrumentsSaved().instrument_name_construction_from_file(instrument_number=3)
            quote_new_when_open_app_signal1_dict['f19'] = str(f19)  # ui.lineEdit_9.setText(f19)
            f20 = InstrumentsSaved().instrument_name_construction_from_file(instrument_number=4)
            quote_new_when_open_app_signal1_dict['f20'] = str(f20)  # ui.lineEdit_12.setText(f20)
            f21 = round(Quote().instrument_mark_price_cost(instrument_number=1), 4)
            f25 = str(f21)
            quote_new_when_open_app_signal1_dict['f25'] = str(f25)  # ui.lineEdit_14.setText(f25)
            f22 = round(Quote().instrument_mark_price_cost(instrument_number=2), 4)
            f26 = str(f22)
            quote_new_when_open_app_signal1_dict['f26'] = str(f26)  # ui.lineEdit_15.setText(f26)
            f23 = round(Quote().instrument_mark_price_cost(instrument_number=3), 4)
            f27 = str(f23)
            quote_new_when_open_app_signal1_dict['f27'] = str(f27)  # ui.lineEdit_13.setText(f27)
            f24 = round(Quote().instrument_mark_price_cost(instrument_number=4), 4)
            f28 = str(f24)
            quote_new_when_open_app_signal1_dict['f28'] = str(f28)  # ui.lineEdit_16.setText(f28)
            f25 = round(Quote().instrument_market_cost(instrument_number=1), 4)
            f29 = str(f25)
            quote_new_when_open_app_signal1_dict['f29'] = str(f29)  # ui.lineEdit_17.setText(f29)
            f26 = round(Quote().instrument_market_cost(instrument_number=2), 4)
            f30 = str(f26)
            quote_new_when_open_app_signal1_dict['f30'] = str(f30)  # ui.lineEdit_18.setText(f30)
            f27 = round(Quote().instrument_market_cost(instrument_number=3), 4)
            f31 = str(f27)
            quote_new_when_open_app_signal1_dict['f31'] = str(f31)  # ui.lineEdit_19.setText(f31)
            f28 = round(Quote().instrument_market_cost(instrument_number=4), 4)
            f32 = str(f28)
            quote_new_when_open_app_signal1_dict['f32'] = str(f32)  # ui.lineEdit_20.setText(f32)

            instrument_name_currency_exchange_rate = ConfigSaved().currency_exchange_rate_for_upper_and_lower()

            if Quote().bid_ask_offer() == 'waiting bid/ask offer':
                f = float(
                    connect.get_last_trades_by_instrument_price(instrument_name=instrument_name_currency_exchange_rate))
                a = round(float(Quote().structure_option_mark_price_cost()), 5)
                a_usd = round(float(a) * f, 2)
                a1 = 'None - NO OPTION OPTION BID/ASK OFFER'
                a1_a = 'None - NO BID/ASK OFFER'
                g = ''
                h = ''

            elif (f13 == 'Unassigned' or f13_k == 'future') and \
                    (f14 == 'Unassigned' or f14_k == 'future') and \
                    (f15 == 'Unassigned' or f15_k == 'future') and \
                    (f16 == 'Unassigned' or f16_k == 'future'):
                a = 'All instruments Unassigned '
                a_usd = ''
                a1 = a
                g = ''
                a1_a = a
                h = ''
            else:
                f = float(
                    connect.get_last_trades_by_instrument_price(instrument_name=instrument_name_currency_exchange_rate))

                a = round(float(Quote().structure_option_mark_price_cost()), 5)
                a_usd = round(float(a) * f, 2)

                a1 = round(float(Quote().structure_option_market_cost()), 5)
                a1_usd = round(float(a1) * f, 2)
                if float(a) == 0:
                    a1_a = 'Strategy MARK Price = 0'
                    h = ''
                else:
                    a1_a = round(abs(float(a1) / float(a)) * 100, 2)
                    h = '% of the Strategy MARK Price'
                g = ' (' + str(a1_usd) + 'USD)'

            quote_new_when_open_app_signal1_dict['lineEdit_22'] = str(
                'Strategy MARK Price: ' + str(a) + ' (' + str(a_usd) + 'USD)')
            quote_new_when_open_app_signal1_dict['lineEdit_23'] = str(
                'Strategy MARKET Price: ' + str(a1) + g)
            quote_new_when_open_app_signal1_dict['lineEdit_21'] = str(
                'Strategy MARKET Price cost ' + str(a1_a) + h)

            sinal.quote_new_when_open_app_signal1.emit(quote_new_when_open_app_signal1_dict)

            Quote().structure_option_greeks_quote()  # Já emite sinal para um signal
            Quote().last_trade_instrument_conditions_quote()  # Já emite sinal para um signal

    def instruments_saved_print_and_check_available_when_open_app2():
        from lists import list_monitor_log
        global list_thread_when_open_app
        textedit_instruments_saved_settext_signal_str = str(InstrumentsSaved().instruments_check())
        sinal.textedit_instruments_saved_settext_signal.emit(textedit_instruments_saved_settext_signal_str)

        instrument1_available = InstrumentsSaved().instrument_available(instrument_number=1)
        instrument2_available = InstrumentsSaved().instrument_available(instrument_number=2)
        instrument3_available = InstrumentsSaved().instrument_available(instrument_number=3)
        instrument4_available = InstrumentsSaved().instrument_available(instrument_number=4)
        
        try:
            if (instrument1_available == 'instrument available' or
                instrument1_available == 'Unassigned') and \
                    (instrument2_available == 'instrument available' or
                     instrument2_available == 'Unassigned') and \
                    (instrument3_available == 'instrument available' or
                     instrument3_available == 'Unassigned') and \
                    (instrument4_available == 'instrument available' or
                     instrument4_available == 'Unassigned'):

                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Instruments Syntax OK')
                msg.setWindowTitle('INFO')
                msg.exec_()
                pass
            else:
                pass

            if instrument1_available == 'instrument NO available':
                list_for_signal = list()
                list_for_signal.clear()
                list_for_signal.append('Instrument 1 Syntax ERROR')
                list_for_signal.append('***** ERROR *****')
                sinal.msg_box_for_thread_when_open_app1_signal.emit(list_for_signal)
                pass
            else:
                pass

            if instrument2_available == 'instrument NO available':
                list_for_signal = list()
                list_for_signal.clear()
                list_for_signal.append('Instrument 2 Syntax ERROR')
                list_for_signal.append('***** ERROR *****')
                sinal.msg_box_for_thread_when_open_app1_signal.emit(list_for_signal)
                pass
            else:
                pass

            if instrument3_available == 'instrument NO available':
                list_for_signal = list()
                list_for_signal.clear()
                list_for_signal.append('Instrument 3 Syntax ERROR')
                list_for_signal.append('***** ERROR *****')
                sinal.msg_box_for_thread_when_open_app1_signal.emit(list_for_signal)
                pass
            else:
                pass

            if instrument4_available == 'instrument NO available':
                list_for_signal = list()
                list_for_signal.clear()
                list_for_signal.append('Instrument 4 Syntax ERROR')
                list_for_signal.append('***** ERROR *****')
                sinal.msg_box_for_thread_when_open_app1_signal.emit(list_for_signal)
                pass
            else:
                pass

        except Exception as er:
            from connection_spread import connect
            connect.logwriter(str(er) + ' Error Code:: 5857')
            list_monitor_log.append(str(er) + ' Error Code:: 5858')

            list_for_signal = list()
            list_for_signal.clear()
            list_for_signal.append('Instruments Checking Syntax ERROR')
            list_for_signal.append('***** ERROR *****')
            sinal.msg_box_for_thread_when_open_app1_signal.emit(list_for_signal)
            pass
        finally:
            pass

    def position_preview_to_gui_when_open_app():
        global list_thread_when_open_app

        max_position_instrument1_for_gui = Config().max_position_from_position_saved_and_instrument_amount(
            instrument_number=1)
        max_position_instrument2_for_gui = Config().max_position_from_position_saved_and_instrument_amount(
            instrument_number=2)
        max_position_instrument3_for_gui = Config().max_position_from_position_saved_and_instrument_amount(
            instrument_number=3)
        max_position_instrument4_for_gui = Config().max_position_from_position_saved_and_instrument_amount(
            instrument_number=4)

        textedit_balance_after_signal_dict = dict()
        textedit_balance_after_signal_dict.clear()

        textedit_balance_after_signal_dict['Instrument 1'] = str(max_position_instrument1_for_gui)
        textedit_balance_after_signal_dict['Instrument 2'] = str(max_position_instrument2_for_gui)
        textedit_balance_after_signal_dict['Instrument 3'] = str(max_position_instrument3_for_gui)
        textedit_balance_after_signal_dict['Instrument 4'] = str(max_position_instrument4_for_gui)

        sinal.textedit_balance_after_signal.emit(textedit_balance_after_signal_dict)

        if 'ERROR' in str(max_position_instrument1_for_gui):
            list_for_signal = list()
            list_for_signal.clear()
            list_for_signal.append('Instrument 1 Syntax ERROR')
            list_for_signal.append('***** ERROR *****')
            sinal.msg_box_for_thread_when_open_app1_signal.emit(list_for_signal)
            pass
        else:
            pass
        if 'ERROR' in str(max_position_instrument2_for_gui):
            list_for_signal = list()
            list_for_signal.clear()
            list_for_signal.append('Instrument 2 Syntax ERROR')
            list_for_signal.append('***** ERROR *****')
            sinal.msg_box_for_thread_when_open_app1_signal.emit(list_for_signal)
            pass
        else:
            pass
        if 'ERROR' in str(max_position_instrument3_for_gui):
            list_for_signal = list()
            list_for_signal.clear()
            list_for_signal.append('Instrument 3 Syntax ERROR')
            list_for_signal.append('***** ERROR *****')
            sinal.msg_box_for_thread_when_open_app1_signal.emit(list_for_signal)
            pass
        else:
            pass
        if 'ERROR' in str(max_position_instrument4_for_gui):
            list_for_signal = list()
            list_for_signal.clear()
            list_for_signal.append('Instrument 4 Syntax ERROR')
            list_for_signal.append('***** ERROR *****')
            sinal.msg_box_for_thread_when_open_app1_signal.emit(list_for_signal)
        else:
            pass

    def instrument_name_construction_from_file_when_open_app(instrument_number=None):

        file_open = 'instruments_spread.txt'

        instrument_number_adjusted_to_list = (int(instrument_number) - 1)

        # open file instruments
        with open(file_open, 'r') as file_instruments:
            lines_file_instruments = file_instruments.readlines()  # file instruments_spread.txt ==> lines
            # Instrument
            list_line_instrument = lines_file_instruments[instrument_number_adjusted_to_list].split()  # line ==> list
            if 'Unassigned' in list_line_instrument:
                return 'Unassigned'
            else:
                instrument_name = str(list_line_instrument[5])
                return str(instrument_name)

    def instruments_saved_print_and_check_available_when_open_app():
        from lists import list_monitor_log
        from connection_spread import led_color
        global list_thread_when_open_app

        setup = ConfigParser(
            allow_no_value=True,
            inline_comment_prefixes='#',
            strict=False
        )
        setup.read('setup.ini')
        date_time_setup = setup['date_time']
        date_time_setup_enable = date_time_setup.getboolean('date_time_enabled')

        if date_time_setup_enable is True:
            sinal.date_time_enabled_signal.emit()
        else:
            sinal.date_time_disabled_signal.emit()

        if led_color() == 'red':  # Erro depois ver o que fazer com esta mensagem box
            list_for_signal = list()
            list_for_signal.clear()
            list_for_signal.append(' Connection Offline ')
            list_for_signal.append('***** ERROR *****')
            sinal.msg_box_for_thread_when_open_app1_signal.emit(list_for_signal)
            while led_color() == 'red':
                time.sleep(3)
                pass
            pass
        else:
            pass

        try:
            instrument_saved_1 = InstrumentsSaved().instrument_available(instrument_number=1)
            instrument_saved_2 = InstrumentsSaved().instrument_available(instrument_number=2)
            instrument_saved_3 = InstrumentsSaved().instrument_available(instrument_number=3)
            instrument_saved_4 = InstrumentsSaved().instrument_available(instrument_number=4)

            if (instrument_saved_1 == 'instrument NO available') or (
                    instrument_saved_2 == 'instrument NO available') or (
                    instrument_saved_3 == 'instrument NO available') or (
                    instrument_saved_4 == 'instrument NO available'):

                with open('instruments_spread.txt', 'w') as instruments_save_file:
                    instruments_save_file.write('Instrument 1: Unassigned\n' +
                                                'Instrument 2: Unassigned\n' +
                                                'Instrument 3: Unassigned\n' +
                                                'Instrument 4: Unassigned\n'
                                                )
                Config().setup_ini_creator()
                textedit_instruments_saved_settext_signal_str = str(InstrumentsSaved().instruments_check())
                sinal.textedit_instruments_saved_settext_signal.emit(textedit_instruments_saved_settext_signal_str)
                Config().position_before_trade_save()
                print_greeks_by_instrument()
                textedit_balance_settext_signal_str = ConfigSaved().position_saved()
                sinal.textedit_balance_settext_signal.emit(textedit_balance_settext_signal_str)
                sinal.position_now_signal_2.emit()
                sinal.pushButton_request_options_structure_cost_signal.emit()  # = call Quote().quote_new()

                instrument_s_for_list = list()
                instrument_s_for_list.clear()

                if instrument_saved_1 == 'instrument NO available':
                    instrument_s_for_list.append('1')
                if instrument_saved_2 == 'instrument NO available':
                    instrument_s_for_list.append('2')
                if instrument_saved_3 == 'instrument NO available':
                    instrument_s_for_list.append('3')
                if instrument_saved_4 == 'instrument NO available':
                    instrument_s_for_list.append('4')
                else:
                    pass

                instrument_s_for_list_str1 = str.replace(str(instrument_s_for_list), '[', '')
                instrument_s_for_list_str2 = str.replace(str(instrument_s_for_list_str1), ']', '')

                list_for_signal = list()
                list_for_signal.clear()
                list_for_signal.append('Instrument(s) Syntax ERROR: ' + str(
                    instrument_s_for_list_str2) + ' - Update ALL instruments to Unassigned')
                list_for_signal.append('***** ERROR *****')
                sinal.msg_box_for_thread_when_open_app1_signal.emit(list_for_signal)

                position_preview_to_gui_when_open_app()
                sinal.instruments_saved_print_and_check_available_signal.emit()
                quote_new_when_open_app()  # Tem varias ui
                sinal.msg_box_for_thread_when_open_app3_signal.emit()
                sinal.strategy_name_update_signal.emit()
                pass
            else:
                print_greeks_by_instrument()  # já se repete em:  ui.textEdit_targets_saved_3.append('Change1')
                # a função 'print_greeks_by_instrument' já tem sinal nela.
                position_preview_to_gui_when_open_app()
                sinal.instruments_saved_print_and_check_available_signal.emit()
                # signal up call instruments_saved_print_and_check_available_when_open_app2()
                quote_new_when_open_app()
                sinal.msg_box_for_thread_when_open_app3_signal.emit()
                Config().date_time_saved()
                Config().reduce_only_saved()
                enable_disable_strike_and_c_or_p_and_maturity()

        except Exception as er:
            from connection_spread import connect
            connect.logwriter(str(er) + ' Error Code:: 6026')
            list_monitor_log.append(str(er) + ' Error Code:: 6027')
            with open('instruments_spread.txt', 'w') as instruments_save_file:
                instruments_save_file.write('Instrument 1: Unassigned\n' +
                                            'Instrument 2: Unassigned\n' +
                                            'Instrument 3: Unassigned\n' +
                                            'Instrument 4: Unassigned\n'
                                            )
            Config().setup_ini_creator()
            textedit_instruments_saved_settext_signal_str = str(InstrumentsSaved().instruments_check())
            sinal.textedit_instruments_saved_settext_signal.emit(textedit_instruments_saved_settext_signal_str)
            print_greeks_by_instrument()
            sinal.textedit_balance_settext_signal.emit(str(ConfigSaved().position_saved()))
            position_preview_to_gui()
            sinal.position_now_signal_2.emit()
            sinal.pushButton_request_options_structure_cost_signal.emit()  # = call Quote().quote_new()

            list_for_signal = list()
            list_for_signal.clear()
            list_for_signal.append('Syntax and Instruments Checking ERROR - Update all instruments to Unassigned')
            list_for_signal.append('***** ERROR *****')
            sinal.msg_box_for_thread_when_open_app1_signal.emit(list_for_signal)
            pass

            sinal.instruments_saved_print_and_check_available_signal.emit()
            sinal.strategy_name_update_signal.emit()
            pass

    def date_time_enabled_signal():
        from connection_spread import connect

        ConfigSaved().setup_ini_check()

        setup = ConfigParser(
            allow_no_value=True,
            inline_comment_prefixes='#',
            strict=False
        )
        setup.read('setup.ini')
        date_time_setup = setup['date_time']

        date_time_setup['date_time_enabled'] = 'True'

        with open('setup.ini', 'w') as configfile:
            setup.write(configfile)

        try:
            connect.logwriter('*** Date and time set Enable saved ***')
        except Exception as error2:
            from connection_spread import connect
            connect.logwriter(str(error2) + ' Error Code:: 6673')
            list_monitor_log.append(str(error2) + ' Error Code:: 6673')
            time.sleep(3)
            pass
        finally:
            pass

        ui.checkbox_date_time_start.setEnabled(True)
        ui.checkbox_date_time_end.setEnabled(True)
        ui.date_time_start.setEnabled(True)
        ui.date_time_end.setEnabled(True)

    def date_time_disabled_signal():
        ui.checkbox_date_time_start.setEnabled(False)
        ui.checkbox_date_time_end.setEnabled(False)
        ui.date_time_start.setEnabled(False)
        ui.date_time_end.setEnabled(False)

    def amount_and_kind_and_reduce_save_to_setup(
        amount1=None, instrument1=None, kind1=None,
        amount2=None, instrument2=None, kind2=None,
        amount3=None, instrument3=None, kind3=None,
        amount4=None, instrument4=None, kind4=None
    ):
        from connection_spread import connect

        instrument1 = instrument1
        instrument2 = instrument2
        instrument3 = instrument3
        instrument4 = instrument4
        
        amount1 = amount1
        amount2 = amount2
        amount3 = amount3
        amount4 = amount4

        kind1 = kind1
        kind2 = kind2
        kind3 = kind3
        kind4 = kind4
        
        setup = ConfigParser(
            allow_no_value=True,
            inline_comment_prefixes='#',
            strict=False
        )
        setup.read('setup.ini')

        amount_setup = setup['amount']
        
        if instrument1 != 'Unassigned' and amount1 != '' and amount1 != 0 and amount1 != '0':
            amount_setup['instrument1_amount'] = str(amount1)
        else:
            amount_setup['instrument1_amount'] = 'Unassigned'
        if instrument2 != 'Unassigned' and amount2 != '' and amount2 != 0 and amount2 != '0':
            amount_setup['instrument2_amount'] = str(amount2)
        else:
            amount_setup['instrument2_amount'] = 'Unassigned'
        if instrument3 != 'Unassigned' and amount3 != '' and amount3 != 0 and amount3 != '0':
            amount_setup['instrument3_amount'] = str(amount3)
        else:
            amount_setup['instrument3_amount'] = 'Unassigned'
        if instrument4 != 'Unassigned' and amount4 != '' and amount4 != 0 and amount4 != '0':
            amount_setup['instrument4_amount'] = str(amount4)
        else:
            amount_setup['instrument4_amount'] = 'Unassigned'

        kind_setup = setup['kind']

        if instrument1 != 'Unassigned' and kind1 == 'o':
            kind_setup['kind_instrument1'] = 'option'
        elif instrument1 != 'Unassigned' and kind1 == 'f':
            kind_setup['kind_instrument1'] = 'future'
        else:
            kind_setup['kind_instrument1'] = 'Unassigned'
        if instrument2 != 'Unassigned' and kind2 == 'o':
            kind_setup['kind_instrument2'] = 'option'
        elif instrument2 != 'Unassigned' and kind2 == 'f':
            kind_setup['kind_instrument2'] = 'future'
        else:
            kind_setup['kind_instrument2'] = 'Unassigned'
        if instrument3 != 'Unassigned' and kind3 == 'o':
            kind_setup['kind_instrument3'] = 'option'
        elif instrument3 != 'Unassigned' and kind3 == 'f':
            kind_setup['kind_instrument3'] = 'future'
        else:
            kind_setup['kind_instrument3'] = 'Unassigned'
        if instrument4 != 'Unassigned' and kind4 == 'o':
            kind_setup['kind_instrument4'] = 'option'
        elif instrument4 != 'Unassigned' and kind4 == 'f':
            kind_setup['kind_instrument4'] = 'future'
        else:
            kind_setup['kind_instrument4'] = 'Unassigned'

        reduce_only_setup = setup['reduce_only']
        
        if instrument1 != 'Unassigned' and amount1 != '' and amount1 != 0 and amount1 != '0':
            if ui.check_box_reduce_only_1.isChecked() is True:
                reduce_only_setup['instrument1'] = 'True'
            else:
                reduce_only_setup['instrument1'] = 'False'
        else:
            reduce_only_setup['instrument1'] = 'False'
        if instrument2 != 'Unassigned' and amount2 != '' and amount2 != 0 and amount2 != '0':
            if ui.check_box_reduce_only_2.isChecked() is True:
                reduce_only_setup['instrument2'] = 'True'
            else:
                reduce_only_setup['instrument2'] = 'False'
        else:
            reduce_only_setup['instrument2'] = 'False'
        if instrument3 != 'Unassigned' and amount3 != '' and amount3 != 0 and amount3 != '0':
            if ui.check_box_reduce_only_3.isChecked() is True:
                reduce_only_setup['instrument3'] = 'True'
            else:
                reduce_only_setup['instrument3'] = 'False'
        else:
            reduce_only_setup['instrument3'] = 'False'
        if instrument4 != 'Unassigned' and amount4 != '' and amount4 != 0 and amount4 != '0':
            if ui.check_box_reduce_only_4.isChecked() is True:
                reduce_only_setup['instrument4'] = 'True'
            else:
                reduce_only_setup['instrument4'] = 'False'
        else:
            reduce_only_setup['instrument4'] = 'False'
        
        with open('setup.ini', 'w') as configfile:
            setup.write(configfile)
        connect.logwriter('*** Amount Adjusted Saved - ' + 'Instrument ' + str(instrument4) + ' ***')

    def instruments_save():  # Já tem signal nas funções que chama. Só usa UI para receber dados, não enviar.
        from connection_spread import led_color
        date_now_instrument = QtCore.QDate.currentDate()
        if (ui.lineEdit_o_or_f_instrumet1.currentText() == 'o' and (
                ui.lineEdit_buy_or_sell_instrumet1.currentText() == '' or
                ui.lineEdit_amount_instrumet1.text() == '' or
                ui.lineEdit_currency_instrumet1.currentText() == '' or
                ui.lineEdit_strike_instrumet1.text() == '' or
                (ui.checkBox_perpetual_1.isChecked() is False and
                 ui.lineEdit_maturity_instrumet1.date() == date_now_instrument.addDays(-1)) or
                ui.lineEdit_c_or_p_instrumet1.currentText() == ''
        )) or \
                (ui.lineEdit_o_or_f_instrumet1.currentText() == 'f' and (
                        ui.lineEdit_buy_or_sell_instrumet1.currentText() == '' or
                        ui.lineEdit_amount_instrumet1.text() == '' or
                        ui.lineEdit_currency_instrumet1.currentText() == '' or
                        (
                                ui.checkBox_perpetual_1.isChecked() is False and
                                ui.lineEdit_maturity_instrumet1.date() == date_now_instrument.addDays(-1))
                )) or \
                (ui.lineEdit_o_or_f_instrumet2.currentText() == 'o' and (
                        ui.lineEdit_buy_or_sell_instrumet2.currentText() == '' or
                        ui.lineEdit_amount_instrumet2.text() == '' or
                        ui.lineEdit_currency_instrumet2.currentText() == '' or
                        ui.lineEdit_strike_instrumet2.text() == '' or
                        (
                                ui.checkBox_perpetual_2.isChecked() is False and
                                ui.lineEdit_maturity_instrumet2.date() == date_now_instrument.addDays(-1)) or
                        ui.lineEdit_c_or_p_instrumet2.currentText() == ''
                )) or \
                (ui.lineEdit_o_or_f_instrumet2.currentText() == 'f' and (
                        ui.lineEdit_buy_or_sell_instrumet2.currentText() == '' or
                        ui.lineEdit_amount_instrumet2.text() == '' or
                        ui.lineEdit_currency_instrumet2.currentText() == '' or
                        (
                                ui.checkBox_perpetual_2.isChecked() is False and
                                ui.lineEdit_maturity_instrumet2.date() == date_now_instrument.addDays(-1))
                )) or \
                (ui.lineEdit_o_or_f_instrumet3.currentText() == 'o' and (
                        ui.lineEdit_buy_or_sell_instrumet3.currentText() == '' or
                        ui.lineEdit_amount_instrumet3.text() == '' or
                        ui.lineEdit_currency_instrumet3.currentText() == '' or
                        ui.lineEdit_strike_instrumet3.text() == '' or
                        (
                                ui.checkBox_perpetual_3.isChecked() is False and
                                ui.lineEdit_maturity_instrumet3.date() == date_now_instrument.addDays(-1)) or
                        ui.lineEdit_c_or_p_instrumet3.currentText() == ''
                )) or \
                (ui.lineEdit_o_or_f_instrumet3.currentText() == 'f' and (
                        ui.lineEdit_buy_or_sell_instrumet3.currentText() == '' or
                        ui.lineEdit_amount_instrumet3.text() == '' or
                        ui.lineEdit_currency_instrumet3.currentText() == '' or
                        (
                                ui.checkBox_perpetual_3.isChecked() is False and
                                ui.lineEdit_maturity_instrumet3.date() == date_now_instrument.addDays(-1))
                )) or \
                (ui.lineEdit_o_or_f_instrumet4.currentText() == 'o' and (
                        ui.lineEdit_buy_or_sell_instrumet4.currentText() == '' or
                        ui.lineEdit_amount_instrumet4.text() == '' or
                        ui.lineEdit_currency_instrumet4.currentText() == '' or
                        ui.lineEdit_strike_instrumet4.text() == '' or
                        (
                                ui.checkBox_perpetual_4.isChecked() is False and
                                ui.lineEdit_maturity_instrumet4.date() == date_now_instrument.addDays(-1)) or
                        ui.lineEdit_c_or_p_instrumet4.currentText() == ''
                )) or \
                (ui.lineEdit_o_or_f_instrumet4.currentText() == 'f' and (
                        ui.lineEdit_buy_or_sell_instrumet4.currentText() == '' or
                        ui.lineEdit_amount_instrumet4.text() == '' or
                        ui.lineEdit_currency_instrumet4.currentText() == '' or
                        (
                                ui.checkBox_perpetual_4.isChecked() is False and
                                ui.lineEdit_maturity_instrumet4.date() == date_now_instrument.addDays(-1))
                )):
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText('All fields are required - ERROR')
            msg.setWindowTitle('***** ERROR *****')
            msg.exec_()
            pass
        else:
            try:
                if (ui.lineEdit_o_or_f_instrumet1.currentText() == 'o' and (
                        str.replace(ui.lineEdit_amount_instrumet1.text(), ',', '.') == 0 or
                        str.replace(ui.lineEdit_strike_instrumet1.text(), ',', '.') == 0
                )) or \
                        (ui.lineEdit_o_or_f_instrumet1.currentText() == 'f' and (
                                str.replace(ui.lineEdit_amount_instrumet1.text(), ',', '.') == 0
                        )) or \
                        (ui.lineEdit_o_or_f_instrumet2.currentText() == 'o' and (
                                str.replace(ui.lineEdit_amount_instrumet2.text(), ',', '.') == 0 or
                                str.replace(ui.lineEdit_strike_instrumet2.text(), ',', '.') == 0
                        )) or \
                        (ui.lineEdit_o_or_f_instrumet2.currentText() == 'f' and (
                                str.replace(ui.lineEdit_amount_instrumet2.text(), ',', '.') == 0
                        )) or \
                        (ui.lineEdit_o_or_f_instrumet3.currentText() == 'o' and (
                                str.replace(ui.lineEdit_amount_instrumet3.text(), ',', '.') == 0 or
                                str.replace(ui.lineEdit_strike_instrumet3.text(), ',', '.') == 0
                        )) or \
                        (ui.lineEdit_o_or_f_instrumet3.currentText() == 'f' and (
                                str.replace(ui.lineEdit_amount_instrumet3.text(), ',', '.') == 0
                        )) or \
                        (ui.lineEdit_o_or_f_instrumet4.currentText() == 'o' and (
                                str.replace(ui.lineEdit_amount_instrumet4.text(), ',', '.') == 0 or
                                str.replace(ui.lineEdit_strike_instrumet4.text(), ',', '.') == 0
                        )) or \
                        (ui.lineEdit_o_or_f_instrumet4.currentText() == 'f' and (
                                str.replace(ui.lineEdit_amount_instrumet4.text(), ',', '.') == 0
                        )):
                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Information)
                    msg.setText('Zero is NOT accept')
                    msg.setWindowTitle('***** ERROR *****')
                    msg.exec_()
                    pass
                else:
                    if (ui.lineEdit_currency_instrumet1.currentText() == 'BTC' and (
                            ui.lineEdit_currency_instrumet2.currentText() == 'ETH' or
                            ui.lineEdit_currency_instrumet3.currentText() == 'ETH' or
                            ui.lineEdit_currency_instrumet4.currentText() == 'ETH'
                    )) or \
                            (ui.lineEdit_currency_instrumet1.currentText() == 'ETH' and (
                                    ui.lineEdit_currency_instrumet2.currentText() == 'BTC' or
                                    ui.lineEdit_currency_instrumet3.currentText() == 'BTC' or
                                    ui.lineEdit_currency_instrumet4.currentText() == 'BTC'
                            )):

                        msg = QtWidgets.QMessageBox()
                        msg.setIcon(QtWidgets.QMessageBox.Information)
                        msg.setText('Instruments currency must be the same')
                        msg.setWindowTitle('***** ERROR *****')
                        msg.exec_()
                        pass
                    elif ui.lineEdit_o_or_f_instrumet1.currentText() == 'o' and (int(float(
                            str.replace(str(ui.lineEdit_amount_instrumet1.text()), ',', '.')) * 10) != float(
                            str.replace(str(ui.lineEdit_amount_instrumet1.text()), ',', '.')) * 10):
                        msg = QtWidgets.QMessageBox()
                        msg.setIcon(QtWidgets.QMessageBox.Information)
                        msg.setText('Instrument 1 Amount must be \n0.1 multiple')
                        msg.setWindowTitle('***** ERROR *****')
                        msg.exec_()
                        pass
                    elif ui.lineEdit_o_or_f_instrumet1.currentText() == 'f' and (float(
                            str.replace(str(ui.lineEdit_amount_instrumet1.text()), ',', '.')) % 10 != 0):
                        msg = QtWidgets.QMessageBox()
                        msg.setIcon(QtWidgets.QMessageBox.Information)
                        msg.setText('Instrument 1 Amount must be \n10 multiple')
                        msg.setWindowTitle('***** ERROR *****')
                        msg.exec_()
                        pass
                    elif ui.lineEdit_o_or_f_instrumet2.currentText() == 'o' and (int(float(
                            str.replace(str(ui.lineEdit_amount_instrumet1.text()), ',', '.')) * 10) != float(
                            str.replace(str(ui.lineEdit_amount_instrumet1.text()), ',', '.')) * 10):
                        msg = QtWidgets.QMessageBox()
                        msg.setIcon(QtWidgets.QMessageBox.Information)
                        msg.setText('Instrument 2 Amount must be \n0.1 multiple')
                        msg.setWindowTitle('***** ERROR *****')
                        msg.exec_()
                        pass
                    elif ui.lineEdit_o_or_f_instrumet2.currentText() == 'f' and (float(
                            str.replace(str(ui.lineEdit_amount_instrumet2.text()), ',', '.')) % 10 != 0):
                        msg = QtWidgets.QMessageBox()
                        msg.setIcon(QtWidgets.QMessageBox.Information)
                        msg.setText('Instrument 2 Amount must be \n10 multiple')
                        msg.setWindowTitle('***** ERROR *****')
                        msg.exec_()
                        pass
                    elif ui.lineEdit_o_or_f_instrumet3.currentText() == 'o' and (int(float(
                            str.replace(str(ui.lineEdit_amount_instrumet1.text()), ',', '.')) * 10) != float(
                            str.replace(str(ui.lineEdit_amount_instrumet1.text()), ',', '.')) * 10):
                        msg = QtWidgets.QMessageBox()
                        msg.setIcon(QtWidgets.QMessageBox.Information)
                        msg.setText('Instrument 3 Amount must be \n0.1 multiple')
                        msg.setWindowTitle('***** ERROR *****')
                        msg.exec_()
                        pass
                    elif ui.lineEdit_o_or_f_instrumet3.currentText() == 'f' and (float(
                            str.replace(str(ui.lineEdit_amount_instrumet3.text()), ',', '.')) % 10 != 0):
                        msg = QtWidgets.QMessageBox()
                        msg.setIcon(QtWidgets.QMessageBox.Information)
                        msg.setText('Instrument 3 Amount must be \n10 multiple')
                        msg.setWindowTitle('***** ERROR *****')
                        msg.exec_()
                        pass
                    elif ui.lineEdit_o_or_f_instrumet4.currentText() == 'o' and (int(float(
                            str.replace(str(ui.lineEdit_amount_instrumet1.text()), ',', '.')) * 10) != float(
                        str.replace(str(
                            ui.lineEdit_amount_instrumet1.text()), ',', '.')) * 10):
                        msg = QtWidgets.QMessageBox()
                        msg.setIcon(QtWidgets.QMessageBox.Information)
                        msg.setText('Instrument 4 Amount must be \n0.1 multiple')
                        msg.setWindowTitle('***** ERROR *****')
                        msg.exec_()
                        pass
                    elif ui.lineEdit_o_or_f_instrumet4.currentText() == 'f' and (float(
                            str.replace(str(ui.lineEdit_amount_instrumet4.text()), ',', '.')) % 10 != 0):
                        msg = QtWidgets.QMessageBox()
                        msg.setIcon(QtWidgets.QMessageBox.Information)
                        msg.setText('Instrument 4 Amount must be \n10 multiple')
                        msg.setWindowTitle('***** ERROR *****')
                        msg.exec_()
                        pass
                    else:
                        if ui.lineEdit_o_or_f_instrumet1.currentText() == '':
                            instrument1_to_save = 'Instrument 1: Unassigned'
                            instrument_name1_before_save = 'Unassigned'
                        elif ui.lineEdit_o_or_f_instrumet1.currentText() == 'o':
                            instrument1_to_save = str(
                                'Instrument 1: option ' +
                                str(ui.lineEdit_buy_or_sell_instrumet1.currentText()) + ' ' +
                                str.replace(str(ui.lineEdit_amount_instrumet1.text()), ',', '.') + ' ' +
                                str.upper(ui.lineEdit_currency_instrumet1.currentText()) + '-' +
                                str.upper(ui.lineEdit_maturity_instrumet1.text()) + '-' +
                                str(ui.lineEdit_strike_instrumet1.text()) + '-' +
                                str.upper(ui.lineEdit_c_or_p_instrumet1.currentText())
                            )
                            instrument_name1_before_save = str.upper(
                                ui.lineEdit_currency_instrumet1.currentText()) + '-' + \
                                str.upper(ui.lineEdit_maturity_instrumet1.text()) + '-' + \
                                str(ui.lineEdit_strike_instrumet1.text()) + '-' + \
                                str.upper(ui.lineEdit_c_or_p_instrumet1.currentText())
                        elif ui.lineEdit_o_or_f_instrumet1.currentText() == 'f' and \
                                ui.checkBox_perpetual_1.isChecked() is False:
                            instrument1_to_save = str(
                                'Instrument 1: future ' +
                                str(ui.lineEdit_buy_or_sell_instrumet1.currentText()) + ' ' +
                                str.replace(str(ui.lineEdit_amount_instrumet1.text()), ',', '.') + ' ' +
                                str.upper(ui.lineEdit_currency_instrumet1.currentText()) + '-' +
                                str.upper(ui.lineEdit_maturity_instrumet1.text())
                            )
                            instrument_name1_before_save = str.upper(ui.lineEdit_currency_instrumet1.currentText()) + \
                                '-' + str.upper(ui.lineEdit_maturity_instrumet1.text())
                        elif ui.lineEdit_o_or_f_instrumet1.currentText() == 'f' and \
                                ui.checkBox_perpetual_1.isChecked() is True:
                            instrument1_to_save = str(
                                'Instrument 1: future ' +
                                str(ui.lineEdit_buy_or_sell_instrumet1.currentText()) + ' ' +
                                str.replace(str(ui.lineEdit_amount_instrumet1.text()), ',', '.') + ' ' +
                                str.upper(ui.lineEdit_currency_instrumet1.currentText()) +
                                '-PERPETUAL'
                            )
                            instrument_name1_before_save = \
                                str.upper(ui.lineEdit_currency_instrumet1.currentText()) + '-PERPETUAL'
                        else:
                            instrument1_to_save = 'Instrument 1: Unassigned'
                            instrument_name1_before_save = 'Unassigned'

                        if ui.lineEdit_o_or_f_instrumet2.currentText() == '':
                            instrument2_to_save = 'Instrument 2: Unassigned'
                            instrument_name2_before_save = 'Unassigned'
                        elif ui.lineEdit_o_or_f_instrumet2.currentText() == 'o':
                            instrument2_to_save = str(
                                'Instrument 2: option ' +
                                str(ui.lineEdit_buy_or_sell_instrumet2.currentText()) + ' ' +
                                str.replace(str(ui.lineEdit_amount_instrumet2.text()), ',', '.') + ' ' +
                                str.upper(ui.lineEdit_currency_instrumet2.currentText()) + '-' +
                                str.upper(ui.lineEdit_maturity_instrumet2.text()) + '-' +
                                str(ui.lineEdit_strike_instrumet2.text()) + '-' +
                                str.upper(ui.lineEdit_c_or_p_instrumet2.currentText())
                            )
                            instrument_name2_before_save = str.upper(
                                ui.lineEdit_currency_instrumet2.currentText()) + '-' + \
                                str.upper(ui.lineEdit_maturity_instrumet2.text()) + '-' + \
                                str(ui.lineEdit_strike_instrumet2.text()) + '-' + \
                                str.upper(ui.lineEdit_c_or_p_instrumet2.currentText())
                        elif ui.lineEdit_o_or_f_instrumet2.currentText() == 'f' and \
                                ui.checkBox_perpetual_2.isChecked() is False:
                            instrument2_to_save = str(
                                'Instrument 2: future ' +
                                str(ui.lineEdit_buy_or_sell_instrumet2.currentText()) + ' ' +
                                str.replace(str(ui.lineEdit_amount_instrumet2.text()), ',', '.') + ' ' +
                                str.upper(ui.lineEdit_currency_instrumet2.currentText()) + '-' +
                                str.upper(ui.lineEdit_maturity_instrumet2.text())
                            )
                            instrument_name2_before_save = str.upper(ui.lineEdit_currency_instrumet2.currentText()) + \
                                '-' + str.upper(ui.lineEdit_maturity_instrumet2.text())
                        elif ui.lineEdit_o_or_f_instrumet2.currentText() == 'f' and \
                                ui.checkBox_perpetual_2.isChecked() is True:
                            instrument2_to_save = str(
                                'Instrument 2: future ' +
                                str(ui.lineEdit_buy_or_sell_instrumet2.currentText()) + ' ' +
                                str.replace(str(ui.lineEdit_amount_instrumet2.text()), ',', '.') + ' ' +
                                str.upper(ui.lineEdit_currency_instrumet2.currentText()) +
                                '-PERPETUAL'
                            )
                            instrument_name2_before_save = \
                                str.upper(ui.lineEdit_currency_instrumet2.currentText()) + '-PERPETUAL'
                        else:
                            instrument2_to_save = 'Instrument 2: Unassigned'
                            instrument_name2_before_save = 'Unassigned'

                        if ui.lineEdit_o_or_f_instrumet3.currentText() == '':
                            instrument3_to_save = 'Instrument 3: Unassigned'
                            instrument_name3_before_save = 'Unassigned'
                        elif ui.lineEdit_o_or_f_instrumet3.currentText() == 'o':
                            instrument3_to_save = str(
                                'Instrument 3: option ' +
                                str(ui.lineEdit_buy_or_sell_instrumet3.currentText()) + ' ' +
                                str.replace(str(ui.lineEdit_amount_instrumet3.text()), ',', '.') + ' ' +
                                str.upper(ui.lineEdit_currency_instrumet3.currentText()) + '-' +
                                str.upper(ui.lineEdit_maturity_instrumet3.text()) + '-' +
                                str(ui.lineEdit_strike_instrumet3.text()) + '-' +
                                str.upper(ui.lineEdit_c_or_p_instrumet3.currentText())
                            )
                            instrument_name3_before_save = str.upper(
                                ui.lineEdit_currency_instrumet3.currentText()) + '-' + \
                                str.upper(ui.lineEdit_maturity_instrumet3.text()) + '-' + \
                                str(ui.lineEdit_strike_instrumet3.text()) + '-' + \
                                str.upper(ui.lineEdit_c_or_p_instrumet3.currentText())
                        elif ui.lineEdit_o_or_f_instrumet3.currentText() == 'f' and \
                                ui.checkBox_perpetual_3.isChecked() is False:
                            instrument3_to_save = str(
                                'Instrument 3: future ' +
                                str(ui.lineEdit_buy_or_sell_instrumet3.currentText()) + ' ' +
                                str.replace(str(ui.lineEdit_amount_instrumet3.text()), ',', '.') + ' ' +
                                str.upper(ui.lineEdit_currency_instrumet3.currentText()) + '-' +
                                str.upper(ui.lineEdit_maturity_instrumet3.text())
                            )
                            instrument_name3_before_save = str.upper(ui.lineEdit_currency_instrumet3.currentText()) + \
                                '-' + str.upper(ui.lineEdit_maturity_instrumet3.text())
                        elif ui.lineEdit_o_or_f_instrumet3.currentText() == 'f' and \
                                ui.checkBox_perpetual_3.isChecked() is True:
                            instrument3_to_save = str(
                                'Instrument 3: future ' +
                                str(ui.lineEdit_buy_or_sell_instrumet3.currentText()) + ' ' +
                                str.replace(str(ui.lineEdit_amount_instrumet3.text()), ',', '.') + ' ' +
                                str.upper(ui.lineEdit_currency_instrumet3.currentText()) +
                                '-PERPETUAL'
                            )
                            instrument_name3_before_save = \
                                str.upper(ui.lineEdit_currency_instrumet3.currentText()) + '-PERPETUAL'
                        else:
                            instrument3_to_save = 'Instrument 3: Unassigned'
                            instrument_name3_before_save = 'Unassigned'
                        if ui.lineEdit_o_or_f_instrumet4.currentText() == '':
                            instrument4_to_save = 'Instrument 4: Unassigned'
                            instrument_name4_before_save = 'Unassigned'
                        elif ui.lineEdit_o_or_f_instrumet4.currentText() == 'o':
                            instrument4_to_save = str(
                                'Instrument 4: option ' +
                                str(ui.lineEdit_buy_or_sell_instrumet4.currentText()) + ' ' +
                                str.replace(str(ui.lineEdit_amount_instrumet4.text()), ',', '.') + ' ' +
                                str.upper(ui.lineEdit_currency_instrumet4.currentText()) + '-' +
                                str.upper(ui.lineEdit_maturity_instrumet4.text()) + '-' +
                                str(ui.lineEdit_strike_instrumet4.text()) + '-' +
                                str.upper(ui.lineEdit_c_or_p_instrumet4.currentText())
                            )
                            instrument_name4_before_save = str.upper(
                                ui.lineEdit_currency_instrumet4.currentText()) + '-' + \
                                str.upper(ui.lineEdit_maturity_instrumet4.text()) + '-' + \
                                str(ui.lineEdit_strike_instrumet4.text()) + '-' + \
                                str.upper(ui.lineEdit_c_or_p_instrumet4.currentText())
                        elif ui.lineEdit_o_or_f_instrumet4.currentText() == 'f' and \
                                ui.checkBox_perpetual_4.isChecked() is False:
                            instrument4_to_save = str(
                                'Instrument 4: future ' +
                                str(ui.lineEdit_buy_or_sell_instrumet4.currentText()) + ' ' +
                                str.replace(str(ui.lineEdit_amount_instrumet4.text()), ',', '.') + ' ' +
                                str.upper(ui.lineEdit_currency_instrumet4.currentText()) + '-' +
                                str.upper(ui.lineEdit_maturity_instrumet4.text())
                            )
                            instrument_name4_before_save = str.upper(ui.lineEdit_currency_instrumet4.currentText()) + \
                                '-' + str.upper(ui.lineEdit_maturity_instrumet4.text())
                        elif ui.lineEdit_o_or_f_instrumet4.currentText() == 'f' and \
                                ui.checkBox_perpetual_4.isChecked() is True:
                            instrument4_to_save = str(
                                'Instrument 4: future ' +
                                str(ui.lineEdit_buy_or_sell_instrumet4.currentText()) + ' ' +
                                str.replace(str(ui.lineEdit_amount_instrumet4.text()), ',', '.') + ' ' +
                                str.upper(ui.lineEdit_currency_instrumet4.currentText()) +
                                '-PERPETUAL'
                            )
                            instrument_name4_before_save = \
                                str.upper(ui.lineEdit_currency_instrumet4.currentText()) + '-PERPETUAL'
                        else:
                            instrument4_to_save = 'Instrument 4: Unassigned'
                            instrument_name4_before_save = 'Unassigned'

                        if led_color() == 'red':
                            msg = QtWidgets.QMessageBox()
                            msg.setIcon(QtWidgets.QMessageBox.Information)
                            msg.setText('Connection Offline\nInstrument don´t updated')
                            msg.setWindowTitle('***** ERROR *****')
                            msg.exec_()
                        else:
                            if Instruments().instrument_check_available_before_save(
                                    instrument_name1=instrument_name1_before_save,
                                    instrument_name2=instrument_name2_before_save,
                                    instrument_name3=instrument_name3_before_save,
                                    instrument_name4=instrument_name4_before_save) \
                                    == 'instrument_check_available_before_save_OK':
                                with open('instruments_spread.txt', 'w') as instruments_save_file:
                                    instruments_save_file.write(str(instrument1_to_save) + '\n' +
                                                                str(instrument2_to_save) + '\n' +
                                                                str(instrument3_to_save) + '\n' +
                                                                str(instrument4_to_save)
                                                                )
                                instruments_saved_print_and_check_available()  # Não tem UI
                                Config().position_before_trade_save()  # não tem 'ui' na função.
                                textedit_instruments_saved_settext_signal_str = str(
                                    InstrumentsSaved().instruments_check())
                                sinal.textedit_instruments_saved_settext_signal.emit(
                                    textedit_instruments_saved_settext_signal_str)
                                amount_and_kind_and_reduce_save_to_setup(
                                    amount1=str.replace(str(
                                        ui.lineEdit_amount_instrumet1.text()), ',', '.'), instrument1=str(
                                        instrument1_to_save), kind1=ui.lineEdit_o_or_f_instrumet1.currentText(),
                                    amount2=str.replace(str(
                                        ui.lineEdit_amount_instrumet2.text()), ',', '.'), instrument2=str(
                                        instrument2_to_save), kind2=ui.lineEdit_o_or_f_instrumet2.currentText(),
                                    amount3=str.replace(str(
                                        ui.lineEdit_amount_instrumet3.text()), ',', '.'), instrument3=str(
                                        instrument3_to_save), kind3=ui.lineEdit_o_or_f_instrumet3.currentText(),
                                    amount4=str.replace(str(
                                        ui.lineEdit_amount_instrumet4.text()), ',', '.'), instrument4=str(
                                        instrument4_to_save), kind4=ui.lineEdit_o_or_f_instrumet4.currentText()
                                )
                                Config().reduce_only_saved()
                                Instruments().amount_adjusted_save()
                                Instruments().adjust_rate_trade_by_reduce_only_save()
                                print_greeks_by_instrument()  # a função 'print_greeks_by_instrument' já tem sinal nela.
                                sinal.textedit_balance_settext_signal.emit(
                                    str(ConfigSaved().position_saved()))  # Sbustitui o abaixo
                                position_preview_to_gui()  # Já tem signal na função.
                                sinal.position_now_signal_2.emit()
                                sinal.pushButton_request_options_structure_cost_signal.emit()
                                # the pushButton_request_options_structure_cost_signal.emit() call Quote().quote_new()
                                strategy_name_save()
                                sinal.date_time_enabled_signal.emit()

                            else:
                                msg = QtWidgets.QMessageBox()
                                msg.setIcon(QtWidgets.QMessageBox.Information)
                                msg.setText('Instrument don´t updated')
                                msg.setWindowTitle('***** ERROR *****')
                                msg.exec_()
                                pass
            except ValueError:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Only Numbers are accepted')
                msg.setWindowTitle('***** ERROR *****')
                msg.exec_()
                pass

    def position_preview_to_gui():
        max_position_instrument1_for_gui = Config().max_position_from_position_saved_and_instrument_amount(
            instrument_number=1)
        max_position_instrument2_for_gui = Config().max_position_from_position_saved_and_instrument_amount(
            instrument_number=2)
        max_position_instrument3_for_gui = Config().max_position_from_position_saved_and_instrument_amount(
            instrument_number=3)
        max_position_instrument4_for_gui = Config().max_position_from_position_saved_and_instrument_amount(
            instrument_number=4)

        textedit_balance_after_signal_dict = dict()
        textedit_balance_after_signal_dict.clear()

        textedit_balance_after_signal_dict['Instrument 1'] = str(max_position_instrument1_for_gui)
        textedit_balance_after_signal_dict['Instrument 2'] = str(max_position_instrument2_for_gui)
        textedit_balance_after_signal_dict['Instrument 3'] = str(max_position_instrument3_for_gui)
        textedit_balance_after_signal_dict['Instrument 4'] = str(max_position_instrument4_for_gui)

        sinal.textedit_balance_after_signal.emit(textedit_balance_after_signal_dict)

        if 'ERROR' in str(max_position_instrument1_for_gui):
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText('Instrument 1 Syntax ERROR')
            msg.setWindowTitle('***** ERROR *****')
            msg.exec_()
        else:
            pass
        if 'ERROR' in str(max_position_instrument2_for_gui):
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText('Instrument 2 Syntax ERROR')
            msg.setWindowTitle('***** ERROR *****')
            msg.exec_()
        else:
            pass
        if 'ERROR' in str(max_position_instrument3_for_gui):
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText('Instrument 3 Syntax ERROR')
            msg.setWindowTitle('***** ERROR *****')
            msg.exec_()
        else:
            pass
        if 'ERROR' in str(max_position_instrument4_for_gui):
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText('Instrument 4 Syntax ERROR')
            msg.setWindowTitle('***** ERROR *****')
            msg.exec_()
        else:
            pass

    def print_greeks_by_instrument():
        import decimal

        instrument1_mark_greek_cost = Instruments().greeks_by_instruments(instrument_number=1)
        instrument1_vega = instrument1_mark_greek_cost['vega']
        instrument1_theta = instrument1_mark_greek_cost['theta']
        instrument1_rho = instrument1_mark_greek_cost['rho']
        instrument1_gamma = instrument1_mark_greek_cost['gamma']
        instrument1_delta = instrument1_mark_greek_cost['delta']

        instrument2_mark_greek_cost = Instruments().greeks_by_instruments(instrument_number=2)
        instrument2_vega = instrument2_mark_greek_cost['vega']
        instrument2_theta = instrument2_mark_greek_cost['theta']
        instrument2_rho = instrument2_mark_greek_cost['rho']
        instrument2_gamma = instrument2_mark_greek_cost['gamma']
        instrument2_delta = instrument2_mark_greek_cost['delta']

        instrument3_mark_greek_cost = Instruments().greeks_by_instruments(instrument_number=3)
        instrument3_vega = instrument3_mark_greek_cost['vega']
        instrument3_theta = instrument3_mark_greek_cost['theta']
        instrument3_rho = instrument3_mark_greek_cost['rho']
        instrument3_gamma = instrument3_mark_greek_cost['gamma']
        instrument3_delta = instrument3_mark_greek_cost['delta']

        instrument4_mark_greek_cost = Instruments().greeks_by_instruments(instrument_number=4)
        instrument4_vega = instrument4_mark_greek_cost['vega']
        instrument4_theta = instrument4_mark_greek_cost['theta']
        instrument4_rho = instrument4_mark_greek_cost['rho']
        instrument4_gamma = instrument4_mark_greek_cost['gamma']
        instrument4_delta = instrument4_mark_greek_cost['delta']

        idg1 = InstrumentsSaved().instrument_direction_construction_from_instrument_file(
            instrument_number=1)
        if idg1 == 'Unassigned':
            instrument1_amount_greeks = 0
        else:
            if idg1 == 'buy':
                instrument1_amount_greeks = abs(float(
                    InstrumentsSaved().instrument_amount_saved(instrument_number=1)))
            elif idg1 == 'sell':
                instrument1_amount_greeks = abs(float(
                    InstrumentsSaved().instrument_amount_saved(
                        instrument_number=1))) * -1
            else:
                instrument1_amount_greeks = 0

        idg2 = InstrumentsSaved().instrument_direction_construction_from_instrument_file(instrument_number=2)
        if idg2 == 'Unassigned':
            instrument2_amount_greeks = 0
        else:
            if idg2 == 'buy':
                instrument2_amount_greeks = abs(float(
                    InstrumentsSaved().instrument_amount_saved(instrument_number=2)))
            elif idg2 == 'sell':
                instrument2_amount_greeks = abs(float(
                    InstrumentsSaved().instrument_amount_saved(
                        instrument_number=2))) * -1
            else:
                instrument2_amount_greeks = 0

        idg3 = InstrumentsSaved().instrument_direction_construction_from_instrument_file(instrument_number=3)
        if idg3 == 'Unassigned':
            instrument3_amount_greeks = 0
        else:
            if idg3 == 'buy':
                instrument3_amount_greeks = abs(float(
                    InstrumentsSaved().instrument_amount_saved(instrument_number=3)))
            elif idg3 == 'sell':
                instrument3_amount_greeks = abs(float(
                    InstrumentsSaved().instrument_amount_saved(
                        instrument_number=3))) * -1
            else:
                instrument3_amount_greeks = 0

        idg4 = InstrumentsSaved().instrument_direction_construction_from_instrument_file(instrument_number=4)
        if idg4 == 'Unassigned':
            instrument4_amount_greeks = 0
        else:
            if idg4 == 'buy':
                instrument4_amount_greeks = abs(float(
                    InstrumentsSaved().instrument_amount_saved(instrument_number=4)))
            elif idg4 == 'sell':
                instrument4_amount_greeks = abs(float(
                    InstrumentsSaved().instrument_amount_saved(
                        instrument_number=4))) * -1
            else:
                instrument4_amount_greeks = 0

        instrument1_vega_total = float(instrument1_vega) * float(instrument1_amount_greeks)
        instrument2_vega_total = float(instrument2_vega) * float(instrument2_amount_greeks)
        instrument3_vega_total = float(instrument3_vega) * float(instrument3_amount_greeks)
        instrument4_vega_total = float(instrument4_vega) * float(instrument4_amount_greeks)

        instrument1_theta_total = float(instrument1_theta) * float(instrument1_amount_greeks)
        instrument2_theta_total = float(instrument2_theta) * float(instrument2_amount_greeks)
        instrument3_theta_total = float(instrument3_theta) * float(instrument3_amount_greeks)
        instrument4_theta_total = float(instrument4_theta) * float(instrument4_amount_greeks)

        instrument1_rho_total = float(instrument1_rho) * float(instrument1_amount_greeks)
        instrument2_rho_total = float(instrument2_rho) * float(instrument2_amount_greeks)
        instrument3_rho_total = float(instrument3_rho) * float(instrument3_amount_greeks)
        instrument4_rho_total = float(instrument4_rho) * float(instrument4_amount_greeks)

        instrument1_gamma_total = round(decimal.Context().create_decimal_from_float(
            instrument1_gamma * instrument1_amount_greeks), 5)
        instrument2_gamma_total = round(decimal.Context().create_decimal_from_float(
            instrument2_gamma * instrument2_amount_greeks), 5)
        instrument3_gamma_total = round(decimal.Context().create_decimal_from_float(
            instrument3_gamma * instrument3_amount_greeks), 5)
        instrument4_gamma_total = round(decimal.Context().create_decimal_from_float(
            instrument4_gamma * instrument4_amount_greeks), 5)

        instrument1_delta_total = float(instrument1_delta) * float(instrument1_amount_greeks)
        instrument2_delta_total = float(instrument2_delta) * float(instrument2_amount_greeks)
        instrument3_delta_total = float(instrument3_delta) * float(instrument3_amount_greeks)
        instrument4_delta_total = float(instrument4_delta) * float(instrument4_amount_greeks)

        print_greeks_by_instrument_dict = dict()

        print_greeks_by_instrument_dict['lineEdit_29'] = round(instrument1_delta_total, 6)
        print_greeks_by_instrument_dict['lineEdit_47'] = round(instrument2_delta_total, 6)
        print_greeks_by_instrument_dict['lineEdit_48'] = round(instrument3_delta_total, 6)
        print_greeks_by_instrument_dict['lineEdit_49'] = round(instrument4_delta_total, 6)

        print_greeks_by_instrument_dict['lineEdit_31'] = round(instrument1_theta_total, 6)
        print_greeks_by_instrument_dict['lineEdit_37'] = round(instrument2_theta_total, 6)
        print_greeks_by_instrument_dict['lineEdit_36'] = round(instrument3_theta_total, 6)
        print_greeks_by_instrument_dict['lineEdit_35'] = round(instrument4_theta_total, 6)

        print_greeks_by_instrument_dict['lineEdit_30'] = round(instrument1_gamma_total, 6)
        print_greeks_by_instrument_dict['lineEdit_44'] = round(instrument2_gamma_total, 6)
        print_greeks_by_instrument_dict['lineEdit_45'] = round(instrument3_gamma_total, 6)
        print_greeks_by_instrument_dict['lineEdit_46'] = round(instrument4_gamma_total, 6)

        print_greeks_by_instrument_dict['lineEdit_32'] = round(instrument1_vega_total, 6)
        print_greeks_by_instrument_dict['lineEdit_41'] = round(instrument2_vega_total, 6)
        print_greeks_by_instrument_dict['lineEdit_42'] = round(instrument3_vega_total, 6)
        print_greeks_by_instrument_dict['lineEdit_43'] = round(instrument4_vega_total, 6)

        print_greeks_by_instrument_dict['lineEdit_33'] = round(instrument1_rho_total, 6)
        print_greeks_by_instrument_dict['lineEdit_38'] = round(instrument2_rho_total, 6)
        print_greeks_by_instrument_dict['lineEdit_39'] = round(instrument3_rho_total, 6)
        print_greeks_by_instrument_dict['lineEdit_40'] = round(instrument4_rho_total, 6)

        sinal.print_greeks_by_instrument_signal.emit(print_greeks_by_instrument_dict)

    def instruments_saved_print_and_check_available_when_open_app_thread_def():
        instruments_saved_print_and_check_available_when_open_app_thread = threading.Thread(
            daemon=True, target=instruments_saved_print_and_check_available_when_open_app)
        instruments_saved_print_and_check_available_when_open_app_thread.start()

    def strategy_name_update_signal():
        _translate = QtCore.QCoreApplication.translate

        setup = ConfigParser(
            allow_no_value=True,
            strict=False
        )
        setup.read('setup.ini')
        default_setup = dict(setup['DEFAULT'])
        name = default_setup['name']
        version = default_setup['version']
        strategy_name = default_setup['strategy_name']
        main_windows_title = str(
            name + ' ' + version + '                    *** Strategy Name: ' + strategy_name + ' ***')
        MainWindow.setWindowTitle(_translate("MainWindow", main_windows_title))

    def strategy_name_save():
        from connection_spread import connect
        strategy_name = str(ui.line_edit_strategy_name.text())
        setup = ConfigParser(
            allow_no_value=True,
            inline_comment_prefixes='#',
            strict=False
        )
        setup.read('setup.ini')
        default_setup = setup['DEFAULT']
        default_setup['strategy_name'] = strategy_name

        with open('setup.ini', 'w') as configfile:
            setup.write(configfile)
        connect.logwriter('***  Strategy name saved ***')
        sinal.strategy_name_update_signal.emit()

    def reduce_only_signal(info):
        true_or_false_reduce_only1 = info['true_or_false_reduce_only1']
        true_or_false_reduce_only2 = info['true_or_false_reduce_only2']
        true_or_false_reduce_only3 = info['true_or_false_reduce_only3']
        true_or_false_reduce_only4 = info['true_or_false_reduce_only4']

        ui.check_box_reduce_only_1.setChecked(true_or_false_reduce_only1)
        ui.check_box_reduce_only_2.setChecked(true_or_false_reduce_only2)
        ui.check_box_reduce_only_3.setChecked(true_or_false_reduce_only3)
        ui.check_box_reduce_only_4.setChecked(true_or_false_reduce_only4)

    def position_now():
        from connection_spread import connect, led_color
        from lists import list_monitor_log

        instrument1_name = InstrumentsSaved().instrument_name_construction_from_file(instrument_number=1)
        instrument2_name = InstrumentsSaved().instrument_name_construction_from_file(instrument_number=2)
        instrument3_name = InstrumentsSaved().instrument_name_construction_from_file(instrument_number=3)
        instrument4_name = InstrumentsSaved().instrument_name_construction_from_file(instrument_number=4)

        a = instrument1_name
        b = instrument2_name
        c = instrument3_name
        d = instrument4_name

        if led_color() == 'red':
            # sinal.msg_box_for_position_now_signal.emit()
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText('Connection Offline\nCurrent Positions don´t updated')
            msg.setWindowTitle('***** ERROR *****')
            msg.exec_()
            pass
        else:
            try:
                if a != 'Unassigned':
                    a1 = connect.get_position_size(instrument_name=a)
                else:
                    a1 = 'Unassigned'

                if b != 'Unassigned':
                    b1 = connect.get_position_size(instrument_name=b)
                else:
                    b1 = 'Unassigned'

                if c != 'Unassigned':
                    c1 = connect.get_position_size(instrument_name=c)
                else:
                    c1 = 'Unassigned'

                if d != 'Unassigned':
                    d1 = connect.get_position_size(instrument_name=d)
                else:
                    d1 = 'Unassigned'

                info1 = dict()
                info1['Instrument 1'] = str(a1)
                info1['Instrument 2'] = str(b1)
                info1['Instrument 3'] = str(c1)
                info1['Instrument 4'] = str(d1)

                info = info1

                # sinal.position_now_signal.emit(info)

                a1 = str(info['Instrument 1'])
                b1 = str(info['Instrument 2'])
                c1 = str(info['Instrument 3'])
                d1 = str(info['Instrument 4'])
                ui.textEdit_balance_2.clear()
                ui.textEdit_balance_2.setText('Instrument 1: ' + str(a1) + '\n' +
                                              'Instrument 2: ' + str(b1) + '\n' +
                                              'Instrument 3: ' + str(c1) + '\n' +
                                              'Instrument 4: ' + str(d1))

                info.clear()
                info1.clear()

            except Exception as er:
                connect.logwriter(str(er) + ' Error Code:: 6778')
                list_monitor_log.append(str(er) + ' Error Code:: 6779')
                ui.textEdit_balance_2.clear()
                ui.textEdit_balance_2.setText(str(er) + ' Error Code:: 6781')
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Current Positions don´t checked')
                msg.setWindowTitle('***** ERROR *****')
                msg.exec_()
                pass
            finally:
                pass

    def pushbutton_request_options_structure_cost_signal():
        Quote().quote_new()

    ui.textEdit_targets_saved_2.setHidden(True)
    ui.textEdit_targets_saved_3.setHidden(True)
    ui.textEdit_targets_saved_4.setHidden(True)
    ui.lineEdit_o_or_f_instrumet1.currentTextChanged.connect(enable_disable_strike_and_c_or_p_and_maturity)
    ui.lineEdit_o_or_f_instrumet2.currentTextChanged.connect(enable_disable_strike_and_c_or_p_and_maturity)
    ui.lineEdit_o_or_f_instrumet3.currentTextChanged.connect(enable_disable_strike_and_c_or_p_and_maturity)
    ui.lineEdit_o_or_f_instrumet4.currentTextChanged.connect(enable_disable_strike_and_c_or_p_and_maturity)
    ui.checkBox_perpetual_1.stateChanged.connect(enable_disable_strike_and_c_or_p_and_maturity)
    ui.checkBox_perpetual_2.stateChanged.connect(enable_disable_strike_and_c_or_p_and_maturity)
    ui.checkBox_perpetual_3.stateChanged.connect(enable_disable_strike_and_c_or_p_and_maturity)
    ui.checkBox_perpetual_4.stateChanged.connect(enable_disable_strike_and_c_or_p_and_maturity)
    ui.pushButton_submit_new_instruments.clicked.connect(instruments_save)
    ui.pushButton_submit_new_plot_payoff.clicked.connect(plot_payoff_for_4_instruments)
    sinal.instruments_saved_print_and_check_available_signal.connect(msg_box_for_thread_when_open_app2)
    sinal.msg_box_for_thread_when_open_app3_signal.connect(msg_box_for_thread_when_open_app3)
    instruments_saved_print_and_check_available_when_open_app_thread_def()
    sinal.strategy_name_update_signal.connect(strategy_name_update_signal)
    sinal.reduce_only_signal.connect(reduce_only_signal)
    sinal.date_time_enabled_signal.connect(date_time_enabled_signal)
    sinal.date_time_disabled_signal.connect(date_time_disabled_signal)
    sinal.position_now_signal_2.connect(position_now)
    sinal.pushButton_request_options_structure_cost_signal.connect(pushbutton_request_options_structure_cost_signal)
    enable_disable_strike_and_c_or_p_and_maturity()


# noinspection PyShadowingNames
def config(ui):
    def save_orders_rate():
        from connection_spread import connect

        try:
            orders_per_second_from_line_edit = round(float(str.replace(ui.lineEdit_orders_rate.text(), ',', '.')), 2)
        except ValueError:
            orders_per_second_from_line_edit = float(5)
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText('Order/Second must be > 0')
            msg.setWindowTitle('***** ERROR *****')
            msg.exec_()

        if orders_per_second_from_line_edit > 0:
            orders_per_second = round(float(orders_per_second_from_line_edit), 2)

        else:
            orders_per_second = round(float(5), 2)
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText('Order/Second must be > 0')
            msg.setWindowTitle('***** ERROR *****')
            msg.exec_()

        setup = ConfigParser(
            allow_no_value=True,
            inline_comment_prefixes='#',
            strict=False
        )
        setup.read('setup.ini')
        default_setup = setup['DEFAULT']
        default_setup['orders_rate'] = str(orders_per_second)
        orders_per_second_saved = default_setup['orders_rate']

        with open('setup.ini', 'w') as configfile:
            setup.write(configfile)

        ui.lineEdit_orders_rate.setText(str(orders_per_second_saved))
        connect.logwriter('*** Order/Second Setup: ' + str(orders_per_second_saved) + ' ***')

    def set_version_and_icon_and_texts_and_dates_signal_receive():
        _translate = QtCore.QCoreApplication.translate

        setup = ConfigParser(
            allow_no_value=True,
            inline_comment_prefixes='#',
            strict=False
        )
        setup.read('setup.ini')
        
        default_setup = dict(setup['DEFAULT'])
        name = default_setup['name']
        version = default_setup['version']
        strategy_name = default_setup['strategy_name']
        
        main_windows_title = str(
            name + ' ' + version + '                    *** Strategy Name: ' + strategy_name + ' ***')
        MainWindow.setWindowTitle(_translate("MainWindow", main_windows_title))

        ui.pushButton_submit_new_plot_payoff.setText("Strategy\nPayoff")

        ui.label_29.setText("Buy or sell option strategy? (Select \"buy\" or \"sell\")")

        ui.comboBox_value_given.setItemText(0, "Set option strategy cost")

        ui.comboBox_value_given_2.setItemText(0, "Set Option Strategy Cost as TRIGGER (optional)")

        ui.pushButton_request_options_structure_cost.setText("UPDATE Option Strategy Cost")

        ui.label_57.setText("Strategy Greeks:")

        ui.tabWidget.setTabText(3, "Strategy")
        ui.tabWidget.setTabText(1, "Trades")
        ui.tabWidget.setTabText(2, "Setup")

        ui.label_44.setText("Strategy Greeks:")

        ui.pushButton_submit_new_instruments.setText("SUBMIT new Trades")

        ui.checkBox_autoScrollBar.setChecked(True)

        # set date:
        date_now_instrument = QtCore.QDate.currentDate()
        ui.lineEdit_maturity_instrumet1.setDate(date_now_instrument.addDays(-1))
        ui.lineEdit_maturity_instrumet2.setDate(date_now_instrument.addDays(-1))
        ui.lineEdit_maturity_instrumet3.setDate(date_now_instrument.addDays(-1))
        ui.lineEdit_maturity_instrumet4.setDate(date_now_instrument.addDays(-1))

        # Others old
        ui.lineEdit_currency_exchange_rate_lower1_2.setEnabled(False)
        ui.pushButton_update_balance.setHidden(True)

        ui.label_8.setText("Trade 1")
        ui.label_9.setText("Trade 2")
        ui.label_11.setText("Trade 3")
        ui.label_10.setText("Trade 4")

        ui.label_33.setText("Trade 4:")
        ui.label_36.setText("Trade 3:")
        ui.label_35.setText("Trade 2:")
        ui.label_34.setText("Trade 1:")

        # Set text License
        try:
            with open('LICENSE.txt', 'r') as license_txt_file:
                license_txt = license_txt_file.read()
                ui.textEdit_license.append(license_txt)
        except FileNotFoundError:
            license_txt = 'License file NOT found\n\nCopyright 2022 Vavarb vavarb@protonmail.com ' \
                          'https://github.com/vavarb\n\nVisit: http://www.apache.org/licenses/LICENSE-2.0'
            ui.textEdit_license.append(license_txt)
        finally:
            pass

        # Set text Contact us
        contact_text = 'Contact us: vavarb@protonmail.com\n' \
                       'Source Code: https://github.com/vavarb/vavabot_options_strategy'
        ui.textEdit_contact_us.append(contact_text)

        # Set text Buy me a coffee
        buy_me_a_coffee_text = 'Buy me a Coffe ☕? If you have found anything useful and you want to support me, ' \
                               'feel free to do it with ₿ITCOIN or Lightning Network! And many thanks in advance. ' \
                               '😁\n\n' \
                               '>>> Lightning Network Adress: vavarb@bipa.app\n' \
                               '>>> ₿ITCOIN Adress: 36RbpSZVNiSxK69kNMH3WHFJqAhfXppU5N'
        ui.textEdit_buy_me_a_coffee.append(buy_me_a_coffee_text)

        # Set Text reduce only
        ui.label_18.setText('Buy or Sell')

        ui.check_box_reduce_only_1.setText(' ')
        ui.check_box_reduce_only_2.setText(' ')
        ui.check_box_reduce_only_3.setText(' ')
        ui.check_box_reduce_only_4.setText(' ')

        ui.label_reduce_only.setText('Reduce\nOnly:')
        ui.label_reduce_only.raise_()

        # Set Text strategy name
        ui.label_strategy_name.setText('Strategy Name:')

        # set date time
        ui.date_time_start.raise_()
        ui.date_time_end.raise_()
        ui.checkbox_date_time_start.raise_()
        ui.checkbox_date_time_end.raise_()
        ui.checkbox_date_time_start.setText('Trading Start:')
        ui.checkbox_date_time_end.setText('Trading End:')

    def set_version_and_icon_and_texts_and_dates():
        sinal.set_version_and_icon_and_texts_and_dates_signal.emit()

    def set_enabled_trigger():
        if ui.comboBox_value_given_2.currentText() == 'Set Option Strategy Cost as TRIGGER (optional)':
            ui.lineEdit_currency_exchange_rate_lower1_2.setEnabled(False)

        else:
            ui.lineEdit_currency_exchange_rate_lower1_2.setEnabled(True)

    def targets_save():
        date_time_start_str = ui.date_time_start.text()
        date_time_start_datetime = datetime.strptime(date_time_start_str, "%d/%m/%Y %H:%M")
        date_time_start_stamp = date_time_start_datetime.timestamp()

        date_time_end_str = ui.date_time_end.text()
        date_time_end_datetime = datetime.strptime(date_time_end_str, "%d/%m/%Y %H:%M")
        date_time_end_stamp = date_time_end_datetime.timestamp()

        if ui.lineEdit_currency_exchange_rate_for_upper_and_lower1.text() == '' or \
                ui.lineEdit_currency_exchange_rate_lower1.text() == '' or \
                ui.lineEdit_buy_or_sell_structure1.currentText() == 'Set buy or sell' or \
                ui.comboBox_value_given.currentText() == \
                'Set option strategy cost' or \
                ui.lineEdit_spread_structure1.text() == '':
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText('All fields are required')
            msg.setWindowTitle('***** ERROR *****')
            msg.exec_()
            pass
        elif date_time_start_stamp >= date_time_end_stamp:
            from connection_spread import connect
            setup = ConfigParser(
                allow_no_value=True,
                inline_comment_prefixes='#',
                strict=False
            )
            setup.read('setup.ini')
            date_time_setup = setup['date_time']

            if ui.checkbox_date_time_start.isChecked() is True:
                date_time_setup['start_ischecked'] = 'True'
            else:
                date_time_setup['start_ischecked'] = 'False'

            if ui.checkbox_date_time_end.isChecked() is True:
                date_time_setup['end_ischecked'] = 'True'
            else:
                date_time_setup['end_ischecked'] = 'False'

            now = datetime.now()
            now10 = now + timedelta(days=10)
            now_10_text = now10.strftime('%d/%m/%Y %H:%M')
            now_text = now.strftime('%d/%m/%Y %H:%M')

            date_time_setup['start'] = now_text
            date_time_setup['end'] = now_10_text

            with open('setup.ini', 'w') as configfile:
                setup.write(configfile)
            connect.logwriter('*** Date and time saved ***')

            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText('Date and time start < end\nis NOT accepted')
            msg.setWindowTitle('***** ERROR *****')
            msg.exec_()
            pass
            Config().date_time_saved()
        else:
            try:
                if float(str.replace(ui.lineEdit_currency_exchange_rate_upper1.text(), ',', '.')) == 0 or \
                         float(str.replace(ui.lineEdit_spread_structure1.text(), ',', '.')) == 0 or \
                         float(str.replace(ui.lineEdit_currency_exchange_rate_lower1.text(), ',', '.')) == 0:
                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Information)
                    msg.setText('Zero is NOT accepted')
                    msg.setWindowTitle('***** ERROR *****')
                    msg.exec_()
                else:
                    if str(ui.comboBox_value_given_2.currentText()) != \
                            'Set Option Strategy Cost as TRIGGER (optional)':
                        lcerl1_2 = str(ui.lineEdit_currency_exchange_rate_lower1_2.text())
                        lcerl1_2_adjusted_dot = str.replace(lcerl1_2, ',', '.')
                        if str(lcerl1_2_adjusted_dot) == '':
                            msg = QtWidgets.QMessageBox()
                            msg.setIcon(QtWidgets.QMessageBox.Information)
                            msg.setText('Set Option Strategy Cost as TRIGGER is Required')
                            msg.setWindowTitle('***** ERROR *****')
                            msg.exec_()
                            pass
                        else:
                            try:
                                if float(lcerl1_2_adjusted_dot) == 0:
                                    msg = QtWidgets.QMessageBox()
                                    msg.setIcon(QtWidgets.QMessageBox.Information)
                                    msg.setText('Set Option Strategy Cost as TRIGGER is Required\nZero is NOT accepted')
                                    msg.setWindowTitle('***** ERROR *****')
                                    msg.exec_()
                                else:
                                    lcerfual = ui.lineEdit_currency_exchange_rate_for_upper_and_lower1.text()
                                    Config().save_targets(
                                        currency_exchange_rate_for_upper_and_lower1=lcerfual,
                                        currency_exchange_rate_upper1=str.replace(
                                            ui.lineEdit_currency_exchange_rate_upper1.text(), ',', '.'),
                                        currency_exchange_rate_lower1=str.replace(
                                            ui.lineEdit_currency_exchange_rate_lower1.text(), ',', '.'),
                                        buy_or_sell_structure1=ui.lineEdit_buy_or_sell_structure1.currentText(),
                                        spread_structure1=str.replace(ui.lineEdit_spread_structure1.text(), ',', '.')
                                    )
                                    date_time_save()
                            except ValueError:
                                msg = QtWidgets.QMessageBox()
                                msg.setIcon(QtWidgets.QMessageBox.Information)
                                msg.setText('Only numbers are accepted')
                                msg.setWindowTitle('***** ERROR *****')
                                msg.exec_()
                                pass
                    else:
                        lcerfual = ui.lineEdit_currency_exchange_rate_for_upper_and_lower1.text()
                        Config().save_targets(
                            currency_exchange_rate_for_upper_and_lower1=lcerfual,
                            currency_exchange_rate_upper1=str.replace(
                                ui.lineEdit_currency_exchange_rate_upper1.text(), ',', '.'),
                            currency_exchange_rate_lower1=str.replace(
                                ui.lineEdit_currency_exchange_rate_lower1.text(), ',', '.'),
                            buy_or_sell_structure1=ui.lineEdit_buy_or_sell_structure1.currentText(),
                            spread_structure1=str.replace(ui.lineEdit_spread_structure1.text(), ',', '.')
                        )
                        date_time_save()
            except ValueError:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Only numbers are accepted')
                msg.setWindowTitle('***** ERROR *****')
                msg.exec_()
                pass

    def target_saved_check_signal_receive():
        with open('value_given_in.txt', 'r') as f7:
            f6 = f7.read()
            if 'BTC' in f6:
                text_to_textedit_targets_saved_if_btc = ConfigSaved().targets_saved()
                text_to_textedit_targets_saved_if_btc_1 = str.replace(
                                                                      text_to_textedit_targets_saved_if_btc,
                                                                      'Set the cost of the Options Structure as '
                                                                      'trigger (optional)',
                                                                      'Set Option Strategy Cost as TRIGGER (optional)')
                text_to_textedit_targets_saved_if_btc_2 = str.replace(text_to_textedit_targets_saved_if_btc_1,
                                                                      'buy or sell the structure',
                                                                      'Buy or sell strategy')
                text_to_textedit_targets_saved_if_btc_3 = str.replace(text_to_textedit_targets_saved_if_btc_2,
                                                                      'Structure cost should be',
                                                                      'Strategy costshould be')
                ui.textEdit_targets_saved.setText(text_to_textedit_targets_saved_if_btc_3)
            elif 'USD' in f6:
                with open('targets_spread.txt', 'r') as f4:
                    f4l = f4.readlines()
                    f4s1 = str(f4l[0])
                    f4s2 = str(f4l[1])
                    f4s3 = str.replace(str(f4l[2]), 'buy or sell the structure', 'Buy or sell strategy')
                    f4s4 = str.replace(str(f4l[3]), 'Structure cost should be', 'Strategy cost should be')
                    f4s5 = str(f4l[4])
                    f4s6 = str.replace(f4l[5], 'Set the cost of the Options Structure as trigger (optional)',
                                       'Set Option Strategy Cost as TRIGGER (optional)')
                    f5 = str.replace(f4s4, 'BTC', 'USD')
                    f6 = str.replace(f4s5, 'for target setting', 'for conditions')
                    ui.textEdit_targets_saved.setText(f4s1 + f4s2 + f4s3 + f5 + f6 + f4s6)
            elif 'Mark Price %' in f6:
                with open('targets_spread.txt', 'r') as f4:
                    f4l = f4.readlines()
                    f4s1 = str(f4l[0])
                    f4s2 = str(f4l[1])
                    f4s3 = str.replace(str(f4l[2]), 'buy or sell the structure', 'Buy or sell strategy')
                    f4s4 = str.replace(str(f4l[3]), 'Structure cost should be', 'Strategy cost should be')
                    f4s5 = str(f4l[4])
                    f4s6 = str.replace(f4l[5], 'Set the cost of the Options Structure as trigger (optional)',
                                       'Set Option Strategy Cost as TRIGGER (optional)')
                    f5 = str.replace(f4s4, 'BTC', '% of the Mark Price')
                    f6 = str.replace(f4s5, 'for target setting', 'for conditions')
                    ui.textEdit_targets_saved.setText(f4s1 + f4s2 + f4s3 + f5 + f6 + f4s6)
            else:
                text_to_textedit_targets_saved_if_btc = ConfigSaved().targets_saved()
                text_to_textedit_targets_saved_if_btc_1 = str.replace(
                    text_to_textedit_targets_saved_if_btc,
                    'Set the cost of the Options Structure as '
                    'trigger (optional)',
                    'Set Option Strategy Cost as TRIGGER (optional)')
                text_to_textedit_targets_saved_if_btc_2 = str.replace(text_to_textedit_targets_saved_if_btc_1,
                                                                      'buy or sell the structure',
                                                                      'Buy or sell strategy')
                text_to_textedit_targets_saved_if_btc_3 = str.replace(text_to_textedit_targets_saved_if_btc_2,
                                                                      'Structure cost should be',
                                                                      'Strategy cost should be')
                ui.textEdit_targets_saved.setText(text_to_textedit_targets_saved_if_btc_3)

    def date_time_signal(info):
        text_date_time_start = info['text_date_time_start']
        text_date_time_end = info['text_date_time_end']
        true_or_false_start_ischecked = info['true_or_false_start_ischecked']
        true_or_false_end_ischecked = info['true_or_false_end_ischecked']

        text_date_time_start1 = ui.date_time_start.dateTimeFromText(text_date_time_start)
        text_date_time_end1 = ui.date_time_end.dateTimeFromText(text_date_time_end)
        ui.date_time_start.setDateTime(text_date_time_start1)
        ui.date_time_end.setDateTime(text_date_time_end1)

        ui.checkbox_date_time_start.setChecked(true_or_false_start_ischecked)
        ui.checkbox_date_time_end.setChecked(true_or_false_end_ischecked)

    def date_time_save():
        from connection_spread import connect

        date_time_start_str = ui.date_time_start.text()
        date_time_start_datetime = datetime.strptime(date_time_start_str, "%d/%m/%Y %H:%M")
        date_time_start_stamp = date_time_start_datetime.timestamp()

        date_time_end_str = ui.date_time_end.text()
        date_time_end_datetime = datetime.strptime(date_time_end_str, "%d/%m/%Y %H:%M")
        date_time_end_stamp = date_time_end_datetime.timestamp()

        setup = ConfigParser(
            allow_no_value=True,
            inline_comment_prefixes='#',
            strict=False
        )
        setup.read('setup.ini')
        date_time_setup = setup['date_time']

        if ui.checkbox_date_time_start.isChecked() is True:
            date_time_setup['start_ischecked'] = 'True'
        else:
            date_time_setup['start_ischecked'] = 'False'

        if ui.checkbox_date_time_end.isChecked() is True:
            date_time_setup['end_ischecked'] = 'True'
        else:
            date_time_setup['end_ischecked'] = 'False'

        if date_time_start_stamp >= date_time_end_stamp:
            now = datetime.now()
            now10 = now + timedelta(days=10)
            now_10_text = now10.strftime('%d/%m/%Y %H:%M')
            now_text = now.strftime('%d/%m/%Y %H:%M')

            date_time_setup['start'] = now_text
            date_time_setup['end'] = now_10_text

            with open('setup.ini', 'w') as configfile:
                setup.write(configfile)
            connect.logwriter('*** Date and time saved ***')

            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText('Date and time start < end\nis NOT accepted')
            msg.setWindowTitle('***** ERROR *****')
            msg.exec_()
            pass
            Config().date_time_saved()
        else:
            date_time_setup['start'] = str(date_time_start_str)
            date_time_setup['end'] = str(date_time_end_str)

            with open('setup.ini', 'w') as configfile:
                setup.write(configfile)
            connect.logwriter('*** Date and time saved ***')
            Config().date_time_saved()

    sinal.set_version_and_icon_and_texts_and_dates_signal.connect(
        set_version_and_icon_and_texts_and_dates_signal_receive)
    set_version_and_icon_and_texts_and_dates()
    sinal.target_saved_check_signal.connect(target_saved_check_signal_receive)
    ConfigSaved().target_saved_check()
    ui.comboBox_value_given_2.currentTextChanged.connect(set_enabled_trigger)
    ui.pushButton_submit_new_targets.clicked.connect(targets_save)
    ConfigSaved().orders_rate_saved2()
    ui.pushButton_orders_rate.clicked.connect(save_orders_rate)
    ui.lineEdit_orders_rate.editingFinished.connect(save_orders_rate)
    sinal.date_time_signal.connect(date_time_signal)
    ui.checkbox_date_time_start.stateChanged.connect(date_time_save)
    ui.checkbox_date_time_end.stateChanged.connect(date_time_save)
    ui.date_time_start.editingFinished.connect(date_time_save)
    ui.date_time_end.editingFinished.connect(date_time_save)


# noinspection PyShadowingNames
def quote(ui):
    def quote_new_for_print_in_tab_quote():
        Quote().quote_new()  # já direcional para signal

    ui.pushButton_request_options_structure_cost.clicked.connect(quote_new_for_print_in_tab_quote)


# noinspection PyShadowingNames
def run(ui):
    def textedit_balance_after_signal(info):
        max_position_instrument1_for_gui = str(info['Instrument 1'])
        max_position_instrument2_for_gui = str(info['Instrument 2'])
        max_position_instrument3_for_gui = str(info['Instrument 3'])
        max_position_instrument4_for_gui = str(info['Instrument 4'])

        ui.textEdit_balance_after.clear()
        ui.textEdit_balance_after.append('Instrument 1: ' + str(max_position_instrument1_for_gui))
        ui.textEdit_balance_after.append('Instrument 2: ' + str(max_position_instrument2_for_gui))
        ui.textEdit_balance_after.append('Instrument 3: ' + str(max_position_instrument3_for_gui))
        ui.textEdit_balance_after.append('Instrument 4: ' + str(max_position_instrument4_for_gui))

        info.clear()

    def position_now_when_open_app_signal(info):
        from connection_spread import connection_thread
        ui.textEdit_balance_2.clear()
        ui.textEdit_balance_2.setText(str(info))
        connection_thread()

    def last_trade_instrument_conditions_quote_signal(info):
        info_dict1 = str(info['lineEdit_24_btc_index_2'])
        info_dict2 = str(info['lineEdit_24_btc_index_3'])

        ui.lineEdit_24_btc_index_2.setText(info_dict1)
        ui.lineEdit_24_btc_index_3.setText(info_dict2)

    def quote_new_when_open_app_signal1(info):
        ui.lineEdit.setText(str(info['f9']))
        ui.lineEdit_2.setText(str(info['f10']))
        ui.lineEdit_3.setText(str(info['f11']))
        ui.lineEdit_4.setText(str(info['f12']))
        ui.lineEdit_7.setText(str(info['f13']))
        ui.lineEdit_5.setText(str(info['f14']))
        ui.lineEdit_8.setText(str(info['f15']))
        ui.lineEdit_6.setText(str(info['f16']))
        ui.lineEdit_10.setText(str(info['f17']))
        ui.lineEdit_11.setText(str(info['f18']))
        ui.lineEdit_9.setText(str(info['f19']))
        ui.lineEdit_12.setText(str(info['f20']))
        ui.lineEdit_14.setText(str(info['f25']))
        ui.lineEdit_15.setText(str(info['f26']))
        ui.lineEdit_13.setText(str(info['f27']))
        ui.lineEdit_16.setText(str(info['f28']))
        ui.lineEdit_17.setText(str(info['f29']))
        ui.lineEdit_18.setText(str(info['f30']))
        ui.lineEdit_19.setText(str(info['f31']))
        ui.lineEdit_20.setText(str(info['f32']))

        ui.lineEdit_22.setText(str(info['lineEdit_22']))
        ui.lineEdit_23.setText(str(info['lineEdit_23']))
        ui.lineEdit_21.setText(str(info['lineEdit_21']))

        # info.clear()

    def textedit_balance_settext_signal(info):
        ui.textEdit_balance.setText(str(info))

    def msg_box_for_thread_when_open_app1_signal(info):
        msg_for_msg_box = str(info[0])
        title_for_msg_box = str(info[1])
        info.clear()

        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText(msg_for_msg_box)
        msg.setWindowTitle(title_for_msg_box)
        msg.exec_()
        pass

    def textedit_instruments_saved_settext_signal(info):
        ui.textEdit_instruments_saved.setText(str(info))

    def print_greeks_by_instrument_signal(info):
        # Delta
        ui.lineEdit_29.setText(str(round(info.get('lineEdit_29', 0), 6)))
        ui.lineEdit_47.setText(str(round(info.get('lineEdit_47', 0), 6)))
        ui.lineEdit_48.setText(str(round(info.get('lineEdit_48', 0), 6)))
        ui.lineEdit_49.setText(str(round(info.get('lineEdit_49', 0), 6)))

        # Theta
        ui.lineEdit_31.setText(str(round(info.get('lineEdit_31', 0), 6)))
        ui.lineEdit_37.setText(str(round(info.get('lineEdit_37', 0), 6)))
        ui.lineEdit_36.setText(str(round(info.get('lineEdit_36', 0), 6)))
        ui.lineEdit_35.setText(str(round(info.get('lineEdit_35', 0), 6)))

        # Gamma
        ui.lineEdit_30.setText(str(round(info.get('lineEdit_30', 0), 6)))
        ui.lineEdit_44.setText(str(round(info.get('lineEdit_44', 0), 6)))
        ui.lineEdit_45.setText(str(round(info.get('lineEdit_45', 0), 6)))
        ui.lineEdit_46.setText(str(round(info.get('lineEdit_46', 0), 6)))

        # Vega
        ui.lineEdit_32.setText(str(round(info.get('lineEdit_32', 0), 6)))
        ui.lineEdit_41.setText(str(round(info.get('lineEdit_41', 0), 6)))
        ui.lineEdit_42.setText(str(round(info.get('lineEdit_42', 0), 6)))
        ui.lineEdit_43.setText(str(round(info.get('lineEdit_43', 0), 6)))

        # Rho
        ui.lineEdit_33.setText(str(round(info.get('lineEdit_33', 0), 6)))
        ui.lineEdit_38.setText(str(round(info.get('lineEdit_38', 0), 6)))
        ui.lineEdit_39.setText(str(round(info.get('lineEdit_39', 0), 6)))
        ui.lineEdit_40.setText(str(round(info.get('lineEdit_40', 0), 6)))

        info.clear()

    def msg_box_for_position_now_signal():
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText('Connection Offline\nCurrent Positions don´t updated')
        msg.setWindowTitle('***** ERROR *****')
        msg.exec_()

    def position_now_signal(info):
        a1 = str(info['Instrument 1'])
        b1 = str(info['Instrument 2'])
        c1 = str(info['Instrument 3'])
        d1 = str(info['Instrument 4'])
        ui.textEdit_balance_2.clear()
        ui.textEdit_balance_2.setText('Instrument 1: ' + str(a1) + '\n' +
                                      'Instrument 2: ' + str(b1) + '\n' +
                                      'Instrument 3: ' + str(c1) + '\n' +
                                      'Instrument 4: ' + str(d1))

        info.clear()

    def receive_signal_por_print_monitor(info):
        msg1 = str(info)
        msg2 = msg1.replace('\n', '')
        ui.textEdit_monitor.append(str(msg2))

    def receive_led_green_for_monitor():
        green_icon = "./green_led_icon.png"
        ui.label_61.setPixmap(QtGui.QPixmap(green_icon))

    def receive_led_red_for_monitor():
        red_icon = "./red_led_icon.png"
        ui.label_61.setPixmap(QtGui.QPixmap(red_icon))

    def receive_autoscroll_monitor():
        if ui.checkBox_autoScrollBar.isChecked() is True:
            ui.textEdit_monitor.verticalScrollBar().setValue(999999)
        else:
            ui.textEdit_monitor.verticalScrollBar()

    def receive_error_in_list_monitor_signal(er):
        ui.textEdit_monitor.append('ERROR in lists_monitor: Error Code:: 6954 ' + str(er))

    def lists_monitor():
        import time
        from lists import list_monitor_log
        from connection_spread import led_color
        try:
            from connection_spread import connect
            counter = 0
            led1 = led_color()

            if led1 == 'green':
                sinal.led_color_green_signal.emit()
            elif led1 == 'red':
                sinal.led_color_red_signal.emit()
            else:
                connect.logwriter('*** ERROR - lists_monitor() Error Code:: 6969 ***')
                er1_str = str('*** ERROR - lists_monitor() Error Code:: 6970 ***')
                sinal.error_in_list_monitor_signal.emit(er1_str)
                pass
        except ImportError:
            counter = 0
            led1 = led_color()

            if led1 == 'green':
                sinal.led_color_green_signal.emit()
            elif led1 == 'red':
                sinal.led_color_red_signal.emit()
            else:
                er1_str = str('*** ERROR - lists_monitor() Error Code:: 6970 ***')
                sinal.error_in_list_monitor_signal.emit(er1_str)
                pass

        while True:
            try:
                if len(list_monitor_log) > 0:
                    for i in list_monitor_log:
                        info = str(datetime.now().strftime("[%Y/%m/%d, %H:%M:%S] ")) + str(i)
                        sinal.textEdit_monitor_signal.emit(info)
                        counter = counter + 1
                    list_monitor_log.clear()
                else:
                    time.sleep(0.0001)

                if led1 != led_color():
                    if led_color() == 'green':
                        led1 = 'green'
                        sinal.led_color_green_signal.emit()
                    elif led_color() == 'red':
                        led1 = 'red'
                        sinal.led_color_red_signal.emit()
                    else:
                        try:
                            from connection_spread import connect
                        except ImportError:
                            er1_str = str('*** ERROR - lists_monitor() Error Code:: 6994 ***')
                            sinal.error_in_list_monitor_signal.emit(er1_str)
                            pass
                        else:
                            connect.logwriter('*** ERROR - lists_monitor() Error Code:: 6993 ***')
                            er1_str = str('*** ERROR - lists_monitor() Error Code:: 6994 ***')
                            sinal.error_in_list_monitor_signal.emit(er1_str)
                            pass
                else:
                    pass

                if counter >= 10000:
                    counter = 0
                    sinal.pushbutton_2_click_signal.emit()
                    time.sleep(0.5)
                    pass
                else:
                    pass
            except Exception as er:
                from connection_spread import connect
                connect.logwriter(str(er) + ' Error Code:: 7009')
                er1 = str('*** ERROR - lists_monitor() Error Code:: 7010: ' + str(er) + ' ***')
                sinal.error_in_list_monitor_signal.emit(er1)
            finally:
                pass

    def clear_monitor_signal():
        ui.textEdit_monitor.clear()

    def structure_cost_for_tab_run_trading_and_btc_index_and_greeks_when_started_trading_signal_0(quote_dic):
        text59 = str(quote_dic['text59'])
        text61 = str(quote_dic['text61'])
        text60 = str(quote_dic['text60'])

        ui.lineEdit_59.setText(text59)
        ui.lineEdit_61.setText(text61)
        ui.lineEdit_60.setText(text60)
        quote_dic.clear()

    def structure_cost_for_tab_run_trading_and_btc_index_and_greeks_when_started_trading_signal_1():
        ui.pushButton.setEnabled(False)
        ui.pushButton.setText('Auto-Request')

    # noinspection PyMethodMayBeStatic
    def structure_cost_for_tab_run_trading_and_btc_index_and_greeks_when_started_trading_signal_2(index):
        ui.lineEdit_24_btc_index.setText(str(index))

    def quote_new_structure_cost_for_print_when_stopped_trading_signal1(quote_dic):
        text59 = str(quote_dic['text59'])
        text61 = str(quote_dic['text61'])
        text60 = str(quote_dic['text60'])

        ui.lineEdit_59.setText(text59)
        ui.lineEdit_61.setText(text61)
        ui.lineEdit_60.setText(text60)

    def receive_greeks_signal(greeks):
        from lists import list_monitor_log
        from connection_spread import led_color
        c = dict(greeks)
        if led_color() == 'red':
            pass
        else:
            try:
                d = str(c['vega'])
                ui.lineEdit_27.setText(d)

                g = str(c['theta'])
                ui.lineEdit_26.setText(g)

                h = str(c['rho'])
                ui.lineEdit_28.setText(h)

                j = c['gamma']
                ui.lineEdit_25.setText(j)

                k = str(c['delta'])
                ui.lineEdit_24.setText(k)
            except Exception as er:
                from connection_spread import connect
                connect.logwriter(str(er) + ' Error Code:: 7068')
                list_monitor_log.append(str(er) + ' Error Code:: 7069')
                list_monitor_log.append('********** index_price_and_greeks ERROR **********')
                pass
            finally:
                pass

    def receive_greeks_signal1(greeks):
        from lists import list_monitor_log
        from connection_spread import led_color
        c = dict(greeks)
        if led_color() == 'red':
            pass
        else:
            try:
                # c = Quote().structure_mark_greek_cost()
                d = str(c['vega'])
                ui.lineEdit_56.setText(d)

                g = str(c['theta'])
                ui.lineEdit_55.setText(g)

                h = str(c['rho'])
                ui.lineEdit_57.setText(h)

                j = c['gamma']
                ui.lineEdit_54.setText(j)

                k = str(c['delta'])
                ui.lineEdit_53.setText(k)

            except Exception as er:
                from connection_spread import connect
                connect.logwriter(str(er) + ' Error Code:: 7100')
                list_monitor_log.append(str(er) + ' Error Code:: 7101')
                list_monitor_log.append('********** index_price_and_greeks ERROR **********')
                pass
            finally:
                pass

    def receive_index_btc_print_signal(index):
        ui.lineEdit_24_btc_index.setText(str(index))

    def receive_chronometer_signal(sec):
        ui.lineEdit_58.setText(str(sec))

    def receive_btc_index_print_gui_adjusts_signal():
        ui.lineEdit_59.show()
        ui.lineEdit_61.show()
        ui.lineEdit_60.show()

        ui.pushButton.setEnabled(False)
        ui.pushButton.setText('COUNTDOWN\nEnabled')

        ui.pushButton_submit_new_credintals.setEnabled(True)
        ui.radioButton_testnet_true.setEnabled(True)
        ui.radioButton_2_testnet_false.setEnabled(True)
        ui.pushButton_submit_new_instruments.setEnabled(True)
        ui.pushButton_submit_new_plot_payoff.setEnabled(True)
        ui.pushButton_submit_new_targets.setEnabled(True)

        ui.lineEdit_orders_rate.setEnabled(True)
        ui.pushButton_orders_rate.setEnabled(True)

        setup = ConfigParser(
            allow_no_value=True,
            inline_comment_prefixes='#',
            strict=False
        )
        setup.read('setup.ini')
        date_time_setup = setup['date_time']
        date_time_setup_enable = date_time_setup.getboolean('date_time_enabled')
        if date_time_setup_enable is True:
            ui.checkbox_date_time_start.setEnabled(True)
            ui.checkbox_date_time_end.setEnabled(True)
            ui.date_time_start.setEnabled(True)
            ui.date_time_end.setEnabled(True)
        else:
            ui.checkbox_date_time_start.setEnabled(False)
            ui.checkbox_date_time_end.setEnabled(False)
            ui.date_time_start.setEnabled(False)
            ui.date_time_end.setEnabled(False)

        ui.check_box_reduce_only_1.setEnabled(True)
        ui.check_box_reduce_only_2.setEnabled(True)
        ui.check_box_reduce_only_3.setEnabled(True)
        ui.check_box_reduce_only_4.setEnabled(True)

    def btc_index_print():
        import time
        global index_greeks_print_on_off
        from lists import list_monitor_log
        from connection_spread import led_color

        index_greeks_print_on_off = 'on'

        sinal.btc_index_print_gui_adjusts_signal.emit()

        while index_greeks_print_on_off == 'on':
            try:
                if led_color() == 'red':
                    time.sleep(3)
                    pass
                else:
                    from connection_spread import connect
                    Quote().quote_new_structure_cost_for_print_when_stopped_trading()

                    a = connect.index_price('btc_usd')
                    b = str(a['index_price'])
                    sinal.index_btc_print_signal.emit(str(b))

                    c = Quote().structure_mark_greek_cost()
                    sinal.greeks_signal.emit(c)

            except Exception as er:
                from connection_spread import connect
                connect.logwriter(str(er) + ' Error Code:: 7165')
                list_monitor_log.append(str(er) + ' Error Code:: 7156')
                list_monitor_log.append('********** BTC index print ERROR **********')
                time.sleep(3)
                pass
            finally:
                pass

            for item in range(10, -1, -1):
                sec = str(item)
                sinal.chronometer_signal.emit(sec)
                time.sleep(1)

        start_thread_trade()

    def btc_index_print_start_thread_signal():
        red_icon = "./red_led_icon.png"
        ui.label_62.setPixmap(QtGui.QPixmap(red_icon))

        ui.pushButton.setText('COUNTDOWN\nEnabled')

        ui.pushButton_stop_arbitrage.setEnabled(False)
        ui.pushButton_start_trading.setEnabled(True)

    def btc_index_print_start_thread():
        import threading
        sinal.btc_index_print_start_thread_signal.emit()

        btc_index_print_thread = threading.Thread(daemon=True, target=btc_index_print, name='btc_index_print_thread')
        btc_index_print_thread.start()

    def run_trade_future():
        import time
        from lists import list_monitor_log
        from connection_spread import connect, led_color
        global trading_on_off
        global run_trade_future_on_off
        global run_trade_option_on_off
        global trading_on_off_for_msg
        global run_target_on_off

        if run_trade_future_on_off == 'on':

            try:
                if led_color() == 'red':
                    list_monitor_log.append('********** Connection Offline **********')
                    time.sleep(3)
                    pass

                else:
                    instrument1_kind = InstrumentsSaved().instrument_kind_saved(instrument_number=1)
                    instrument2_kind = InstrumentsSaved().instrument_kind_saved(instrument_number=2)
                    instrument3_kind = InstrumentsSaved().instrument_kind_saved(instrument_number=3)
                    instrument4_kind = InstrumentsSaved().instrument_kind_saved(instrument_number=4)

                    if (instrument1_kind == 'option' or instrument1_kind == 'Unassigned') and \
                            (instrument2_kind == 'option' or instrument2_kind == 'Unassigned') and \
                            (instrument3_kind == 'option' or instrument3_kind == 'Unassigned') and \
                            (instrument4_kind == 'option' or instrument4_kind == 'Unassigned'):
                        list_monitor_log.append('********** THERE ARE NOT FUTURE ORDERS FOR TRADING **********')
                        run_trade_future_on_off = 'off'

                    aa1 = ConditionsCheck().position_future_smaller_max_position_instrument(instrument_number=1)
                    aa2 = ConditionsCheck().position_future_smaller_max_position_instrument(instrument_number=2)
                    aa3 = ConditionsCheck().position_future_smaller_max_position_instrument(instrument_number=3)
                    aa4 = ConditionsCheck().position_future_smaller_max_position_instrument(instrument_number=4)

                    if aa1 == 'instrument_run_trade_no' and aa2 == 'instrument_run_trade_no' and \
                            aa3 == 'instrument_run_trade_no' and aa4 == 'instrument_run_trade_no':
                        list_monitor_log.append('**************** NO MORE FUTURE ORDERS **************** ')
                        run_trade_future_on_off = 'off'

                    else:
                        # instrument 1
                        if instrument1_kind == 'future':
                            if aa1 == 'instrument_run_trade_ok':
                                bb = ConditionsCheck().targets_achieved_future()
                                if bb == 'targets_future_ok':
                                    list_monitor_log.append('*** Waiting to Send Future Order')
                                    ConditionsCheck().send_future_orders(
                                        instrument_number=1)
                                else:
                                    pass
                            elif aa1 == 'instrument_run_trade_no':
                                pass
                            else:
                                connect.logwriter(
                                    '********** ERROR IN vavabot_spread.py Error Code:: 7241 **********')
                                list_monitor_log.append(
                                    '********** ERROR IN vavabot_spread.py Error Code:: 7243 **********')
                                pass
                        else:
                            pass

                        # instrument 2
                        if instrument2_kind == 'future':
                            if aa2 == 'instrument_run_trade_ok':
                                bb = ConditionsCheck().targets_achieved_future()
                                if bb == 'targets_future_ok':
                                    list_monitor_log.append('*** Waiting to Send Future Order')
                                    ConditionsCheck().send_future_orders(
                                        instrument_number=2)
                                else:
                                    pass
                            elif aa1 == 'instrument_run_trade_no':
                                pass
                            else:
                                connect.logwriter(
                                    '********** ERROR IN vavabot_spread.py Error Code:: 7262 **********')
                                list_monitor_log.append(
                                    '********** ERROR IN vavabot_spread.py Error Code:: 7264 **********')
                                pass
                        else:
                            pass

                        # instrument 3
                        if instrument3_kind == 'future':
                            if aa3 == 'instrument_run_trade_ok':
                                bb = ConditionsCheck().targets_achieved_future()
                                if bb == 'targets_future_ok':
                                    list_monitor_log.append('*** Waiting to Send Future Order')
                                    ConditionsCheck().send_future_orders(
                                        instrument_number=3)
                                else:
                                    pass
                            elif aa1 == 'instrument_run_trade_no':
                                pass
                            else:
                                connect.logwriter(
                                    '********** ERROR IN vavabot_spread.py Error Code:: 7283 **********')
                                list_monitor_log.append(
                                    '********** ERROR IN vavabot_spread.py Error Code:: 7285 **********')
                                pass
                        else:
                            pass

                        # instrument 4
                        if instrument4_kind == 'future':
                            if aa4 == 'instrument_run_trade_ok':
                                bb = ConditionsCheck().targets_achieved_future()
                                if bb == 'targets_future_ok':
                                    list_monitor_log.append('*** Waiting to Send Future Order')
                                    ConditionsCheck().send_future_orders(
                                        instrument_number=4)
                                else:
                                    pass
                            elif aa1 == 'instrument_run_trade_no':
                                pass
                            else:
                                connect.logwriter(
                                    '********** ERROR IN vavabot_spread.py Error Code:: 7304 **********')
                                list_monitor_log.append(
                                    '********** ERROR IN vavabot_spread.py Error Code:: 7306 **********')
                                pass
                        else:
                            pass

            except Exception as error3:
                from connection_spread import connect
                connect.logwriter(str(error3) + ' Error Code:: 7313')
                list_monitor_log.append('run_trade_future_on_off - error3: Error Code:: 7314 ' + str(error3))
                pass
            finally:
                pass
        else:
            list_monitor_log.append('run_trade_future_on_off is off')
            pass

    # noinspection PyMethodMayBeStatic
    def structure_mark_greek_cost_signal(greeks):
        from lists import list_monitor_log
        from connection_spread import led_color
        c = dict(greeks)
        if led_color() == 'red':
            pass
        else:
            try:
                d = str(c['vega'])
                ui.lineEdit_27.setText(d)

                g = str(c['theta'])
                ui.lineEdit_26.setText(g)

                h = str(c['rho'])
                ui.lineEdit_28.setText(h)

                j = c['gamma']
                ui.lineEdit_25.setText(j)

                k = str(c['delta'])
                ui.lineEdit_24.setText(k)

            except Exception as er:
                from connection_spread import connect
                connect.logwriter(str(er) + ' Error Code:: 7348')
                list_monitor_log.append(str(er) + ' Error Code:: 7349')
                list_monitor_log.append('********* structure_mark_greek_cost_signal ERROR'
                                        '**********')
                pass
            finally:
                pass
        c.clear()

    def start_signal_1(info):
        try:
            from connection_spread import connect
            ui.label_58.show()
            if info == 'start':
                setup = ConfigParser(
                    allow_no_value=True,
                    inline_comment_prefixes='#',
                    strict=False
                )
                setup.read('setup.ini')

                date_time_setup = setup['date_time']

                true_or_false_end_ischecked = date_time_setup.getboolean('end_ischecked')

                date_time_end_str = date_time_setup['end']
                date_time_end_datetime = datetime.strptime(date_time_end_str, "%d/%m/%Y %H:%M")

                if true_or_false_end_ischecked is True:
                    ui.label_58.setText(
                        '*** Trading Started - Time End is checked - ' + str(date_time_end_datetime) + ' ***'
                    )
                    connect.logwriter(
                        '*** Trading Started - Time End is checked - ' + str(date_time_end_datetime) + ' ***'
                    )
                else:
                    ui.label_58.setText('*** Trading Started - Time End is NOT checked ***')
                    connect.logwriter('*** Trading Started - Time End is NOT checked ***')

                green_icon = "./green_led_icon.png"
                ui.label_62.setPixmap(QtGui.QPixmap(green_icon))

                ui.pushButton.setText('Trading\nStarted')
            elif info == 'date_time_start':
                setup = ConfigParser(
                    allow_no_value=True,
                    inline_comment_prefixes='#',
                    strict=False
                )
                setup.read('setup.ini')

                date_time_setup = setup['date_time']

                date_time_start_str = date_time_setup['start']
                date_time_start_datetime = datetime.strptime(date_time_start_str, "%d/%m/%Y %H:%M")

                ui.label_58.setText('*** Waiting for Time Start - ' + str(date_time_start_datetime) + ' - ***')
                connect.logwriter('*** Waiting for Time Start - ' + str(date_time_start_datetime) + ' - ***')

                green_icon = "./red_led_icon.png"
                ui.label_62.setPixmap(QtGui.QPixmap(green_icon))

                ui.pushButton.setText('Waiting for\nTime')
            else:
                ui.label_58.setText('********** ERROR 8500 **********')
                connect.logwriter('********** ERROR 8500 **********')
        except Exception as error2:
            from connection_spread import connect
            connect.logwriter(str(error2) + ' Error Code:: 8504')
            list_monitor_log.append(str(error2) + ' Error Code:: 8504')
            time.sleep(3)
            pass
        finally:
            pass

    def start_signal_2():
        ui.label_58.show()
        ui.label_58.setText(
            '*** Trading Completed at ' + str(datetime.now().strftime('%d/%m/%Y %H:%M:%S')) + ' ***'
        )

    def start_signal_3():
        from connection_spread import connect
        ui.label_58.show()
        ui.label_58.setText(
            '*** Trading Stopped at ' + str(datetime.now().strftime('%d/%m/%Y %H:%M:%S')) + ' ***'
        )
        connect.logwriter(
            '*** Trading Stopped at ' + str(datetime.now().strftime('%d/%m/%Y %H:%M:%S')) + ' ***'
        )

    def start_signal_4():
        red_icon = "./red_led_icon.png"
        ui.label_62.setPixmap(QtGui.QPixmap(red_icon))

        ui.label_58.show()
        ui.label_58.setText(
            '********** TRADING FINISHED at ' + str(datetime.now().strftime('%d/%m/%Y %H:%M:%S')) + ' **********'
        )

    def structure_cost_link():
        ConditionsCheck().structure_cost_for_tab_run_trading_and_btc_index_and_greeks_when_started_trading()

    def position_preview_to_gui_2():
        from connection_spread import connect
        max_position_instrument1_for_gui = Config().max_position_from_position_saved_and_instrument_amount(
            instrument_number=1)
        max_position_instrument2_for_gui = Config().max_position_from_position_saved_and_instrument_amount(
            instrument_number=2)
        max_position_instrument3_for_gui = Config().max_position_from_position_saved_and_instrument_amount(
            instrument_number=3)
        max_position_instrument4_for_gui = Config().max_position_from_position_saved_and_instrument_amount(
            instrument_number=4)

        textedit_balance_after_signal_dict = dict()
        textedit_balance_after_signal_dict.clear()

        textedit_balance_after_signal_dict['Instrument 1'] = str(max_position_instrument1_for_gui)
        textedit_balance_after_signal_dict['Instrument 2'] = str(max_position_instrument2_for_gui)
        textedit_balance_after_signal_dict['Instrument 3'] = str(max_position_instrument3_for_gui)
        textedit_balance_after_signal_dict['Instrument 4'] = str(max_position_instrument4_for_gui)

        sinal.textedit_balance_after_signal.emit(textedit_balance_after_signal_dict)
        try:
            if 'ERROR' in str(max_position_instrument1_for_gui):
                connect.logwriter('********** ERROR - Instrument 1 Syntax ERROR -  Error Code 9252 - **********')
            else:
                pass
            if 'ERROR' in str(max_position_instrument2_for_gui):
                connect.logwriter('********** ERROR - Instrument 1 Syntax ERROR -  Error Code 9256 - **********')
            else:
                pass
            if 'ERROR' in str(max_position_instrument3_for_gui):
                connect.logwriter('********** ERROR - Instrument 1 Syntax ERROR -  Error Code 9260 - **********')
            else:
                pass
            if 'ERROR' in str(max_position_instrument4_for_gui):
                connect.logwriter('********** ERROR - Instrument 1 Syntax ERROR -  Error Code 9264 - **********')
            else:
                pass
        except Exception as error3:
            from lists import list_monitor_log
            list_monitor_log.append(
                '********** ERROR - Instrument 1 Syntax ERROR -  Error Code 9269 - **********' + str(error3)
            )
            pass
        finally:
            pass

    def position_now2():
        from connection_spread import connect, led_color
        from lists import list_monitor_log

        instrument1_name = InstrumentsSaved().instrument_name_construction_from_file(instrument_number=1)
        instrument2_name = InstrumentsSaved().instrument_name_construction_from_file(instrument_number=2)
        instrument3_name = InstrumentsSaved().instrument_name_construction_from_file(instrument_number=3)
        instrument4_name = InstrumentsSaved().instrument_name_construction_from_file(instrument_number=4)

        a = instrument1_name
        b = instrument2_name
        c = instrument3_name
        d = instrument4_name

        if led_color() == 'red':
            sinal.msg_box_for_position_now_signal.emit()
            pass
        else:
            try:
                if a != 'Unassigned':
                    a1 = connect.get_position_size(instrument_name=a)
                else:
                    a1 = 'Unassigned'

                if b != 'Unassigned':
                    b1 = connect.get_position_size(instrument_name=b)
                else:
                    b1 = 'Unassigned'

                if c != 'Unassigned':
                    c1 = connect.get_position_size(instrument_name=c)
                else:
                    c1 = 'Unassigned'

                if d != 'Unassigned':
                    d1 = connect.get_position_size(instrument_name=d)
                else:
                    d1 = 'Unassigned'

                info1 = dict()
                info1['Instrument 1'] = str(a1)
                info1['Instrument 2'] = str(b1)
                info1['Instrument 3'] = str(c1)
                info1['Instrument 4'] = str(d1)

                info = info1

                sinal.position_now_signal.emit(info)

            except Exception as er:
                connect.logwriter(str(er) + ' Error Code:: 6778')
                list_monitor_log.append(str(er) + ' Error Code:: 6779')
                ui.textEdit_balance_2.clear()
                ui.textEdit_balance_2.setText(str(er) + ' Error Code:: 6781')
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Current Positions don´t checked')
                msg.setWindowTitle('***** ERROR *****')
                msg.exec_()
                pass
            finally:
                pass

    def print_greeks_by_instrument_2():
        import decimal

        instrument1_mark_greek_cost = Instruments().greeks_by_instruments(instrument_number=1)
        instrument1_vega = instrument1_mark_greek_cost['vega']
        instrument1_theta = instrument1_mark_greek_cost['theta']
        instrument1_rho = instrument1_mark_greek_cost['rho']
        instrument1_gamma = instrument1_mark_greek_cost['gamma']
        instrument1_delta = instrument1_mark_greek_cost['delta']

        instrument2_mark_greek_cost = Instruments().greeks_by_instruments(instrument_number=2)
        instrument2_vega = instrument2_mark_greek_cost['vega']
        instrument2_theta = instrument2_mark_greek_cost['theta']
        instrument2_rho = instrument2_mark_greek_cost['rho']
        instrument2_gamma = instrument2_mark_greek_cost['gamma']
        instrument2_delta = instrument2_mark_greek_cost['delta']

        instrument3_mark_greek_cost = Instruments().greeks_by_instruments(instrument_number=3)
        instrument3_vega = instrument3_mark_greek_cost['vega']
        instrument3_theta = instrument3_mark_greek_cost['theta']
        instrument3_rho = instrument3_mark_greek_cost['rho']
        instrument3_gamma = instrument3_mark_greek_cost['gamma']
        instrument3_delta = instrument3_mark_greek_cost['delta']

        instrument4_mark_greek_cost = Instruments().greeks_by_instruments(instrument_number=4)
        instrument4_vega = instrument4_mark_greek_cost['vega']
        instrument4_theta = instrument4_mark_greek_cost['theta']
        instrument4_rho = instrument4_mark_greek_cost['rho']
        instrument4_gamma = instrument4_mark_greek_cost['gamma']
        instrument4_delta = instrument4_mark_greek_cost['delta']

        idg1 = InstrumentsSaved().instrument_direction_construction_from_instrument_file(
            instrument_number=1)
        if idg1 == 'Unassigned':
            instrument1_amount_greeks = 0
        else:
            if idg1 == 'buy':
                instrument1_amount_greeks = abs(float(
                    InstrumentsSaved().instrument_amount_saved(instrument_number=1)))
            elif idg1 == 'sell':
                instrument1_amount_greeks = abs(float(
                    InstrumentsSaved().instrument_amount_saved(
                        instrument_number=1))) * -1
            else:
                instrument1_amount_greeks = 0

        idg2 = InstrumentsSaved().instrument_direction_construction_from_instrument_file(instrument_number=2)
        if idg2 == 'Unassigned':
            instrument2_amount_greeks = 0
        else:
            if idg2 == 'buy':
                instrument2_amount_greeks = abs(float(
                    InstrumentsSaved().instrument_amount_saved(instrument_number=2)))
            elif idg2 == 'sell':
                instrument2_amount_greeks = abs(float(
                    InstrumentsSaved().instrument_amount_saved(
                        instrument_number=2))) * -1
            else:
                instrument2_amount_greeks = 0

        idg3 = InstrumentsSaved().instrument_direction_construction_from_instrument_file(instrument_number=3)
        if idg3 == 'Unassigned':
            instrument3_amount_greeks = 0
        else:
            if idg3 == 'buy':
                instrument3_amount_greeks = abs(float(
                    InstrumentsSaved().instrument_amount_saved(instrument_number=3)))
            elif idg3 == 'sell':
                instrument3_amount_greeks = abs(float(
                    InstrumentsSaved().instrument_amount_saved(
                        instrument_number=3))) * -1
            else:
                instrument3_amount_greeks = 0

        idg4 = InstrumentsSaved().instrument_direction_construction_from_instrument_file(instrument_number=4)
        if idg4 == 'Unassigned':
            instrument4_amount_greeks = 0
        else:
            if idg4 == 'buy':
                instrument4_amount_greeks = abs(float(
                    InstrumentsSaved().instrument_amount_saved(instrument_number=4)))
            elif idg4 == 'sell':
                instrument4_amount_greeks = abs(float(
                    InstrumentsSaved().instrument_amount_saved(
                        instrument_number=4))) * -1
            else:
                instrument4_amount_greeks = 0

        instrument1_vega_total = float(instrument1_vega) * float(instrument1_amount_greeks)
        instrument2_vega_total = float(instrument2_vega) * float(instrument2_amount_greeks)
        instrument3_vega_total = float(instrument3_vega) * float(instrument3_amount_greeks)
        instrument4_vega_total = float(instrument4_vega) * float(instrument4_amount_greeks)

        instrument1_theta_total = float(instrument1_theta) * float(instrument1_amount_greeks)
        instrument2_theta_total = float(instrument2_theta) * float(instrument2_amount_greeks)
        instrument3_theta_total = float(instrument3_theta) * float(instrument3_amount_greeks)
        instrument4_theta_total = float(instrument4_theta) * float(instrument4_amount_greeks)

        instrument1_rho_total = float(instrument1_rho) * float(instrument1_amount_greeks)
        instrument2_rho_total = float(instrument2_rho) * float(instrument2_amount_greeks)
        instrument3_rho_total = float(instrument3_rho) * float(instrument3_amount_greeks)
        instrument4_rho_total = float(instrument4_rho) * float(instrument4_amount_greeks)

        instrument1_gamma_total = round(decimal.Context().create_decimal_from_float(
            instrument1_gamma * instrument1_amount_greeks), 5)
        instrument2_gamma_total = round(decimal.Context().create_decimal_from_float(
            instrument2_gamma * instrument2_amount_greeks), 5)
        instrument3_gamma_total = round(decimal.Context().create_decimal_from_float(
            instrument3_gamma * instrument3_amount_greeks), 5)
        instrument4_gamma_total = round(decimal.Context().create_decimal_from_float(
            instrument4_gamma * instrument4_amount_greeks), 5)

        instrument1_delta_total = float(instrument1_delta) * float(instrument1_amount_greeks)
        instrument2_delta_total = float(instrument2_delta) * float(instrument2_amount_greeks)
        instrument3_delta_total = float(instrument3_delta) * float(instrument3_amount_greeks)
        instrument4_delta_total = float(instrument4_delta) * float(instrument4_amount_greeks)

        print_greeks_by_instrument_dict = dict()

        print_greeks_by_instrument_dict['lineEdit_29'] = round(instrument1_delta_total, 6)
        print_greeks_by_instrument_dict['lineEdit_47'] = round(instrument2_delta_total, 6)
        print_greeks_by_instrument_dict['lineEdit_48'] = round(instrument3_delta_total, 6)
        print_greeks_by_instrument_dict['lineEdit_49'] = round(instrument4_delta_total, 6)

        print_greeks_by_instrument_dict['lineEdit_31'] = round(instrument1_theta_total, 6)
        print_greeks_by_instrument_dict['lineEdit_37'] = round(instrument2_theta_total, 6)
        print_greeks_by_instrument_dict['lineEdit_36'] = round(instrument3_theta_total, 6)
        print_greeks_by_instrument_dict['lineEdit_35'] = round(instrument4_theta_total, 6)

        print_greeks_by_instrument_dict['lineEdit_30'] = round(instrument1_gamma_total, 6)
        print_greeks_by_instrument_dict['lineEdit_44'] = round(instrument2_gamma_total, 6)
        print_greeks_by_instrument_dict['lineEdit_45'] = round(instrument3_gamma_total, 6)
        print_greeks_by_instrument_dict['lineEdit_46'] = round(instrument4_gamma_total, 6)

        print_greeks_by_instrument_dict['lineEdit_32'] = round(instrument1_vega_total, 6)
        print_greeks_by_instrument_dict['lineEdit_41'] = round(instrument2_vega_total, 6)
        print_greeks_by_instrument_dict['lineEdit_42'] = round(instrument3_vega_total, 6)
        print_greeks_by_instrument_dict['lineEdit_43'] = round(instrument4_vega_total, 6)

        print_greeks_by_instrument_dict['lineEdit_33'] = round(instrument1_rho_total, 6)
        print_greeks_by_instrument_dict['lineEdit_38'] = round(instrument2_rho_total, 6)
        print_greeks_by_instrument_dict['lineEdit_39'] = round(instrument3_rho_total, 6)
        print_greeks_by_instrument_dict['lineEdit_40'] = round(instrument4_rho_total, 6)

        sinal.print_greeks_by_instrument_signal.emit(print_greeks_by_instrument_dict)

    def update_position_and_amount_adjusted_and_print_gui():
        Config().position_before_trade_save()
        Instruments().amount_adjusted_save()
        Instruments().adjust_rate_trade_by_reduce_only_save()
        print_greeks_by_instrument_2()
        sinal.textedit_balance_settext_signal.emit(
            str(ConfigSaved().position_saved()))
        position_preview_to_gui_2()
        position_now2()
        Quote().quote_new_structure_cost_for_print_when_stopped_trading()
        # sinal.pushButton_request_options_structure_cost_signal.emit()  # = call Quote().quote_new()

    def start():
        import time
        from lists import list_monitor_log
        from connection_spread import led_color
        global trading_on_off
        global run_trade_future_on_off
        global run_trade_option_on_off
        global trading_on_off_for_msg
        global run_target_on_off
        global send_future_orders_while
        global dont_stop_trading_and_update_amount_adjusted

        trading_on_off = 'on'
        run_trade_option_on_off = 'on'
        run_trade_future_on_off = 'on'
        trading_on_off_for_msg = 'on'
        run_target_on_off = 'on'
        send_future_orders_while = True

        setup = ConfigParser(
            allow_no_value=True,
            inline_comment_prefixes='#',
            strict=False
        )
        setup.read('setup.ini')

        date_time_setup = setup['date_time']

        date_time_start_str = date_time_setup['start']
        date_time_start_datetime = datetime.strptime(date_time_start_str, "%d/%m/%Y %H:%M")
        date_time_start_stamp = date_time_start_datetime.timestamp()

        date_time_end_str = date_time_setup['end']
        date_time_end_datetime = datetime.strptime(date_time_end_str, "%d/%m/%Y %H:%M")
        date_time_end_stamp = date_time_end_datetime.timestamp()

        true_or_false_start_ischecked = date_time_setup.getboolean('start_ischecked')
        true_or_false_end_ischecked = date_time_setup.getboolean('end_ischecked')

        reduce_only_setup = setup['reduce_only']
        dont_stop_trading_and_update_amount_adjusted = reduce_only_setup.getboolean(
            'dont_stop_trading_and_update_amount_adjusted'
        )

        if true_or_false_start_ischecked is True:
            waiting_date_time_start = True
            counter_run_trade_option = 11

            sinal.start_signal_1.emit('date_time_start')

            while waiting_date_time_start is True and trading_on_off == 'on':
                try:
                    from connection_spread import connect

                    connect.logwriter(
                        '*** Time Start is checked - ' + str(date_time_start_datetime) + ' - ***'
                    )

                    if true_or_false_end_ischecked is True:
                        connect.logwriter('*** Time End is checked - ' + str(date_time_end_datetime) + ' ***')
                    else:
                        connect.logwriter('*** Time End is NOT checked ***')

                    if date_time_start_stamp >= datetime.now().timestamp():
                        connect.logwriter('*** Waiting for Time Start ***')
                        time.sleep(1)
                        try:
                            from connection_spread import connect
                            if led_color() == 'red':
                                list_monitor_log.append('********** Connection Offline **********')
                                time.sleep(3)
                                pass
                            else:
                                counter_run_trade_option = counter_run_trade_option - 1
                                sinal.chronometer_signal.emit(str(counter_run_trade_option))
                                if counter_run_trade_option == 0:
                                    structure_cost_link()
                                    list_monitor_log.append('***** Update Strategy cost,'
                                                            ' greeks and BTC index for tab Run *****')
                                    sinal.chronometer_signal.emit(str(counter_run_trade_option))
                                    counter_run_trade_option = 11
                                else:
                                    pass
                        except Exception as error2:
                            from connection_spread import connect
                            connect.logwriter(str(error2) + ' Error Code:: 8574')
                            list_monitor_log.append(str(error2) + ' Error Code:: 8574')
                            time.sleep(3)
                            pass
                        finally:
                            pass
                    else:
                        setup = ConfigParser(
                            allow_no_value=True,
                            inline_comment_prefixes='#',
                            strict=False
                        )
                        setup.read('setup.ini')
                        date_time_setup = setup['date_time']
                        date_time_setup_enable = date_time_setup.getboolean('date_time_enabled')

                        if date_time_setup_enable is True:
                            update_position_and_amount_adjusted_and_print_gui()

                            setup = ConfigParser(
                                allow_no_value=True,
                                inline_comment_prefixes='#',
                                strict=False
                            )
                            setup.read('setup.ini')
                            date_time_setup = setup['date_time']

                            date_time_setup['date_time_enabled'] = 'False'

                            with open('setup.ini', 'w') as configfile:
                                setup.write(configfile)

                            connect.logwriter('*** Date and time Enabled set False saved ***\n'
                                              '*** Positions before trades and amount adjusted uptaded ***')
                        else:
                            pass

                        connect.logwriter('*** Start Trading by Time ***')
                        waiting_date_time_start = False

                except Exception as error2:
                    from connection_spread import connect
                    connect.logwriter(str(error2) + ' Error Code:: 8587')
                    list_monitor_log.append(str(error2) + ' Error Code:: 8587')
                    time.sleep(3)
                    pass
                finally:
                    pass
        else:
            try:
                from connection_spread import connect
                connect.logwriter('*** Time Start is NOT checked ***')
            except Exception as error2:
                from connection_spread import connect
                connect.logwriter(str(error2) + ' Error Code:: 8590')
                list_monitor_log.append(str(error2) + ' Error Code:: 8590')
                time.sleep(3)
                pass
            finally:
                pass

        if true_or_false_end_ischecked is True:
            if date_time_end_stamp < datetime.now().timestamp():
                try:
                    from connection_spread import connect
                    connect.logwriter('*** Time End is checked - ' + str(date_time_end_datetime) + ' ***')
                    connect.logwriter('*** Trading Stopped by Timeout - ' + str(date_time_end_datetime) + ' ***')
                except Exception as error2:
                    from connection_spread import connect
                    connect.logwriter(str(error2) + ' Error Code:: 8610')
                    list_monitor_log.append(str(error2) + ' Error Code:: 8610')
                    time.sleep(3)
                    pass
                finally:
                    trading_on_off = 'off'
                    run_trade_future_on_off = 'off'
                    run_trade_option_on_off = 'off'
                    run_target_on_off = 'off'
                    trading_on_off_for_msg = 'off'
                    send_future_orders_while = False
            else:
                try:
                    from connection_spread import connect
                    connect.logwriter('*** Time End is checked - ' + str(date_time_end_datetime) + ' ***')
                except Exception as error2:
                    from connection_spread import connect
                    connect.logwriter(str(error2) + ' Error Code:: 8621')
                    list_monitor_log.append(str(error2) + ' Error Code:: 8621')
                    time.sleep(3)
                    pass
                finally:
                    pass
        else:
            try:
                from connection_spread import connect
                connect.logwriter('*** Time End is NOT checked ***')
            except Exception as error2:
                from connection_spread import connect
                connect.logwriter(str(error2) + ' Error Code:: 8633')
                list_monitor_log.append(str(error2) + ' Error Code:: 8633')
                time.sleep(3)
                pass
            finally:
                pass

        if dont_stop_trading_and_update_amount_adjusted is True:
            pass
        else:
            pass

        sinal.start_signal_1.emit('start')

        while trading_on_off == 'on':
            try:
                from connection_spread import connect
                # RUN TRADE
                if trading_on_off != 'on':
                    break
                else:
                    pass
                counter_run_trade_option = 11
                while run_trade_option_on_off == 'on':
                    try:
                        from connection_spread import connect
                        if led_color() == 'red':
                            list_monitor_log.append('********** Connection Offline **********')
                            time.sleep(3)
                            pass
                        else:
                            counter_run_trade_option = counter_run_trade_option - 1
                            sinal.chronometer_signal.emit(str(counter_run_trade_option))

                            if dont_stop_trading_and_update_amount_adjusted is True:
                                update_position_and_amount_adjusted_and_print_gui()
                                list_monitor_log.append(
                                    '*********** Updated Position and Amounts Adjusteds '
                                    '***********')
                            else:
                                pass

                            if counter_run_trade_option == 0:
                                ConditionsCheck(). \
                                    structure_cost_for_tab_run_trading_and_btc_index_and_greeks_when_started_trading()
                                list_monitor_log.append('***** Update Strategy cost,'
                                                        ' greeks and BTC index for tab Run *****')
                                sinal.chronometer_signal.emit(str(counter_run_trade_option))
                                counter_run_trade_option = 11
                            else:
                                pass

                            # Posição tem que ser menor que a quantidade que se quer negociar.
                            aa = ConditionsCheck().position_option_smaller_max_position_instruments_()
                            if aa == 'position_option_smaller_max_position_instruments_no':
                                if dont_stop_trading_and_update_amount_adjusted is True:
                                    list_monitor_log.append(
                                        '*********** Option Position Greater than or Equal to Maximum Position '
                                        '***********')
                                    list_monitor_log.append(
                                        '*********** Don`t Stop Trading Eanbled ***********')
                                    connect.logwriter(
                                        '*********** Option Position Greater than or Equal to Maximum Position '
                                        '***********')
                                    connect.logwriter(
                                        '*********** Don`t Stop Trading Eanbled ***********')
                                    run_trade_future()
                                    trading_on_off = 'on'
                                    run_trade_option_on_off = 'on'
                                    run_trade_future_on_off = 'on'
                                    trading_on_off_for_msg = 'on'
                                    run_target_on_off = 'on'
                                    send_future_orders_while = True
                                    pass
                                else:
                                    list_monitor_log.append(
                                        '*********** Option Position Greater than or Equal to Maximum Position '
                                        '***********')
                                    connect.logwriter(
                                        '*********** Option Position Greater than or Equal to Maximum Position '
                                        '***********')
                                    if run_trade_future_on_off == 'on':
                                        run_trade_future()
                                    else:
                                        run_trade_option_on_off = 'off'
                                        break
                            elif aa == 'position_option_smaller_max_position_instruments_ok':
                                list_monitor_log.append('*** Option Position Smaller Max Position ***')
                                run_target_on_off = 'on'  # para poder executar o targets_achieved() se ainda há options

                                if true_or_false_end_ischecked is True:
                                    if date_time_end_stamp < datetime.now().timestamp():
                                        trading_on_off = 'off'
                                        run_trade_future_on_off = 'off'
                                        run_trade_option_on_off = 'off'
                                        run_target_on_off = 'off'
                                        trading_on_off_for_msg = 'off'
                                        send_future_orders_while = False

                                        list_monitor_log.append('*** Trading Stopped by Timeout ***')
                                        connect.logwriter('*** Trading Stopped by Timeout ***')
                                    else:
                                        list_monitor_log.append('*** Trading time is NOT over ***')
                                else:
                                    pass

                                # Verifica se a diferança entre "mark price" e "market price" está maior que x%
                                bb = ConditionsCheck().min_max_price_option_buy_or_sell_order_by_mark_price()
                                if bb == 'ok':
                                    list_monitor_log.append('*** Ratio between Bid/Ask offer and Mark Price '
                                                            'OK (<30%) ***')
                                    list_monitor_log.append('*** Waiting for conditions to be filled ***')
                                    # Verifica se os alvos forma atingidos.
                                    cc = ConditionsCheck().targets_achieved()
                                    if cc == 'targets_ok':  # Verifica os targets
                                        list_monitor_log.append('*** Waiting to submit option orders ***')
                                        # verifica se todos instruments tem oferta no "book"
                                        bid_ask_offer = Quote().bid_ask_offer()
                                        if bid_ask_offer != 'waiting bid/ask offer':
                                            list_monitor_log.append('*** There are bid/ask offer - '
                                                                    'Waiting Send Orders ***')
                                            ConditionsCheck().send_options_orders()
                                            run_trade_future()
                                        else:
                                            list_monitor_log.append('*** WAITING FOR BID/ASK OFFER - '
                                                                    'There are NOT Bid/Ask offer ***')
                                            pass
                                    else:
                                        list_monitor_log.append(
                                            '***** WAITING FOR TARGETS *****')
                                        pass
                                elif bb == 'waiting trade':
                                    pass
                                else:
                                    connect.logwriter(
                                        '********** ERROR IN vavabot_spread.py Error Code:: 7474 **********')
                                    list_monitor_log.append('********** ERROR IN vavabot_spread.py '
                                                            'Error Code:: 7476 **********')
                                    pass
                            else:
                                connect.logwriter(
                                    '********** ERROR IN vavabot_spread.py Error Code:: 7480 **********')
                                list_monitor_log.append('******* ERROR IN vavabot_spread.py Error Code:: 7481 *******')
                                pass
                    except Exception as error2:
                        from connection_spread import connect
                        connect.logwriter(str(error2) + ' Error Code:: 7486')
                        list_monitor_log.append(str(error2) + ' Error Code:: 7487')
                        time.sleep(3)
                        pass
                    finally:
                        pass
                if trading_on_off_for_msg == 'on':
                    list_monitor_log.append('**************** NO MORE OPTION ORDERS FOR TRADING ****************')
                    pass
                elif trading_on_off_for_msg == 'off':
                    trading_on_off = 'off'
                    pass
                else:
                    connect.logwriter(
                        '********** ERROR IN vavabot_spread.py Error Code:: 7499 **********')
                    list_monitor_log.append('********** ERROR IN vavabot_spread.py Error Code:: 7500 **********')
                    pass

                if trading_on_off_for_msg == 'on':

                    sinal.start_signal_2.emit()

                    trading_on_off = 'off'
                elif trading_on_off == 'off':
                    pass
                else:
                    connect.logwriter(
                        '********** ERROR IN vavabot_spread.py Error Code:: 7512 **********')
                    list_monitor_log.append('********** ERROR IN vavabot_spread.py Error Code:: 7513 **********')
                    pass
            except Exception as er:
                from connection_spread import connect
                connect.logwriter(str(er) + ' Error Code:: 7517')
                list_monitor_log.append(str(er) + ' Error Code:: 7518')
                pass
            finally:
                pass
        if trading_on_off_for_msg == 'off':
            try:
                from connection_spread import connect
                list_monitor_log.append(
                    '********** TRADING STOPPED at ' + str(datetime.now().strftime('%d/%m/%Y %H:%M:%S')) + ' **********'
                )
                connect.logwriter(
                    '********** TRADING STOPPED at ' + str(datetime.now().strftime('%d/%m/%Y %H:%M:%S')) + ' **********'
                )
            except Exception as er:
                from connection_spread import connect
                connect.logwriter(str(er) + ' Error Code:: 8856')
                list_monitor_log.append(str(er) + ' Error Code:: 8856')
                pass
            finally:
                pass
            sinal.start_signal_3.emit()

            btc_index_print_start_thread()
            pass
        else:
            try:
                from connection_spread import connect
                list_monitor_log.append(
                    '********** TRADING FINISHED at ' + str(datetime.now().strftime('%d/%m/%Y %H:%M:%S')) +
                    ' **********'
                )
                connect.logwriter(
                    '********** TRADING FINISHED at ' + str(datetime.now().strftime('%d/%m/%Y %H:%M:%S')) +
                    ' **********'
                )
            except Exception as er:
                from connection_spread import connect
                connect.logwriter(str(er) + ' Error Code:: 8876')
                list_monitor_log.append(str(er) + ' Error Code:: 8876')
                pass
            finally:
                pass
            sinal.start_signal_4.emit()

            btc_index_print_start_thread()
            pass

    def start_thread_trade_signal():
        ui.pushButton_stop_arbitrage.setEnabled(True)
        ui.pushButton_start_trading.setEnabled(False)

        ui.pushButton_submit_new_credintals.setEnabled(False)
        ui.radioButton_testnet_true.setEnabled(False)
        ui.radioButton_2_testnet_false.setEnabled(False)
        ui.pushButton_submit_new_instruments.setEnabled(False)
        ui.pushButton_submit_new_plot_payoff.setEnabled(False)
        ui.pushButton_submit_new_targets.setEnabled(False)

        ui.lineEdit_orders_rate.setEnabled(False)
        ui.pushButton_orders_rate.setEnabled(False)

        ui.checkbox_date_time_start.setEnabled(False)
        ui.checkbox_date_time_end.setEnabled(False)
        ui.date_time_start.setEnabled(False)
        ui.date_time_end.setEnabled(False)

        ui.check_box_reduce_only_1.setEnabled(True)
        ui.check_box_reduce_only_2.setEnabled(True)
        ui.check_box_reduce_only_3.setEnabled(True)
        ui.check_box_reduce_only_4.setEnabled(True)
        Config().reduce_only_saved()
        ui.check_box_reduce_only_1.setEnabled(False)
        ui.check_box_reduce_only_2.setEnabled(False)
        ui.check_box_reduce_only_3.setEnabled(False)
        ui.check_box_reduce_only_4.setEnabled(False)

    def start_thread_trade():
        import threading

        sinal.start_thread_trade_signal.emit()

        start_thread_trade_clicked = threading.Thread(daemon=True, target=start)
        start_thread_trade_clicked.start()

    def start_trading():
        global index_greeks_print_on_off

        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText('Start Trading?')
        msg.setWindowTitle('*** WARNING ***')
        msg.addButton('Ok', msg.AcceptRole)
        msg.addButton('Cancel', msg.RejectRole)
        pass

        if msg.exec_() == msg.Rejected:
            index_greeks_print_on_off = 'off'  # ok clicked
        else:
            pass  # cancel clicked

    def stop_trading():
        global trading_on_off
        global run_trade_option_on_off
        global run_trade_future_on_off
        global run_target_on_off
        global trading_on_off_for_msg
        global send_future_orders_while
        global dont_stop_trading_and_update_amount_adjusted

        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText('Stop Trading?')
        msg.setWindowTitle('*** WARNING ***')
        msg.addButton('Ok', msg.AcceptRole)
        msg.addButton('Cancel', msg.RejectRole)
        pass

        if msg.exec_() == msg.Rejected:  # ok clicked
            trading_on_off = 'off'
            run_trade_future_on_off = 'off'
            run_trade_option_on_off = 'off'
            run_target_on_off = 'off'
            trading_on_off_for_msg = 'off'
            send_future_orders_while = False
            dont_stop_trading_and_update_amount_adjusted = False
        else:
            pass  # cancel clicke

    sinal.textEdit_monitor_signal.connect(receive_signal_por_print_monitor)
    sinal.led_color_green_signal.connect(receive_led_green_for_monitor)
    sinal.led_color_red_signal.connect(receive_led_red_for_monitor)
    sinal.error_in_list_monitor_signal.connect(receive_error_in_list_monitor_signal)
    sinal.start_thread_trade_signal.connect(start_thread_trade_signal)
    sinal.start_signal_1.connect(start_signal_1)
    sinal.start_signal_2.connect(start_signal_2)
    sinal.start_signal_3.connect(start_signal_3)
    sinal.start_signal_4.connect(start_signal_4)
    sinal.structure_cost_for_tab_run_trading_and_btc_index_and_greeks_when_started_trading_signal_0.connect(
        structure_cost_for_tab_run_trading_and_btc_index_and_greeks_when_started_trading_signal_0)
    sinal.structure_cost_for_tab_run_trading_and_btc_index_and_greeks_when_started_trading_signal_1.connect(
        structure_cost_for_tab_run_trading_and_btc_index_and_greeks_when_started_trading_signal_1)
    sinal.structure_cost_for_tab_run_trading_and_btc_index_and_greeks_when_started_trading_signal_2.connect(
        structure_cost_for_tab_run_trading_and_btc_index_and_greeks_when_started_trading_signal_2)
    sinal.structure_mark_greek_cost_signal.connect(structure_mark_greek_cost_signal)
    sinal.btc_index_print_start_thread_signal.connect(btc_index_print_start_thread_signal)
    sinal.index_btc_print_signal.connect(receive_index_btc_print_signal)
    sinal.greeks_signal.connect(receive_greeks_signal)
    sinal.greeks_signal1.connect(receive_greeks_signal1)
    sinal.chronometer_signal.connect(receive_chronometer_signal)
    sinal.btc_index_print_gui_adjusts_signal.connect(receive_btc_index_print_gui_adjusts_signal)
    sinal.quote_new_structure_cost_for_print_when_stopped_trading_signal1.connect(
        quote_new_structure_cost_for_print_when_stopped_trading_signal1)
    sinal.position_now_signal.connect(position_now_signal)
    sinal.msg_box_for_position_now_signal.connect(msg_box_for_position_now_signal)
    sinal.print_greeks_by_instrument_signal.connect(print_greeks_by_instrument_signal)
    sinal.textedit_instruments_saved_settext_signal.connect(textedit_instruments_saved_settext_signal)
    sinal.msg_box_for_thread_when_open_app1_signal.connect(msg_box_for_thread_when_open_app1_signal)
    sinal.textedit_balance_settext_signal.connect(textedit_balance_settext_signal)
    sinal.quote_new_when_open_app_signal1.connect(quote_new_when_open_app_signal1)
    sinal.last_trade_instrument_conditions_quote_signal.connect(last_trade_instrument_conditions_quote_signal)
    sinal.position_now_when_open_app_signal.connect(position_now_when_open_app_signal)
    sinal.textedit_balance_after_signal.connect(textedit_balance_after_signal)
    sinal.pushbutton_2_click_signal.connect(clear_monitor_signal)
    monitor_thread = threading.Thread(daemon=True, target=lists_monitor)
    monitor_thread.start()
    ui.pushButton_start_print_loglog.hide()
    ui.label_58.hide()
    ui.pushButton_2.hide()
    ui.pushButton_2.setEnabled(False)
    ui.pushButton.setEnabled(False)
    ui.pushButton_stop_arbitrage.setEnabled(False)
    ui.pushButton_start_trading.clicked.connect(start_trading)
    ui.pushButton_stop_arbitrage.clicked.connect(stop_trading)
    ui.textEdit_monitor.textChanged.connect(receive_autoscroll_monitor)
    ui.checkBox_autoScrollBar.clicked.connect(receive_autoscroll_monitor)
    btc_index_print_start_thread()


# noinspection PyShadowingNames
def about(ui):
    def disagree_license_when_open_app():
        ui.tab_credentials.setDisabled(True)
        ui.tab_instruments.setDisabled(True)
        ui.tab_targets.setDisabled(True)
        ui.tab_strutucture_quote.setDisabled(True)
        ui.tab_run_trading.setDisabled(True)

    def disagree_license():
        from connection_spread import connect

        ui.tab_credentials.setDisabled(True)
        ui.tab_instruments.setDisabled(True)
        ui.tab_targets.setDisabled(True)
        ui.tab_strutucture_quote.setDisabled(True)
        ui.tab_run_trading.setDisabled(True)

        connect.logwriter('License: I Disagreed')

        ui.radioButton_agree.setEnabled(False)
        ui.radioButton_disagree.setEnabled(False)

    def agree_license():
        from connection_spread import connect

        ui.tab_credentials.setDisabled(False)
        ui.tab_instruments.setDisabled(False)
        ui.tab_targets.setDisabled(False)
        ui.tab_strutucture_quote.setDisabled(False)
        ui.tab_run_trading.setDisabled(False)

        connect.logwriter('License: I Agreed')

        ui.radioButton_agree.setEnabled(False)
        ui.radioButton_disagree.setEnabled(False)

    disagree_license_when_open_app()
    ui.radioButton_agree.clicked.connect(agree_license)
    ui.radioButton_disagree.clicked.connect(disagree_license)


# noinspection PyShadowingNames
def add_widges(ui):
    # ADD check_box_dont_stop_trading
    check_box_dont_stop_trading = QtWidgets.QCheckBox(ui.frame_2)

    def set_check_box_dont_stop_trading():
        check_box_dont_stop_trading.setGeometry(QtCore.QRect(510, 0, 140, 40))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setPointSize(8)
        font.setBold(True)
        check_box_dont_stop_trading.setFont(font)
        check_box_dont_stop_trading.setObjectName("check_box_reduce_only_9")
        check_box_dont_stop_trading.setText('Don`t Stop Trading\neven if there are no\norders to be sent')

    def dont_stop_trading_and_update_amount_adjusted_save():
        if check_box_dont_stop_trading.isChecked() is True:
            print('test')

    set_check_box_dont_stop_trading()
    check_box_dont_stop_trading.stateChanged.connect(dont_stop_trading_and_update_amount_adjusted_save)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    credentials(ui=ui)
    config(ui=ui)
    quote(ui=ui)
    run(ui=ui)
    instruments(ui=ui)
    about(ui=ui)
    add_widges(ui=ui)
    sys.exit(app.exec_())
