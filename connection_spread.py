
from vavabot_options_spread_6_1_2 import Deribit, CredentialsSaved
import time
from lists import list_monitor_log
import threading

connect = Deribit(client_id=CredentialsSaved.api_secret_saved(),
                  client_secret=CredentialsSaved.secret_key_saved(),
                  wss_url=CredentialsSaved.url())

led = 'red'


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
            connect_set_heartbeat = connect.set_heartbeat()
            if connect_set_heartbeat == 'ok':
                list_monitor_log.append('connection ok')
                led = 'green'
                time.sleep(2)
                pass
            elif connect_set_heartbeat == 'too_many_requests':
                list_monitor_log.append(str('***************** ERROR too_many_requests ******************'))
                connect.logwriter(str('***************** ERROR too_many_requests ******************'))
                connect.cancel_all()
                time.sleep(10)
                connect.cancel_all()
            else:
                list_monitor_log.append('********** Offline - Connection ERROR **********')
                connect.logwriter(str('********** OffLine - Connection ERROR **********'))
                led = 'red'
                time.sleep(2)
                connect = Deribit(client_id=CredentialsSaved.api_secret_saved(),
                                  client_secret=CredentialsSaved.secret_key_saved(),
                                  wss_url=CredentialsSaved.url())
                connect_set_heartbeat2 = connect.set_heartbeat()
                if connect_set_heartbeat2 == 'ok':
                    list_monitor_log.append(str('***************** Reeturn Connection ******************'))
                    connect.logwriter(str('***************** Reeturn Connection ******************'))
                    connect.cancel_all()
                    time.sleep(2)
                elif connect_set_heartbeat2 == 'too_many_requests':
                    list_monitor_log.append(str('***************** ERROR too_many_requests ******************'))
                    connect.logwriter(str('***************** ERROR too_many_requests ******************'))
                    connect.cancel_all()
                    time.sleep(10)
                    connect.cancel_all()
                    pass
                else:
                    pass

        except Exception as e:
            led = 'red'
            time.sleep(10)
            list_monitor_log.append('********** Thread_connection - Connection ERROR ********** ' + str(e))
            connect.logwriter('********** Thread_connection - Connection ERROR ********** ' + str(e))
            pass
        finally:
            pass


run_thread = threading.Thread(daemon=True, target=connection)
run_thread.start()
