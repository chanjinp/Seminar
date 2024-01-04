# 네트워크 세미나 시뮬레이션 환경 구성
# 기존 EBO의 경우 우선 순위 범위가 RA-RU의 수만큼 사용
import queue
import random
from turtle import color

import numpy as np
import matplotlib.pyplot as plt

NUM_SIM = 1  # 시뮬레이션 반복 수
NUM_DTI = 100000  # 1번 시뮬레이션에서 수행될 Data Transmission Interval 수

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
TWT_INTERVAL = DIFS + TF_SZ_us + SIFS * 2 + DTI + BA_SZ_us  # DIFS + 트리거 프레임 전송 시간 + SIFS + DTI + SIFS + Block Ack 전송 시간 => 전체 TWT 시간

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
PKS_dealy_results = []
# RU Result 관리 목록
RU_idle_results = []
RU_Success_results = []
RU_coll_results = []

# graph x
x_list = []


class Station:
    # Station에는 EBO의 우선순위를 알 수 있는 EBO 속성과 BusyTone을 수신했는지 여부를 확인하는 속성이 필요
    def __init__(self):
        self.ru = 0  # 할당된 RU
        self.cw = MIN_OCW  # 초기 OCW
        self.bo = random.randrange(0, self.cw)  # Backoff Counter
        self.ebo = -1  # 초기 EBO 값은 default로 -1로 설정
        self.busyTone = False  # 초기 Busytone의 경우
        self.tx_status = False  # True 전송 시도, False 전송 시도 X
        self.suc_status = False  # True 전송 성공, False 전송 실패 [충돌]
        self.delay = 0
        self.retry = 0
        self.data_size = 0  # 데이터 사이즈 (bytes)
    def __lt__(self, other):
        return self.ebo < other.ebo



def createSTA(USER):
    for i in range(0, USER):
        sta = Station()
        stationList.append(sta)


def allocationRA_RU():  # Random Ru 할당
    for sta in stationList:
        if (sta.bo <= 0):  # 백오프 타이머가 0보다 작아졌을 때
            # 백오프 타이머가 0보다 작아진 경우에만 ebo 우선 순위를 부여한다.
            sta.ru = random.randrange(0, NUM_RU)  # 랜덤으로 RU 할당
            sta.ebo = random.randrange(0, RU)  # 표준 EBO의 경우에는 0부터 RU의 수만큼의 범위에서 EBO 우선순위 부여
            sta.tx_status = True  # 전송 시도
        else:
            sta.bo -= NUM_RU  # 백오프타이머 감소 [RU의 수만큼 점차 감소]
            sta.tx_status = False  # 전송 시도 하지 않음.


def setSuccess(ru):
    for sta in stationList:
        if (sta.tx_status == True):  # 만약 전송 시도를 했다면
            if (sta.ru == ru and sta.busyTone == False):    # 전송을 시도했고 BusyTone 수신을 안했다면
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


def checkCollision():  # 충돌 검사
    coll_RU = []  # RU 충돌하는지 확인하기 위한 배열
    for i in range(0, NUM_RU):
        pq = queue.PriorityQueue()
        coll_RU.append(pq)
    for sta in stationList:
        if (sta.tx_status == True):  # 전송 시도 중인 STA만 확인
            coll_RU[int(sta.ru)].put((-sta.ebo, sta))  # 충돌이 일어난 RU에 겹친 것들이 쌓여간다.
    # RU 단위로 충돌 여부 확인
    for i in range(0, RU):  # STA이 할당 가능한 RU의 개수만큼 반복
        incRUTX()  # RU 전송 시도 수 증가
        if (coll_RU[i].qsize() == 1):  # 해당 부분의 배열 길이가 1개인 경우에는 RU의 충돌이 일어나지 않았음.
            setSuccess(i)
            incRUSuccess()
        elif (coll_RU[i].qsize() <= 0):  # 해당 인덱스의 값이 0보다 작은 경우 [= 0인 경우]에는 RU가 할당되지 않았음
            incRUIdle()
        else:  # 해당 RU 부분에는 충돌이 일어났음
            max_ebo, first_sta = coll_RU[i].get()  # 첫 번째 원소만 가지고 뺌 -> 반전 우선순위이기 때문에 제일 큰 값이 나옴
            max_ebo *= -1
            while not coll_RU[i].empty():
                ebo, sta = coll_RU[i].get()  # 우선순위 큐에서 ebo와 sta에 대해서 뽑아냄
                ebo *= -1
                if (max_ebo == ebo):  # 해당 경우인 경우에 RU가 겹쳤고 우선순위가 같은 것이 있기 때문에 RU 충돌이 일어남
                    setCollision(i)
                    incRUCollision()
                else:
                    setSuccess(i)
                    incRUSuccess()
                    sta.busyTone = True  # 아닌 경우에는 모든 겹치는 STA에 대해서 busyTone을 수신했다고 가정

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
                sta.ebo = -1    # EBO 초기화
                sta.tx_status = False  # True 전송 시도, False 전송 시도 않음
                sta.suc_status = False  # True 전송 성공, False 전송 실패(충돌)
                sta.delay = 0
                sta.retry = 0
                sta.data_sz = 0  # 데이터 사이즈 (bytes)
            else:  # 전송 실패 (충돌) #sta.suc_status == False
                sta.ru = 0  # 할당된 RU
                sta.retry += 1 # 재전송 시도 1 증가
                if (sta.retry >= RETRY_BS):  # 해당 패킷 폐기 및 변수 값 초기화
                    sta.cw = MIN_OCW  # 초기 OCW
                    sta.retry = 0
                    sta.delay = 0
                    sta.data_sz = 0  # 데이터 사이즈 (bytes)
                    sta.ebo = -1
                    sta.busyTone = False
                elif (sta.busyTone == True):    # BusyTone 신호를 받았다면
                    sta.cw = MIN_OCW    # 초기 OCW
                    sta.ebo = -1    # EBO 초기화
                    sta.busyTone = False    # BusyTone 수신 초기화
                else:
                    sta.cw *= 2
                    if (sta.cw > MAX_OCW):
                        sta.cw = MAX_OCW  # 최대 OCW
                sta.bo = random.randrange(0, sta.cw)  # backoffCounter
                sta.tx_status = False  # True 전송 시도, False 전송 시도 않음
                sta.suc_status = False  # True 전송 성공, False 전송 실패(충돌)


def print_Performance():
    PKS_coll_rate = (Stats_PKT_Collision / Stats_PKT_TX_Trial) * 100
    PKS_throughput = (Stats_PKT_Success * PACKET_SIZE * 8) / (NUM_SIM * NUM_DTI * TWT_INTERVAL)
    PKS_delay = (Stats_PKT_Delay / Stats_PKT_Success) * TWT_INTERVAL

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
    PKS_dealy_results.append(PKS_delay)

    RU_idle_results.append(RU_idle_rate)
    RU_Success_results.append(RU_Success_rate)
    RU_coll_results.append(RU_Collision_rate)


def print_graph():
    for i in range(1, USER_MAX + 1):
        x_list.append(i)  # x축 리스트 세팅

    plt.figure(figsize=(20, 10))

    # PKS 속도
    plt.subplot(231)
    plt.plot(x_list, PKS_throughput_results, color='blue', marker='o')
    plt.title('Packet Throughput')
    plt.xlabel('Number or STA')
    plt.ylabel('throughput')

    # PKS 충돌율
    plt.subplot(232)
    plt.plot(x_list, PKS_coll_results, color='red', marker='o')
    plt.title('Packet Collision Rate')
    plt.xlabel('Number or STA')
    plt.ylabel('collision rate')

    # PKS 지연
    plt.subplot(233)
    plt.plot(x_list, PKS_dealy_results, color='yellow', marker='o')
    plt.title('Packet delay')
    plt.xlabel('Number or STA')
    plt.ylabel('delay')

    # RU idle 비율
    plt.subplot(234)
    plt.plot(x_list, RU_idle_results, color='green', marker='o')
    plt.title('RU idle rate')
    plt.xlabel('Number or STA')
    plt.ylabel('idle rate')

    # RU 성공률
    plt.subplot(235)
    plt.plot(x_list, RU_Success_results, color='black', marker='o')
    plt.title('RU Success rate')
    plt.xlabel('Number or STA')
    plt.ylabel('success rate')

    # RU 충돌율
    plt.subplot(236)
    plt.plot(x_list, RU_coll_results, color='pink', marker='o')
    plt.title('RU collision rate')
    plt.xlabel('Number or STA')
    plt.ylabel('collision rate')

    plt.show()
    plt.close()


def resultClear():
    global Stats_PKT_TX_Trial
    global Stats_PKT_Success
    global Stats_PKT_Collision
    global Stats_PKT_Delay
    global Stats_RU_TX_Trial
    global Stats_RU_Idle
    global Stats_RU_Success
    global Stats_RU_Collision

    Stats_PKT_TX_Trial = 0
    Stats_PKT_Success = 0
    Stats_PKT_Collision = 0
    Stats_PKT_Delay = 0
    Stats_RU_TX_Trial = 0
    Stats_RU_Idle = 0
    Stats_RU_Success = 0
    Stats_RU_Collision = 0


def main():
    global USER_MAX
    global current_User
    USER_MAX = 100
    for i in range(1, USER_MAX + 1):
        print("======" + str(i) + "번" + "======")
        current_User = i
        resultClear()  # 결과들 초기화하는 함수
        for k in range(0, NUM_SIM):  # 시뮬레이션 횟수
            stationList.clear()  # stationlist 초기화
            createSTA(i)  # User의 수가 1일 때부터 100일 때까지 반복
            for j in range(0, NUM_DTI):
                incTrial()  # 모든 STA은 연결이 되었고 전송을 시도한다고 가정
                allocationRA_RU()  # Random한 RU를 할당
                checkCollision()  # 충돌 확인
                addStats()  # 충돌 확인 과정에서 알게된 상태와 전송 성공에 관련해서 상태 추가
                changeStaVariables()  # 결론적으로 전송을 성공했다면 상태 전부 초기화 과정 및 충돌을 했다면 cw의 값을 2배로 조정
        print_Performance()  # 시뮬레이션이 끝난 후의 성능 출력
    print_graph()  # 모든 시뮬레이션 결과를 그래프로 출력


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
#             incTrial()
#             allocationRA_RU()
#             checkCollision()
#             addStats()
#             changeStaVariables()
#
#     print_Performance()
#
# main()
