# pyLazyModule
A simple practice of dynamic module loader to avoid explicitly importing optional dependencies when a module is not accessed. This is useful when using multiple optional backends for deep learning.

## Usage

```python
# __init.py__
from typing import TYPE_CHECKING

if TYPE_CHECKING: # VSCode or other IDE requires explicit import to enable code-completion
    import module1
    from . import module2
    from .module3 import class3
else: # Runtime
    from pylazymodule import LazyModule
    module1 = LazyModule("module1")
    module2 = LazyModule(".module2") # Support relative import
    class3 = LazyModule(".module3.class3") # Can also be used to import attr

# __main__.py
from . import (
    module1,
    module2,
    class3
)
# Always successful while importing

obj3 = class3()
# If .module3 not found, raise `ModuleNotFound` in runtime
# If .module3.class3 not found, raise `AttributeError` in runtime
```