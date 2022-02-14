# Load the Python Standard and DesignScript Libraries
import sys
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

from functools import reduce

# The inputs to this node will be stored as a list in the IN variables.
dataEnteringNode = IN

# Place your code below this line

###################################################################################################
curry = lambda f: lambda a,*args: f(a, *args) if (len(args)) else lambda *args: f(a, *args)

add = curry(lambda a,b: a + b)

filter = curry(filter)
map = curry(map)

def _take(length, iter):
    res = []
    for a in iter:
        res.append(a)
        if len(res) == length:
            return res
take = curry(_take)
reduce = curry(reduce)

go = lambda *args: reduce(lambda a,f: f(a), args) ## 함수도 축약 가능 ##
###########################################

    
Qfunc_len = lambda list, length: go( list,
        filter(lambda a: a % 2),
        map(lambda a: a * a),
        take(length),
        reduce(add)
        )
    
Qfunc = lambda list: go( list,
        filter(lambda a: not a % 2),
        filter(lambda a: not a % 4),
        map(lambda a: a * a),
        reduce(add)
        )

###################################################################################################




f1 = lambda list, length: go(list,
    filter(lambda a: a % 2),
    map(lambda a: a * a),
    take(length),
    reduce(add))
    
f2 = lambda list: go(list,
    filter(lambda a: a % 2),
    map(lambda a: a * a),
    reduce(add))

result = f2([1,2,3,4,5,6,7,8,9,10])
#result = add(15)(20)

# Assign your output to the OUT variable.
OUT = result