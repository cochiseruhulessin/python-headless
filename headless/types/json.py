"""Declares JSON type variables."""
import typing


__all__ = [
    'JSONArray',
    'JSONObject',
    'JSONScalar',
]


JSONScalar: typing.TypeAlias = float | int | str

JSONObject: typing.TypeAlias = dict[JSONScalar, 'JSONObject']

JSONArray: typing.TypeAlias = list[JSONScalar | JSONObject | typing.List['JSONArray']]
