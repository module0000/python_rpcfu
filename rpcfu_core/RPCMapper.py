from rpc_controllers import tests


class InsufficientArguments(Exception):
    """Exception for insufficient arguments passed from web client to RPC"""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class RPCMapper(object):
    """"Mapper to connect URLs with a module's functions"""

    # Override __call__ so we can send requests to the appropriate module and function
    def __call__(self, url, **args):
        # URL's appear like 1) /foo/bar or 2) /foo
        if url.find("/") == -1:  # catches urls like /foo
            rpcfu_module = None
            rpcfu_function = url
        else:  # catches urls like /foo/bar
            rpcfu_module = url[:url.find("/")]
            rpcfu_function = url[url.find("/") + 1:]

        # Calls individual functions from within imported modules
        if rpcfu_module == "tests":
            rpcfu_module = tests
        elif rpcfu_module is None:  # Module to receive calls when no module is specified
            rpcfu_module = tests

        try:
            if hasattr(rpcfu_module, rpcfu_function):
                return getattr(rpcfu_module, rpcfu_function)(**args)
            else:
                return {"error": "RPC '%s' does not exist" % url}
        except TypeError as e:
                return {"error": e.args}
        except InsufficientArguments as e:
            #This exception should be thrown manually - eg a provided dict is missing expected fields
            return {"error": "insufficient arguments", "missing arguments": e.value}
