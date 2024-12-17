import streamlit as st
import cirq
import numpy as np


# 构造 OFT 的函数
def qft(num_qubits):
    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit()

    for i in range(num_qubits):
        circuit.append(cirq.H(qubits[i]))
        for j in range(i + 1, num_qubits):
            theta =np.pi/(2 ** (j - i))
            circuit.append(cirq.CZ(qubits[j], qubits[i]) ** (theta / np.pi))
            for i in range(num_qubits // 2):
                circuit.append(cirq.SWAP(qubits[i], qubits[num_qubits - i - 1]))
    return circuit, qubits


# Streamlit 界面
st.title("量子傅里叶变换(QFT)模拟器")


# 输入量子比特数
num_qubits = st.number_input("输入量子比特数量:", min_value=2, max_value=10, value=3)


# 输入自定义初态
st.subheader("设置初始态")
default_state = [1] + [0] * (2**num_qubits - 1) # 默认 |0...0>
custom_state_input = st.text_input(
    f"输入 {2**num_qubits} 个复数值(用逗号分隔):",
    value = ",".join(map(str, default_state))
)


#解析用户输入的初态
try:
    custom_state = np.array([complex(x) for x in custom_state_input.split(",")], dtype=complex)
    if len(custom_state)!= 2**num_qubits:
        st.error(f"输入的初态长度必须为{2**num_qubits}。")
        st.stop()
    if not np.isclose(np.sum(np.abs(custom_state)**2),1):
        st.error("输入的初态向量必须归一化(总概率为 1)。")
        st.stop()
except Exception as e:
    st.error(f"初态输入无效:{e}")
    st.stop()

    
# 显示 QFT 电路
st.subheader(f"{num_qubits} 量子比特的 QFT 电路")
circuit, qubits = qft(num_qubits)
st.text(circuit)


# 模拟 OFT 电路
simulator = cirq.Simulator()
result = simulator.simulate(circuit, initial_state=custom_state)
#显示最终的状态向量
st.subheader("最终状态向量")
final_state = np.around(result.final_state_vector, decimals=3)
st.write(final_state)