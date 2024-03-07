import numpy as np
from matplotlib import pyplot as plt

simulation_obo = np.load('E:\Seminar\Perform\OBO_V2_Perform.npy')
simulation_ebo = np.load('E:\Seminar\Perform\EBO_V2_Perform.npy')
simulation_ebo_obo = np.load('E:\Seminar\Perform\EBO_UORA_V2_Perform.npy')
simulation_ebo_ctrl = np.load('E:\Seminar\Perform\EBO_CTRL_V2_Perform.npy') # ebo 비례제어기법 시뮬레이션 결과

def print_graph():
    x_list = []
    for i in range(1, 101):
        x_list.append(i) #x축 리스트 세팅

    plt.figure(figsize=(20,10))

    #PKS 속도
    plt.subplot(241)
    plt.plot(x_list, simulation_obo[0], color='red')
    plt.plot(x_list, simulation_ebo[0], color='blue')
    plt.plot(x_list, simulation_ebo_obo[0], color='pink')
    plt.plot(x_list, simulation_ebo_ctrl[0], color='green')
    # plt.plot(x_list, simulation_ebo_ctrl[0], color='green')
    plt.title('Packet Throughput')
    plt.xlabel('DTI')
    plt.ylabel('throughput')
    plt.legend(['OBO', 'EBO', 'EBO_UORA','EBO_CTRL'])

    #PKS 충돌율
    plt.subplot(242)
    plt.plot(x_list, simulation_obo[1], color='red')
    plt.plot(x_list, simulation_ebo[1], color='blue')
    plt.plot(x_list, simulation_ebo_obo[1], color='pink')
    plt.plot(x_list, simulation_ebo_ctrl[1], color='green')
    plt.title('Packet Collision Rate')
    plt.xlabel('DTI')
    plt.ylabel('collision rate')
    plt.legend(['OBO', 'EBO', 'EBO_UORA','EBO_CTRL'])


    #PKS 지연
    plt.subplot(243)
    plt.plot(x_list, simulation_obo[2], color='red')
    plt.plot(x_list, simulation_ebo[2], color='blue')
    plt.plot(x_list, simulation_ebo_obo[2], color='pink')
    plt.plot(x_list, simulation_ebo_ctrl[2], color='green')
    plt.title('Packet delay')
    plt.xlabel('DTI')
    plt.ylabel('delay')
    plt.legend(['OBO', 'EBO', 'EBO_UORA','EBO_CTRL'])


    #RU idle 비율
    plt.subplot(244)
    plt.plot(x_list, simulation_obo[3], color='red')
    plt.plot(x_list, simulation_ebo[3], color='blue')
    plt.plot(x_list, simulation_ebo_obo[3], color='pink')
    plt.plot(x_list, simulation_ebo_ctrl[3], color='green')
    plt.title('RU idle rate')
    plt.xlabel('DTI')
    plt.ylabel('idle rate')
    plt.legend(['OBO', 'EBO', 'EBO_UORA','EBO_CTRL'])


    #RU 성공률
    plt.subplot(245)
    plt.plot(x_list, simulation_obo[4], color='red')
    plt.plot(x_list, simulation_ebo[4], color='blue')
    plt.plot(x_list, simulation_ebo_obo[4], color='pink')
    plt.plot(x_list, simulation_ebo_ctrl[4], color='green')
    plt.title('RU Success rate')
    plt.xlabel('DTI')
    plt.ylabel('success rate')
    plt.legend(['OBO', 'EBO', 'EBO_UORA','EBO_CTRL'])


    #RU 충돌율
    plt.subplot(246)
    plt.plot(x_list, simulation_obo[5], color='red')
    plt.plot(x_list, simulation_ebo[5], color='blue')
    plt.plot(x_list, simulation_ebo_obo[5], color='pink')
    plt.plot(x_list, simulation_ebo_ctrl[5], color='green')
    plt.title('RU collision rate')
    plt.xlabel('DTI')
    plt.ylabel('collision rate')
    plt.legend(['OBO', 'EBO', 'EBO_UORA','EBO_CTRL'])

    plt.subplot(247)
    plt.plot(x_list, simulation_obo[6], color='red')
    plt.plot(x_list, simulation_ebo[6], color='blue')
    plt.plot(x_list, simulation_ebo_obo[6], color='pink')
    plt.plot(x_list, simulation_ebo_ctrl[6], color='green')
    plt.title('Station')
    plt.xlabel('DTI')
    plt.ylabel('User')
    plt.legend(['OBO', 'EBO', 'EBO_UORA','EBO_CTRL'])


    plt.show()
    plt.close()

print_graph()