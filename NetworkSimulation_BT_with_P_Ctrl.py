# 네트워크 세미나 시뮬레이션 환경 구성
# 기존 EBO의 경우 우선 순위 범위가 RA-RU의 수만큼 사용
import random
from turtle import color

import numpy as np
import matplotlib.pyplot as plt


NUM_SIM = 1  # 시뮬레이션 반복 수
NUM_DTI = 10000  # 1번 시뮬레이션에서 수행될 Data Transmission Interval 수
simulation_list = []    # 총 모든 시뮬레이션 결과 리스트

# AP set
SIFS = 16
DIFS = 32
NUM_RU = 8  # AP에 정해져있는 RU의 수
PACKET_SIZE = 1000
TF_SIZE = 89
DATA_RATE = 1
BA_SIZE = 32
DTI = 32  # Data Transmission Interval 시간, 단위: us => 의미하는 바는 STA이 보내는 데이터의 길이가 각 STA마다 다르지만 정해진 시간만큼은 일정하기 때문에 DTI로 고정

# 기본 설정 파라미터 값
RU = 8  # STA에게 할당가능한 RU의 수
MIN_OCW = 8  # 최소 백오프 카운터
MAX_OCW = 64  # 최대 백오프 카운터
RETRY_BS = 10  # 백오프 스테이지 최댓값 = 충돌 실패 후 백오프타이머를 계속 시도할 때의 최대 횟수

# Transmission time in us
PKT_SZ_us = (PACKET_SIZE * 8) / (DATA_RATE * 1000)  # 데이터 패킷 전송 시간, 단위: us
TF_SZ_us = (TF_SIZE * 8) / (DATA_RATE * 1000)  # 트리거 프레임 전송 시간, 단위: us
BA_SZ_us = (BA_SIZE * 8) / (DATA_RATE * 1000)  # 블록 ACK 전송 시간, 단위: us

# BusyTone
BT_us = 9 # us
NUM_BT = NUM_RU # 각 STA은 해당 변수에 맞춰 BT 경쟁을 수행함
# NUM_BT == 1 --> BT 사용 X
# NUM_BT > 1  --> BT 사용 O
NUM_BT_ACC = 0 # throughput 계산 시 BT overhead 계산을 위해 사용되는 변수

OPTIMAL_COL_RATE = 0.6 # 패킷 단위 성능

TWT_INTERVAL = (DIFS + TF_SZ_us + SIFS * 2 + DTI + BA_SZ_us)  # DIFS + 트리거 프레임 전송 시간 + SIFS + DTI + SIFS + Block Ack 전송 시간 => 전체 TWT 시간

# 성능 변수
# 패킷 단위 성능
Stats_PKT_TX_Trial = 0  # 전송 시도 수
Stats_PKT_Success = 0  # 전송 성공 수
Stats_PKT_Collision = 0  # 충돌 발생 수
Stats_PKT_Delay = 0  # 패킷 당 전송 시도 DTI 수

# RU 단위 성능
Stats_RU_TX_Trial = 0  # 전송 시도 수
Stats_RU_Idle = 0  # 빈 RU 수
Stats_RU_Success = 0  # 전송 성공 RU 수
Stats_RU_Collision = 0  # 충돌 발생 RU 수

# station 관리 목록
stationList = []

# PKS Result 관리 목록
PKS_throughput_results = []
PKS_coll_results = []
PKS_delay_results = []
# RU Result 관리 목록
RU_idle_results = []
RU_Success_results = []
RU_coll_results = []

# graph x
x_list = []

class Station:
    def __init__(self):
        self.ru = 0  # 할당된 RU
        self.cw = MIN_OCW  # 초기 OCW
        self.bo = random.randrange(0, self.cw)  # Backoff Counter
        self.tx_status = False  # True 전송 시도, False 전송 시도 X
        self.suc_status = False  # True 전송 성공, False 전송 실패 [충돌]
        self.delay = 0
        self.retry = 0
        self.data_size = 0  # 데이터 사이즈 (bytes)
        self.bt_priority = 0 # 비지톤 우선순위


def createSTA(USER):
    for i in range(0, USER):
        sta = Station()
        stationList.append(sta)

def adjust_NUM_BT():
    # NUM_BT 비례제어
    # NUM_BT 최소값은 1

    global NUM_BT
    global NUM_BT_ACC

    ERR_MARGIN = 0.03 # threshold
    K = 8 # Gain

    # 1. calculate collision rate (패킷 단위 성능)

    col_rate = 0

    if(Stats_PKT_TX_Trial != 0): # 전송 시도의 수가 0이 아니라면
        col_rate = round((Stats_PKT_Collision / Stats_PKT_TX_Trial), 2)

    # 2. 비례제어
    error = round(col_rate - OPTIMAL_COL_RATE, 2)

    if (error < -ERR_MARGIN) or (ERR_MARGIN < error): # threshold value 절댓값

        NUM_BT = int(NUM_BT * (1 + K * error))

    # 3. 최대, 최소값 필터링

    if (NUM_BT < 1):
        NUM_BT = 1
    if (NUM_BT > 10):
        NUM_BT = 10

    if(NUM_BT > 1):
        NUM_BT_ACC += NUM_BT

def allocationRA_RU():
    for sta in stationList:
        if (sta.bo <= 0):  # 백오프 타이머가 0보다 작아졌을 때
            sta.tx_status = True  # 전송 시도
            sta.ru = random.randrange(0, NUM_RU)  # 랜덤으로 RU 할당
            sta.bt_priority = random.randrange(0, NUM_BT) # 비지톤 우선순위 할당
        else:
            sta.bo -= NUM_RU  # 백오프타이머 감소 [RU의 수만큼 점차 감소]
            sta.tx_status = False  # 전송 시도 하지 않음.


def checkCollision():
    coll_RU = []
    for i in range(0, NUM_RU):
        coll_RU.append(0)
    for sta in stationList:
        if (sta.tx_status == True):  # 전송 시도 중인 STA만 확인
            coll_RU[int(sta.ru)] += 1  # 선택된 RU의 인덱스 부분에 +1씩 증가 => 만약 2 이상의 값이 있다면 해당 RU는 2개 이상의 STA이 존재 => 충돌
    # RU 단위로 충돌 여부 확인
    for i in range(0, RU):  # STA이 할당 가능한 RU의 개수만큼 반복
        incRUTX()  # RU 전송 시도 수 증가
        if (coll_RU[i] == 1):  # 해당 인덱스의 값이 1인 경우에는 하나의 STA만 할당되었다.
            setSuccess(i)
            incRUSuccess()
        elif (coll_RU[i] <= 0):  # 해당 인덱스의 값이 0보다 작은 경우 [= 0인 경우]에는 RU가 할당되지 않았음
            incRUIdle()
        else:
            setCollision(i)
            incRUCollision()  # 위의 경우에 제외된 경우에는 충돌이 일어났음

def checkBusyTone():

    if NUM_BT == 1:
        return

    # 우선순위가 작을수록 높은 것이다
    min_priority_list = []
    for i in range(0, NUM_RU):
        min_priority_list.append(NUM_BT - 1)

    # 각 RU에서 경쟁에서 승리할 수 있는 OBO 값 파악
    for sta in stationList:
        if (sta.tx_status == True):
            if(sta.bt_priority < min_priority_list[int(sta.ru)]):
                min_priority_list[int(sta.ru)] = sta.bt_priority

    # MIN OBO에 해당하는 STA만 전송을 시도하고, 나머지는 전송 포기
    # 전송을 포기한 STA는 동일한 OCW 범위 내에서 랜덤하게 OBO를 초기화
    for sta in stationList:
        if (sta.tx_status == True):
            if(sta.bt_priority > min_priority_list[int(sta.ru)]):

                sta.retry += 1
                if (sta.retry >= RETRY_BS):  # 해당 패킷 폐기 및 변수 값 초기화
                    sta.cw = MIN_OCW  # 초기 OCW
                    sta.retry = 0
                    sta.delay = 0

                # 전송 포기
                sta.tx_status = False
                sta.suc_status = False

                # OBO 초기화
                sta.bo = random.randrange(0, sta.cw)


def setSuccess(ru):
    for sta in stationList:
        if (sta.tx_status == True):  # 만약 전송 시도를 했다면
            if (sta.ru == ru):
                sta.suc_status = True  # 전송 성공


def setCollision(ru):
    for sta in stationList:
        if (sta.tx_status == True):  # 만약 전송 시도를 했다면
            if (sta.ru == ru):
                sta.suc_status = False  # 전송 실패 [충돌]


def incRUTX():
    global Stats_RU_TX_Trial  # 전송 시도 수
    Stats_RU_TX_Trial += 1


def incRUCollision():
    global Stats_RU_Collision  # 충돌 발생 RU 수
    Stats_RU_Collision += 1


def incRUSuccess():
    global Stats_RU_Success  # 전송 성공 RU 수
    Stats_RU_Success += 1


def incRUIdle():
    global Stats_RU_Idle  # 빈 RU 수
    Stats_RU_Idle += 1


def addStats():
    global Stats_PKT_TX_Trial  # 전송 시도 수
    global Stats_PKT_Success  # 전송 성공 수
    global Stats_PKT_Collision  # 충돌 발생 수
    global Stats_PKT_Delay  # 패킷 당 전송 시도 DTI 수

    for sta in stationList:
        if (sta.tx_status == True):  # 전송 시도
            Stats_PKT_TX_Trial += 1  # 전송 시도 수
            if (sta.suc_status == True):  # 전송 성공
                Stats_PKT_Success += 1  # 전송 성공 수
                Stats_PKT_Delay += sta.delay  # 패킷 당 전송 시도 DTI 수
            else:  # 전송 실패 (충돌)
                Stats_PKT_Collision += 1  # 충돌 발생 수


def incTrial():
    for sta in stationList:
        sta.delay += 1  # 전송 시도 수 1 증가


def changeStaVariables():
    for sta in stationList:
        if (sta.tx_status == True):  # 전송 시도
            if (sta.suc_status == True):  # 전송 성공
                sta.ru = 0  # 할당된 RU 초기화
                sta.cw = MIN_OCW  # 초기 OCW -> 기존 OCW의 범위에서 재설정
                sta.bo = random.randrange(0, sta.cw)  # backoffCounter
                sta.tx_status = False  # True 전송 시도, False 전송 시도 않음
                sta.suc_status = False  # True 전송 성공, False 전송 실패(충돌)
                sta.delay = 0
                sta.retry = 0
                sta.data_sz = 0  # 데이터 사이즈 (bytes)
            else:  # 전송 실패 (충돌)
                sta.ru = 0  # 할당된 RU
                sta.retry += 1
                if (sta.retry >= RETRY_BS):  # 해당 패킷 폐기 및 변수 값 초기화
                    sta.cw = MIN_OCW  # 초기 OCW
                    sta.retry = 0
                    sta.delay = 0
                    sta.data_sz = 0  # 데이터 사이즈 (bytes)
                else:
                    sta.cw *= 2
                    if (sta.cw > MAX_OCW):
                        sta.cw = MAX_OCW  # 최대 OCW
                sta.bo = random.randrange(0, sta.cw)  # backoffCounter
                sta.tx_status = False  # True 전송 시도, False 전송 시도 않음
                sta.suc_status = False  # True 전송 성공, False 전송 실패(충돌)


def print_Performance():
    PKS_coll_rate = (Stats_PKT_Collision / Stats_PKT_TX_Trial) * 100
    PKS_throughput = (Stats_PKT_Success * PACKET_SIZE * 8) / ((NUM_BT_ACC * BT_us) + (NUM_SIM * NUM_DTI * TWT_INTERVAL)) # BusyTone overhead 합산
    PKS_delay = (Stats_PKT_Delay / Stats_PKT_Success) * TWT_INTERVAL

    print("[BusyTone 사용 개수]")
    print("NUM_BT_ACC: ", NUM_BT_ACC)

    print("[패킷 단위 성능]")
    print("전송 시도 수 : ", Stats_PKT_TX_Trial)
    print("전송 성공 수 : ", Stats_PKT_Success)

    print("전송 실패 수 : ", Stats_PKT_Collision)
    print("충돌율 : ", PKS_coll_rate)
    print("지연 : ", Stats_PKT_Delay / Stats_PKT_Success)
    print(">> 통신 속도 : ", PKS_throughput)  # 단위: Mbps
    print(">> 지연 : ", PKS_delay)  # 단위: us

    # print(TWT_INTERVAL)
    print("[RU 단위 성능]")
    RU_idle_rate = (Stats_RU_Idle / Stats_RU_TX_Trial) * 100
    RU_Success_rate = (Stats_RU_Success / Stats_RU_TX_Trial) * 100
    RU_Collision_rate = (Stats_RU_Collision / Stats_RU_TX_Trial) * 100
    print("전송 시도 수 : ", Stats_RU_TX_Trial)
    print("전송 성공 수 : ", Stats_RU_Success)
    print("전송 실패 수 : ", Stats_RU_Collision)
    print("Idle 수 : ", Stats_RU_Idle)
    print("Idle 비율 : ", RU_idle_rate)
    print("성공율 : ", RU_Success_rate)
    print(">> 충돌율 : ", RU_Collision_rate)

    PKS_coll_results.append(PKS_coll_rate)
    PKS_throughput_results.append(PKS_throughput)
    PKS_delay_results.append(PKS_delay)

    RU_idle_results.append(RU_idle_rate)
    RU_Success_results.append(RU_Success_rate)
    RU_coll_results.append(RU_Collision_rate)


def print_graph():
    for i in range(1, USER_MAX+1):
        x_list.append(i) #x축 리스트 세팅

    plt.figure(figsize=(20,10))

    #PKS 속도
    plt.subplot(231)
    plt.plot(x_list, PKS_throughput_results, color='blue', marker='o')
    plt.title('Packet Throughput')
    plt.xlabel('Number or STA')
    plt.ylabel('throughput')

    #PKS 충돌율
    plt.subplot(232)
    plt.plot(x_list, PKS_coll_results, color='red', marker='o')
    plt.title('Packet Collision Rate')
    plt.xlabel('Number or STA')
    plt.ylabel('collision rate')


    #PKS 지연
    plt.subplot(233)
    plt.plot(x_list, PKS_delay_results, color='yellow', marker='o')
    plt.title('Packet delay')
    plt.xlabel('Number or STA')
    plt.ylabel('delay')


    #RU idle 비율
    plt.subplot(234)
    plt.plot(x_list, RU_idle_results, color='green', marker='o')
    plt.title('RU idle rate')
    plt.xlabel('Number or STA')
    plt.ylabel('idle rate')


    #RU 성공률
    plt.subplot(235)
    plt.plot(x_list, RU_Success_results, color='black', marker='o')
    plt.title('RU Success rate')
    plt.xlabel('Number or STA')
    plt.ylabel('success rate')


    #RU 충돌율
    plt.subplot(236)
    plt.plot(x_list, RU_coll_results, color='pink', marker='o')
    plt.title('RU collision rate')
    plt.xlabel('Number or STA')
    plt.ylabel('collision rate')


    plt.show()
    plt.close()

def save():
    global simulation_list

    simulation_list.append(PKS_throughput_results)
    simulation_list.append(PKS_coll_results)
    simulation_list.append(PKS_delay_results)
    simulation_list.append(RU_idle_results)
    simulation_list.append(RU_Success_results)
    simulation_list.append(RU_coll_results)

    np.save('E:\Seminar\EBO_CTRL',simulation_list)
    # np.save('E:\Pycharm\Seminar\EBO_CTRL', simulation_list)
def resultClear():

    global Stats_PKT_TX_Trial
    global Stats_PKT_Success
    global Stats_PKT_Collision
    global Stats_PKT_Delay
    global Stats_RU_TX_Trial
    global Stats_RU_Idle
    global Stats_RU_Success
    global Stats_RU_Collision
    global NUM_BT_ACC
    global NUM_BT

    Stats_PKT_TX_Trial = 0
    Stats_PKT_Success = 0
    Stats_PKT_Collision = 0
    Stats_PKT_Delay = 0
    Stats_RU_TX_Trial = 0
    Stats_RU_Idle = 0
    Stats_RU_Success = 0
    Stats_RU_Collision = 0
    NUM_BT_ACC = 0
    NUM_BT = 0


def main():
    global USER_MAX
    global current_User
    USER_MAX = 100
    for i in range(1, USER_MAX+1):
        print("======" + str(i) + "번" + "======")
        current_User = i
        resultClear()  # 결과들 초기화하는 함수
        for k in range(0, NUM_SIM):  # 시뮬레이션 횟수
            stationList.clear()  # stationlist 초기화
            createSTA(i)  # User의 수가 1일 때부터 100일 때까지 반복
            for j in range(0, NUM_DTI):
                incTrial()
                adjust_NUM_BT() # BT 페이즈 수 조절 (비례제어)
                allocationRA_RU()
                checkBusyTone() # 비지톤 phase 추가
                checkCollision()
                addStats()
                changeStaVariables()
        print_Performance()
    # print_graph()
    save()
main()

# def main():
#     global current_User
#     current_User = 5
#     for i in range(0, NUM_SIM):
#         # 시뮬레이션 반복할 때마다 모든 노드 삭제 후 재 생성
#         stationList.clear()  # 모든 노드 삭제
#         createSTA(current_User)  # 노드 생성
#
#         for j in range(0, NUM_DTI):
#             # k = 0
#             # for sta in stationList:
#             #    print("ID: ", k, "BO: ", sta.bo)
#             #    k += 1
#
#             incTrial()
#             allocationRA_RU()
#             checkCollision()
#             addStats()
#             changeStaVariables()
#
#     print_Performance()
#
# main()
