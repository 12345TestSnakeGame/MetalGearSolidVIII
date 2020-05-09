
class type_expression:
    width = 0
    name = ''


class basic_type(type_expression):
    def __init__(self, type_name: str, type_width: int):
        self.name = type_name
        self.width = type_width

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class complex_type(type_expression):
    pass


class pointer_type(complex_type):
    def __init__(self, origin_type: type_expression):
        self.point = origin_type
        self.width = 4

    def __str__(self):
        return 'pointer(' + self.name + ')'

    def __repr__(self):
        return self.__str__()


class array_type(complex_type):
    def __init__(self, size: int, element_type: type_expression):
        self.element = element_type
        self.size = size
        self.width = size * element_type.width

    def __str__(self):
        return 'array(' + str(self.size) + ', ' + self.element.__str__() + ')'

    def __repr__(self):
        return self.__str__()


class record_type(complex_type):
    def __init__(self, components: {}):
        self.components = components
        self.width = sum(list(map(lambda x: x[1][1], components.items())))

    def __str__(self):
        return 'RECORD{\n' + '\n'.join(list(map(lambda x: x[1][0].__str__(), self.components.items()))) + '\n}'

    def __repr__(self):
        return self.__str__()


if __name__ == '__main__':
    pass