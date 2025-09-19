import hashlib
from rest_framework import status
from rest_framework.response import Response


class CustomResponse:
    @staticmethod
    def success(message=None, data=None, status_code=status.HTTP_200_OK):
        response = {"success": True}
        if message:
            response["message"] = message
        if data is not None:
            response["data"] = data
        return Response(response, status=status_code)

    @staticmethod
    def error(message=None, errors=None, status_code=status.HTTP_400_BAD_REQUEST):
        response = {"success": False}
        if message:
            response["message"] = message
        if errors is not None:
            response["errors"] = errors
        return Response(response, status=status_code)