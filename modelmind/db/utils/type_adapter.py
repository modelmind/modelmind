from pydantic import TypeAdapter as PydanticTypeAdapter

# https://docs.pydantic.dev/latest/concepts/type_adapter/#parsing-data-into-a-specified-type


class TypeAdapterSingleton:
    _adapters: dict[type, PydanticTypeAdapter] = {}

    @classmethod
    def get_adapter(cls, model) -> PydanticTypeAdapter:
        if model not in cls._adapters:
            cls._adapters[model] = PydanticTypeAdapter(model)
        return cls._adapters[model]


class TypeAdapter:
    @classmethod
    def validate(cls, model, value):
        return TypeAdapterSingleton.get_adapter(model).validate_python(value)
