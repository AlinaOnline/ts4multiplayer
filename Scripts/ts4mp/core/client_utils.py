import ts4mp.core.overrides.mp_essential_overrides as essential_overrides
from ts4mp.debug.log import ts4mp_log

def on_successful_client_connect():
    essential_overrides.override_functions_depending_on_client_or_not(True)
    ts4mp_log("client state", "Successful client connect")