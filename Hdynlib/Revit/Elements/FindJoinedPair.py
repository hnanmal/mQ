def findJoinedPair(elements):
    result = []
    Ididx = [i.Id for i in elements]
    _log = []
    for i in elements:
        tmp1= [i]
        if i.Id not in _log:
            _log.append(i.Id)
            joinlist = i.GetJoinedElements()
            if len(joinlist):
                for j in joinlist:
                    if j.Id in Ididx:
                        idx = Ididx.index(j.Id)
                        _log.append(idx)
                        tmp1.append(j)
                        
            result.append(tmp1)
        else:
            pass
    return result