from enums import Type, Source, ToPost

class Content():
    content_type = ""
    source_type = ""
    source_link = ""
    text = ""
    media_url_list = []

    def __init__(self, _id, content_type, source_type, source_link, text, media_url_list):
        self.id = _id
        self.content_type = content_type
        self.source_type = source_type
        self.source_link = source_link
        self.text = text
        self.media_url_list = media_url_list
