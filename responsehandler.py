class ResponseHandler:

    responses = 0

    def __init__(self) -> None:
        pass

    def handle_response(self, resp):

        return

    def handle_error(self, err):

        return

    def handle_prediction(self, response_htm):
        # TODO get data (or other resource) and interpret it, post it, save it

        return

    def sum_responses(self, a):
        return lambda a : a + self.responses
