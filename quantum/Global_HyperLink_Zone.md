# Global HyperLink Zone

Beneath Qubitrix’s corporate towers lies the Global Hyperlink Zone - their prototype quantum internet. Its five access nodes authenticate through specific quantum gate patterns. Retrieve the sequence, stabilize the hyperlink, and force entry into their hidden backbone. One wrong move, and the link collapses.

For the challenge we are given a python file which contains qiskit code for initializing the server. It takes instruction from the user in a specified format.

### Understanding the code
When we provide the input to the script based on that it first checks if the given instruction is in a specific format. Format being `Gate:Parameter`.\
Once this format is confirmed then the script creates a 5-bit quantum circuit. After this circuit is complete measurements are done. This measurement is done repeatedly for each qbit which concatenates the measured bits into long bit-string.\
Then the following condition is checked:
- share0 == share1 == share3
- share2 == share4
- share0/1/3 != share2/4

If the above checks passed then the flag is returned.

### Gates
Generic information about the gates:
- X Gate (Pauli-X): The quantum equivalent of a classical NOT gate, flipping $|0\rangle$ to $|1\rangle$ and $|1\rangle$ to $|0\rangle$, essential for bit-flips.
- H Gate (Hadamard): Creates an equal superposition from a definite state:
    - $H|0\rangle = \dfrac{|0\rangle + |1\rangle}{\sqrt{2}}$
    - $H|1\rangle = \dfrac{|0\rangle - |1\rangle}{\sqrt{2}}$
- S Gate (Phase): Applies a phase shift of $i$ (equivalently $e^{i\pi/2}$) to the $|1\rangle$ state, while leaving $|0\rangle$ unchanged.
- T Gate ($\pi/8$ Gate): Applies a phase shift of $e^{i\pi/4}$ to the $|1\rangle$ state, also known as the $\pi/8$ gate, crucial for universal quantum computation.

- CX (CNOT)	Applies a Pauli-X (NOT) gate.	
- CY	Applies a Pauli-Y gate (flips and phases).	
- CZ	Applies a Pauli-Z gate (applies a phase shift).


### Intution and Exploit
A H (Hadamard) gate makes a qubit produce random measurement outcomes on every shot.\
A CX (CNOT) with control A and target B makes B’s measured bit match A’s measured bit for each shot (if B started at 0).\
So we make a qbit 0 random and copy it to qbit 1 and 3, similar is done with qbit 2 and 4.

**Exploit**: `H:0;CX:0,1;CX:0,3;H:2;CX:2,4`

what happens:

    H:0 — make qubit 0 random each shot.
    CX:0,1 and CX:0,3 — copy qubit 0’s result to qubits 1 and 3.
    H:2 — make qubit 2 random each shot (independent).
    CX:2,4 — copy qubit 2’s result to qubit 4.

We can send this exploit using the following one liner.\
`printf 'H:0;CX:0,1;CX:0,3;H:2;CX:2,4\n' | nc <ip> <port>`

Once we do the the flag will be printed.
### COMPLETE