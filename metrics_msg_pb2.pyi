from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CPUDist(_message.Message):
    __slots__ = ["range2usecs"]
    class Range2usecsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: float
        def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
    RANGE2USECS_FIELD_NUMBER: _ClassVar[int]
    range2usecs: _containers.ScalarMap[str, float]
    def __init__(self, range2usecs: _Optional[_Mapping[str, float]] = ...) -> None: ...

class MetricsRequest(_message.Message):
    __slots__ = ["metrics"]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    metrics: str
    def __init__(self, metrics: _Optional[str] = ...) -> None: ...

class MetricsResponse(_message.Message):
    __slots__ = ["cpu", "cpu_avg", "cpu_sum"]
    CPU_AVG_FIELD_NUMBER: _ClassVar[int]
    CPU_FIELD_NUMBER: _ClassVar[int]
    CPU_SUM_FIELD_NUMBER: _ClassVar[int]
    cpu: _containers.RepeatedCompositeFieldContainer[CPUDist]
    cpu_avg: CPUDist
    cpu_sum: CPUDist
    def __init__(self, cpu_avg: _Optional[_Union[CPUDist, _Mapping]] = ..., cpu_sum: _Optional[_Union[CPUDist, _Mapping]] = ..., cpu: _Optional[_Iterable[_Union[CPUDist, _Mapping]]] = ...) -> None: ...
