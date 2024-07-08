

def getTimeStamp():
    import datetime
    timeStr = datetime.datetime.now().strftime('_%Y-%m-%d_%H%M%S')
    res = timeStr
    return res


def findReadFile(foldername, fileheadername, extralocation = ''): 
    import os

    # os.chdir(extralocation)
    path = foldername


    allfiles =os.listdir(path + '/')

    inres = []
    for s in allfiles: 

        if s.find(fileheadername) != -1: # 
            inres.append(s)

    inres.sort(reverse = True)


    return inres[0]
