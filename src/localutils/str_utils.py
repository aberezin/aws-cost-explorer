from _typeshed import SupportsRead


# noinspection PyTypeChecker
def cast_to_str(data: SupportsRead[str | bytes]) -> str:
    if isinstance(data, bytes):
        return data.decode()
    return data

