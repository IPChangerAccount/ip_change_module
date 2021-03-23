import requests
import logging

from .constants_change_ip import *
class ApiTalker:
    
    API_IP = 'http://192.168.99.254'

    URL_BASE = API_IP + '/?' + RP_REQ_OPERATION + '={op}&{pars_pairs}'

    @classmethod
    def get_new_gateway(cls, 
                        prev_failed_gates : list, 
                        last_failed_gate : str,
                        prev_gate : str):

        current_gate_param = f'{RP_PREV_GATE}={prev_gate}'

        params = current_gate_param
        
        if prev_failed_gates != None and len(prev_failed_gates) > 0:
            fg_as_str = ','.join(prev_failed_gates)
            failed_gates_param = f'{RP_FAILED_GATES}={fg_as_str}'
            params += f'&{failed_gates_param}'

        if last_failed_gate != None:
            las_fg_param = f'{RP_LAST_FAIL_GATE}={last_failed_gate}'
            params += f'&{las_fg_param}'

        req_url = cls.URL_BASE.format(op         = OP_NEW_GATE,
                                      pars_pairs = params)


        req_res = requests.get(req_url)  

        return req_res.status_code, req_res.json()


    @classmethod
    def finish_ip_change(cls, prev_gate : str, new_gate : str):

        prev_gate_param = f'{RP_PREV_GATE}={prev_gate}'   
        new_gate_param = f'{RP_SUCCESS_GATE}={new_gate}'

        params ='&'.join([prev_gate_param, new_gate_param])


        req_url = cls.URL_BASE.format(op         = OP_FIN_IP_CHANGE,
                                      pars_pairs = params)


        req_res = requests.get(req_url)  

        return req_res.status_code, req_res.json


class ApiRequest:

    failed_gates     = None
    last_failed_gate = None
    current_gate     = None
    successful_gate  = None

    def __init__(self, curr_gate) -> None:
        self.current_gate = curr_gate
        self.failed_gates = list()


    def mark_gate_as_failed(self, failed_gate):
        self.failed_gates.append(failed_gate)
        self.last_failed_gate = failed_gate

    def get_new_gate(self):

        new_gate = None
        
        rc, res = ApiTalker.get_new_gateway(self.failed_gates, 
                                            self.last_failed_gate, 
                                            self.current_gate)

        if rc == RC_OK:
            new_gate = res.get(NEW_GATEWAY)
 
            logging.debug(f'Received new gate: {new_gate}')
        else:
            # TODO raise exception
            # Handle the exception in top level
            # Log exception for user and tell him contact suppot.

            raise ValueError('Could not get an available gateway.')

        return new_gate

    def confirm_gate_usage_towards_api(self, new_gate):
        rc, res = ApiTalker.finish_ip_change(self.current_gate, 
                                             new_gate)


        if rc == RC_OK:
            logging.debug('Gate change finished.')
            
        else:
            # TODO raise exception
            # Handle the exception in top level
            # Log exception for user and tell him contact suppot.
            pass

        return res

                                            




