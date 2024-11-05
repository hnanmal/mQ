################Module For Functional Programing#########################
from functools import reduce
from itertools import chain
from itertools import groupby
from copy import deepcopy

curry = lambda f: lambda a, *args: (
    f(a, *args) if (len(args)) else lambda *args: f(a, *args)
)

filter, map, reduce = curry(filter), curry(map), curry(reduce)

go = lambda *args: reduce(lambda a, f: f(a), args)  ## 함수도 축약 가능 ##


def dictUpdate(dic1, dic2):
    dic1.update(dic2)
    return dic1


def dictsMerge(dics):
    res = reduce(dictUpdate, dics)
    return res


def dictDeleteKeys(dic, keys):
    for k in keys:
        del dic[k]
    return dic


def flat(a):
    if isinstance(a, list):
        for i in a:
            yield from flat(i)
    else:
        yield a


def grpBy(iter, key):
    f, grpKeys, grps = key, [], []
    sorted_ = sorted(iter, key=f)
    for key, grp_data in groupby(sorted_, key=f):
        grpKeys.append(key)
        grps.append(list(grp_data))
    return grps, grpKeys


#########################################################################
