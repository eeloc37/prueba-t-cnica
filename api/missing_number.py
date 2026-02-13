class NaturalNumbersSet:
    def __init__(self, limit: int = 100):
        self.limit = limit
        self.numbers = list(range(1, limit + 1))
        self.extracted = False

    def extract(self, number: int) -> None:
        if not isinstance(number, int):
            raise TypeError("El número debe ser entero")

        if number < 1 or number > self.limit:
            raise ValueError(f"El número debe estar entre 1 y {self.limit}")

        self.numbers.remove(number)
        self.extracted = True

    def get_missing_number(self) -> int:
        if not self.extracted:
            raise ValueError("No se ha extraído ningún número")
        
        expected_sum = self.limit * (self.limit + 1) // 2
        current_sum = sum(self.numbers)
        return expected_sum - current_sum
    
# Ejemplo de uso
if __name__ == "__main__":
    natural_set = NaturalNumbersSet(limit=10)
    natural_set.extract(3)
    natural_set.extract(7)
    missing_number = natural_set.get_missing_number()
    print(f"El número faltante es: {missing_number}")