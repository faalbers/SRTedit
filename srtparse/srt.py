import six

class Srt():
    def __init__(self):
        self._entries = []
        self._format = ''

    def add_entry(self, item):
        if not isinstance(item, Entry):
            raise RuntimeError(six.u("item not recognized"))
        self._entries.append(item)
    
    def get_entryDataFields(self):
        fields = set()
        for entry in self._entries:
            for field in entry.data.keys():
                fields.add(field)
        fields = list(fields)
        fields.sort()
        return fields
    

    def add_formatLine(self, formatLine, new=False):
        if new:
            self._format = ''
        self._format += formatLine + '\n'
    
    def save(self, fileName):
        file = open(fileName, 'w')
        file.write(str(self))
        file.close()

    def __str__(self):
        res = []
        fields = self.get_entryDataFields()
        fields.sort(key=len, reverse=True)
        for entry in self._entries:
            res.append(entry.count)
            res.append(entry.time)
            data = self._format
            for field in fields:
                data = data.replace('$%s$' % field, field)
            
            #data = data.replace('@%s@' % field, entry.data[field])
            dataSplit = data.split('@')
            data = ''
            partCount = 2
            for part in dataSplit:
                partCount -= 1
                if partCount == 0:
                    for field in fields:
                        if field in part:
                            numdata = ''
                            for char in entry.data[field]:
                                if char.isdigit() or char == '.':
                                    numdata += char
                            part = part.replace(field, numdata)
                    partCount = 2
                    try:
                        part = str(eval(part))
                    except:
                        pass
                data += part
            res.append(data.strip('\n'))
            res.append('')
        res.append('')
        return '\n'.join(res)



class Field(object):
    def __init__(self, name, ftype, required=False,
                 default=None, custom_print_format=None):
        self.name = name
        self.ftype = ftype
        self.required = required
        self.default = default
        self.custom_print_format = custom_print_format

class BaseEntry(object):

    _fields = []
    _sub_entry = False

    def __init__(self, **kwargs):
        for field in self._fields:
            val = kwargs.get(field.name, field.default)
            setattr(self, field.name, val)

class Entry(BaseEntry):
    _sub_entry = True
    _fields = [
        Field('count', 'str', required=True),
        Field('time', 'str', required=True),
        Field('data', 'dict', required=True),
    ]

    #def __init__(self, **kwargs):
    #    super(Entry, self).__init__(**kwargs)
