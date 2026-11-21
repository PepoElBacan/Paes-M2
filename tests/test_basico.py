"""Pruebas básicas: python3 -m unittest discover -s tests"""
import json
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from sistema import autotest, banco, estado  # noqa: E402
from sistema.taxonomia import TEMAS  # noqa: E402


class TestBanco(unittest.TestCase):
    def setUp(self):
        self.b = banco.cargar()

    def test_cantidades(self):
        por = {}
        for q in self.b:
            por[q["prueba"]] = por.get(q["prueba"], 0) + 1
        for p in ("I2024", "R2024", "I2025", "I2026", "I2027"):
            self.assertEqual(por[p], 55, p)
        self.assertEqual(len(self.b), 349)

    def test_temas_validos_y_claves(self):
        for q in self.b:
            self.assertIn(q["tema"], TEMAS, q["id"])
            if not q["eliminada"]:
                self.assertIn(q["clave"], list("ABCDE"), q["id"])
        # cada prueba completa tiene exactamente 5 pilotos
        for p in ("I2024", "R2024", "I2025", "I2026", "I2027"):
            self.assertEqual(sum(q["piloto"] for q in self.b if q["prueba"] == p), 5, p)

    def test_clavijero_coincide_con_hoja_del_usuario(self):
        import csv
        ids = {q["id"]: q for q in self.b}
        for r in csv.DictReader(open(RAIZ / "datos" / "respuestas_ensayo_I2026.csv")):
            q = ids[f"I2026-{int(r['n']):02d}"]
            self.assertEqual(q["clave"] or "", r["correcta"], q["id"])

    def test_tabla_puntaje(self):
        t = json.loads((RAIZ / "datos" / "tabla_puntaje.json").read_text())
        self.assertEqual(t["I2026"]["40"], 762)      # ejemplo oficial del clavijero
        for p, tab in t.items():
            v = [tab[str(i)] for i in range(51)]
            self.assertEqual(v, sorted(v), p)


class TestGeneradores(unittest.TestCase):
    def test_autotest(self):
        self.assertTrue(autotest.correr(60, verbose=False))


class TestRepeticionEspaciada(unittest.TestCase):
    def test_intervalos_y_dominio(self):
        from datetime import date
        est = estado.vacio()
        d = date(2026, 11, 21)
        e = estado.registrar_intento(est, "X-01", False, d)
        self.assertEqual(e["proximo"], "2026-11-22")        # error → reintento +1 día
        e = estado.registrar_intento(est, "X-01", True, d)
        self.assertEqual(e["proximo"], "2026-11-24")        # 1.er acierto → +3 días
        e = estado.registrar_intento(est, "X-01", True, d)
        self.assertEqual(e["proximo"], "2026-11-28")        # 2.º acierto → +7 días
        e = estado.registrar_intento(est, "X-01", True, d)
        self.assertTrue(e["dominada"])                       # 3 aciertos seguidos = dominada
        e = estado.registrar_intento(est, "X-01", False, d)
        self.assertFalse(e["dominada"])
        self.assertEqual(e["racha"], 0)

    def test_nivel_sube_con_4_de_5(self):
        est = estado.vacio()
        for ok in (1, 1, 0, 1, 1):
            subio = estado.registrar_practica(est, "ALG-cua", ok)
        self.assertTrue(subio)
        self.assertEqual(est["temas"]["ALG-cua"]["nivel"], 2)


class TestRefuerzo(unittest.TestCase):
    def test_tarjeta_de_refuerzo(self):
        from datetime import date, timedelta
        from sistema import refuerzo as R
        est = estado.vacio()
        R.abrir_carta(est, "ALG-cua", "vertice-maximo", 2)
        c = est["cartas"]["ALG-cua|vertice-maximo"]
        self.assertEqual(c["proximo"], (estado.hoy() + timedelta(days=1)).isoformat())   # vuelve mañana
        R.resolver_carta(est, "ALG-cua|vertice-maximo", True)
        self.assertEqual(c["racha"], 1)
        R.resolver_carta(est, "ALG-cua|vertice-maximo", True)
        R.resolver_carta(est, "ALG-cua|vertice-maximo", True)
        self.assertTrue(c["dominada"])                                                    # 3 seguidos
        R.abrir_carta(est, "ALG-cua", "vertice-maximo", 1)                               # volver a fallar la reabre
        self.assertFalse(c["dominada"])
        self.assertEqual((c["racha"], c["nivel"]), (0, 1))

    def test_subtemas_debiles_desde_tu_ensayo(self):
        from sistema import refuerzo as R
        est = estado.vacio()
        estado.registrar_ensayo(est, "I2026", 31, 49, 640, {}, fecha=__import__("datetime").date(2026, 11, 14))
        d = {x["k"]: x for x in R.debiles(est, banco.cargar(), {})}
        v = d["ALG-cua|vertice-maximo"]            # P29, P30 y P31 de tu ensayo
        self.assertEqual((v["err"], v["n"]), (3, 3))
        self.assertTrue(v["gen"])

    def test_cada_subtema_generado_existe(self):
        from sistema import refuerzo as R
        for tema, subs in R.subtemas_gen().items():
            self.assertTrue(subs, tema)


if __name__ == "__main__":
    unittest.main()
