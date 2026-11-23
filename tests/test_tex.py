import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from mate_tex import convertir  # noqa: E402


class TestTex(unittest.TestCase):
    def test_fracciones_y_potencias(self):
        self.assertEqual(convertir("3/4"), r"$\dfrac{3}{4}$")
        self.assertEqual(convertir("x² − 7x + 6 = 0"), r"$x^{2} - 7x + 6 = 0$")

    def test_texto_y_dinero_no_se_tocan(self):
        s = convertir("En una alcancía hay 26 monedas de $100 y de $10.")
        self.assertNotIn("$1", s.replace(r"\$1", ""))
        self.assertEqual(s, r"En una alcancía hay 26 monedas de \$100 y de \$10.")

    def test_unidades_fuera_de_la_fraccion(self):
        self.assertEqual(convertir("147/2√3 cm²"), r"$\dfrac{147}{2}\sqrt{3}\,\text{cm}^{2}$")

    def test_probabilidad_condicional(self):
        self.assertIn(r"P(\text{mujer}\mid \text{tatuaje})", convertir("P(mujer | tatuaje) = 120/155"))

    def test_idempotencia_de_dolares_pares(self):
        for s in ["k = ±4", "log_3 20 = log 20 / log 3", "(x,y)→(−y,x)", "[4/5, ∞[", "Cuadrante IV"]:
            self.assertEqual(len([c for i, c in enumerate(convertir(s)) if c == "$" and convertir(s)[i - 1] != "\\"]) % 2, 0)


if __name__ == "__main__":
    unittest.main()
