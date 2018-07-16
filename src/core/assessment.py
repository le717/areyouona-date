__all__ = ["make"]


def __reply_no() -> str:
    return "no"


def __reply_maybe() -> str:
    return "maybe"


def __reply_yes() -> str:
    return "yes"


def make(user_details: dict) -> str:
    return __reply_no()
