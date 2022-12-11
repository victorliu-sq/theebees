from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CPUDistFloat(_message.Message):
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

class CPUDistUint32(_message.Message):
    __slots__ = ["range2usecs"]
    class Range2usecsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    RANGE2USECS_FIELD_NUMBER: _ClassVar[int]
    range2usecs: _containers.ScalarMap[str, int]
    def __init__(self, range2usecs: _Optional[_Mapping[str, int]] = ...) -> None: ...

class MetricsRequest(_message.Message):
    __slots__ = ["metrics", "node_name"]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    metrics: str
    node_name: str
    def __init__(self, metrics: _Optional[str] = ..., node_name: _Optional[str] = ...) -> None: ...

class MetricsResponse(_message.Message):
    __slots__ = ["cpu", "cpu_avg", "cpu_sum", "pidpersec_avg", "pidpersec_sum", "runqlat_avg", "runqlat_sum"]
    CPU_AVG_FIELD_NUMBER: _ClassVar[int]
    CPU_FIELD_NUMBER: _ClassVar[int]
    CPU_SUM_FIELD_NUMBER: _ClassVar[int]
    PIDPERSEC_AVG_FIELD_NUMBER: _ClassVar[int]
    PIDPERSEC_SUM_FIELD_NUMBER: _ClassVar[int]
    RUNQLAT_AVG_FIELD_NUMBER: _ClassVar[int]
    RUNQLAT_SUM_FIELD_NUMBER: _ClassVar[int]
    cpu: MultipleCPUDistUint32
    cpu_avg: CPUDistFloat
    cpu_sum: CPUDistUint32
    pidpersec_avg: float
    pidpersec_sum: int
    runqlat_avg: RunqlatFloat
    runqlat_sum: RunqlatUint32
    def __init__(self, cpu_avg: _Optional[_Union[CPUDistFloat, _Mapping]] = ..., cpu_sum: _Optional[_Union[CPUDistUint32, _Mapping]] = ..., cpu: _Optional[_Union[MultipleCPUDistUint32, _Mapping]] = ..., pidpersec_avg: _Optional[float] = ..., pidpersec_sum: _Optional[int] = ..., runqlat_avg: _Optional[_Union[RunqlatFloat, _Mapping]] = ..., runqlat_sum: _Optional[_Union[RunqlatUint32, _Mapping]] = ...) -> None: ...

class MultipleCPUDistUint32(_message.Message):
    __slots__ = ["multiple_range2usecs"]
    MULTIPLE_RANGE2USECS_FIELD_NUMBER: _ClassVar[int]
    multiple_range2usecs: _containers.RepeatedCompositeFieldContainer[CPUDistUint32]
    def __init__(self, multiple_range2usecs: _Optional[_Iterable[_Union[CPUDistUint32, _Mapping]]] = ...) -> None: ...

class RunqlatFloat(_message.Message):
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

class RunqlatUint32(_message.Message):
    __slots__ = ["range2usecs"]
    class Range2usecsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(self, key: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...
    RANGE2USECS_FIELD_NUMBER: _ClassVar[int]
    range2usecs: _containers.ScalarMap[str, int]
    def __init__(self, range2usecs: _Optional[_Mapping[str, int]] = ...) -> None: ...
