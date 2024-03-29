import numpy as np
from matplotlib import pyplot as plt

simulation_obo = np.load('E:\Seminar\OBO.npy')  # obo 시뮬레이션 결과
simulation_ebo = np.load('E:\Seminar\EBO.npy')  # ebo 시뮬레이션 결과
simulation_ebo_ctrl = np.load('E:\Seminar\EBO_CTRL.npy') # ebo 비례제어기법 시뮬레이션 결과
simulation_ebo_obo = np.load('E:\Seminar\EBO+UORA.npy') # EBO + UORA 기법 시뮬레이션 결과


def print_graph():
    x_list = []
    USER_MAX = 100
    for i in range(1, USER_MAX+1):
        x_list.append(i) #x축 리스트 세팅

    plt.figure(figsize=(20,10))

    #PKS 속도
    plt.subplot(231)
    plt.plot(x_list, simulation_obo[0], color='red')
    plt.plot(x_list, simulation_ebo[0], color='blue')
    plt.plot(x_list, simulation_ebo_obo[0], color='yellow')
    # plt.plot(x_list, simulation_ebo_ctrl[0], color='green')
    plt.title('Packet Throughput')
    plt.xlabel('Number or STA')
    plt.ylabel('throughput')
    plt.legend(['OBO', 'EBO', 'EBO_OBO'])
    # plt.legend(['OBO', 'EBO', 'EBO_CTRL'])

    #PKS 충돌율
    plt.subplot(232)
    plt.plot(x_list, simulation_obo[1], color='red')
    plt.plot(x_list, simulation_ebo[1], color='blue')
    plt.plot(x_list, simulation_ebo_obo[1], color='yellow')
    # plt.plot(x_list, simulation_ebo_ctrl[1], color='green')
    plt.title('Packet Collision Rate')
    plt.xlabel('Number or STA')
    plt.ylabel('collision rate')
    plt.legend(['OBO', 'EBO', 'EBO_OBO'])
    # plt.legend(['OBO', 'EBO', 'EBO_CTRL'])


    #PKS 지연
    plt.subplot(233)
    plt.plot(x_list, simulation_obo[2], color='red')
    plt.plot(x_list, simulation_ebo[2], color='blue')
    plt.plot(x_list, simulation_ebo_obo[2], color='yellow')
    # plt.plot(x_list, simulation_ebo_ctrl[2], color='green')
    plt.title('Packet delay')
    plt.xlabel('Number or STA')
    plt.ylabel('delay')
    plt.legend(['OBO', 'EBO', 'EBO_OBO'])
    # plt.legend(['OBO', 'EBO', 'EBO_CTRL'])


    #RU idle 비율
    plt.subplot(234)
    plt.plot(x_list, simulation_obo[3], color='red')
    plt.plot(x_list, simulation_ebo[3], color='blue')
    plt.plot(x_list, simulation_ebo_obo[3], color='yellow')
    # plt.plot(x_list, simulation_ebo_ctrl[3], color='green')
    plt.title('RU idle rate')
    plt.xlabel('Number or STA')
    plt.ylabel('idle rate')
    plt.legend(['OBO', 'EBO', 'EBO_OBO'])
    # plt.legend(['OBO', 'EBO', 'EBO_CTRL'])


    #RU 성공률
    plt.subplot(235)
    plt.plot(x_list, simulation_obo[4], color='red')
    plt.plot(x_list, simulation_ebo[4], color='blue')
    plt.plot(x_list, simulation_ebo_obo[4], color='yellow')
    # plt.plot(x_list, simulation_ebo_ctrl[4], color='green')
    plt.title('RU Success rate')
    plt.xlabel('Number or STA')
    plt.ylabel('success rate')
    plt.legend(['OBO', 'EBO', 'EBO_OBO'])
    # plt.legend(['OBO', 'EBO', 'EBO_CTRL'])


    #RU 충돌율
    plt.subplot(236)
    plt.plot(x_list, simulation_obo[5], color='red')
    plt.plot(x_list, simulation_ebo[5], color='blue')
    plt.plot(x_list, simulation_ebo_obo[5], color='yellow')
    # plt.plot(x_list, simulation_ebo_ctrl[5], color='green')
    plt.title('RU collision rate')
    plt.xlabel('Number or STA')
    plt.ylabel('collision rate')
    plt.legend(['OBO', 'EBO', 'EBO_OBO'])
    # plt.legend(['OBO', 'EBO', 'EBO_CTRL'])


    plt.show()
    plt.close()

print_graph()