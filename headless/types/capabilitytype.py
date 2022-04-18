"""Declares :class:`CapabilityType`."""
import enum


class CapabilityType(str, enum.Enum):
    oauth2 = 'oauth2'