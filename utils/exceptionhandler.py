from rest_framework.views import exception_handler
from rest_framework.exceptions import ErrorDetail
import json
from rest_framework import status

def custom_exception_handler(exc,context):
    
    handlers={
        'ValidationError':_handle_ValidationError,
        'Http404':_handle_generic_error,
        'PermissionDenied':_handle_generic_error,
        'NotAuthenticated':_handle_authentication_error,
        'InvalidToken':_handle_authentication_tokrn_perm,
        'AuthenticationFailed':_handle_authication_fail,
        'MethodNotAllowed':_handle_MethodNotAllowed,
        'ValueError': _handle_ValueError,
    }


    response=exception_handler(exc,context)
    
    if isinstance(response.data, list):
        pass
    else:
        if response is not None:
            response.data['status_code']=response.status_code
        
    
    exception_class=exc.__class__.__name__

    if exception_class in handlers:
        return handlers[exception_class](exc,context,response)
    return response

    
# Handaling


# 1 not_auth Hadling
def _handle_authentication_error(exc,context,response):
    error=response.data 
    response.data={
        'status':response.status_code,
        'message':error['detail'],
        'data':'{}'
    }

    return response

# 2 auth token handling
def _handle_authentication_tokrn_perm(exc,context,response):
    error=response.data    
    response.data={
        'status':response.status_code,
        'message':error['detail'],
        'data':'{}'
    }

    return response


#3 Validation Handing
def _handle_ValidationError(exc,context,response):
    if isinstance(response.data, list):
        # print('data', response.data)
        response.data={
            'status': status.HTTP_400_BAD_REQUEST,
            'message':response.data[0],
            'data':{}
        }
        # pass
    else:
        keys=list(response.data.keys())
        values=list(response.data.values())
        print(response.data)
        response.data={
            'status':response.status_code,
            'message':keys[0]+" "+values[0][0],
            'data':{}
        }
    return response


#authication fail hanindaling 
def _handle_authication_fail(exc,context,response):
    errors=[]
    for  i in response.data:
        print(i)
        if i != "status_code":
            a=response.data[i]
            op = a
            errors.append(op.title())        
    response.data={
        'status':response.status_code,
        'message':errors[0],
        'data':'{}'
    }

    return response



def _handle_MethodNotAllowed(exc,context,response):
    error=response.data   
    response.data={
        'status':response.status_code,
        'message':error['detail'],
        'data':'{}'
    }

    return response

def _handle_ValueError(exc, context,response):
    error = response.data
    response.data={
        'status': response.status_code,
        'message': error['detail']
    }
    return response

def _handle_generic_error(exc,context,response):
    return response

