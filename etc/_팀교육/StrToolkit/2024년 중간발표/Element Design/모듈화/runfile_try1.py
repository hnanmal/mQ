from en_2dstruct.userfunction import *
import copy
import os
import json

## 폴더이름문자열 텍스트파일: 현재 exe 경로에서 
## tgtPath = 읽어온 텍스트 내용

file1 = open('HSD_model_path.txt','r', encoding='UTF8')
indata = file1.readlines()
file1.close()

targetpath = indata[0]

if targetpath == '':
    os.chdir(targetpath)

foldername = 'HSD_frame_module_IO' #
filename = findReadFile(foldername,'HSD_load distribution')
path = foldername+'/'+filename

runtime = getTimeStamp()

frame_dict = rabbit2kgbsturct(path)

totalresult = {}

for frk in frame_dict.keys():
    frm = frame_dict[frk] 

    #frame 별로 반복
    resultf = anabunny(*frm)
    
    totalresult[frk] = copy.deepcopy(resultf)


save_revitresult(totalresult, foldername, runtime)

# element force 그리기 
force_res = {}
for frk in totalresult.keys(): # frame별
    frm = totalresult[frk]

    lt_res = {}
    for lt in frm.keys(): #load type 별
        frmlt = frm[lt]

        el_res = {}
        for elk in frmlt['element'].keys(): # element 별
            el_res[elk] = Showelementforce(elk, frmlt['element'], frame_dict[frk][4][lt],0)[elk]

        lt_res[lt] = el_res

    force_res[frk] = lt_res



with open(foldername +'/HSD_element_force_json'+runtime+'.txt', 'w') as outfilevar:
    json.dump(force_res, outfilevar)



print('run complete')
print('input : ', filename)
print(f'result : HSD_element_force_json{runtime}, HSD_element_force_json{runtime}',)
# os.system("pause")





#####################################################################

