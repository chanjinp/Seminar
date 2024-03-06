import numpy as np
from matplotlib import pyplot as plt

simulation_ebo_ctrl = np.load('E:\Seminar\EBO_CTRLV2.npy') # ebo 비례제어기법 시뮬레이션 결과


def print_graph():
    x_list = []
    for i in range(1, 101):
        x_list.append(i) #x축 리스트 세팅

    plt.figure(figsize=(20,10))

    #PKS 속도
    plt.subplot(241)
    plt.plot(x_list, simulation_ebo_ctrl[0], color='green')
    # plt.plot(x_list, simulation_ebo_ctrl[0], color='green')
    plt.title('Packet Throughput')
    plt.xlabel('DTI')
    plt.ylabel('throughput')
    plt.legend(['EBO_CTRL'])
    # plt.legend(['OBO', 'EBO', 'EBO_OBO'])
    # plt.legend(['OBO', 'EBO', 'EBO_CTRL'])

    #PKS 충돌율
    plt.subplot(242)
    plt.plot(x_list, simulation_ebo_ctrl[1], color='green')
    # plt.plot(x_list, simulation_ebo_ctrl[1], color='green')
    plt.title('Packet Collision Rate')
    plt.xlabel('DTI')
    plt.ylabel('collision rate')
    plt.legend(['EBO_CTRL'])
    # plt.legend(['OBO', 'EBO', 'EBO_OBO'])
    # plt.legend(['OBO', 'EBO', 'EBO_CTRL'])


    #PKS 지연
    plt.subplot(243)
    plt.plot(x_list, simulation_ebo_ctrl[2], color='green')
    # plt.plot(x_list, simulation_ebo_ctrl[2], color='green')
    plt.title('Packet delay')
    plt.xlabel('DTI')
    plt.ylabel('delay')
    plt.legend(['EBO_CTRL'])
    # plt.legend(['OBO', 'EBO', 'EBO_OBO'])
    # plt.legend(['OBO', 'EBO', 'EBO_CTRL'])


    #RU idle 비율
    plt.subplot(244)
    plt.plot(x_list, simulation_ebo_ctrl[3], color='green')
    plt.title('RU idle rate')
    plt.xlabel('DTI')
    plt.ylabel('idle rate')
    plt.legend(['EBO_CTRL'])
    # plt.legend(['OBO', 'EBO', 'EBO_OBO'])
    # plt.legend(['OBO', 'EBO', 'EBO_CTRL'])


    #RU 성공률
    plt.subplot(245)
    plt.plot(x_list, simulation_ebo_ctrl[4], color='green')
    plt.title('RU Success rate')
    plt.xlabel('DTI')
    plt.ylabel('success rate')
    plt.legend(['EBO_CTRL'])
    # plt.legend(['OBO', 'EBO', 'EBO_OBO'])
    # plt.legend(['OBO', 'EBO', 'EBO_CTRL'])


    #RU 충돌율
    plt.subplot(246)
    plt.plot(x_list, simulation_ebo_ctrl[5], color='green')
    plt.title('RU collision rate')
    plt.xlabel('DTI')
    plt.ylabel('collision rate')
    plt.legend(['EBO_CTRL'])
    # plt.legend(['OBO', 'EBO', 'EBO_OBO'])
    # plt.legend(['OBO', 'EBO', 'EBO_CTRL'])

    plt.subplot(247)
    plt.plot(x_list, simulation_ebo_ctrl[6], color='green')
    plt.title('Station')
    plt.xlabel('DTI')
    plt.ylabel('User')
    plt.legend(['EBO_CTRL'])
    # plt.legend(['OBO', 'EBO', 'EBO_OBO'])
    # plt.legend(['OBO', 'EBO', 'EBO_CTRL'])


    plt.show()
    plt.close()

print_graph()