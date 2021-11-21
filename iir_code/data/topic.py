class Topic(object):
    id: str
    title: str
    description: str

    def __init__(self, id: str, title: str, description: str):
        self.id = id
        self.title = title
        self.description = description
