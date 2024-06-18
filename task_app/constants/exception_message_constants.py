from rest_framework import status

NOTHING_TO_UPDATE_MSG = "Updated fields have the same values as in the object. The update did not happen."

NO_CONTENT_EXCEPTION_DATA = {"data": {}, "status_code": status.HTTP_204_NO_CONTENT}

NOTHING_TO_UPDATE_DATA = {"data": NOTHING_TO_UPDATE_MSG, "status_code": status.HTTP_200_OK}

