# Python 표준 및 DesignScript 라이브러리 로드
import sys
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

import io

# 이 노드에 대한 입력값은 IN 변수에 리스트로 저장됩니다.
dataEnteringNode = IN

path = r'd:\mk\mQ\Laboratory\0_상상\test.py'
# 코드를 이 선 아래에 배치

_f = open(r"D:\mk\mQ\Laboratory\0_상상\test.py", 'r', encoding='UTF-8')
f = ''.join(_f)

result = exec(f)

#for i in range(1,6):
#    f.write(f"{i}번째 줄이다.\n")

#f.close()
# 출력을 OUT 변수에 지정합니다.
OUT = result