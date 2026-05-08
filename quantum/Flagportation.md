# Flagportation

## Understanding the code components
Lets first see what are the imported methods from qutip does.
- basis: generates a Fock state ket vector, so the encoder function present in the code represent the following:\
    basis(2, 0): $|0\rangle$,    basis(2, 1): $|1\rangle$\
    basis(2, 0) + basis(2, 1): $|+\rangle$\
    basis(2, 0) - basis(2, 1): $|-\rangle$

- tensor: this is for genrating tensor product between the qubits, here it represents:
    $|q0\rangle \otimes |q1\rangle \otimes |q2\rangle$

- The flaw is that the encoding basis (Z or X) is printed before the user applies corrections or measures. This tells us the attacker exactly which basis the flag bit was encoded in.

- After examining the code and going through the math we can see that we can come to a conclusion which sort of correction to apply when we have a certain value pairs for m0 and m1.

- Two main sections of code that we need to analyze are the encoder part and the prepare method.
    - Encoder part mentions which the states for m0 and m1, with which what is the starting point and the basis that was taken.
    - Prepare describes the whole process that we go through so as to get the `state` and `_basis` at end.

- Analyzing the prepate method
```python
def prepare(self, bits: str):
        q0, _basis = self.encoder[bits] # taking the q0 and basis from the encoder
        q1 = basis(2, 0) # ket 0
        q2 = basis(2, 0) # ket 0
        
        state = tensor(q0, q1, q2) # mentioned above

        state = self.proc.H(3, 1) * state # apply Hadamard gate on qubit 1
        state = self.proc.CNOT(3, 1, 2) * state # apply Controlled Not gate where qubit1 is the control bit and qubit2 is the acting one

        state = self.proc.CNOT(3, 0, 1) * state # apply Controlled Not gate where qubit0 is the control bit and qubit1 is the acting one
        state = self.proc.H(3, 0) * state # Apply hadamard gate on qubit 0

        return state, _basis
```

## Peforming Prepare operation on all the cases

Initial state: $|q0\rangle \otimes |0\rangle \otimes |0\rangle$

Where $|q0\rangle$ is one of: $|0\rangle, |1\rangle, |+\rangle, |-\rangle$

---

### Case 1: $q0 = |0\rangle$

**Step 1:** Apply $H(q1)$:
$$|0\rangle \otimes \frac{|0\rangle + |1\rangle}{\sqrt{2}} \otimes |0\rangle = \frac{1}{\sqrt{2}}(|0,0,0\rangle + |0,1,0\rangle)$$

**Step 2:** Apply $CNOT(q1 \to q2)$ (flip q2 if q1 is 1):
$$\frac{1}{\sqrt{2}}(|0,0,0\rangle + |0,1,1\rangle)$$

**Step 3:** Apply $CNOT(q0 \to q1)$ (flip q1 if q0 is 1). Since q0=0, nothing changes:
$$\frac{1}{\sqrt{2}}(|0,0,0\rangle + |0,1,1\rangle)$$

**Step 4:** Apply $H(q0)$:
$$H|0\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}}$$

$$\Rightarrow \frac{1}{2}(|0,0,0\rangle + |1,0,0\rangle + |0,1,1\rangle + |1,1,1\rangle)$$

**Measurements of q0, q1:**
- $(m0, m1) = (0,0)$ → collapses to $|0,0,0\rangle$ → **q2 = |0⟩** (original)
- $(m0, m1) = (1,0)$ → collapses to $|1,0,0\rangle$ → **q2 = |0⟩** (original)
- $(m0, m1) = (0,1)$ → collapses to $|0,1,1\rangle$ → **q2 = |1⟩** (bit-flipped)
- $(m0, m1) = (1,1)$ → collapses to $|1,1,1\rangle$ → **q2 = |1⟩** (bit-flipped)

---

### Case 2: $q0 = |1\rangle$

**Step 1:** After $H(q1)$:
$$\frac{1}{\sqrt{2}}(|1,0,0\rangle + |1,1,0\rangle)$$

**Step 2:** After $CNOT(q1 \to q2)$:
$$\frac{1}{\sqrt{2}}(|1,0,0\rangle + |1,1,1\rangle)$$

**Step 3:** After $CNOT(q0 \to q1)$ (q0=1, so q1 flips):
$$\frac{1}{\sqrt{2}}(|1,1,0\rangle + |1,0,1\rangle)$$

**Step 4:** After $H(q0)$ where $H|1\rangle = \frac{|0\rangle - |1\rangle}{\sqrt{2}}$:
$$\frac{1}{2}(|0,1,0\rangle - |1,1,0\rangle + |0,0,1\rangle - |1,0,1\rangle)$$

**Measurements of q0, q1:**
- $(m0, m1) = (0,0)$ → collapses to $|0,0,1\rangle$ →  **q2 = |1⟩** (original)
- $(m0, m1) = (1,0)$ → collapses to $|1,0,1\rangle$ →  **q2 = |1⟩** (original)
- $(m0, m1) = (0,1)$ → collapses to $|0,1,0\rangle$ →  **q2 = |0⟩** (bit-flipped, need $X$)
- $(m0, m1) = (1,1)$ → collapses to $|1,1,0\rangle$ → **q2 = |0⟩** (bit-flipped, need $X$)

---

### Case 3: $q0 = |+\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}}$

**Step 1:** After $H(q1)$:
$$\frac{1}{\sqrt{2}}(|0,0,0\rangle + |0,1,0\rangle + |1,0,0\rangle +|1,1,0\rangle)$$

**Step 2:** After $CNOT(q1 \to q2)$:
$$\frac{1}{\sqrt{2}}(|0,0,0\rangle + |0,1,1\rangle + |1,0,0\rangle +|1,1,1\rangle)$$

**Step 3:** After $CNOT(q0 \to q1)$ (q0=1, so q1 flips):
$$\frac{1}{\sqrt{2}}(|0,0,0\rangle + |0,1,1\rangle + |1,1,0\rangle +|1,0,1\rangle)$$

**Step 4:** After $H(q0)$ where $H|1\rangle = \frac{|0\rangle - |1\rangle}{\sqrt{2}}$:
$$\frac{1}{2\sqrt{2}}(|0,0,0\rangle + |1,0,0\rangle + |0,1,1\rangle + |1,1,1\rangle + |0,1,0\rangle - |1,1,0\rangle + |0,0,1\rangle - |1,0,1\rangle)$$

**Measurements of q0, q1:**
- $(m0, m1) = (0,0)$ → **q2** in state $|0\rangle + |1\rangle = |+\rangle$ (original)
- $(m0, m1) = (1,0)$ → **q2** in state $|0\rangle - |1\rangle = |-\rangle$ (phase-flipped, need $Z$)
- $(m0, m1) = (0,1)$ → **q2** in state $|1\rangle + |0\rangle = |+\rangle$ (original, applying X will not have any affect)
- $(m0, m1) = (1,1)$ → **q2** in state $|1\rangle - |0\rangle = -|-\rangle$ (both flips, need $X;Z$)

---

### Case 4: $q0 = |-\rangle = \frac{|0\rangle - |1\rangle}{\sqrt{2}}$

**Step 1:** After $H(q1)$:
$$\frac{1}{\sqrt{2}}(|0,0,0\rangle + |0,1,0\rangle - |1,0,0\rangle - |1,1,0\rangle)$$

**Step 2:** After $CNOT(q1 \to q2)$:
$$\frac{1}{\sqrt{2}}(|0,0,0\rangle + |0,1,1\rangle - |1,0,0\rangle -|1,1,1\rangle)$$

**Step 3:** After $CNOT(q0 \to q1)$ (q0=1, so q1 flips):
$$\frac{1}{\sqrt{2}}(|0,0,0\rangle + |0,1,1\rangle - |1,1,0\rangle -|1,0,1\rangle)$$

**Step 4:** After $H(q0)$ where $H|1\rangle = \frac{|0\rangle - |1\rangle}{\sqrt{2}}$:
$$\frac{1}{2\sqrt{2}}(|0,0,0\rangle + |1,0,0\rangle + |0,1,1\rangle + |1,1,1\rangle - |0,1,0\rangle + |1,1,0\rangle - |0,0,1\rangle + |1,0,1\rangle)$$

**Measurements of q0, q1:**
- $(m0, m1) = (0,0)$ → **q2** in state $|-\rangle$ (original)
- $(m0, m1) = (1,0)$ → **q2** in state $|+\rangle$ (applying Z should resolve)
- $(m0, m1) = (0,1)$ → **q2** in state $|1\rangle - |0\rangle = -|-\rangle$ (bit flipped Need X)
- $(m0, m1) = (1,1)$ → **q2** in state $|+\rangle$ (Applying X and Z will have the original, we can just apply Z as well)

---

### The Correction Table

| (m0, m1) | Correction |
|----------|------------|
| (0, 0) | **Identity** |
| (1, 0) | **Z:2** |
| (0, 1) | **X:2** |
| (1, 1) | **X:2;Z:2** |

The measurement outcomes $(m0, m1)$ from the Bell basis measurement **uniquely encode two classical bits** that tell Bob exactly what correction gates to apply, **regardless of the original state**. This is the fundamental principle of quantum teleportation!


The flag was encoded into 2-bit pairs, so for recovering it we need to use two bit pairs as well in which the first bit is the basis and second is what we extract as result. 
```python
from pwn import *

ip = "154.57.164.63"
port = 30407

conn = remote(ip, port)
bit_pairs = []

def recv_line_stripped():
    return conn.recvline().decode(errors="ignore").strip()

try:
    while True:
        conn.recvuntil(b"Basis : ")
        basis = recv_line_stripped()
        m0 = recv_line_stripped()
        m1 = recv_line_stripped()
        m0 = int(m0.split()[-1])
        m1 = int(m1.split()[-1])

        # Apply correction
        if m0 == 0 and m1 == 0:
            instructions = "Z:2;Z:2"
        elif m0 == 0 and m1 == 1:
            instructions = "X:2"
        elif m0 == 1 and m1 == 0:
            instructions = "Z:2"
        elif m0 == 1 and m1 == 1:
            instructions = "X:2;Z:2"
        
        conn.sendlineafter(b"Specify the instructions : ", instructions.encode())
        conn.sendlineafter(b"Specify the measurement basis : ", basis.encode())
        res = recv_line_stripped()
        res_bit = int(res.split()[-1])
        
        # Decode: basis 'Z'→0, basis 'X'→1, then append result
        first_bit = '0' if basis == 'Z' else '1'
        bit_pairs.append(first_bit + str(res_bit))
        
except EOFError:
    binary_string = ''.join(bit_pairs)
    flag = bytes(int(binary_string[i : i + 8], 2) for i in range(0, len(binary_string), 8))
    print(flag.decode())
```
