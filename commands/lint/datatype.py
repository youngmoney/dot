class DataType(type):
    SELF_TYPE = "SELF_TYPE"

    def __new__(cls, name, bases, attrs):
        inst = super().__new__(cls, name, bases, attrs)
        fields = {}
        defaults = {}
        for k in attrs:
            if k.startswith("datatype_"):
                if k == "datatype_Defaults":
                    if isinstance(attrs[k], dict):
                        defaults = attrs[k]
                    else:
                        raise TypeError(
                            "DataType defaults 'datatype_Defaults' must be a dictionary of <field>:<default> pairs."
                        )
                else:
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
            elif isinstance(field_type, type):
                return
            elif field_type == DataType.SELF_TYPE:
                return
            else:
                raise TypeError(
                    f"DataType '{field}' invalid: '{field_type}' is not a valid type."
                )

        for field in fields:
            field_type = fields[field]
            validate_field(field, field_type)

        def apply_type(key, field_type, value):
            if field_type == DataType.SELF_TYPE:
                return inst(value)
            if not isinstance(field_type, type):
                raise TypeError(
                    f"DataType '{key}' invalid: '{field_type}' is not a type."
                )
            try:
                return field_type(value)
            except:
                raise TypeError(
                    f"Error parsing '{key}': cannot convert '{value}' to '{field_type}'"
                )

        original_init = attrs["__init__"] if "__init__" in attrs else None

        def init(self, *vargs, **kwargs):
            input_object = None
            if len(vargs) == 0:
                input_object = kwargs
            elif len(vargs) == 1 and isinstance(vargs[0], dict):
                input_object = vargs[0]
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


class Test(metaclass=DataType):
    datatype_a = int
    datatype_b = str
    datatype_c = [int]
    datatype_d = {str: int}
    datatype_recurse = {str: DataType.SELF_TYPE}
    datatype_Defaults = {"c": [0]}

    def __init__(self):
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
