class DataType(type):
    Self = type("<self>", (object,), {})

    def __new__(cls, name, bases, attrs):
        inst = super().__new__(cls, name, bases, attrs)
        fields = {}
        defaults = {}
        if "__init__" in attrs:
            init = attrs["__init__"]
            code = getattr(init, "__code__", None)
            init_defaults = getattr(init, "__defaults__", None)
            args = getattr(code, "co_varnames", None)
            if code is not None and init_defaults is not None and args is not None:
                args = list(reversed(args))
                init_defaults = list(reversed(init_defaults))
                for i in range(min(len(init_defaults), len(args))):
                    defaults[args[i]] = init_defaults[i]

        for k in attrs:
            if k.startswith("datatype_"):
                fields[k[len("datatype_") :]] = attrs[k]

        def validate_field(field, field_type):
            if isinstance(field_type, list):
                if len(field_type) != 1:
                    raise TypeError(
                        "DataType '{field}' invalid: specify a list as [<list type>]."
                    )
                validate_field(field + ".list_type", field_type[0])
            elif isinstance(field_type, dict):
                if len(field_type.keys()) != 1:
                    raise TypeError(
                        f"DataType '{field}' invalid: specify a dictionary as {{str:<value type>}}."
                    )
                key_type = list(field_type.keys())[0]
                value_type = field_type[key_type]
                if key_type != str:
                    raise TypeError(
                        f"DataType '{field}' invalid: specify a dictionary as {{str:<value type>}}."
                    )
                validate_field(field + ".value_type", value_type)
            elif field_type == DataType.Self:
                return
            elif isinstance(field_type, type):
                return
            else:
                raise TypeError(
                    f"DataType '{field}' invalid: '{field_type}' is not a valid type."
                )

        for field in fields:
            field_type = fields[field]
            validate_field(field, field_type)

        def apply_type(key, field_type, value):
            if field_type == DataType.Self:
                return inst(value)
            if not isinstance(field_type, type):
                raise TypeError(
                    f"DataType '{key}' invalid: '{field_type}' is not a type."
                )
            try:
                return field_type(value)
            except:
                raise TypeError(
                    f"Error parsing '{key}': cannot convert '{value}' to '{field_type.__name__}'"
                )

        original_init = attrs["__init__"] if "__init__" in attrs else None

        def init(self, *vargs, **kwargs):
            input_object = None
            if len(vargs) == 0:
                input_object = kwargs
            elif len(vargs) == 1 and isinstance(vargs[0], dict):
                input_object = vargs[0]
            elif len(vargs) == 1 and vargs[0] is None:
                input_object = {}
            else:
                raise TypeError(
                    "ParseError: DataType must be constructed with either a dictionary or keyword arguments."
                )

            for field_key in fields:
                field_type = fields[field_key]
                input_value = None
                if field_key in input_object:
                    input_value = input_object[field_key]
                elif field_key in defaults:
                    input_value = defaults[field_key]

                if input_value is None:
                    setattr(self, field_key, None)
                elif isinstance(field_type, list):
                    l = []
                    list_type = field_type[0]

                    try:
                        as_list = list(input_value)
                    except:
                        raise TypeError(
                            f"ParseError: Expected '{field_key}' to be a list."
                        )
                    for i in as_list:
                        l.append(apply_type(field_key, field_type[0], i))
                    setattr(self, field_key, l)

                elif isinstance(field_type, dict):
                    d = {}
                    key_type = list(field_type.keys())[0]
                    value_type = field_type[key_type]
                    if not isinstance(input_value, dict):
                        raise TypeError(
                            f"ParseError: Expected '{field_key}' to be a dictionary."
                        )
                    for key, value in input_value.items():
                        d[apply_type(key, key_type, key)] = apply_type(
                            key, value_type, value
                        )
                    setattr(self, field_key, d)

                else:
                    setattr(
                        self, field_key, apply_type(field_key, field_type, input_value)
                    )

            if original_init:
                original_init(self)

        inst.__init__ = init

        def rep(self):
            return str(f"{self.__class__.__name__}({self.datatype_Object()})")

        inst.__repr__ = rep

        def datatype_Object(self, short=True):
            d = {}
            for k in fields:
                value = getattr(self, k, None)
                if value is None and short:
                    continue
                d[k] = value

            return d

        inst.datatype_Object = datatype_Object

        def value_string(value):
            if isinstance(value, list):
                v = value_string(value[0])
                value = f"[{v}]"
            elif isinstance(value, dict):
                key = list(value.keys())[0]
                k = value_string(key)
                v = value_string(value[key])
                value = f"{{{k}: {v}}}"
            elif isinstance(value, type):
                value = value.__name__
            return value

        def schema():
            parts = []
            for field in fields:
                value = value_string(fields[field])
                parts.append(f"{field} = {value}")
            return "\n".join(parts)

        inst.datatype_Schema = schema

        return inst


class Option(type):
    def __new__(cls, name, bases, attrs):
        inst = super().__new__(cls, name, bases, attrs)
        values = []
        inverse_values = {}
        values_normal = []
        upper_to_name = {}
        for a in attrs:
            if a.startswith("_"):
                continue
            values.append(a.upper())
            values_normal.append(a)
            upper_to_name[a.upper()] = a
            if attrs[a] is not None:
                if attrs[a] in inverse_values:
                    raise TypeError(
                        f"Option {name} cannot add '{a}' with value '{attrs[a]}' because it is already in use."
                    )
                else:
                    inverse_values[attrs[a]] = a.upper()

        def init(self, input_value):
            if input_value in inverse_values:
                input_value = inverse_values[input_value]
            if isinstance(input_value, str):
                value = input_value.upper()
                if value in values:
                    self._value = value
                    return
            if isinstance(input_value, self.__class__):
                self._value = input_value._value
                return

            raise TypeError(f"Unable to parse option '{input_value}'.")

        inst.__init__ = init

        def get(self):
            if not self._value in values:
                raise TypeError(f"Current value is invalid: {self._value}.")
            return self._value

        inst.value = get

        def rep(self):
            normal = upper_to_name[self.value()]
            return f"{name}.{normal}"

        inst.__repr__ = rep

        def eq(self, other):
            if isinstance(other, self.__class__):
                return self._value == other._value
            try:
                opt = inst(other)
                return self == opt
            except:
                pass
            return False

        inst.__eq__ = eq

        for v in values_normal:
            setattr(inst, v, inst(v))

        return inst


class Opts(metaclass=Option):
    opt1 = 0
    opt2 = 1


class Test(metaclass=DataType):
    datatype_a = int
    datatype_b = str
    datatype_c = [int]
    datatype_d = {str: int}
    datatype_recurse = {str: DataType.Self}

    def __init__(self, b="hello", c=[1, 2]):
        if self.a is not None:
            self.a += 1


def tests():
    print(Test({"a": 1}))
    print(Test({"b": 1}))
    print(Test({"a": "1"}))
    print(Test({"c": ["1"]}))
    print(Test({"d": {"1": "1"}}))
    print(Test({"d": {"1": "1"}}))
    print(Test({"recurse": {"this": {"a": 1}}}))
    print(Test.datatype_Schema())
