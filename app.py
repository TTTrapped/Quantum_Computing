import random
import cirq
import numpy as np
import streamlit as st

# 创建并模拟量子电路
def create_and_simulate_circuit(a, b):
    # 创建量子比特
    qubits = [cirq.LineQubit(i) for i in range(5)]
    circuit = cirq.Circuit()

    # 设置第0个量子比特为用户指定的态 a|0⟩ + b|1⟩
    # 使用Hadamard和相位门构造任意量子态 a|0⟩ + b|1⟩
    theta = 2 * np.arccos(np.abs(a))  # 从a计算角度theta
    phi = np.angle(b)  # 从b计算相位phi

    # 将量子比特设置为 |ψ⟩ = a|0⟩ + b|1⟩
    circuit.append(cirq.ry(theta)(qubits[0]))  # 将振幅调整为a
    circuit.append(cirq.rz(phi)(qubits[0]))   # 设置相位为b的相位

    # 编码阶段
    circuit.append([cirq.CNOT(qubits[0], qubits[1]), cirq.CNOT(qubits[0], qubits[2])])

    # 模拟错误
    p = np.random.random()
    error_type = "No Error"
    if p < 0.25:
        pass
    elif 0.25 <= p < 0.5:
        circuit.append(cirq.X(qubits[0]))
        error_type = "Bit-flip on qubit 0"
    elif 0.5 <= p < 0.75:
        circuit.append(cirq.X(qubits[1]))
        error_type = "Bit-flip on qubit 1"
    elif p >= 0.75:
        circuit.append(cirq.X(qubits[2]))
        error_type = "Bit-flip on qubit 2"

    # 错误检测阶段
    circuit.append([cirq.CNOT(qubits[0], qubits[3]), cirq.CNOT(qubits[1], qubits[3])])
    circuit.append([cirq.CNOT(qubits[0], qubits[4]), cirq.CNOT(qubits[2], qubits[4])])

    # 测量阶段
    circuit.append([cirq.measure(qubits[3], key='m1')])
    circuit.append([cirq.measure(qubits[4], key='m2')])

    # 执行量子电路
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1)

    # 获取测量结果
    m1 = result.measurements['m1'][0][0]
    m2 = result.measurements['m2'][0][0]

    return circuit.to_text_diagram(), error_type, {"m1": m1, "m2": m2}

# Streamlit UI
def main():
    st.title("Quantum Error Detection Simulator")

    st.sidebar.header("Input Parameters")
    a = st.sidebar.number_input("Enter a (amplitude of |0⟩)", min_value=-1.0, max_value=1.0, value=0.6, step=0.01)
    b = st.sidebar.number_input("Enter b (amplitude of |1⟩)", min_value=-1.0, max_value=1.0, value=0.8, step=0.01)

    if st.sidebar.button("Simulate"):
        # 创建并运行量子电路
        circuit_diagram, error_type, measurements = create_and_simulate_circuit(a, b)

        st.subheader("Quantum Circuit")
        st.text(circuit_diagram)

        st.subheader("Error Type")
        st.write(error_type)

        st.subheader("Measurement Results")
        st.write(f"m1: {measurements['m1']}, m2: {measurements['m2']}")

if __name__ == "__main__":
    main()
