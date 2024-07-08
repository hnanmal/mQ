import json


def calljson(filepath):

    with open(filepath, 'r') as f:
        json_data = json.load(f)

    return json_data # json.dumps(json_data) #, indent="\t"


# datas = calljson('predator/HSD_load distribution_2024-06-24_13_26.txt')
# print(datas)
# print(datas[0][:])
# print(datas[0][6]["startNode"])
# print(len(datas))
# print(len(datas[3]))
# print(datas[0][0].keys())
# print(datas[0][0]['sectionProp'])
# print(json.dumps(datas[0], indent="\t"))

def loadtype_filter(idict, name_):
    lt = idict['load_type']

    if lt == "joint":
        return [idict['load_type']]
    elif lt =="uniform":
        return [idict['load_type'],name_ , idict['wx'], idict['wy']]
    elif lt =="beampoint":
        return [idict['load_type']]
    elif lt =="beamtriangle":
        return [idict['load_type']]
    else:
        print("미구현 load type")



def nodeseparator(nd):
    # print(nd)
    name = nd['name']
    x = nd.get('X')
    y = nd.get('Y')
    z = nd.get('Z')
    if x == None:
        coordinate = [y,z] 
    elif y == None:
        coordinate = [x,z]  
    elif z == None:
        coordinate = [x,y]
    else:
        coordinate = [x,y,z]
    return [name, *coordinate]


def rearraytoframe(datas):

    frame_number = 1
    frame_dict = {}
    for frame in datas: 
        frame_name = f"frame{frame_number}"
        frame_number = frame_number + 1
        
        #element별 input에 사용되는 변수 초기화
        nodedict = {}
        element_inputframe = []
        element_inputtruss = []
        boundary_input =[]
        ndtest = {}
        GUID = {}
        unbrsegment = {}
        load_input = {} # 아래와 같이 load input을 {loadtype : []} 형태로 정의
        for element_d in frame:
            lk = element_d.get('load')
            if lk != None:
                for i in lk.keys():
                    load_input[i] = []

        for element_d in frame: 
            # node 정보 수집 # z가 마지막에 오니까..


            # nodedict.update({element_d['startNode']['name']:list(element_d['startNode'].values())})
            # nodedict.update({element_d['endNode']['name']:list(element_d['endNode'].values())})


            ##중복 엘리먼트에 대한 내용 확인 
            ndtest.update({element_d['startNode']['name'] : element_d['startNode']})
            ndtest.update({element_d['endNode']['name'] : element_d['endNode']})
            node = nodeseparator(element_d['startNode'])
            # print(node)
            node2 = nodeseparator(element_d['endNode'])
            # print(element_d['element_name'])
            # print(node, node2) # 확인
            

            # element evaulate
            A = element_d['sectionProp']['A']
            I = element_d['sectionProp']['I']
            E = element_d['materialPropDict']['E']
            if element_d['role'] == 'turss':
                element_inputtruss.append([element_d['element_name'], element_d['startNode']['name'],element_d['endNode']['name'],A,E])
            else:
                element_inputframe.append([element_d['element_name'], element_d['startNode']['name'],element_d['endNode']['name'],A,I,E])

            # 지점조건
            bd = element_d.get("boundary")
            if bd != None:
                boundary_input.append([bd['node_name'], *bd['condition']])



            # Load 자료 정리
            load_d = element_d.get('load')
            if load_d != None:

                for loadtype in load_d.keys():
                    load = load_d[loadtype]
  
                    if load != None:
                        load_input[loadtype].append(loadtype_filter(load, element_d['element_name']))

        

            #GUID 정보 저장
            GUID[element_d['element_name']] = element_d['GUID']

            #unbrsegment 정보저장
            unbrsegment[element_d['element_name']] = element_d.get('unbr_segment')
            
        nodelist=[]
        for i in list(ndtest.values()):
            nodelist.append(nodeseparator(i))
        # print(nodelist)
        frame_dict[frame_name] = [nodelist, element_inputtruss, element_inputframe, boundary_input, load_input, GUID, unbrsegment]



    return frame_dict



#######################################
# 사용자 사용함수 

def rabbit2kgbsturct(filepath): 
    datas = calljson(filepath)
    # print("allkeys",datas[0][0].keys())
    frame_dict = rearraytoframe(datas)

    return frame_dict


# def getrabbitguid(filepath):
#     frame_number = 1
#     frame_dict = {}
#     datas = calljson(filepath)

#     for frame in datas: 
#         frame_name = f"frame{frame_number}"
#         frame_number = frame_number + 1



# frame_dict = rabbit2kgbsturct('predator/HSD_load distribution_2024-06-24_13_26.txt')

# print("test result")
# print(frame_dict['frame1'][0])
# print(frame_dict['frame1'][1])
# print(frame_dict['frame1'][2])
# print(frame_dict['frame1'][3])
# print(frame_dict['frame1'][4])
# print(frame_dict['frame1'][5])





