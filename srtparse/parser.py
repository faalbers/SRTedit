from datetime import datetime
from srtparse import DEFAULT_DATETIME_FORMAT
from srtparse.srt import (
    Srt,
    Entry,
)

class SrtParserException(Exception):
    pass

class SrtParser(object):

    @classmethod
    def parse(cls_, file_name, date_format=None):
        file_handle = open(file_name)
        data = file_handle.read()
        file_handle.close()
        if len(data) == 0:
            raise SrtParserException('Data is empty')
        srt_obj = Srt()
        chunks = data.split('\n\n')
        for chunk in chunks:
            if not chunk:
                continue
            item = cls_.parseItem(chunk)
            srt_obj.add_entry(item)
        for dataField in srt_obj.get_entryDataFields():
            srt_obj.add_formatLine('$%s$: @%s@' % (dataField, dataField))
        return srt_obj

    @classmethod
    def parseItem(cls_, chunk):
        curItem = Entry()
        lines = chunk.split('\n')

        curItem.count = lines[0]
        curItem.time = lines[1]

        curItem.data = {}
        for dataEntry in lines[2].split():
            data = dataEntry.split(':')
            curItem.data[data[0]] = data[1]

        return curItem
