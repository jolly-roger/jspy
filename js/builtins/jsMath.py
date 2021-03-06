import math
import random

from js.builtins import get_arg, put_native_function
from js.builtins.object_space import object_space

from js.put_property import put_property

from js.object_space import w_return

from js.wrappers._w import _w
from js.wrappers.W_Math import W_Math


def setup(global_object):
    w_Math = W_Math()
    put_property(global_object, u'Math', w_Math)

    put_native_function(w_Math, u'abs', js_abs, params=[u'x'])
    put_native_function(w_Math, u'floor', floor, params=[u'x'])
    put_native_function(w_Math, u'round', js_round, params=[u'x'])
    put_native_function(w_Math, u'random', js_random)
    put_native_function(w_Math, u'min', js_min, params=[u'value1', u'value2'])
    put_native_function(w_Math, u'max', js_max, params=[u'value1', u'value2'])
    put_native_function(w_Math, u'pow', js_pow, params=[u'x', u'y'])
    put_native_function(w_Math, u'sqrt', js_sqrt, params=[u'x'])
    put_native_function(w_Math, u'log', js_log, params=[u'x'])
    put_native_function(w_Math, u'sin', js_sin, params=[u'x'])
    put_native_function(w_Math, u'tan', js_tan, params=[u'x'])
    put_native_function(w_Math, u'acos', js_acos, params=[u'x'])
    put_native_function(w_Math, u'asin', js_asin, params=[u'x'])
    put_native_function(w_Math, u'atan', js_atan, params=[u'x'])
    put_native_function(w_Math, u'atan2', js_atan2, params=[u'y', u'x'])
    put_native_function(w_Math, u'ceil', js_ceil, params=[u'x'])
    put_native_function(w_Math, u'cos', js_cos, params=[u'x'])
    put_native_function(w_Math, u'exp', js_exp, params=[u'x'])

    # 15.8.1

    # 15.8.1.1
    put_property(w_Math, u'E', _w(E), writable=False, enumerable=False, configurable=False)

    # 15.8.1.2
    put_property(w_Math, u'LN10', _w(LN10), writable=False, enumerable=False, configurable=False)

    # 15.8.1.3
    put_property(w_Math, u'LN2', _w(LN2), writable=False, enumerable=False, configurable=False)

    # 15.8.1.4
    put_property(w_Math, u'LOG2E', _w(LOG2E), writable=False, enumerable=False, configurable=False)

    # 15.8.1.5
    put_property(w_Math, u'LOG10E', _w(LOG10E), writable=False, enumerable=False, configurable=False)

    # 15.8.1.6
    put_property(w_Math, u'PI', _w(PI), writable=False, enumerable=False, configurable=False)

    # 15.8.1.7
    put_property(w_Math, u'SQRT1_2', _w(SQRT1_2), writable=False, enumerable=False, configurable=False)

    # 15.8.1.8
    put_property(w_Math, u'SQRT2', _w(SQRT2), writable=False, enumerable=False, configurable=False)


# 15.8.2.9
@w_return
def floor(this, args):
    arg0 = get_arg(args, 0)
    x = arg0.ToNumber()

    if math.isnan(x):
        return float('nan')

    return math.floor(x)


# 15.8.2.1
@w_return
def js_abs(this, args):
    arg0 = get_arg(args, 0)
    x = arg0.ToNumber()

    if math.isnan(x):
        return float('nan')

    return abs(x)


# 15.8.2.15
@w_return
def js_round(this, args):
    arg0 = get_arg(args, 0)
    x = arg0.ToNumber()

    if math.isnan(x):
        return x

    if x == 0:
        return x

    if x > 0 and x < 0.5:
        return 0

    if x < 0 and x >= -0.5:
        return -0.0

    if math.isinf(x):
        return x

    return math.floor(x + 0.5)


def isodd(i):
    import math
    return math.fmod(i, 2.0) == 1.0


CMP_LT = -1
CMP_GT = 1
CMP_EQ = 0


def cmp_signed_zero(a, b):
    from js.baseop import sign
    sign_a = sign(a)
    sign_b = sign(b)

    if a == 0 and b == 0:
        if sign_a < sign_b:
            return CMP_LT
        if sign_a > sign_b:
            return CMP_GT
        return CMP_EQ

    if a < b:
        return CMP_LT
    if a > b:
        return CMP_GT
    return CMP_EQ


def eq_signed_zero(a, b):
    return cmp_signed_zero(a, b) is CMP_EQ


# 15.8.2.13
@w_return
def js_pow(this, args):
    w_x = get_arg(args, 0)
    w_y = get_arg(args, 1)
    x = w_x.ToNumber()
    y = w_y.ToNumber()

    if math.isnan(y):
        return float('nan')
    if y == 0:
        return 1
    if math.isnan(x):
        return float('nan')
    if abs(x) > 1 and y == float('inf'):
        return float('inf')
    if abs(x) > 1 and y == float('-inf'):
        return 0
    if abs(x) == 1 and math.isinf(y):
        return float('nan')
    if abs(x) < 1 and y == float('inf'):
        return 0
    if abs(x) < 1 and y == float('-inf'):
        return float('inf')
    if x == float('inf') and y > 0:
        return float('inf')
    if x == float('inf') and y < 0:
        return 0
    if x == float('-inf') and y > 0 and isodd(y):
        return float('-inf')
    if x == float('-inf') and y > 0 and not isodd(y):
        return float('inf')
    if x == float('-inf') and y < 0 and isodd(y):
        return -0.0
    if x == float('-inf') and y < 0 and not isodd(y):
        return 0
    if eq_signed_zero(x, 0.0) and y > 0:
        return 0
    if eq_signed_zero(x, 0.0) and y < 0:
        return float('inf')
    if eq_signed_zero(x, -0.0) and y > 0 and isodd(y):
        return -0.0
    if eq_signed_zero(x, -0.0) and y > 0 and not isodd(y):
        return +0
    if eq_signed_zero(x, -0.0) and y < 0 and isodd(y):
        return float('-inf')
    if eq_signed_zero(x, -0.0) and y < 0 and not isodd(y):
        return float('inf')
    if x < 0 and not isinstance(y, int):
        return float('nan')

    try:
        return math.pow(x, y)
    except OverflowError:
        return float('inf')


# 15.8.2.17
@w_return
def js_sqrt(this, args):
    arg0 = get_arg(args, 0)
    x = arg0.ToNumber()

    if math.isnan(x):
        return float('nan')

    if x < 0:
        return float('nan')

    if math.isinf(x):
        return float('inf')

    return math.sqrt(x)


# 15.8.2.10
@w_return
def js_log(this, args):
    arg0 = get_arg(args, 0)
    x = arg0.ToNumber()

    if math.isnan(x):
        return float('nan')

    if x < 0:
        return float('nan')

    if x == 0:
        return float('-inf')

    if x == float('inf'):
        return float('inf')

    return math.log(x)


# 15.8.2.11
@w_return
def js_min(this, args):
    values = []
    for arg in args:
        value = arg.ToNumber()
        if math.isnan(value):
            return float('nan')
        values.append(value)

    if len(values) == 0:
        return float('inf')

    if len(values) == 1:
        return values[0]

    min_ = min(values[0], values[1])

    for i in xrange(2, len(values)):
        min_ = min(values[i], min_)

    if min_ == 0 and -0.0 in values:
        min_ = -0.0

    return min_


# 15.8.2.12
@w_return
def js_max(this, args):
    values = []
    for arg in args:
        value = arg.ToNumber()
        if math.isnan(value):
            return float('nan')
        values.append(value)

    if len(values) == 0:
        return float('-inf')

    if len(values) == 1:
        return values[0]

    max_ = max(values[0], values[1])

    for i in xrange(2, len(values)):
        max_ = max(values[i], max_)

    return max_


# 15.8.2.17
@w_return
def js_sin(this, args):
    arg0 = get_arg(args, 0)
    x = arg0.ToNumber()

    if math.isnan(x) or math.isinf(x):
        return float('nan')

    if x < 0:
        return float('nan')

    return math.sin(x)


# 15.8.2.18
@w_return
def js_tan(this, args):
    arg0 = get_arg(args, 0)
    x = arg0.ToNumber()

    if math.isnan(x) or math.isinf(x):
        return float('nan')

    if x < 0:
        return float('nan')

    return math.tan(x)


# 15.8.2.2
@w_return
def js_acos(this, args):
    arg0 = get_arg(args, 0)
    x = arg0.ToNumber()

    if math.isnan(x) or math.isinf(x):
        return float('nan')

    if x > 1 or x < -1:
        return float('nan')

    return math.acos(x)


# 15.8.2.3
@w_return
def js_asin(this, args):
    arg0 = get_arg(args, 0)
    x = arg0.ToNumber()

    if math.isnan(x) or math.isinf(x):
        return float('nan')

    if x > 1 or x < -1:
        return float('nan')

    return math.asin(x)


# 15.8.2.4
@w_return
def js_atan(this, args):
    arg0 = get_arg(args, 0)
    x = arg0.ToNumber()

    if math.isnan(x):
        return float('nan')

    if x == float('inf'):
        return math.pi / 2

    if x == float('-inf'):
        return -math.pi / 2

    return math.atan(x)


# 15.8.2.5
@w_return
def js_atan2(this, args):
    arg0 = get_arg(args, 0)
    arg1 = get_arg(args, 1)
    y = arg0.ToNumber()
    x = arg1.ToNumber()

    if math.isnan(x) or math.isnan(y):
        return float('nan')

    return math.atan2(y, x)


# 15.8.2.6
@w_return
def js_ceil(this, args):
    arg0 = get_arg(args, 0)
    x = arg0.ToNumber()

    if math.isnan(x):
        return float('nan')

    if x == float('inf'):
        return float('inf')

    if x == float('-inf'):
        return float('-inf')

    return math.ceil(x)


# 15.8.2.7
@w_return
def js_cos(this, args):
    arg0 = get_arg(args, 0)
    x = arg0.ToNumber()

    if math.isnan(x) or math.isinf(x):
        return float('nan')

    return math.cos(x)


# 15.8.2.8
@w_return
def js_exp(this, args):
    arg0 = get_arg(args, 0)
    x = arg0.ToNumber()

    if math.isnan(x):
        return float('nan')

    if x == float('inf'):
        return float('inf')

    if x == float('-inf'):
        return 0

    return math.exp(x)


# 15.8.2.14
@w_return
def js_random(this, args):
    return random.random()

# 15.8.1.1
E = math.e

# 15.8.1.2
LN10 = math.log(10)

# 15.8.1.3
LN2 = math.log(2)

# 15.8.1.4
LOG2E = math.log(math.e) / math.log(2)

# 15.8.1.5
LOG10E = math.log10(math.e)

# 15.8.1.6
PI = math.pi

# 15.8.1.7
SQRT1_2 = math.sqrt(0.5)

# 15.8.1.8
SQRT2 = math.sqrt(2)
