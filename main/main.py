import sympy as sp

class LeastSquaresApproximator():
    def __init__(self,) -> None:
        self.basis = ["1", "x", "x**2", "x**3", "x**4", "x**5"]

    def innerProduct(self, lowerLimit: int, upperLimit: int,
                     funcA, funcB, funcW) -> any:
        x = sp.Symbol("x")
        func = funcA*funcB*funcW
        product = sp.integrate(func, (x, lowerLimit, upperLimit)).evalf()
        return product
        
    def evaluate(self, func, lowerLimit, upperLimit,
                 basis: list[str], funcW: str|int=1):
        try:
            if basis == [""]:
                basis = self.basis
            for index, funcB in enumerate(basis):
                basis[index] = sp.sympify(funcB)
            func = sp.sympify(func)
            funcW = sp.sympify(funcW)
        except sp.SympifyError as e:
            raise ValueError(e.args[0])
        matrixA, matrixB = [], []
        for line in range(len(basis)):
            matrixA.append([])
            product = self.innerProduct(lowerLimit, upperLimit, func, basis[line], funcW)
            matrixB.append([product])
            for col in range(len(basis)):
                product = self.innerProduct(lowerLimit, upperLimit, basis[col], basis[line], funcW)
                matrixA[line].append(product)
        matrixA, matrixB = sp.Matrix(matrixA), sp.Matrix(matrixB)
        solMatrix = matrixA.solve(matrixB)
        aproxFunc = solMatrix[0]*basis[0]
        for index in range(1, len(basis)):
            aproxFunc += solMatrix[index]*basis[index]
        funcNorm = self.innerProduct(lowerLimit, upperLimit, func, func, funcW)
        summation = solMatrix[0]*matrixB[0]
        for index in range(1, len(matrixB)):
            summation += solMatrix[index]*matrixB[index]
        methodError = sp.sqrt(abs(funcNorm - summation))
        return aproxFunc, methodError