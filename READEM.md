# PROTOCOLOBB84-API

*Empowering Secure Quantum Communication for the Future*

![Last Commit](https://img.shields.io/github/last-commit/JoaquinGaldame/PROTOCOLOBB84-API?style=flat&color=blue)
![Python](https://img.shields.io/badge/python-100%25-blue)
![Languages](https://img.shields.io/badge/languages-1-success)

---

### Built with the tools and technologies:

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

---

## Table of Contents

- [Overview](#overview)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)



  ---

## 📌 Overview

El **Protocolo BB84** es uno de los algoritmos fundamentales de la **criptografía cuántica**, diseñado para el intercambio seguro de claves mediante qubits.  
Su fortaleza radica en que cualquier intento de espionaje (interceptación de qubits por un atacante, Eva) altera el sistema cuántico, introduciendo errores detectables por los usuarios legítimos (Ana y Beto).

Esta API implementa una **simulación del protocolo BB84** usando **FastAPI** y **NumPy**, permitiendo experimentar de forma práctica con los conceptos de la criptografía cuántica.  

Se incluyen dos modos de simulación:  
- 🔒 **Sin espía (Eva ausente):** Ana y Beto logran acordar una clave secreta con alta tasa de coincidencia.  
- 🕵️ **Con espía (Eva presente):** se introduce ruido en la comunicación, reduciendo la coincidencia y exponiendo la intrusión.  

---

## ⚙️ Getting Started

### ✅ Prerequisites

- Python 3.9+
- pip

### 📦 Installation

Clonar el repositorio e instalar dependencias:

```bash
git clone https://github.com/USER/PROTOCOLOBB84-API.git
cd PROTOCOLOBB84-API

pip install -r requirements.txt