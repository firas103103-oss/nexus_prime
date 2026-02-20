from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AgentStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AGENT_STATUS_UNSPECIFIED: _ClassVar[AgentStatus]
    AGENT_STATUS_IDLE: _ClassVar[AgentStatus]
    AGENT_STATUS_BUSY: _ClassVar[AgentStatus]
    AGENT_STATUS_ERROR: _ClassVar[AgentStatus]
    AGENT_STATUS_OFFLINE: _ClassVar[AgentStatus]
    AGENT_STATUS_BOOTING: _ClassVar[AgentStatus]
    AGENT_STATUS_DRAINING: _ClassVar[AgentStatus]

class PulseType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PULSE_TYPE_UNSPECIFIED: _ClassVar[PulseType]
    PULSE_TYPE_HEARTBEAT: _ClassVar[PulseType]
    PULSE_TYPE_STATE_UPDATE: _ClassVar[PulseType]
    PULSE_TYPE_TASK_RESULT: _ClassVar[PulseType]
    PULSE_TYPE_ERROR: _ClassVar[PulseType]
    PULSE_TYPE_REGISTRATION: _ClassVar[PulseType]
    PULSE_TYPE_INTENT: _ClassVar[PulseType]

class DirectiveType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DIRECTIVE_TYPE_UNSPECIFIED: _ClassVar[DirectiveType]
    DIRECTIVE_TYPE_EXECUTE_TASK: _ClassVar[DirectiveType]
    DIRECTIVE_TYPE_RECONFIGURE: _ClassVar[DirectiveType]
    DIRECTIVE_TYPE_SCALE: _ClassVar[DirectiveType]
    DIRECTIVE_TYPE_SHUTDOWN: _ClassVar[DirectiveType]
    DIRECTIVE_TYPE_ACK: _ClassVar[DirectiveType]
    DIRECTIVE_TYPE_BROADCAST: _ClassVar[DirectiveType]

class TaskStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TASK_STATUS_UNSPECIFIED: _ClassVar[TaskStatus]
    TASK_STATUS_QUEUED: _ClassVar[TaskStatus]
    TASK_STATUS_DISPATCHED: _ClassVar[TaskStatus]
    TASK_STATUS_RUNNING: _ClassVar[TaskStatus]
    TASK_STATUS_SUCCESS: _ClassVar[TaskStatus]
    TASK_STATUS_FAILED: _ClassVar[TaskStatus]
    TASK_STATUS_PARTIAL: _ClassVar[TaskStatus]
    TASK_STATUS_TIMEOUT: _ClassVar[TaskStatus]

class AgentType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    AGENT_TYPE_UNSPECIFIED: _ClassVar[AgentType]
    AGENT_TYPE_PLANET: _ClassVar[AgentType]
    AGENT_TYPE_SERVICE: _ClassVar[AgentType]
    AGENT_TYPE_HUMAN: _ClassVar[AgentType]
    AGENT_TYPE_SWARM: _ClassVar[AgentType]
AGENT_STATUS_UNSPECIFIED: AgentStatus
AGENT_STATUS_IDLE: AgentStatus
AGENT_STATUS_BUSY: AgentStatus
AGENT_STATUS_ERROR: AgentStatus
AGENT_STATUS_OFFLINE: AgentStatus
AGENT_STATUS_BOOTING: AgentStatus
AGENT_STATUS_DRAINING: AgentStatus
PULSE_TYPE_UNSPECIFIED: PulseType
PULSE_TYPE_HEARTBEAT: PulseType
PULSE_TYPE_STATE_UPDATE: PulseType
PULSE_TYPE_TASK_RESULT: PulseType
PULSE_TYPE_ERROR: PulseType
PULSE_TYPE_REGISTRATION: PulseType
PULSE_TYPE_INTENT: PulseType
DIRECTIVE_TYPE_UNSPECIFIED: DirectiveType
DIRECTIVE_TYPE_EXECUTE_TASK: DirectiveType
DIRECTIVE_TYPE_RECONFIGURE: DirectiveType
DIRECTIVE_TYPE_SCALE: DirectiveType
DIRECTIVE_TYPE_SHUTDOWN: DirectiveType
DIRECTIVE_TYPE_ACK: DirectiveType
DIRECTIVE_TYPE_BROADCAST: DirectiveType
TASK_STATUS_UNSPECIFIED: TaskStatus
TASK_STATUS_QUEUED: TaskStatus
TASK_STATUS_DISPATCHED: TaskStatus
TASK_STATUS_RUNNING: TaskStatus
TASK_STATUS_SUCCESS: TaskStatus
TASK_STATUS_FAILED: TaskStatus
TASK_STATUS_PARTIAL: TaskStatus
TASK_STATUS_TIMEOUT: TaskStatus
AGENT_TYPE_UNSPECIFIED: AgentType
AGENT_TYPE_PLANET: AgentType
AGENT_TYPE_SERVICE: AgentType
AGENT_TYPE_HUMAN: AgentType
AGENT_TYPE_SWARM: AgentType

class AgentMetrics(_message.Message):
    __slots__ = ("cpu_usage_percent", "memory_usage_percent", "request_latency_ms", "active_tasks", "completed_tasks", "failed_tasks", "uptime_seconds", "custom_metrics")
    class CustomMetricsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: float
        def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
    CPU_USAGE_PERCENT_FIELD_NUMBER: _ClassVar[int]
    MEMORY_USAGE_PERCENT_FIELD_NUMBER: _ClassVar[int]
    REQUEST_LATENCY_MS_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_TASKS_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_TASKS_FIELD_NUMBER: _ClassVar[int]
    FAILED_TASKS_FIELD_NUMBER: _ClassVar[int]
    UPTIME_SECONDS_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_METRICS_FIELD_NUMBER: _ClassVar[int]
    cpu_usage_percent: float
    memory_usage_percent: float
    request_latency_ms: float
    active_tasks: int
    completed_tasks: int
    failed_tasks: int
    uptime_seconds: float
    custom_metrics: _containers.ScalarMap[str, float]
    def __init__(self, cpu_usage_percent: _Optional[float] = ..., memory_usage_percent: _Optional[float] = ..., request_latency_ms: _Optional[float] = ..., active_tasks: _Optional[int] = ..., completed_tasks: _Optional[int] = ..., failed_tasks: _Optional[int] = ..., uptime_seconds: _Optional[float] = ..., custom_metrics: _Optional[_Mapping[str, float]] = ...) -> None: ...

class AgentState(_message.Message):
    __slots__ = ("status", "current_task", "metrics", "last_pulse")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CURRENT_TASK_FIELD_NUMBER: _ClassVar[int]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    LAST_PULSE_FIELD_NUMBER: _ClassVar[int]
    status: AgentStatus
    current_task: str
    metrics: AgentMetrics
    last_pulse: _timestamp_pb2.Timestamp
    def __init__(self, status: _Optional[_Union[AgentStatus, str]] = ..., current_task: _Optional[str] = ..., metrics: _Optional[_Union[AgentMetrics, _Mapping]] = ..., last_pulse: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class AgentIntent(_message.Message):
    __slots__ = ("requested_action", "target_agent", "priority", "payload", "deadline")
    REQUESTED_ACTION_FIELD_NUMBER: _ClassVar[int]
    TARGET_AGENT_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    DEADLINE_FIELD_NUMBER: _ClassVar[int]
    requested_action: str
    target_agent: str
    priority: int
    payload: _struct_pb2.Struct
    deadline: _timestamp_pb2.Timestamp
    def __init__(self, requested_action: _Optional[str] = ..., target_agent: _Optional[str] = ..., priority: _Optional[int] = ..., payload: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., deadline: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class TaskResult(_message.Message):
    __slots__ = ("command_id", "status", "output", "error_message", "execution_time_ms", "executing_agent")
    COMMAND_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    EXECUTION_TIME_MS_FIELD_NUMBER: _ClassVar[int]
    EXECUTING_AGENT_FIELD_NUMBER: _ClassVar[int]
    command_id: str
    status: TaskStatus
    output: _struct_pb2.Struct
    error_message: str
    execution_time_ms: int
    executing_agent: str
    def __init__(self, command_id: _Optional[str] = ..., status: _Optional[_Union[TaskStatus, str]] = ..., output: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., error_message: _Optional[str] = ..., execution_time_ms: _Optional[int] = ..., executing_agent: _Optional[str] = ...) -> None: ...

class TaskCommand(_message.Message):
    __slots__ = ("command_id", "command_type", "origin", "payload", "priority", "deadline", "max_retries", "timeout_ms")
    COMMAND_ID_FIELD_NUMBER: _ClassVar[int]
    COMMAND_TYPE_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    DEADLINE_FIELD_NUMBER: _ClassVar[int]
    MAX_RETRIES_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_MS_FIELD_NUMBER: _ClassVar[int]
    command_id: str
    command_type: str
    origin: str
    payload: _struct_pb2.Struct
    priority: int
    deadline: _timestamp_pb2.Timestamp
    max_retries: int
    timeout_ms: int
    def __init__(self, command_id: _Optional[str] = ..., command_type: _Optional[str] = ..., origin: _Optional[str] = ..., payload: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., priority: _Optional[int] = ..., deadline: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., max_retries: _Optional[int] = ..., timeout_ms: _Optional[int] = ...) -> None: ...

class RoutingInfo(_message.Message):
    __slots__ = ("target_agent", "fallback_agents", "max_retries", "routing_rule_id")
    TARGET_AGENT_FIELD_NUMBER: _ClassVar[int]
    FALLBACK_AGENTS_FIELD_NUMBER: _ClassVar[int]
    MAX_RETRIES_FIELD_NUMBER: _ClassVar[int]
    ROUTING_RULE_ID_FIELD_NUMBER: _ClassVar[int]
    target_agent: str
    fallback_agents: _containers.RepeatedScalarFieldContainer[str]
    max_retries: int
    routing_rule_id: str
    def __init__(self, target_agent: _Optional[str] = ..., fallback_agents: _Optional[_Iterable[str]] = ..., max_retries: _Optional[int] = ..., routing_rule_id: _Optional[str] = ...) -> None: ...

class AgentPulse(_message.Message):
    __slots__ = ("agent_id", "pulse_type", "timestamp", "state", "intent", "result", "capabilities", "endpoint", "agent_type", "display_name", "error_code", "error_message", "error_stack_trace", "sequence_number", "correlation_id")
    AGENT_ID_FIELD_NUMBER: _ClassVar[int]
    PULSE_TYPE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    INTENT_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    CAPABILITIES_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    AGENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    ERROR_CODE_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ERROR_STACK_TRACE_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    CORRELATION_ID_FIELD_NUMBER: _ClassVar[int]
    agent_id: str
    pulse_type: PulseType
    timestamp: _timestamp_pb2.Timestamp
    state: AgentState
    intent: AgentIntent
    result: TaskResult
    capabilities: _containers.RepeatedScalarFieldContainer[str]
    endpoint: str
    agent_type: AgentType
    display_name: str
    error_code: str
    error_message: str
    error_stack_trace: str
    sequence_number: int
    correlation_id: str
    def __init__(self, agent_id: _Optional[str] = ..., pulse_type: _Optional[_Union[PulseType, str]] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., state: _Optional[_Union[AgentState, _Mapping]] = ..., intent: _Optional[_Union[AgentIntent, _Mapping]] = ..., result: _Optional[_Union[TaskResult, _Mapping]] = ..., capabilities: _Optional[_Iterable[str]] = ..., endpoint: _Optional[str] = ..., agent_type: _Optional[_Union[AgentType, str]] = ..., display_name: _Optional[str] = ..., error_code: _Optional[str] = ..., error_message: _Optional[str] = ..., error_stack_trace: _Optional[str] = ..., sequence_number: _Optional[int] = ..., correlation_id: _Optional[str] = ...) -> None: ...

class OrchestratorDirective(_message.Message):
    __slots__ = ("directive_id", "directive_type", "timestamp", "command", "routing", "system_state", "config", "ack_for_pulse_id", "message", "sequence_number", "correlation_id")
    DIRECTIVE_ID_FIELD_NUMBER: _ClassVar[int]
    DIRECTIVE_TYPE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    ROUTING_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_STATE_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    ACK_FOR_PULSE_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    CORRELATION_ID_FIELD_NUMBER: _ClassVar[int]
    directive_id: str
    directive_type: DirectiveType
    timestamp: _timestamp_pb2.Timestamp
    command: TaskCommand
    routing: RoutingInfo
    system_state: SystemSnapshot
    config: _struct_pb2.Struct
    ack_for_pulse_id: str
    message: str
    sequence_number: int
    correlation_id: str
    def __init__(self, directive_id: _Optional[str] = ..., directive_type: _Optional[_Union[DirectiveType, str]] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., command: _Optional[_Union[TaskCommand, _Mapping]] = ..., routing: _Optional[_Union[RoutingInfo, _Mapping]] = ..., system_state: _Optional[_Union[SystemSnapshot, _Mapping]] = ..., config: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., ack_for_pulse_id: _Optional[str] = ..., message: _Optional[str] = ..., sequence_number: _Optional[int] = ..., correlation_id: _Optional[str] = ...) -> None: ...

class AgentRegistration(_message.Message):
    __slots__ = ("name", "display_name", "agent_type", "capabilities", "endpoint", "metadata")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    AGENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    CAPABILITIES_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    name: str
    display_name: str
    agent_type: AgentType
    capabilities: _containers.RepeatedScalarFieldContainer[str]
    endpoint: str
    metadata: _containers.ScalarMap[str, str]
    def __init__(self, name: _Optional[str] = ..., display_name: _Optional[str] = ..., agent_type: _Optional[_Union[AgentType, str]] = ..., capabilities: _Optional[_Iterable[str]] = ..., endpoint: _Optional[str] = ..., metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class RegistrationAck(_message.Message):
    __slots__ = ("success", "agent_id", "message", "registered_at", "system_state")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    AGENT_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    REGISTERED_AT_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_STATE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    agent_id: str
    message: str
    registered_at: _timestamp_pb2.Timestamp
    system_state: SystemSnapshot
    def __init__(self, success: bool = ..., agent_id: _Optional[str] = ..., message: _Optional[str] = ..., registered_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., system_state: _Optional[_Union[SystemSnapshot, _Mapping]] = ...) -> None: ...

class CommandAck(_message.Message):
    __slots__ = ("success", "command_id", "target_agent", "status", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    COMMAND_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_AGENT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    command_id: str
    target_agent: str
    status: TaskStatus
    message: str
    def __init__(self, success: bool = ..., command_id: _Optional[str] = ..., target_agent: _Optional[str] = ..., status: _Optional[_Union[TaskStatus, str]] = ..., message: _Optional[str] = ...) -> None: ...

class SystemSnapshot(_message.Message):
    __slots__ = ("online_agents", "total_agents", "queued_commands", "running_commands", "cluster_cpu_percent", "cluster_memory_percent", "timestamp", "agents")
    ONLINE_AGENTS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_AGENTS_FIELD_NUMBER: _ClassVar[int]
    QUEUED_COMMANDS_FIELD_NUMBER: _ClassVar[int]
    RUNNING_COMMANDS_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_CPU_PERCENT_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_MEMORY_PERCENT_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    AGENTS_FIELD_NUMBER: _ClassVar[int]
    online_agents: int
    total_agents: int
    queued_commands: int
    running_commands: int
    cluster_cpu_percent: float
    cluster_memory_percent: float
    timestamp: _timestamp_pb2.Timestamp
    agents: _containers.RepeatedCompositeFieldContainer[AgentSummary]
    def __init__(self, online_agents: _Optional[int] = ..., total_agents: _Optional[int] = ..., queued_commands: _Optional[int] = ..., running_commands: _Optional[int] = ..., cluster_cpu_percent: _Optional[float] = ..., cluster_memory_percent: _Optional[float] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., agents: _Optional[_Iterable[_Union[AgentSummary, _Mapping]]] = ...) -> None: ...

class AgentSummary(_message.Message):
    __slots__ = ("name", "display_name", "status", "agent_type", "last_seen", "current_task", "capabilities")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    AGENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    LAST_SEEN_FIELD_NUMBER: _ClassVar[int]
    CURRENT_TASK_FIELD_NUMBER: _ClassVar[int]
    CAPABILITIES_FIELD_NUMBER: _ClassVar[int]
    name: str
    display_name: str
    status: AgentStatus
    agent_type: AgentType
    last_seen: _timestamp_pb2.Timestamp
    current_task: str
    capabilities: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, name: _Optional[str] = ..., display_name: _Optional[str] = ..., status: _Optional[_Union[AgentStatus, str]] = ..., agent_type: _Optional[_Union[AgentType, str]] = ..., last_seen: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., current_task: _Optional[str] = ..., capabilities: _Optional[_Iterable[str]] = ...) -> None: ...
