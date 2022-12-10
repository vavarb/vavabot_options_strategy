
from vavabot_options_strategy_9_2 import Deribit, CredentialsSaved, ConfigSaved
import time
from lists import list_monitor_log
import threading
global connect

ConfigSaved().remove_log_spread_log_if_bigger_500kb_when_open_app()
ConfigSaved().setup_ini_check()
led = 'red'


def connection1():
    global connect
    global led
    connect = Deribit(client_id=CredentialsSaved.api_secret_saved(),
                      client_secret=CredentialsSaved.secret_key_saved(),
                      wss_url=CredentialsSaved.url())
    connection_test = connect.test()
    if 'version' in str(connection_test):
        connect.logwriter('*** First Connection - connection ok ***')
        led = 'green'
        hello = connect.hello()
        connect.logwriter(str(hello))
        time.sleep(2)

        pass
    else:
        list_monitor_log.append('********** First Connection - Connection Error **********')
        set_led_red()


def set_led_red():
    global led
    led = 'red'


def set_led_green():
    global led
    led = 'green'


def led_color():
    global led
    led_color1 = led
    return str(led_color1)


def connection():
    global connect
    global led

    while True:
        try:
            global connect
            connection_test = connect.test()
            if 'version' in str(connection_test):
                list_monitor_log.append('* Thread_connection - connection ok *')
                time.sleep(2)
                connect.cancel_all()
                set_led_green()
                break
            elif 'too_many_requests' in str(connection_test) or '10028' in str(connection_test):
                list_monitor_log.append(str('***************** Thread_connection - ERROR too_many_requests '
                                            '******************'))
                connect.logwriter(str('***************** Thread_connection - ERROR too_many_requests '
                                      '******************'))
                connect.cancel_all()
                time.sleep(10)
                connect.cancel_all()
            else:
                list_monitor_log.append('********** Thread_connection - Offline - Connection ERROR **********')
                connect.logwriter(str('********** Thread_connection -  OffLine - Connection ERROR **********'))
                led = 'red'
                time.sleep(2)
                connect = Deribit(client_id=CredentialsSaved.api_secret_saved(),
                                  client_secret=CredentialsSaved.secret_key_saved(),
                                  wss_url=CredentialsSaved.url())
                connection_test2 = connect.test()
                if 'version' in str(connection_test2):
                    list_monitor_log.append(str('***************** Thread_connection - Reeturn Connection '
                                                '******************'))
                    connect.logwriter(str('***************** Thread_connection - Reeturn Connection '
                                          '******************'))
                    connect.cancel_all()
                    set_led_green()
                    break
                elif 'too_many_requests' in str(connection_test2) or '10028' in str(connection_test2):
                    list_monitor_log.append(str('***************** Thread_connection - ERROR too_many_requests '
                                                '******************'))
                    connect.logwriter(str('***************** Thread_connection - ERROR too_many_requests '
                                          '******************'))
                    connect.cancel_all()
                    time.sleep(10)
                    connect.cancel_all()
                else:
                    pass

        except Exception as e:
            led = 'red'
            time.sleep(10)
            list_monitor_log.append('********** Thread_connection ERROR: ' + str(e) + ' - Offline - **********')
            connect.logwriter('********** Thread_connection ERROR: ' + str(e) + ' - Offline - **********')
            connect = Deribit(client_id=CredentialsSaved.api_secret_saved(),
                              client_secret=CredentialsSaved.secret_key_saved(),
                              wss_url=CredentialsSaved.url())
            connect.cancel_all()
            time.sleep(2)
            connect.cancel_all()
            pass
        finally:
            pass


run_thread = threading.Thread(daemon=True, target=connection, name='run_thread')


def connection_thread():
    global run_thread
    run_thread = threading.Thread(daemon=True, target=connection, name='run_thread')
    run_thread.start()
