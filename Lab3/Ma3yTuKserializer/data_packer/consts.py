import types


PRIMITIVE_TYPES=(int, str, bool, float, types.NoneType)


IGNORE_DUNDER=( 
    "__mro__",
    "__doc__",
    "__base__",
    "__basicsize__",
    "__class__",
    "__dictoffset__",
    "__name__",
    "__qualname__",
    "__text_signature__",
    "__itemsize__",
    "__flags__",
    "__weakrefoffset__",
    "__objclass__",
    )

IGNORE_TYPES=(
    types.WrapperDescriptorType,
    types.MethodDescriptorType,
    types.BuiltinFunctionType,
    types.MappingProxyType,
    types.GetSetDescriptorType,
)

IGNORE_CODE=(
    "co_positions",
    "co_lines",
    "co_exceptiontable",
    "co_lnotab",
)