# Hoja de fórmulas M2 (para repasar el día 29)

> Las fórmulas están escritas en LaTeX (entre signos de pesos). En la app se ven como en un libro; en GitHub también.

## Números
- Producto de potencias: $a^m\cdot a^n=a^{m+n}$
- Cociente de potencias: $\dfrac{a^m}{a^n}=a^{m-n}$
- Potencia de potencia: $(a^m)^n=a^{mn}$
- Exponente negativo: $a^{-n}=\dfrac1{a^n}$
- Exponente fraccionario: $a^{m/n}=\sqrt[n]{a^m}$
- Definición de logaritmo: $\log_b a=x\iff b^x=a$
- Producto y cociente: $\log(ab)=\log a+\log b$ · $\log\dfrac ab=\log a-\log b$
- Potencia dentro del logaritmo: $\log a^n=n\log a$
- Cambio de base: $\log_b a=\dfrac{\log a}{\log b}$
- **Dato útil:** $\log5=1-\log2$
- Aumentar un $p\,\%$: $\times\left(1+\dfrac p{100}\right)$ · disminuir: $\times\left(1-\dfrac p{100}\right)$ · los porcentajes sucesivos se multiplican.
- Interés compuesto: $C\,(1+i)^n$
- Crecimiento: $A\cdot b^t$ · "duplica cada $d$": $A\cdot2^{t/d}$

## Álgebra y funciones
- Cuadrado de binomio: $(a\pm b)^2=a^2\pm2ab+b^2$
- Diferencia de cuadrados: $a^2-b^2=(a+b)(a-b)$
- Desigualdad: al multiplicar o dividir por un negativo **se invierte**.
- Sistema 2x2, una solución: $\dfrac{a_1}{a_2}\neq\dfrac{b_1}{b_2}$
- Sistema 2x2, ninguna solución: $\dfrac{a_1}{a_2}=\dfrac{b_1}{b_2}\neq\dfrac{c_1}{c_2}$ · si las tres razones son iguales, infinitas.
- Recta: $y=mx+n$ con $m=\dfrac{\Delta y}{\Delta x}$
- Proporcionalidad directa: $y=kx$ · inversa: $xy=k$
- **Cuadrática, vértice:** $x_v=-\dfrac b{2a}$ y después $y_v=f(x_v)$
- **Cuadrática, discriminante:** $\Delta=b^2-4ac$
- Suma y producto de raíces: $x_1+x_2=-\dfrac ba$ · $x_1x_2=\dfrac ca$
- Concavidad: $a>0$ abre arriba (mínimo) · $a<0$ abre abajo (máximo)
- Reflexiones: $-f(x)$ refleja en X · $f(-x)$ refleja en Y.

## Geometría
- Pitágoras: $a^2+b^2=c^2$
- Razón de semejanza $k$: áreas $k^2$ · volúmenes $k^3$
- Triángulo: $\dfrac{bh}2$ · trapecio: $\dfrac{(B+b)\,h}2$ · círculo: $\pi r^2$
- Hexágono regular de lado $l$: $\dfrac{3\sqrt3}2\,l^2$
- Prisma: $A_b\cdot h$ · cilindro: $\pi r^2h$
- Cono: $\tfrac13\pi r^2h$ · esfera: $\tfrac43\pi r^3$
- Suma y ponderación de vectores: $(a,b)\pm(c,d)=(a\pm c,\ b\pm d)$ · $k(a,b)=(ka,\ kb)$
- Módulo de un vector: $\lvert(a,b)\rvert=\sqrt{a^2+b^2}$
- Reflexión en el eje X: $(x,-y)$ · en el eje Y: $(-x,y)$
- Rotación de $90^\circ$ antihoraria: $(x,y)\to(-y,\ x)$
- **Homotecia de centro $C$ y razón $k$:** $P'=C+k\,(P-C)$
- Razones trigonométricas: $\operatorname{sen}=\dfrac{\text{op}}{\text{hip}}$ · $\cos=\dfrac{\text{ady}}{\text{hip}}$ · $\tan=\dfrac{\text{op}}{\text{ady}}$
- Identidades: $\operatorname{sen}^2\theta+\cos^2\theta=1$ · $\operatorname{sen}2\theta=2\operatorname{sen}\theta\cos\theta$
- Ángulos notables (seno): $30^\circ\to\tfrac12$ · $45^\circ\to\tfrac{\sqrt2}2$ · $60^\circ\to\tfrac{\sqrt3}2$

## Probabilidad y estadística
- Laplace: $\dfrac{\text{favorables}}{\text{totales}}$ · sin reposición: el denominador baja.
- Probabilidad condicional: $P(A\mid B)=\dfrac{P(A\cap B)}{P(B)}$
- Eventos independientes: $P(A\cap B)=P(A)\,P(B)$
- Cargos distintos (el orden importa): $P(n,k)=\dfrac{n!}{(n-k)!}$
- Comité (el orden no importa): $C(n,k)=\dfrac{n!}{k!\,(n-k)!}$
- Rango intercuartil: $IQR=Q_3-Q_1$
- Desviación estándar: $\sigma=\sqrt{\dfrac{\sum(x-\bar x)^2}{n}}$ · coeficiente de variación: $CV=\dfrac\sigma{\bar x}$
- Dato atípico: fuera de $[\,Q_1-1{,}5\cdot IQR\ ;\ Q_3+1{,}5\cdot IQR\,]$
- Binomial: $P(X=k)=\binom nk\,p^k(1-p)^{n-k}$ · esperanza $E=np$
- Normal: $68\,\%$ ($\pm1\sigma$) · $95\,\%$ ($\pm2\sigma$) · $99{,}7\,\%$ ($\pm3\sigma$)
