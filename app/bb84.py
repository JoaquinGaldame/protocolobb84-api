import random
from typing import List, Dict
from app.Q_Lenguaje_v2 import ket0, ket1, h, medir

class BB84RealSimulator:
    def __init__(self, largo: int, con_espia: bool = False):
        self.largo = largo
        self.con_espia = con_espia

        # Variables
        self.baseAna: List[str] = []
        self.baseBeto: List[str] = []
        self.bitsAna: List[int] = []
        self.bitsBeto: List[int] = []
        self.clave: List[int] = []

        self.baseEva: List[str] = []
        self.bitsBetoEva: List[int] = []
        self.claveEva: List[int] = []

    def _envia_qubits(self, bits: List[int], bases: List[str]):
        """Convierte bits en qubits usando bases Z/X"""
        qubits = []
        for i in range(len(bits)):
            if bits[i] == 0:
                qubits.append(ket0 if bases[i] == 'Z' else h(ket0))
            else:
                qubits.append(ket1 if bases[i] == 'Z' else h(ket1))
        return qubits

    def _lee_qubits(self, qubits, bases: List[str]):
        """Mide qubits según base"""
        resultados = []
        for i, base in enumerate(bases):
            if base == 'Z':
                resultados.append(medir(qubits[i]))
            else:
                resultados.append(medir(h(qubits[i])))
        return resultados

    def _fase_sin_espia(self, qubits):
        """Ana y Beto generan clave sin espía"""
        lecturas_beto = self._lee_qubits(qubits, self.baseBeto)
        for i in range(self.largo):
            self.bitsBeto.append(lecturas_beto[i][1][0])  # escalar
            if self.baseAna[i] == self.baseBeto[i]:
                self.clave.append(self.bitsBeto[i])

    def _fase_con_espia(self, qubits):
        """Eva intercepta y reenvía"""
        # Eva mide en bases aleatorias
        self.baseEva = [random.choice(['Z','X']) for _ in range(self.largo)]
        qubits_eva = self._lee_qubits(qubits, self.baseEva)

        # Beto mide lo reenviado
        lecturas_beto_eva = self._lee_qubits(qubits_eva, self.baseBeto)
        for i in range(self.largo):
            self.bitsBetoEva.append(lecturas_beto_eva[i][1][0])
            if self.baseAna[i] == self.baseBeto[i] and self.bitsAna[i] == self.bitsBetoEva[i]:
                self.claveEva.append(self.bitsBetoEva[i])

    def run(self) -> Dict:
        # Paso 1: Generar bases y bits
        self.baseAna = [random.choice(['Z','X']) for _ in range(self.largo)]
        self.baseBeto = [random.choice(['Z','X']) for _ in range(self.largo)]
        self.bitsAna = [random.choice([0,1]) for _ in range(self.largo)]

        qubits_ana = self._envia_qubits(self.bitsAna, self.baseAna)

        # Paso 2 y 3: Sin espía
        self._fase_sin_espia(qubits_ana)

        result = {
            "baseAna": self.baseAna,
            "baseBeto": self.baseBeto,
            "bitsAna": self.bitsAna,
            "bitsBeto": self.bitsBeto,
            "claveCompartida": self.clave,
            "porcentaje": round(len(self.clave)/self.largo*100, 2)
        }

        # Paso 4: Con espía
        if self.con_espia:
            self._fase_con_espia(qubits_ana)
            result.update({
                "baseEva": self.baseEva,
                "bitsBetoEva": self.bitsBetoEva,
                "claveConEva": self.claveEva,
                "porcentajeConEva": round(len(self.claveEva)/self.largo*100, 2)
            })

        return result
