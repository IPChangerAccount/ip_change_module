import sys
import traceback

from .ip_operations import NetworkHandler
from .API_core.api_talker import ApiRequest


def change_ip() -> bool:
    """Tries to change current machine IP.

    Returns:
        bool: True if IP change was successful. False otherwise.
    """

    result = False

    try:
        print('\n\nStarting get new IP procedure...')
        conn_details = NetworkHandler.get_connection_details()

        api_request = ApiRequest(conn_details[NetworkHandler.DEFAULT_GATEWAY])
        print('    Requesting new gateway...')
        new_gate = api_request.get_new_gate()
        print(f'    New gateway {new_gate} received. Applying...')
        

        if NetworkHandler.change_default_gateway(new_gate, conn_details):
            api_request.confirm_gate_usage_towards_api(new_gate)
            result = True
            print('Success! IP changed.')
        else:
            # TODO Here send failed result to the gateway
            print('FAILED! Please contact support.')

    except Exception as ex:
        print(sys.exc_info()[0])
        print(traceback.format_exc())

        
        err_text = \
          f'\nAN ERROR OCCURRED! Error text: {str(ex)}. '\
           + '\nPlease contact support.\n'

        print(err_text)

    return result
