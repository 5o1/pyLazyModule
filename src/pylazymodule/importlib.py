import importlib
from types import ModuleType
import inspect
from typing import Optional

class LazyModule(ModuleType):
    def __init__(self, module_path: str):
        assert module_path
        self.__module_path = module_path

        stack = inspect.stack(1)
        caller_frame = stack[1] 
        caller_module = inspect.getmodule(caller_frame[0])
        self.__package = caller_module.__package__ if caller_module else None

        self.__module = None


    def _resolve_import_path(self, path: str, package: Optional[str]):
        prefix_dots = len(path) - len(path.lstrip("."))
        parts = path.lstrip(".").split(".")
        parts[0] = "." * prefix_dots + parts[0]

        module = None
        attr_chain = []
        e = None

        for i in range(len(parts) - 1, -1, -1):
            try:
                module = importlib.import_module(".".join(parts[:i + 1]), package)
                attr_chain = parts[i+1:]
            except ModuleNotFoundError as _e:
                e = _e
                continue

        if module is None:
            raise e

        for attr in attr_chain:
            module = getattr(module, attr)
        return module

    def _load_module(self):
        if self.__module is None:
            self.__module = self._resolve_import_path(f"{self.__module_path}", self.__package)
        return self.__module
    
    def __getattr__(self, attr):
        return getattr(self._load_module(), attr)
    
    def __getattribute__(self, attr):
        if str(attr) in [
            "__doc__", "__name__", "__dict__", "__annotations__", "__file__",
            "__package__", "__path__", "__spec__", "__loader__", "__builtins__",
            "__call__", "__dir__", "__repr__", "__all__"
            ]:
            module = super().__getattribute__('_load_module')()
            return getattr(module, attr)
        return super().__getattribute__(attr)
    
    def __call__(self, *args, **kwargs):
        module = self._load_module()
        if callable(module):
            return module(*args, **kwargs)
        raise TypeError(f"'{self.__module.__path__}' is not callable")