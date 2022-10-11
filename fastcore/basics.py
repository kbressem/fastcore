# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/01_basics.ipynb.

# %% auto 0
__all__ = ['defaults', 'null', 'num_methods', 'rnum_methods', 'inum_methods', 'arg0', 'arg1', 'arg2', 'arg3', 'arg4', 'Self',
           'ifnone', 'maybe_attr', 'basic_repr', 'is_array', 'listify', 'tuplify', 'true', 'NullType', 'tonull',
           'get_class', 'mk_class', 'wrap_class', 'ignore_exceptions', 'exec_local', 'risinstance', 'Inf', 'in_',
           'ret_true', 'ret_false', 'stop', 'gen', 'chunked', 'otherwise', 'custom_dir', 'AttrDict',
           'get_annotations_ex', 'eval_type', 'type_hints', 'annotations', 'anno_ret', 'signature_ex', 'union2tuple',
           'argnames', 'with_cast', 'store_attr', 'attrdict', 'properties', 'camel2words', 'camel2snake', 'snake2camel',
           'class2attr', 'getcallable', 'getattrs', 'hasattrs', 'setattrs', 'try_attrs', 'GetAttrBase', 'GetAttr',
           'delegate_attr', 'ShowPrint', 'Int', 'Str', 'Float', 'flatten', 'concat', 'strcat', 'detuplify', 'replicate',
           'setify', 'merge', 'range_of', 'groupby', 'last_index', 'filter_dict', 'filter_keys', 'filter_values',
           'cycle', 'zip_cycle', 'sorted_ex', 'not_', 'argwhere', 'filter_ex', 'renumerate', 'first', 'only',
           'nested_attr', 'nested_setdefault', 'nested_callable', 'nested_idx', 'set_nested_idx', 'val2idx',
           'uniqueify', 'loop_first_last', 'loop_first', 'loop_last', 'fastuple', 'bind', 'mapt', 'map_ex', 'compose',
           'maps', 'partialler', 'instantiate', 'using_attr', 'copy_func', 'patch_to', 'patch', 'patch_property',
           'compile_re', 'ImportEnum', 'StrEnum', 'str_enum', 'Stateful', 'PrettyString', 'even_mults', 'num_cpus',
           'add_props', 'typed', 'exec_new', 'exec_import', 'str2bool', 'lt', 'gt', 'le', 'ge', 'eq', 'ne', 'add',
           'sub', 'mul', 'truediv', 'is_', 'is_not']

# %% ../nbs/01_basics.ipynb 1
from .imports import *
import builtins,types
import pprint
try: from types import UnionType
except ImportError: UnionType = None

# %% ../nbs/01_basics.ipynb 5
defaults = SimpleNamespace()

# %% ../nbs/01_basics.ipynb 6
def ifnone(a, b):
    "`b` if `a` is None else `a`"
    return b if a is None else a

# %% ../nbs/01_basics.ipynb 9
def maybe_attr(o, attr):
    "`getattr(o,attr,o)`"
    return getattr(o,attr,o)

# %% ../nbs/01_basics.ipynb 12
def basic_repr(flds=None):
    "Minimal `__repr__`"
    if isinstance(flds, str): flds = re.split(', *', flds)
    flds = list(flds or [])
    def _f(self):
        res = f'{type(self).__module__}.{type(self).__name__}'
        if not flds: return f'<{res}>'
        sig = ', '.join(f'{o}={getattr(self,o)!r}' for o in flds)
        return f'{res}({sig})'
    return _f

# %% ../nbs/01_basics.ipynb 18
def is_array(x):
    "`True` if `x` supports `__array__` or `iloc`"
    return hasattr(x,'__array__') or hasattr(x,'iloc')

# %% ../nbs/01_basics.ipynb 20
def listify(o=None, *rest, use_list=False, match=None):
    "Convert `o` to a `list`"
    if rest: o = (o,)+rest
    if use_list: res = list(o)
    elif o is None: res = []
    elif isinstance(o, list): res = o
    elif isinstance(o, str) or is_array(o): res = [o]
    elif is_iter(o): res = list(o)
    else: res = [o]
    if match is not None:
        if is_coll(match): match = len(match)
        if len(res)==1: res = res*match
        else: assert len(res)==match, 'Match length mismatch'
    return res

# %% ../nbs/01_basics.ipynb 33
def tuplify(o, use_list=False, match=None):
    "Make `o` a tuple"
    return tuple(listify(o, use_list=use_list, match=match))

# %% ../nbs/01_basics.ipynb 35
def true(x):
    "Test whether `x` is truthy; collections with >0 elements are considered `True`"
    try: return bool(len(x))
    except: return bool(x)

# %% ../nbs/01_basics.ipynb 37
class NullType:
    "An object that is `False` and can be called, chained, and indexed"
    def __getattr__(self,*args):return null
    def __call__(self,*args, **kwargs):return null
    def __getitem__(self, *args):return null
    def __bool__(self): return False

null = NullType()

# %% ../nbs/01_basics.ipynb 40
def tonull(x):
    "Convert `None` to `null`"
    return null if x is None else x

# %% ../nbs/01_basics.ipynb 42
def get_class(nm, *fld_names, sup=None, doc=None, funcs=None, **flds):
    "Dynamically create a class, optionally inheriting from `sup`, containing `fld_names`"
    attrs = {}
    for f in fld_names: attrs[f] = None
    for f in listify(funcs): attrs[f.__name__] = f
    for k,v in flds.items(): attrs[k] = v
    sup = ifnone(sup, ())
    if not isinstance(sup, tuple): sup=(sup,)

    def _init(self, *args, **kwargs):
        for i,v in enumerate(args): setattr(self, list(attrs.keys())[i], v)
        for k,v in kwargs.items(): setattr(self,k,v)

    all_flds = [*fld_names,*flds.keys()]
    def _eq(self,b):
        return all([getattr(self,k)==getattr(b,k) for k in all_flds])

    if not sup: attrs['__repr__'] = basic_repr(all_flds)
    attrs['__init__'] = _init
    attrs['__eq__'] = _eq
    res = type(nm, sup, attrs)
    if doc is not None: res.__doc__ = doc
    return res

# %% ../nbs/01_basics.ipynb 46
def mk_class(nm, *fld_names, sup=None, doc=None, funcs=None, mod=None, **flds):
    "Create a class using `get_class` and add to the caller's module"
    if mod is None: mod = sys._getframe(1).f_locals
    res = get_class(nm, *fld_names, sup=sup, doc=doc, funcs=funcs, **flds)
    mod[nm] = res

# %% ../nbs/01_basics.ipynb 51
def wrap_class(nm, *fld_names, sup=None, doc=None, funcs=None, **flds):
    "Decorator: makes function a method of a new class `nm` passing parameters to `mk_class`"
    def _inner(f):
        mk_class(nm, *fld_names, sup=sup, doc=doc, funcs=listify(funcs)+[f], mod=f.__globals__, **flds)
        return f
    return _inner

# %% ../nbs/01_basics.ipynb 53
class ignore_exceptions:
    "Context manager to ignore exceptions"
    def __enter__(self): pass
    def __exit__(self, *args): return True

# %% ../nbs/01_basics.ipynb 56
def exec_local(code, var_name):
    "Call `exec` on `code` and return the var `var_name"
    loc = {}
    exec(code, globals(), loc)
    return loc[var_name]

# %% ../nbs/01_basics.ipynb 58
def risinstance(types, obj=None):
    "Curried `isinstance` but with args reversed"
    types = tuplify(types)
    if obj is None: return partial(risinstance,types)
    if any(isinstance(t,str) for t in types):
        return any(t.__name__ in types for t in type(obj).__mro__)
    return isinstance(obj, types)

# %% ../nbs/01_basics.ipynb 70
class _InfMeta(type):
    @property
    def count(self): return itertools.count()
    @property
    def zeros(self): return itertools.cycle([0])
    @property
    def ones(self):  return itertools.cycle([1])
    @property
    def nones(self): return itertools.cycle([None])

# %% ../nbs/01_basics.ipynb 71
class Inf(metaclass=_InfMeta):
    "Infinite lists"
    pass

# %% ../nbs/01_basics.ipynb 76
_dumobj = object()
def _oper(op,a,b=_dumobj): return (lambda o:op(o,a)) if b is _dumobj else op(a,b)

def _mk_op(nm, mod):
    "Create an operator using `oper` and add to the caller's module"
    op = getattr(operator,nm)
    def _inner(a, b=_dumobj): return _oper(op, a,b)
    _inner.__name__ = _inner.__qualname__ = nm
    _inner.__doc__ = f'Same as `operator.{nm}`, or returns partial if 1 arg'
    mod[nm] = _inner

# %% ../nbs/01_basics.ipynb 77
def in_(x, a):
    "`True` if `x in a`"
    return x in a

operator.in_ = in_

# %% ../nbs/01_basics.ipynb 78
_all_ = ['lt','gt','le','ge','eq','ne','add','sub','mul','truediv','is_','is_not','in_']

# %% ../nbs/01_basics.ipynb 79
for op in ['lt','gt','le','ge','eq','ne','add','sub','mul','truediv','is_','is_not','in_']: _mk_op(op, globals())

# %% ../nbs/01_basics.ipynb 85
def ret_true(*args, **kwargs):
    "Predicate: always `True`"
    return True

# %% ../nbs/01_basics.ipynb 87
def ret_false(*args, **kwargs):
    "Predicate: always `False`"
    return False

# %% ../nbs/01_basics.ipynb 88
def stop(e=StopIteration):
    "Raises exception `e` (by default `StopException`)"
    raise e

# %% ../nbs/01_basics.ipynb 89
def gen(func, seq, cond=ret_true):
    "Like `(func(o) for o in seq if cond(func(o)))` but handles `StopIteration`"
    return itertools.takewhile(cond, map(func,seq))

# %% ../nbs/01_basics.ipynb 91
def chunked(it, chunk_sz=None, drop_last=False, n_chunks=None):
    "Return batches from iterator `it` of size `chunk_sz` (or return `n_chunks` total)"
    assert bool(chunk_sz) ^ bool(n_chunks)
    if n_chunks: chunk_sz = max(math.ceil(len(it)/n_chunks), 1)
    if not isinstance(it, Iterator): it = iter(it)
    while True:
        res = list(itertools.islice(it, chunk_sz))
        if res and (len(res)==chunk_sz or not drop_last): yield res
        if len(res)<chunk_sz: return

# %% ../nbs/01_basics.ipynb 94
def otherwise(x, tst, y):
    "`y if tst(x) else x`"
    return y if tst(x) else x

# %% ../nbs/01_basics.ipynb 98
def custom_dir(c, add):
    "Implement custom `__dir__`, adding `add` to `cls`"
    return object.__dir__(c) + listify(add)

# %% ../nbs/01_basics.ipynb 101
class AttrDict(dict):
    "`dict` subclass that also provides access to keys as attrs"
    def __getattr__(self,k): return self[k] if k in self else stop(AttributeError(k))
    def __setattr__(self, k, v): (self.__setitem__,super().__setattr__)[k[0]=='_'](k,v)
    def __dir__(self): return super().__dir__() + list(self.keys())
    def _repr_markdown_(self): return f'```json\n{pprint.pformat(self, indent=2)}\n```'
    def copy(self): return AttrDict(**self)

# %% ../nbs/01_basics.ipynb 105
def get_annotations_ex(obj, *, globals=None, locals=None):
    "Backport of py3.10 `get_annotations` that returns globals/locals"
    if isinstance(obj, type):
        obj_dict = getattr(obj, '__dict__', None)
        if obj_dict and hasattr(obj_dict, 'get'):
            ann = obj_dict.get('__annotations__', None)
            if isinstance(ann, types.GetSetDescriptorType): ann = None
        else: ann = None

        obj_globals = None
        module_name = getattr(obj, '__module__', None)
        if module_name:
            module = sys.modules.get(module_name, None)
            if module: obj_globals = getattr(module, '__dict__', None)
        obj_locals = dict(vars(obj))
        unwrap = obj
    elif isinstance(obj, types.ModuleType):
        ann = getattr(obj, '__annotations__', None)
        obj_globals = getattr(obj, '__dict__')
        obj_locals,unwrap = None,None
    elif callable(obj):
        ann = getattr(obj, '__annotations__', None)
        obj_globals = getattr(obj, '__globals__', None)
        obj_locals,unwrap = None,obj
    else: raise TypeError(f"{obj!r} is not a module, class, or callable.")

    if ann is None: ann = {}
    if not isinstance(ann, dict): raise ValueError(f"{obj!r}.__annotations__ is neither a dict nor None")
    if not ann: ann = {}

    if unwrap is not None:
        while True:
            if hasattr(unwrap, '__wrapped__'):
                unwrap = unwrap.__wrapped__
                continue
            if isinstance(unwrap, functools.partial):
                unwrap = unwrap.func
                continue
            break
        if hasattr(unwrap, "__globals__"): obj_globals = unwrap.__globals__

    if globals is None: globals = obj_globals
    if locals is None: locals = obj_locals

    return dict(ann), globals, locals

# %% ../nbs/01_basics.ipynb 107
def eval_type(t, glb, loc):
    "`eval` a type or collection of types, if needed, for annotations in py3.10+"
    if isinstance(t,str):
        if '|' in t: return Union[eval_type(tuple(t.split('|')), glb, loc)]
        return eval(t, glb, loc)
    if isinstance(t,(tuple,list)): return type(t)([eval_type(c, glb, loc) for c in t])
    return t

# %% ../nbs/01_basics.ipynb 112
def _eval_type(t, glb, loc):
    res = eval_type(t, glb, loc)
    return NoneType if res is None else res

def type_hints(f):
    "Like `typing.get_type_hints` but returns `{}` if not allowed type"
    if not isinstance(f, typing._allowed_types): return {}
    ann,glb,loc = get_annotations_ex(f)
    return {k:_eval_type(v,glb,loc) for k,v in ann.items()}

# %% ../nbs/01_basics.ipynb 119
def annotations(o):
    "Annotations for `o`, or `type(o)`"
    res = {}
    if not o: return res
    res = type_hints(o)
    if not res: res = type_hints(getattr(o,'__init__',None))
    if not res: res = type_hints(type(o))
    return res

# %% ../nbs/01_basics.ipynb 122
def anno_ret(func):
    "Get the return annotation of `func`"
    return annotations(func).get('return', None) if func else None

# %% ../nbs/01_basics.ipynb 128
def _ispy3_10(): return sys.version_info.major >=3 and sys.version_info.minor >=10

def signature_ex(obj, eval_str:bool=False):
    "Backport of `inspect.signature(..., eval_str=True` to <py310"
    from inspect import Signature, Parameter, signature

    def _eval_param(ann, k, v):
        if k not in ann: return v
        return Parameter(v.name, v.kind, annotation=ann[k], default=v.default)

    if not eval_str: return signature(obj)
    if _ispy3_10(): return signature(obj, eval_str=eval_str)
    sig = signature(obj)
    if sig is None: return None
    ann = type_hints(obj)
    params = [_eval_param(ann,k,v) for k,v in sig.parameters.items()]
    return Signature(params, return_annotation=sig.return_annotation)

# %% ../nbs/01_basics.ipynb 129
def union2tuple(t):
    if (getattr(t, '__origin__', None) is Union
        or (UnionType and isinstance(t, UnionType))): return t.__args__
    return t

# %% ../nbs/01_basics.ipynb 131
def argnames(f, frame=False):
    "Names of arguments to function or frame `f`"
    code = getattr(f, 'f_code' if frame else '__code__')
    return code.co_varnames[:code.co_argcount+code.co_kwonlyargcount]

# %% ../nbs/01_basics.ipynb 133
def with_cast(f):
    "Decorator which uses any parameter annotations as preprocessing functions"
    anno, out_anno, params = annotations(f), anno_ret(f), argnames(f)
    c_out = ifnone(out_anno, noop)
    defaults = dict(zip(reversed(params), reversed(f.__defaults__ or {})))
    @functools.wraps(f)
    def _inner(*args, **kwargs):
        args = list(args)
        for i,v in enumerate(params):
            if v in anno:
                c = anno[v]
                if v in kwargs: kwargs[v] = c(kwargs[v])
                elif i<len(args): args[i] = c(args[i])
                elif v in defaults: kwargs[v] = c(defaults[v])
        return c_out(f(*args, **kwargs))
    return _inner

# %% ../nbs/01_basics.ipynb 135
def _store_attr(self, anno, **attrs):
    stored = getattr(self, '__stored_args__', None)
    for n,v in attrs.items():
        if n in anno: v = anno[n](v)
        setattr(self, n, v)
        if stored is not None: stored[n] = v

# %% ../nbs/01_basics.ipynb 136
def store_attr(names=None, self=None, but='', cast=False, store_args=None, **attrs):
    "Store params named in comma-separated `names` from calling context into attrs in `self`"
    fr = sys._getframe(1)
    args = argnames(fr, True)
    if self: args = ('self', *args)
    else: self = fr.f_locals[args[0]]
    if store_args is None: store_args = not hasattr(self,'__slots__')
    if store_args and not hasattr(self, '__stored_args__'): self.__stored_args__ = {}
    anno = annotations(self) if cast else {}
    if names and isinstance(names,str): names = re.split(', *', names)
    ns = names if names is not None else getattr(self, '__slots__', args[1:])
    added = {n:fr.f_locals[n] for n in ns}
    attrs = {**attrs, **added}
    if isinstance(but,str): but = re.split(', *', but)
    attrs = {k:v for k,v in attrs.items() if k not in but}
    return _store_attr(self, anno, **attrs)

# %% ../nbs/01_basics.ipynb 165
def attrdict(o, *ks, default=None):
    "Dict from each `k` in `ks` to `getattr(o,k)`"
    return {k:getattr(o, k, default) for k in ks}

# %% ../nbs/01_basics.ipynb 167
def properties(cls, *ps):
    "Change attrs in `cls` with names in `ps` to properties"
    for p in ps: setattr(cls,p,property(getattr(cls,p)))

# %% ../nbs/01_basics.ipynb 169
_c2w_re = re.compile(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))')
_camel_re1 = re.compile('(.)([A-Z][a-z]+)')
_camel_re2 = re.compile('([a-z0-9])([A-Z])')

# %% ../nbs/01_basics.ipynb 170
def camel2words(s, space=' '):
    "Convert CamelCase to 'spaced words'"
    return re.sub(_c2w_re, rf'{space}\1', s)

# %% ../nbs/01_basics.ipynb 172
def camel2snake(name):
    "Convert CamelCase to snake_case"
    s1   = re.sub(_camel_re1, r'\1_\2', name)
    return re.sub(_camel_re2, r'\1_\2', s1).lower()

# %% ../nbs/01_basics.ipynb 174
def snake2camel(s):
    "Convert snake_case to CamelCase"
    return ''.join(s.title().split('_'))

# %% ../nbs/01_basics.ipynb 176
def class2attr(self, cls_name):
    "Return the snake-cased name of the class; strip ending `cls_name` if it exists."
    return camel2snake(re.sub(rf'{cls_name}$', '', self.__class__.__name__) or cls_name.lower())

# %% ../nbs/01_basics.ipynb 178
def getcallable(o, attr):
    "Calls `getattr` with a default of `noop`"
    return getattr(o, attr, noop)

# %% ../nbs/01_basics.ipynb 180
def getattrs(o, *attrs, default=None):
    "List of all `attrs` in `o`"
    return [getattr(o,attr,default) for attr in attrs]

# %% ../nbs/01_basics.ipynb 183
def hasattrs(o,attrs):
    "Test whether `o` contains all `attrs`"
    return all(hasattr(o,attr) for attr in attrs)

# %% ../nbs/01_basics.ipynb 185
def setattrs(dest, flds, src):
    f = dict.get if isinstance(src, dict) else getattr
    flds = re.split(r",\s*", flds)
    for fld in flds: setattr(dest, fld, f(src, fld))

# %% ../nbs/01_basics.ipynb 188
def try_attrs(obj, *attrs):
    "Return first attr that exists in `obj`"
    for att in attrs:
        try: return getattr(obj, att)
        except: pass
    raise AttributeError(attrs)

# %% ../nbs/01_basics.ipynb 191
class GetAttrBase:
    "Basic delegation of `__getattr__` and `__dir__`"
    _attr=noop
    def __getattr__(self,k):
        if k[0]=='_' or k==self._attr: return super().__getattr__(k)
        return self._getattr(getattr(self, self._attr)[k])
    def __dir__(self): return custom_dir(self, getattr(self, self._attr))

# %% ../nbs/01_basics.ipynb 192
class GetAttr:
    "Inherit from this to have all attr accesses in `self._xtra` passed down to `self.default`"
    _default='default'
    def _component_attr_filter(self,k):
        if k.startswith('__') or k in ('_xtra',self._default): return False
        xtra = getattr(self,'_xtra',None)
        return xtra is None or k in xtra
    def _dir(self): return [k for k in dir(getattr(self,self._default)) if self._component_attr_filter(k)]
    def __getattr__(self,k):
        if self._component_attr_filter(k):
            attr = getattr(self,self._default,None)
            if attr is not None: return getattr(attr,k)
        raise AttributeError(k)
    def __dir__(self): return custom_dir(self,self._dir())
#     def __getstate__(self): return self.__dict__
    def __setstate__(self,data): self.__dict__.update(data)

# %% ../nbs/01_basics.ipynb 212
def delegate_attr(self, k, to):
    "Use in `__getattr__` to delegate to attr `to` without inheriting from `GetAttr`"
    if k.startswith('_') or k==to: raise AttributeError(k)
    try: return getattr(getattr(self,to), k)
    except AttributeError: raise AttributeError(k) from None

# %% ../nbs/01_basics.ipynb 218
class ShowPrint:
    "Base class that prints for `show`"
    def show(self, *args, **kwargs): print(str(self))

# %% ../nbs/01_basics.ipynb 220
class Int(int,ShowPrint):
    "An extensible `int`"
    pass

# %% ../nbs/01_basics.ipynb 221
class Str(str,ShowPrint):
    "An extensible `str`"
    pass
class Float(float,ShowPrint):
    "An extensible `float`"
    pass

# %% ../nbs/01_basics.ipynb 225
def flatten(o):
    "Concatenate all collections and items as a generator"
    for item in o:
        if isinstance(item, str): yield item; continue
        try: yield from flatten(item)
        except TypeError: yield item

# %% ../nbs/01_basics.ipynb 226
def concat(colls)->list:
    "Concatenate all collections and items as a list"
    return list(flatten(colls))

# %% ../nbs/01_basics.ipynb 229
def strcat(its, sep:str='')->str:
    "Concatenate stringified items `its`"
    return sep.join(map(str,its))

# %% ../nbs/01_basics.ipynb 231
def detuplify(x):
    "If `x` is a tuple with one thing, extract it"
    return None if len(x)==0 else x[0] if len(x)==1 and getattr(x, 'ndim', 1)==1 else x

# %% ../nbs/01_basics.ipynb 233
def replicate(item,match):
    "Create tuple of `item` copied `len(match)` times"
    return (item,)*len(match)

# %% ../nbs/01_basics.ipynb 235
def setify(o):
    "Turn any list like-object into a set."
    return o if isinstance(o,set) else set(listify(o))

# %% ../nbs/01_basics.ipynb 237
def merge(*ds):
    "Merge all dictionaries in `ds`"
    return {k:v for d in ds if d is not None for k,v in d.items()}

# %% ../nbs/01_basics.ipynb 239
def range_of(x):
    "All indices of collection `x` (i.e. `list(range(len(x)))`)"
    return list(range(len(x)))

# %% ../nbs/01_basics.ipynb 241
def groupby(x, key, val=noop):
    "Like `itertools.groupby` but doesn't need to be sorted, and isn't lazy, plus some extensions"
    if   isinstance(key,int): key = itemgetter(key)
    elif isinstance(key,str): key = attrgetter(key)
    if   isinstance(val,int): val = itemgetter(val)
    elif isinstance(val,str): val = attrgetter(val)
    res = {}
    for o in x: res.setdefault(key(o), []).append(val(o))
    return res

# %% ../nbs/01_basics.ipynb 245
def last_index(x, o):
    "Finds the last index of occurence of `x` in `o` (returns -1 if no occurence)"
    try: return next(i for i in reversed(range(len(o))) if o[i] == x)
    except StopIteration: return -1

# %% ../nbs/01_basics.ipynb 247
def filter_dict(d, func):
    "Filter a `dict` using `func`, applied to keys and values"
    return {k:v for k,v in d.items() if func(k,v)}

# %% ../nbs/01_basics.ipynb 250
def filter_keys(d, func):
    "Filter a `dict` using `func`, applied to keys"
    return {k:v for k,v in d.items() if func(k)}

# %% ../nbs/01_basics.ipynb 252
def filter_values(d, func):
    "Filter a `dict` using `func`, applied to values"
    return {k:v for k,v in d.items() if func(v)}

# %% ../nbs/01_basics.ipynb 254
def cycle(o):
    "Like `itertools.cycle` except creates list of `None`s if `o` is empty"
    o = listify(o)
    return itertools.cycle(o) if o is not None and len(o) > 0 else itertools.cycle([None])

# %% ../nbs/01_basics.ipynb 256
def zip_cycle(x, *args):
    "Like `itertools.zip_longest` but `cycle`s through elements of all but first argument"
    return zip(x, *map(cycle,args))

# %% ../nbs/01_basics.ipynb 258
def sorted_ex(iterable, key=None, reverse=False):
    "Like `sorted`, but if key is str use `attrgetter`; if int use `itemgetter`"
    if isinstance(key,str):   k=lambda o:getattr(o,key,0)
    elif isinstance(key,int): k=itemgetter(key)
    else: k=key
    return sorted(iterable, key=k, reverse=reverse)

# %% ../nbs/01_basics.ipynb 259
def not_(f):
    "Create new function that negates result of `f`"
    def _f(*args, **kwargs): return not f(*args, **kwargs)
    return _f

# %% ../nbs/01_basics.ipynb 261
def argwhere(iterable, f, negate=False, **kwargs):
    "Like `filter_ex`, but return indices for matching items"
    if kwargs: f = partial(f,**kwargs)
    if negate: f = not_(f)
    return [i for i,o in enumerate(iterable) if f(o)]

# %% ../nbs/01_basics.ipynb 262
def filter_ex(iterable, f=noop, negate=False, gen=False, **kwargs):
    "Like `filter`, but passing `kwargs` to `f`, defaulting `f` to `noop`, and adding `negate` and `gen`"
    if f is None: f = lambda _: True
    if kwargs: f = partial(f,**kwargs)
    if negate: f = not_(f)
    res = filter(f, iterable)
    if gen: return res
    return list(res)

# %% ../nbs/01_basics.ipynb 263
def range_of(a, b=None, step=None):
    "All indices of collection `a`, if `a` is a collection, otherwise `range`"
    if is_coll(a): a = len(a)
    return list(range(a,b,step) if step is not None else range(a,b) if b is not None else range(a))

# %% ../nbs/01_basics.ipynb 265
def renumerate(iterable, start=0):
    "Same as `enumerate`, but returns index as 2nd element instead of 1st"
    return ((o,i) for i,o in enumerate(iterable, start=start))

# %% ../nbs/01_basics.ipynb 267
def first(x, f=None, negate=False, **kwargs):
    "First element of `x`, optionally filtered by `f`, or None if missing"
    x = iter(x)
    if f: x = filter_ex(x, f=f, negate=negate, gen=True, **kwargs)
    return next(x, None)

# %% ../nbs/01_basics.ipynb 269
def only(o):
    "Return the only item of `o`, raise if `o` doesn't have exactly one item"
    it = iter(o)
    try: res = next(it)
    except StopIteration: raise ValueError('iterable has 0 items') from None
    try: next(it)
    except StopIteration: return res
    raise ValueError(f'iterable has more than 1 item')

# %% ../nbs/01_basics.ipynb 271
def nested_attr(o, attr, default=None):
    "Same as `getattr`, but if `attr` includes a `.`, then looks inside nested objects"
    try:
        for a in attr.split("."): o = getattr(o, a)
    except AttributeError: return default
    return o

# %% ../nbs/01_basics.ipynb 273
def nested_setdefault(o, attr, default):
    "Same as `setdefault`, but if `attr` includes a `.`, then looks inside nested objects"
    attrs = attr.split('.')
    for a in attrs[:-1]: o = o.setdefault(a, type(o)())
    return o.setdefault(attrs[-1], default)

# %% ../nbs/01_basics.ipynb 277
def nested_callable(o, attr):
    "Same as `nested_attr` but if not found will return `noop`"
    return nested_attr(o, attr, noop)

# %% ../nbs/01_basics.ipynb 279
def _access(coll, idx): return coll.get(idx, None) if hasattr(coll, 'get') else coll[idx] if idx<len(coll) else None

def _nested_idx(coll, *idxs):
    *idxs,last_idx = idxs
    for idx in idxs:
        if isinstance(coll,str) or not isinstance(coll, typing.Collection): return None,None
        coll = coll.get(idx, None) if hasattr(coll, 'get') else coll[idx] if idx<len(coll) else None
    return coll,last_idx

# %% ../nbs/01_basics.ipynb 280
def nested_idx(coll, *idxs):
    "Index into nested collections, dicts, etc, with `idxs`"
    if not coll or not idxs: return coll
    coll,idx = _nested_idx(coll, *idxs)
    if not coll or not idxs: return coll
    return _access(coll, idx)

# %% ../nbs/01_basics.ipynb 282
def set_nested_idx(coll, value, *idxs):
    "Set value indexed like `nested_idx"
    coll,idx = _nested_idx(coll, *idxs)
    coll[idx] = value

# %% ../nbs/01_basics.ipynb 284
def val2idx(x):
    "Dict from value to index"
    return {v:k for k,v in enumerate(x)}

# %% ../nbs/01_basics.ipynb 286
def uniqueify(x, sort=False, bidir=False, start=None):
    "Unique elements in `x`, optional `sort`, optional return reverse correspondence, optional prepend with elements."
    res = list(dict.fromkeys(x))
    if start is not None: res = listify(start)+res
    if sort: res.sort()
    return (res,val2idx(res)) if bidir else res

# %% ../nbs/01_basics.ipynb 288
# looping functions from https://github.com/willmcgugan/rich/blob/master/rich/_loop.py
def loop_first_last(values):
    "Iterate and generate a tuple with a flag for first and last value."
    iter_values = iter(values)
    try: previous_value = next(iter_values)
    except StopIteration: return
    first = True
    for value in iter_values:
        yield first,False,previous_value
        first,previous_value = False,value
    yield first,True,previous_value

# %% ../nbs/01_basics.ipynb 290
def loop_first(values):
    "Iterate and generate a tuple with a flag for first value."
    return ((b,o) for b,_,o in loop_first_last(values))

# %% ../nbs/01_basics.ipynb 292
def loop_last(values):
    "Iterate and generate a tuple with a flag for last value."
    return ((b,o) for _,b,o in loop_first_last(values))

# %% ../nbs/01_basics.ipynb 295
num_methods = """
    __add__ __sub__ __mul__ __matmul__ __truediv__ __floordiv__ __mod__ __divmod__ __pow__
    __lshift__ __rshift__ __and__ __xor__ __or__ __neg__ __pos__ __abs__
""".split()
rnum_methods = """
    __radd__ __rsub__ __rmul__ __rmatmul__ __rtruediv__ __rfloordiv__ __rmod__ __rdivmod__
    __rpow__ __rlshift__ __rrshift__ __rand__ __rxor__ __ror__
""".split()
inum_methods = """
    __iadd__ __isub__ __imul__ __imatmul__ __itruediv__
    __ifloordiv__ __imod__ __ipow__ __ilshift__ __irshift__ __iand__ __ixor__ __ior__
""".split()

# %% ../nbs/01_basics.ipynb 296
class fastuple(tuple):
    "A `tuple` with elementwise ops and more friendly __init__ behavior"
    def __new__(cls, x=None, *rest):
        if x is None: x = ()
        if not isinstance(x,tuple):
            if len(rest): x = (x,)
            else:
                try: x = tuple(iter(x))
                except TypeError: x = (x,)
        return super().__new__(cls, x+rest if rest else x)

    def _op(self,op,*args):
        if not isinstance(self,fastuple): self = fastuple(self)
        return type(self)(map(op,self,*map(cycle, args)))

    def mul(self,*args):
        "`*` is already defined in `tuple` for replicating, so use `mul` instead"
        return fastuple._op(self, operator.mul,*args)

    def add(self,*args):
        "`+` is already defined in `tuple` for concat, so use `add` instead"
        return fastuple._op(self, operator.add,*args)

def _get_op(op):
    if isinstance(op,str): op = getattr(operator,op)
    def _f(self,*args): return self._op(op,*args)
    return _f

for n in num_methods:
    if not hasattr(fastuple, n) and hasattr(operator,n): setattr(fastuple,n,_get_op(n))

for n in 'eq ne lt le gt ge'.split(): setattr(fastuple,n,_get_op(n))
setattr(fastuple,'__invert__',_get_op('__not__'))
setattr(fastuple,'max',_get_op(max))
setattr(fastuple,'min',_get_op(min))

# %% ../nbs/01_basics.ipynb 314
class _Arg:
    def __init__(self,i): self.i = i
arg0 = _Arg(0)
arg1 = _Arg(1)
arg2 = _Arg(2)
arg3 = _Arg(3)
arg4 = _Arg(4)

# %% ../nbs/01_basics.ipynb 315
class bind:
    "Same as `partial`, except you can use `arg0` `arg1` etc param placeholders"
    def __init__(self, func, *pargs, **pkwargs):
        self.func,self.pargs,self.pkwargs = func,pargs,pkwargs
        self.maxi = max((x.i for x in pargs if isinstance(x, _Arg)), default=-1)

    def __call__(self, *args, **kwargs):
        args = list(args)
        kwargs = {**self.pkwargs,**kwargs}
        for k,v in kwargs.items():
            if isinstance(v,_Arg): kwargs[k] = args.pop(v.i)
        fargs = [args[x.i] if isinstance(x, _Arg) else x for x in self.pargs] + args[self.maxi+1:]
        return self.func(*fargs, **kwargs)

# %% ../nbs/01_basics.ipynb 327
def mapt(func, *iterables):
    "Tuplified `map`"
    return tuple(map(func, *iterables))

# %% ../nbs/01_basics.ipynb 329
def map_ex(iterable, f, *args, gen=False, **kwargs):
    "Like `map`, but use `bind`, and supports `str` and indexing"
    g = (bind(f,*args,**kwargs) if callable(f)
         else f.format if isinstance(f,str)
         else f.__getitem__)
    res = map(g, iterable)
    if gen: return res
    return list(res)

# %% ../nbs/01_basics.ipynb 337
def compose(*funcs, order=None):
    "Create a function that composes all functions in `funcs`, passing along remaining `*args` and `**kwargs` to all"
    funcs = listify(funcs)
    if len(funcs)==0: return noop
    if len(funcs)==1: return funcs[0]
    if order is not None: funcs = sorted_ex(funcs, key=order)
    def _inner(x, *args, **kwargs):
        for f in funcs: x = f(x, *args, **kwargs)
        return x
    return _inner

# %% ../nbs/01_basics.ipynb 339
def maps(*args, retain=noop):
    "Like `map`, except funcs are composed first"
    f = compose(*args[:-1])
    def _f(b): return retain(f(b), b)
    return map(_f, args[-1])

# %% ../nbs/01_basics.ipynb 341
def partialler(f, *args, order=None, **kwargs):
    "Like `functools.partial` but also copies over docstring"
    fnew = partial(f,*args,**kwargs)
    fnew.__doc__ = f.__doc__
    if order is not None: fnew.order=order
    elif hasattr(f,'order'): fnew.order=f.order
    return fnew

# %% ../nbs/01_basics.ipynb 345
def instantiate(t):
    "Instantiate `t` if it's a type, otherwise do nothing"
    return t() if isinstance(t, type) else t

# %% ../nbs/01_basics.ipynb 347
def _using_attr(f, attr, x): return f(getattr(x,attr))

# %% ../nbs/01_basics.ipynb 348
def using_attr(f, attr):
    "Construct a function which applies `f` to the argument's attribute `attr`"
    return partial(_using_attr, f, attr)

# %% ../nbs/01_basics.ipynb 352
class _Self:
    "An alternative to `lambda` for calling methods on passed object."
    def __init__(self): self.nms,self.args,self.kwargs,self.ready = [],[],[],True
    def __repr__(self): return f'self: {self.nms}({self.args}, {self.kwargs})'

    def __call__(self, *args, **kwargs):
        if self.ready:
            x = args[0]
            for n,a,k in zip(self.nms,self.args,self.kwargs):
                x = getattr(x,n)
                if callable(x) and a is not None: x = x(*a, **k)
            return x
        else:
            self.args.append(args)
            self.kwargs.append(kwargs)
            self.ready = True
            return self

    def __getattr__(self,k):
        if not self.ready:
            self.args.append(None)
            self.kwargs.append(None)
        self.nms.append(k)
        self.ready = False
        return self

    def _call(self, *args, **kwargs):
        self.args,self.kwargs,self.nms = [args],[kwargs],['__call__']
        self.ready = True
        return self

# %% ../nbs/01_basics.ipynb 353
class _SelfCls:
    def __getattr__(self,k): return getattr(_Self(),k)
    def __getitem__(self,i): return self.__getattr__('__getitem__')(i)
    def __call__(self,*args,**kwargs): return self.__getattr__('_call')(*args,**kwargs)

Self = _SelfCls()

# %% ../nbs/01_basics.ipynb 354
_all_ = ['Self']

# %% ../nbs/01_basics.ipynb 360
def copy_func(f):
    "Copy a non-builtin function (NB `copy.copy` does not work for this)"
    if not isinstance(f,FunctionType): return copy(f)
    fn = FunctionType(f.__code__, f.__globals__, f.__name__, f.__defaults__, f.__closure__)
    fn.__kwdefaults__ = f.__kwdefaults__
    fn.__dict__.update(f.__dict__)
    fn.__annotations__.update(f.__annotations__)
    fn.__qualname__ = f.__qualname__
    return fn

# %% ../nbs/01_basics.ipynb 367
def patch_to(cls, as_prop=False, cls_method=False):
    "Decorator: add `f` to `cls`"
    if not isinstance(cls, (tuple,list)): cls=(cls,)
    def _inner(f):
        for c_ in cls:
            nf = copy_func(f)
            nm = f.__name__
            # `functools.update_wrapper` when passing patched function to `Pipeline`, so we do it manually
            for o in functools.WRAPPER_ASSIGNMENTS: setattr(nf, o, getattr(f,o))
            nf.__qualname__ = f"{c_.__name__}.{nm}"
            if cls_method:
                setattr(c_, nm, MethodType(nf, c_))
            else:
                setattr(c_, nm, property(nf) if as_prop else nf)
        # Avoid clobbering existing functions
        return globals().get(nm, builtins.__dict__.get(nm, None))
    return _inner

# %% ../nbs/01_basics.ipynb 378
def patch(f=None, *, as_prop=False, cls_method=False):
    "Decorator: add `f` to the first parameter's class (based on f's type annotations)"
    if f is None: return partial(patch, as_prop=as_prop, cls_method=cls_method)
    ann,glb,loc = get_annotations_ex(f)
    cls = union2tuple(eval_type(ann.pop('cls') if cls_method else next(iter(ann.values())), glb, loc))
    return patch_to(cls, as_prop=as_prop, cls_method=cls_method)(f)

# %% ../nbs/01_basics.ipynb 386
def patch_property(f):
    "Deprecated; use `patch(as_prop=True)` instead"
    warnings.warn("`patch_property` is deprecated and will be removed; use `patch(as_prop=True)` instead")
    cls = next(iter(f.__annotations__.values()))
    return patch_to(cls, as_prop=True)(f)

# %% ../nbs/01_basics.ipynb 388
def compile_re(pat):
    "Compile `pat` if it's not None"
    return None if pat is None else re.compile(pat)

# %% ../nbs/01_basics.ipynb 390
class ImportEnum(enum.Enum):
    "An `Enum` that can have its values imported"
    @classmethod
    def imports(cls):
        g = sys._getframe(1).f_locals
        for o in cls: g[o.name]=o

# %% ../nbs/01_basics.ipynb 393
class StrEnum(str,ImportEnum):
    "An `ImportEnum` that behaves like a `str`"
    def __str__(self): return self.name

# %% ../nbs/01_basics.ipynb 395
def str_enum(name, *vals):
    "Simplified creation of `StrEnum` types"
    return StrEnum(name, {o:o for o in vals})

# %% ../nbs/01_basics.ipynb 397
class Stateful:
    "A base class/mixin for objects that should not serialize all their state"
    _stateattrs=()
    def __init__(self,*args,**kwargs):
        self._init_state()
        super().__init__(*args,**kwargs) # required for mixin usage

    def __getstate__(self):
        return {k:v for k,v in self.__dict__.items()
                if k not in self._stateattrs+('_state',)}

    def __setstate__(self, state):
        self.__dict__.update(state)
        self._init_state()

    def _init_state(self):
        "Override for custom init and deserialization logic"
        self._state = {}

# %% ../nbs/01_basics.ipynb 403
class PrettyString(str):
    "Little hack to get strings to show properly in Jupyter."
    def __repr__(self): return self

# %% ../nbs/01_basics.ipynb 409
def even_mults(start, stop, n):
    "Build log-stepped array from `start` to `stop` in `n` steps."
    if n==1: return stop
    mult = stop/start
    step = mult**(1/(n-1))
    return [start*(step**i) for i in range(n)]

# %% ../nbs/01_basics.ipynb 411
def num_cpus():
    "Get number of cpus"
    try:                   return len(os.sched_getaffinity(0))
    except AttributeError: return os.cpu_count()

defaults.cpus = num_cpus()

# %% ../nbs/01_basics.ipynb 413
def add_props(f, g=None, n=2):
    "Create properties passing each of `range(n)` to f"
    if g is None: return (property(partial(f,i)) for i in range(n))
    return (property(partial(f,i), partial(g,i)) for i in range(n))

# %% ../nbs/01_basics.ipynb 416
def _typeerr(arg, val, typ): return TypeError(f"{arg}=={val} not {typ}")

# %% ../nbs/01_basics.ipynb 417
def typed(f):
    "Decorator to check param and return types at runtime"
    names = f.__code__.co_varnames
    anno = annotations(f)
    ret = anno.pop('return',None)
    def _f(*args,**kwargs):
        kw = {**kwargs}
        if len(anno) > 0:
            for i,arg in enumerate(args): kw[names[i]] = arg
            for k,v in kw.items():
                if k in anno and not isinstance(v,anno[k]): raise _typeerr(k, v, anno[k])
        res = f(*args,**kwargs)
        if ret is not None and not isinstance(res,ret): raise _typeerr("return", res, ret)
        return res
    return functools.update_wrapper(_f, f)

# %% ../nbs/01_basics.ipynb 425
def exec_new(code):
    "Execute `code` in a new environment and return it"
    pkg = None if __name__=='__main__' else Path().cwd().name
    g = {'__name__': __name__, '__package__': pkg}
    exec(code, g)
    return g

# %% ../nbs/01_basics.ipynb 427
def exec_import(mod, sym):
    "Import `sym` from `mod` in a new environment"
#     pref = '' if __name__=='__main__' or mod[0]=='.' else '.'
    return exec_new(f'from {mod} import {sym}')

# %% ../nbs/01_basics.ipynb 428
def str2bool(s):
    "Case-insensitive convert string `s` too a bool (`y`,`yes`,`t`,`true`,`on`,`1`->`True`)"
    if not isinstance(s,str): return bool(s)
    if not s: return False
    s = s.lower()
    if s in ('y', 'yes', 't', 'true', 'on', '1'): return 1
    elif s in ('n', 'no', 'f', 'false', 'off', '0'): return 0
    else: raise ValueError()
