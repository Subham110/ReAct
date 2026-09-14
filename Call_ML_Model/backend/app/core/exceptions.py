class BaseAgentException(Exception):
    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

class KNNServiceUnavailableException(BaseAgentException):
    def __init__(self, detail: str = "ML_Model_KNN microservice is unreachable."):
        super().__init__(message=detail, status_code=503)

class KNNServiceErrorException(BaseAgentException):
    def __init__(self, detail: str):
        super().__init__(message=detail, status_code=502)

class InvalidFlowerDimensionsException(BaseAgentException):
    def __init__(self, detail: str):
        super().__init__(message=detail, status_code=422)

class AgentExecutionException(BaseAgentException):
    def __init__(self, detail: str):
        super().__init__(message=detail, status_code=500)

KNNServiceUnavailable = KNNServiceUnavailableException
KNNServiceError = KNNServiceErrorException
InvalidFlowerDimensions = InvalidFlowerDimensionsException
AgentExecutionError = AgentExecutionException

