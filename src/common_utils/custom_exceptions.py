

class ResponseTextByTagsNotFoundError(Exception):
    def __init__(self):
        super().__init__(self, 'Response Text By Tags Not Found')


class CollectionAlreadyExistsInDatabaseError(Exception):
    def __init__(self):
        super().__init__(self, 'Collection Already Exists In Database')


class CollectionNotExistsInDatabaseError(Exception):
    def __init__(self):
        super().__init__(self, 'Collection Not Exists In Database')


