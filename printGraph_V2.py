import numpy as np
from matplotlib import pyplot as plt

simulation_obo = np.load('E:\Seminar\OBO_V2.npy')
simulation_ebo = np.load('E:\Seminar\EBO_V2.npy')
simulation_ebo_ctrl = np.load('E:\Seminar\EBO_CTRL_V2.npy') # ebo 비례제어기법 시뮬레이션 결과
simulation_ebo_obo = np.load('E:\Seminar\EBO_UORA_V2.npy')


def print_graph():
    x_list = []
    for i in range(1, 11):
        x_list.append(i) #x축 리스트 세팅

    plt.figure(figsize=(30,15))

    #PKS 속도
    plt.subplot(231)
    plt.plot(x_list, simulation_obo[0], color='red', marker='o', linestyle='-', label='OBO')
    plt.plot(x_list, simulation_ebo[0], color='blue', marker='o', linestyle='-', label='EBO')
    plt.plot(x_list, simulation_ebo_ctrl[0], color='green', marker='o', linestyle='-', label='EBO CTRL')
    plt.plot(x_list, simulation_ebo_obo[0], color='pink', marker='o', linestyle='-', label='EBO OBO')

    plt.title('Packet Throughput')
    plt.xlabel('Simulation')
    plt.ylabel('throughput')
    plt.legend(['OBO', 'EBO', 'EBO_CTRL', 'EBO_UORA'])

    #PKS 충돌율
    plt.subplot(232)
    plt.plot(x_list, simulation_obo[1], color='red', marker='o', linestyle='-', label='OBO')
    plt.plot(x_list, simulation_ebo[1], color='blue', marker='o', linestyle='-', label='EBO')
    plt.plot(x_list, simulation_ebo_ctrl[1], color='green', marker='o', linestyle='-', label='EBO CTRL')
    plt.plot(x_list, simulation_ebo_obo[1], color='pink', marker='o', linestyle='-', label='EBO OBO')

    plt.title('Packet Collision Rate')
    plt.xlabel('Simulation')
    plt.ylabel('collision rate')
    plt.legend(['OBO', 'EBO', 'EBO_CTRL', 'EBO_UORA'])


    #PKS 지연
    plt.subplot(233)
    plt.plot(x_list, simulation_obo[2], color='red', marker='o', linestyle='-', label='OBO')
    plt.plot(x_list, simulation_ebo[2], color='blue', marker='o', linestyle='-', label='EBO')
    plt.plot(x_list, simulation_ebo_ctrl[2], color='green', marker='o', linestyle='-', label='EBO CTRL')
    plt.plot(x_list, simulation_ebo_obo[2], color='pink', marker='o', linestyle='-', label='EBO OBO')

    plt.title('Packet delay')
    plt.xlabel('Simulation')
    plt.ylabel('delay')
    plt.legend(['OBO', 'EBO', 'EBO_CTRL', 'EBO_UORA'])


    #RU idle 비율
    plt.subplot(234)
    plt.plot(x_list, simulation_obo[3], color='red', marker='o', linestyle='-', label='OBO')
    plt.plot(x_list, simulation_ebo[3], color='blue', marker='o', linestyle='-', label='EBO')
    plt.plot(x_list, simulation_ebo_ctrl[3], color='green', marker='o', linestyle='-', label='EBO CTRL')
    plt.plot(x_list, simulation_ebo_obo[3], color='pink', marker='o', linestyle='-', label='EBO OBO')

    plt.title('RU idle rate')
    plt.xlabel('Simulation')
    plt.ylabel('idle rate')
    plt.legend(['OBO', 'EBO', 'EBO_CTRL', 'EBO_UORA'])


    #RU 성공률
    plt.subplot(235)
    plt.plot(x_list, simulation_obo[4], color='red', marker='o', linestyle='-', label='OBO')
    plt.plot(x_list, simulation_ebo[4], color='blue', marker='o', linestyle='-', label='EBO')
    plt.plot(x_list, simulation_ebo_ctrl[4], color='green', marker='o', linestyle='-', label='EBO CTRL')
    plt.plot(x_list, simulation_ebo_obo[4], color='pink', marker='o', linestyle='-', label='EBO OBO')

    plt.title('RU Success rate')
    plt.xlabel('Simulation')
    plt.ylabel('success rate')
    plt.legend(['OBO', 'EBO', 'EBO_CTRL', 'EBO_UORA'])


    #RU 충돌율
    plt.subplot(236)
    plt.plot(x_list, simulation_obo[5], color='red', marker='o', linestyle='-', label='OBO')
    plt.plot(x_list, simulation_ebo[5], color='blue', marker='o', linestyle='-', label='EBO')
    plt.plot(x_list, simulation_ebo_ctrl[5], color='green', marker='o', linestyle='-', label='EBO CTRL')
    plt.plot(x_list, simulation_ebo_obo[5], color='pink', marker='o', linestyle='-', label='EBO OBO')

    plt.title('RU collision rate')
    plt.xlabel('Simulation')
    plt.ylabel('collision rate')
    plt.legend(['OBO', 'EBO', 'EBO_CTRL', 'EBO_UORA'])



    plt.show()
    plt.close()

print_graph()