from main import saludo

def test_saludo():
    assert saludo("Mundo") == "Hola, Mundo!"

def test_despedida():
    assert saludo("Adios") == "Nos vemos"