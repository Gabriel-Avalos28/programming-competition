abecedario = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# Configuración de los rotores
juego = {
    'I': ['EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'Q'],
    'II': ['AJDKSIRUXBLHWTMCQGZNPYFVOE', 'E'],
    'III': ['BDFHJLCPRTXVZNYEIWGAKMUSQO', 'V'],
    'IV': ['ESOVPZJAYQUIRHXLNFTGKDCMWB', 'J'],
    'V': ['VZBRGITYUPSDNHLXAWMJQOFECK', 'Z']
}

# Reflectores (UKW)
UKW = {
    'B': 'YRUHQSLDPXNGOKMIEBFZCWVJAT',
    'C': 'FVPJIAOYEDRZXWGCTKUQSBNMHL'
}

class Reflector:
    def __init__(self, abecedario, reflejo):
        self.abecedario = abecedario
        self.reflejo = reflejo

    def refleja(self, indice):
        letra = self.reflejo[indice]
        return self.abecedario.index(letra)

class Rotor:
    def __init__(self, abecedario, pareo, paso='Z', orden=1):
        self.abecedario = abecedario
        self.pareo = pareo
        self.paso = paso
        self._ini = 0
        self.orden = orden

    def avanza(self):
        self._ini = (self._ini + 1) % len(self.abecedario)

    def paso_alcanzado(self):
        return self._ini == self.abecedario.index(self.paso)

    def codifica(self, indice):
        indice = (indice + self._ini) % len(self.abecedario)
        letra = self.pareo[indice]
        return (self.abecedario.index(letra) - self._ini) % len(self.abecedario)

    def decodifica(self, indice):
        indice = (indice + self._ini) % len(self.abecedario)
        letra = self.abecedario[indice]
        return (self.pareo.index(letra) - self._ini) % len(self.abecedario)

class Enigma:
    def __init__(self, abecedario, rotores, reflector, inicio='AAA'):
        self.abecedario = abecedario
        self.rotores = rotores
        self.reflector = reflector
        self.inicio = inicio

    def configurar_inicio(self):
        for i, rotor in enumerate(self.rotores):
            rotor._ini = self.abecedario.index(self.inicio[i])

    def codifica_cadena(self, cadena):
        cadena = cadena.replace(" ", "X").upper()
        resultado = ""
        for letra in cadena:
            if letra not in self.abecedario:
                continue
            indice = self.abecedario.index(letra)

            # Pasar por los rotores (ida)
            for rotor in self.rotores:
                rotor.avanza()
                indice = rotor.codifica(indice)

            # Reflejar
            indice = self.reflector.refleja(indice)

            # Pasar por los rotores (vuelta)
            for rotor in reversed(self.rotores):
                indice = rotor.decodifica(indice)

            resultado += self.abecedario[indice]
        return resultado

# Configuración del Enigma
def configurar_enigma():
    reflector = Reflector(abecedario, UKW['B'])
    rotor1 = Rotor(abecedario, juego['I'][0], juego['I'][1], orden=1)
    rotor2 = Rotor(abecedario, juego['II'][0], juego['II'][1], orden=2)
    rotor3 = Rotor(abecedario, juego['III'][0], juego['III'][1], orden=3)
    enigma = Enigma(abecedario, [rotor1, rotor2, rotor3], reflector, inicio='GAI')
    enigma.configurar_inicio()
    return enigma

# Ejemplo de uso
enigma = configurar_enigma()
entrada = "SIPUEDEN"
resultado = enigma.codifica_cadena(entrada)
print("Entrada:", entrada)
print("Codificado:", resultado)
