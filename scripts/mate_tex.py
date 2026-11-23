"""Convierte el texto con matemática "en Unicode" de los ejercicios generados (x², √3, 1/2, ⇒, log_2 8…)
a texto con LaTeX entre $…$ (se muestra con KaTeX en la app web).

Reglas de seguridad: solo se convierten expresiones con operadores o símbolos matemáticos claros; los
números sueltos, las palabras y los signos de pesos ($100) se dejan como texto (el $ literal queda como \\$).
"""
import re

SUP = dict(zip("⁰¹²³⁴⁵⁶⁷⁸⁹ⁿ", "0123456789n"))
SUB = dict(zip("₀₁₂₃₄₅₆₇₈₉ᵥₙ", "0123456789vn"))
SUPS = "".join(SUP)
SUBS = "".join(SUB)
OPS = {"=": "=", "+": "+", "−": "-", "·": r"\cdot ", "×": r"\times ", "÷": r"\div ", "<": "<", ">": ">",
       "≤": r"\le ", "≥": r"\ge ", "≠": r"\ne ", "≈": r"\approx ", "±": r"\pm ", "⇒": r"\Rightarrow ",
       "⇔": r"\Leftrightarrow ", "→": r"\to "}
FUNCS = {"log": r"\log", "ln": r"\ln", "sen": r"\operatorname{sen}", "cos": r"\cos", "tan": r"\tan"}
GREEK = {"θ": r"\theta", "σ": r"\sigma", "Δ": r"\Delta", "π": r"\pi", "φ": r"\varphi"}
LONE = set("xzktnrpqθσ")          # letras sueltas que se consideran variables
CLUSTER = set("abcdfgkmnpqrtuvwxyz")   # 4ac, 100x
UNIT = re.compile(r"[ ]?(cm|mm|dm|km|m)([²³])(?![A-Za-zÀ-ÿ])")
NUM = re.compile(r"\d+(?:[ ]\d{3}(?!\d))*(?:[,.]\d+)?")
LETTER = re.compile(r"[A-Za-zÀ-ÿθσΔπφ]")


class R:
    """resultado parcial: tex, fin, y banderas de si el trozo ya es 'claramente matemático'"""
    __slots__ = ("t", "j", "sp", "grupo", "interior")

    def __init__(self, t, j, sp=False, grupo=False, interior=None):
        self.t, self.j, self.sp, self.grupo, self.interior = t, j, sp, grupo, interior


class P:
    def __init__(self, s):
        self.s = s
        self.n = len(s)

    # ── utilidades ──
    def ch(self, i):
        return self.s[i] if i < self.n else ""

    def sup_sub(self, i):
        """sub/superíndices Unicode consecutivos tras una base → (tex, fin, hubo)"""
        t, j = "", i
        sb = ""
        while self.ch(j) and self.ch(j) in SUBS:
            sb += SUB[self.ch(j)]
            j += 1
        sp = ""
        while self.ch(j) and self.ch(j) in SUPS:
            sp += SUP[self.ch(j)]
            j += 1
        if sb:
            t += "_{" + sb + "}"
        if sp:
            t += "^{" + sp + "}"
        return t, j, bool(sb or sp)

    # ── átomos ──
    def numero(self, i):
        m = NUM.match(self.s, i)
        if not m:
            return None
        txt = m.group(0).replace(" ", r"\,")
        txt = re.sub(r"(\d),(\d)", r"\1{,}\2", txt)
        return R(txt, m.end())

    def grupo(self, i):
        c = self.ch(i)
        cierre = {"(": ")", "[": "]"}.get(c)
        if not cierre:
            return None
        d, j = 0, i
        while j < self.n:
            if self.s[j] in "([":
                d += 1
            elif self.s[j] in ")]":
                d -= 1
                if d == 0:
                    break
            j += 1
        else:
            return None
        if self.s[j] != cierre:
            return None
        inner = self.s[i + 1:j]
        if not inner.strip():
            return None
        partes = self.partir(inner)
        res = self.partes_ok(partes)
        if res is None and "," in inner:
            partes = inner.split(",")
            res = self.partes_ok(partes)
        if res is None:
            return None
        tex_p, sp = res
        t = ", ".join(tex_p)
        if "\\dfrac" in t or "\\sqrt" in t:
            t = (r"\left" + c + t + r"\right" + cierre)
        else:
            t = c + t + cierre
        return R(t, j + 1, sp or len(partes) > 1, grupo=True, interior=tex_p[0] if len(partes) == 1 else None)

    def partes_ok(self, partes):
        tex_p, sp = [], False
        for q in partes:
            r = self.todo(q.strip())
            if r is None:
                return None
            tex_p.append(r.t)
            sp = sp or r.sp
        return tex_p, sp

    def intervalo(self, i):
        """[a, b[  ]a, b]  ]−∞, b[  (corchetes enfrentados)"""
        j = i + 1
        while j < self.n and self.s[j] not in "[]":
            j += 1
        if j >= self.n:
            return None
        partes = self.s[i + 1:j].split(", ")
        if len(partes) != 2:
            return None
        res = self.partes_ok(partes)
        if res is None:
            return None
        return R(self.s[i] + res[0][0] + r",\," + res[0][1] + self.s[j], j + 1, True)

    def partir(self, inner):
        out, d, a = [], 0, 0
        for k, c in enumerate(inner):
            if c in "([":
                d += 1
            elif c in ")]":
                d -= 1
            elif c in ",;" and d == 0 and (k + 1 >= len(inner) or inner[k + 1] == " "):
                out.append(inner[a:k])
                a = k + 1
        out.append(inner[a:])
        return out

    def todo(self, txt):
        """parsea txt completo como expresión (para el interior de un grupo)"""
        q = P(txt)
        r = q.expr(0, interior=True)
        if r is None or r.j != len(txt):
            return None
        return r

    def atomo(self, i):
        c = self.ch(i)
        if not c:
            return None
        if c == "\\":
            return None
        if c == "$":
            r = self.numero(i + 1)
            return R(r"\$" + r.t, r.j) if r else None
        if c.isdigit():
            r = self.numero(i)
            if self.ch(r.j) == "%" or (self.ch(r.j) == " " and self.ch(r.j + 1) == "%"):
                k = r.j + (1 if self.ch(r.j) == "%" else 2)
                r = R(r.t + r"\,\%", k)
            t, j, sp = self.sup_sub(r.j)
            r = R(r.t + t, j, sp)
            if self.ch(r.j) == "°":
                r = R(r.t + r"^{\circ}", r.j + 1, True)
            # 4ac, 100x
            k = r.j
            m = re.match(r"([A-Za-zθσ](?:[%s]*)){1,3}" % (SUBS + SUPS), self.s[k:k + 12])
            if m and all(x in CLUSTER or x in SUBS + SUPS or x in GREEK for x in m.group(0)) and not LETTER.match(self.ch(k + len(m.group(0)))) \
                    and not self.ch(k + len(m.group(0))).isdigit():
                tex = ""
                for x in m.group(0):
                    tex += x if x not in SUBS + SUPS else ""
                # construir con sub/sup
                tex, j2 = "", k
                while j2 < k + len(m.group(0)):
                    tex += GREEK.get(self.s[j2], self.s[j2])
                    t2, j3, _ = self.sup_sub(j2 + 1)
                    tex += t2
                    j2 = j3
                return R(r.t + tex, j2, r.sp or bool(re.search(r"[_^]", tex)))
            return r
        if c == "√":
            j = i + 1
            neg = ""
            if self.ch(j) in "−-" and self.ch(j + 1) and (self.ch(j + 1).isdigit() or self.ch(j + 1).isalpha()):
                neg, j = "-", j + 1
            a = self.atomo_simple(j)
            if not a:
                return None
            cuerpo = a.interior if (a.grupo and a.interior is not None) else a.t
            return R(r"\sqrt{" + neg + cuerpo + "}", a.j, True)
        if c in "([":
            r = self.grupo(i)
            if r is None and c == "[":
                r = self.intervalo(i)
            return r
        if c == "]":
            return self.intervalo(i)
        if c == "|":
            k = self.s.find("|", i + 1)
            if k < 0:
                return None
            r = self.todo(self.s[i + 1:k].strip())
            if r is None:
                return None
            return R(r"\lvert " + r.t + r"\rvert ", k + 1, True)
        if c == "∞":
            return R(r"\infty ", i + 1, True)
        if c == "½":
            return R(r"\tfrac12 ", i + 1, True)
        if c in GREEK or c.isalpha() and c.isascii():
            return self.letra(i)
        return None

    def atomo_simple(self, i):
        c = self.ch(i)
        if c.isdigit():
            r = self.numero(i)
            return r
        if c in "([":
            return self.grupo(i)
        if c.isalpha():
            return self.letra(i)
        return None

    def letra(self, i):
        s = self.s
        # función
        for nom in sorted(FUNCS, key=len, reverse=True):
            if s.startswith(nom, i) and not LETTER.match(self.ch(i + len(nom))) or (s.startswith(nom, i) and self.ch(i + len(nom)) in "_" + SUBS):
                j = i + len(nom)
                sub = ""
                if self.ch(j) == "_":
                    m = re.match(r"\d+|[A-Za-z]", s[j + 1:])
                    if m:
                        sub, j = "_{" + m.group(0) + "}", j + 1 + len(m.group(0))
                    else:
                        a = self.atomo_simple(j + 1)
                        if not a:
                            return None
                        sub, j = "_{" + (a.interior or a.t) + "}", a.j
                elif self.ch(j) and self.ch(j) in SUBS:
                    t, j, _ = self.sup_sub(j)
                    sub = t
                if self.ch(j) == " ":
                    j += 1
                arg = self.factor(j)
                if arg is None:
                    return None
                return R(FUNCS[nom] + sub + " " + arg.t, arg.j, True)
        c = s[i]
        if c.isalpha() and c.isascii() and LETTER.match(self.ch(i + 1) or " "):
            m = re.match(r"[A-Za-zÀ-ÿ]+", s[i:])
            run = m.group(0)
            if 2 <= len(run) <= 3 and all(x in CLUSTER for x in run):        # kx, qy, ax²
                j = i + len(run)
                t, j2, sp = self.sup_sub(j)
                if self.ch(j2).isdigit() or LETTER.match(self.ch(j2) or " "):
                    return None
                return R(run + t, j2, sp)
            return None                                     # palabra, no variable
        base = GREEK.get(c, c)
        t, j, sp = self.sup_sub(i + 1)
        if self.ch(j).isdigit() or (LETTER.match(self.ch(j) or " ") and not sp):
            return None
        # x₁x₂ → encadenar
        tex = base + t
        while sp and self.ch(j) and LETTER.match(self.ch(j)) and self.ch(j + 1) and (self.ch(j + 1) in SUBS + SUPS):
            b = GREEK.get(self.ch(j), self.ch(j))
            t2, j, _ = self.sup_sub(j + 1)
            tex += b + t2
        # P(mujer | tatuaje)
        if c == "P" and self.ch(j) == "(" and not sp:
            k = self.s.find(")", j)
            inner = self.s[j + 1:k] if k > 0 else ""
            if "|" in inner and "(" not in inner:
                a, b = [x.strip() for x in inner.split("|", 1)]
                def parte(x):
                    r = self.todo(x) if x else None
                    return r.t if r else r"\text{" + x + "}"
                return R("P(" + parte(a) + r"\mid " + parte(b) + ")", k + 1, True)
        if self.ch(j) == "'" and not LETTER.match(self.ch(j + 1) or " "):
            tex += "'"
            j += 1
        return R(tex, j, sp)

    # ── factores y términos ──
    def con_post(self, a):
        """potencia ^ y unidades después de un átomo"""
        while True:
            if self.ch(a.j) == "^":
                b = self.exponente(a.j + 1)
                if not b:
                    break
                a = R(a.t + "^{" + b.t + "}", b.j, True)
            elif self.ch(a.j) == "°":
                a = R(a.t + r"^{\circ}", a.j + 1, True)
            elif self.ch(a.j) and self.ch(a.j) in SUPS and not a.t.endswith("}") :
                t, j, _ = self.sup_sub(a.j)
                a = R(a.t + t, j, True)
            else:
                break
        return a

    def exponente(self, i):
        neg = ""
        if self.ch(i) in "−-":
            neg, i = "-", i + 1
        a = self.atomo_simple(i)
        if not a:
            return None
        cuerpo = a.interior if (a.grupo and a.interior is not None) else a.t
        return R((neg + cuerpo).replace(r"\dfrac", r"\frac"), a.j)

    def factor(self, i):
        """producto de átomos pegados: 3√3, x₁x₂, (a+b)(a−b), P(A)"""
        a = self.atomo(i)
        if a is None:
            return None
        a = self.con_post(a)
        tex, sp, j, grupos = a.t, a.sp, a.j, [a] if a.grupo else []
        prev_g = a.grupo or a.t.endswith("}")
        while True:
            c = self.ch(j)
            if c and (c in "√([" or (c.isalpha() and c.isascii() and not c.isspace()) or c in GREEK) and not (c == "(" and False):
                b = self.atomo(j)
                if b is None:
                    break
                # evitar pegar palabras: letra tras átomo solo si el átomo termina en sub/sup o grupo
                if c.isalpha() and not prev_g:
                    break
                b = self.con_post(b)
                tex += b.t
                sp = sp or b.sp
                j = b.j
                a = R(tex, j, sp)
                prev_g = b.grupo or b.t.endswith("}")
                grupos = []
            else:
                break
        interior = grupos[0].interior if (len(grupos) == 1 and tex == grupos[0].t) else None
        return R(tex, j, sp, grupo=bool(interior), interior=interior)

    def termino(self, i):
        neg = ""
        c = self.ch(i)
        if c == "−" or (c == "-" and self.ch(i + 1) and not self.ch(i + 1).isspace()):
            neg, i = "-", i + 1
        elif c == "±":
            neg, i = r"\pm ", i + 1
        f = self.factor(i)
        if f is None:
            return None
        sep = 3 if self.s[f.j:f.j + 3] == " / " else (1 if self.ch(f.j) == "/" and self.ch(f.j + 1) and not self.ch(f.j + 1).isspace() else 0)
        if sep:
            k = f.j + sep
            neg2 = ""
            if self.ch(k) in "−-" and self.ch(k + 1) and not self.ch(k + 1).isspace():
                neg2, k = "-", k + 1
            g = self.factor(k)
            if g is not None:
                num = f.interior if f.interior is not None else f.t
                den = g.interior if g.interior is not None else g.t
                m = re.fullmatch(r"(\d+)(\\sqrt\{.*\})", den)
                if m and re.fullmatch(r"\d+", num):          # "147/2√3" en estos ejercicios significa (147/2)·√3
                    return self.con_unidad(R(neg + r"\dfrac{" + num + "}{" + m.group(1) + "}" + m.group(2), g.j, True))
                return self.con_unidad(R(neg + r"\dfrac{" + num + "}{" + neg2 + den + "}", g.j, True))
        return self.con_unidad(R(neg + f.t, f.j, f.sp))

    def con_unidad(self, r):
        m = UNIT.match(self.s, r.j)
        if m and (r.t[:1].isdigit() or r.t.startswith(("\\$", "-", "\\dfrac")) or "sqrt" in r.t):
            return R(r.t + r"\,\text{" + m.group(1) + "}^{" + SUP[m.group(2)] + "}", m.end(), True)
        return r

    def expr(self, i, interior=False):
        t = self.termino(i)
        if t is None:
            return None
        tex, j, sp, nop = t.t, t.j, t.sp, 0
        while True:
            k = j
            while self.ch(k) == " ":
                k += 1
            c = self.ch(k)
            if c in OPS and c != "−" or c == "−" or (c == "-" and self.ch(k + 1) == " " and k > j):
                kop = k + 1
                while self.ch(kop) == " ":
                    kop += 1
                op = OPS.get(c, "-")
                t2 = self.termino(kop)
                if t2 is None:
                    # "x =" colgante: una variable suelta seguida de "="
                    if c == "=" and nop == 0 and re.match(r"[A-Za-z]|\\theta|\\sigma", tex) and not interior:
                        return R(tex + " =", k + 1, True)
                    break
                tex += " " + op + " " + t2.t
                j = t2.j
                nop += 1
                sp = True
            else:
                break
        return R(tex, j, sp or nop > 0)


def convertir(texto):
    """texto con Unicode matemático → texto con $…$ (los $ literales quedan como \\$)"""
    if not texto or not isinstance(texto, str):
        return texto
    p = P(texto)
    s, out, i, buf = texto, [], 0, []
    while i < len(s):
        c = s[i]
        ok_pos = i == 0 or not (s[i - 1].isalnum() or s[i - 1] in "_$" or s[i - 1] in SUPS + SUBS)
        r = p.expr(i) if ok_pos and (c.isalnum() or c in "√([]|−-±$∞½θσΔπφ") else None
        if r is not None:
            lone_ok = r.sp or (len(r.t) <= 3 and r.t in LONE_TEX) or re.fullmatch(r"-\d[\d{},\\]*", r.t) is not None
            if lone_ok and r.j > i:
                if not buf and out and out[-1][0] == "m":                  # trozos matemáticos pegados
                    out[-1] = ("m", out[-1][1] + r.t.strip())
                    i = r.j
                    continue
                if buf == [" "] and out and out[-1][0] == "m":      # dos trozos matemáticos separados por un espacio: unirlos
                    out[-1] = ("m", out[-1][1] + r"\ " + r.t.strip())
                    buf = []
                    i = r.j
                    continue
                if buf:
                    out.append(("t", "".join(buf).replace("$", r"\$")))
                    buf = []
                out.append(("m", r.t.strip()))
                i = r.j
                continue
        if c in "⇒⇔→≤≥≠≈" or c in SUPS or c in SUBS:                    # símbolo suelto fuera de una expresión
            if buf:
                out.append(("t", "".join(buf).replace("$", r"\$")))
                buf = []
            if c in SUPS or c in SUBS:
                t, j2, _ = p.sup_sub(i)
                out.append(("m", t if t[:1] in "^_" else "^" + t))
                i = j2
            else:
                out.append(("m", OPS[c].strip()))
                i += 1
            continue
        buf.append(c)
        i += 1
    if buf:
        out.append(("t", "".join(buf).replace("$", r"\$")))
    return "".join("$" + v + "$" if k == "m" else v for k, v in out)


LONE_TEX = set(LONE) | {r"\theta", r"\sigma"}
