#!/usr/bin/env python3
# ABOUTME: Genera ventas_ecommerce_peru.csv (500 000 pedidos de e-commerce en Peru, 2023-2025) para el trabajo grupal de la Semana 10.
# ABOUTME: Solo libreria estandar y semilla fija: volver a ejecutarlo produce exactamente el mismo CSV (solo ASCII, sin comas dentro de campos).

import random
import sys
from bisect import bisect_right
from datetime import date, timedelta
from itertools import accumulate
from pathlib import Path

SEMILLA = 10
N_PEDIDOS = 500_000
N_CLIENTES = 220_000
PRIMER_ID_PEDIDO = 1_000_001
PRIMER_ID_CLIENTE = 100_001
SALIDA = Path(__file__).resolve().parents[2] / "ventas_ecommerce_peru.csv"

ENCABEZADO = (
    "id_pedido,fecha_pedido,hora_pedido,id_cliente,departamento,categoria,producto,"
    "precio_unitario,cantidad,descuento_pct,monto_total,metodo_pago,canal,estado,"
    "dias_entrega,calificacion"
)


class Muestreador:
    """Sorteo ponderado rapido (busqueda binaria sobre pesos acumulados)."""

    def __init__(self, items, pesos):
        self.items = list(items)
        self.acum = list(accumulate(pesos))
        self.total = self.acum[-1]

    def sortear(self, rng):
        return self.items[bisect_right(self.acum, rng.random() * self.total)]


# ---------------------------------------------------------------- geografia
# (departamento, peso de pedidos, media de dias de entrega, desviacion)
DEPARTAMENTOS = [
    ("Lima", 44.0, 1.8, 0.7),
    ("Callao", 4.5, 2.0, 0.7),
    ("Arequipa", 6.0, 3.3, 1.0),
    ("La_Libertad", 5.0, 3.5, 1.1),
    ("Piura", 4.0, 3.8, 1.2),
    ("Lambayeque", 3.8, 3.6, 1.1),
    ("Cusco", 3.6, 5.8, 1.6),
    ("Junin", 3.0, 5.0, 1.5),
    ("Ica", 2.8, 3.0, 1.0),
    ("Cajamarca", 1.9, 6.2, 1.8),
    ("Puno", 1.8, 6.5, 1.8),
    ("Ancash", 1.8, 4.5, 1.4),
    ("San_Martin", 1.6, 7.0, 2.0),
    ("Loreto", 1.4, 10.0, 2.5),
    ("Huanuco", 1.0, 6.3, 1.8),
    ("Tacna", 1.0, 3.8, 1.1),
    ("Ayacucho", 0.9, 6.5, 1.8),
    ("Ucayali", 0.9, 8.5, 2.2),
    ("Apurimac", 0.5, 7.0, 2.0),
    ("Tumbes", 0.5, 4.2, 1.3),
    ("Madre_de_Dios", 0.4, 9.0, 2.4),
    ("Moquegua", 0.5, 3.8, 1.1),
    ("Huancavelica", 0.3, 7.5, 2.0),
    ("Pasco", 0.3, 6.5, 1.8),
    ("Amazonas", 0.3, 7.5, 2.0),
]
ENTREGA = {d: (media, desv) for d, _, media, desv in DEPARTAMENTOS}

# --------------------------------------------------------------- catalogo
# categoria -> peso base, prob. de devolucion, pesos de cantidad (1, 2, 3...), productos
# producto -> (nombre, peso, precio minimo, precio maximo) en soles
CATEGORIAS = {
    "Tecnologia": dict(peso=0.19, devolucion=0.050, cantidad=[90, 7, 2, 1], productos=[
        ("Laptop", 14, 1800, 5200), ("Smartphone", 28, 500, 4200), ("Tablet", 8, 400, 2200),
        ("Audifonos", 16, 40, 900), ("Smart_TV", 9, 900, 4800), ("Monitor", 8, 350, 1800),
        ("Smartwatch", 9, 150, 1500), ("Parlante", 8, 60, 700)]),
    "Moda": dict(peso=0.20, devolucion=0.090, cantidad=[58, 28, 10, 4], productos=[
        ("Zapatillas", 18, 120, 600), ("Polo", 20, 30, 150), ("Jean", 12, 60, 250),
        ("Casaca", 10, 90, 450), ("Vestido", 10, 70, 350), ("Zapatos", 10, 100, 450),
        ("Mochila", 10, 50, 300), ("Reloj", 10, 80, 900)]),
    "Hogar": dict(peso=0.15, devolucion=0.045, cantidad=[72, 18, 7, 3], productos=[
        ("Licuadora", 14, 80, 400), ("Refrigeradora", 8, 1200, 4500), ("Cocina", 6, 700, 2500),
        ("Colchon", 10, 400, 2200), ("Sofa", 6, 800, 3500), ("Lavadora", 7, 1000, 3500),
        ("Microondas", 11, 250, 800), ("Sabanas", 18, 50, 260)]),
    "Supermercado": dict(peso=0.15, devolucion=0.012, cantidad=[30, 28, 20, 12, 6, 4], productos=[
        ("Canasta", 16, 80, 250), ("Aceite", 14, 8, 25), ("Cafe", 12, 15, 60),
        ("Leche_Pack", 14, 20, 60), ("Detergente", 14, 15, 60), ("Snacks_Pack", 12, 15, 70),
        ("Vino", 8, 30, 200), ("Paneton", 10, 15, 50)]),
    "Belleza": dict(peso=0.10, devolucion=0.035, cantidad=[55, 28, 12, 5], productos=[
        ("Perfume", 18, 80, 600), ("Crema_Facial", 16, 30, 260), ("Shampoo", 14, 15, 70),
        ("Maquillaje", 14, 60, 400), ("Secador", 8, 80, 450), ("Plancha_Pelo", 8, 70, 400),
        ("Protector_Solar", 12, 25, 90), ("Kit_Barba", 10, 60, 300)]),
    "Deportes": dict(peso=0.08, devolucion=0.050, cantidad=[70, 20, 7, 3], productos=[
        ("Bicicleta", 8, 500, 3500), ("Mancuernas", 12, 50, 400), ("Running", 18, 150, 700),
        ("Pelota", 16, 30, 180), ("Carpa", 8, 100, 700), ("Bolso_Gym", 14, 40, 200),
        ("Yoga_Mat", 14, 30, 140), ("Casco", 10, 50, 260)]),
    "Juguetes": dict(peso=0.07, devolucion=0.040, cantidad=[60, 25, 10, 5], productos=[
        ("Lego_Set", 18, 80, 900), ("Muneca", 14, 40, 300), ("Carro_RC", 10, 60, 400),
        ("Peluche", 16, 25, 150), ("Rompecabezas", 10, 20, 120), ("Juego_Mesa", 12, 40, 250),
        ("Consola", 6, 1500, 3500), ("Videojuego", 14, 120, 380)]),
    "Libros": dict(peso=0.06, devolucion=0.020, cantidad=[62, 25, 9, 4], productos=[
        ("Novela", 24, 25, 90), ("Libro_Tecnico", 18, 60, 220), ("Libro_Infantil", 18, 20, 80),
        ("Texto_Escolar", 16, 30, 140), ("Manga", 12, 25, 70), ("Comic", 8, 25, 90),
        ("Preuniversitario", 8, 80, 250), ("Autoayuda", 10, 30, 90)]),
}

# Estacionalidad por mes (Dia de la Madre en mayo, inicio de clases en marzo, Navidad, etc.)
ESTACIONALIDAD = {
    "Tecnologia": {7: 1.10, 11: 1.45, 12: 1.30},
    "Moda": {1: 0.90, 5: 1.20, 6: 1.10, 7: 1.20, 12: 1.25},
    "Hogar": {5: 1.15, 11: 1.25, 12: 1.10},
    "Supermercado": {4: 1.05, 12: 1.45},
    "Belleza": {2: 1.20, 5: 1.60, 6: 1.10, 12: 1.10},
    "Deportes": {1: 1.35, 6: 1.05, 7: 1.10, 9: 1.10},
    "Juguetes": {4: 1.20, 11: 1.25, 12: 2.60},
    "Libros": {1: 1.20, 2: 1.90, 3: 1.90, 12: 0.90},
}
# Tendencia por anio (el supermercado online crece mas rapido; moda y libros pierden participacion)
TENDENCIA = {
    "Tecnologia": {2023: 1.00, 2024: 1.10, 2025: 1.22},
    "Moda": {2023: 1.00, 2024: 0.98, 2025: 0.95},
    "Hogar": {2023: 1.00, 2024: 1.03, 2025: 1.06},
    "Supermercado": {2023: 1.00, 2024: 1.25, 2025: 1.55},
    "Belleza": {2023: 1.00, 2024: 1.05, 2025: 1.10},
    "Deportes": {2023: 1.00, 2024: 1.00, 2025: 1.02},
    "Juguetes": {2023: 1.00, 2024: 0.98, 2025: 0.96},
    "Libros": {2023: 1.00, 2024: 0.90, 2025: 0.80},
}
INFLACION = {2023: 1.00, 2024: 1.03, 2025: 1.06}

# ------------------------------------------------------------- calendario
PESO_ANIO = {2023: 0.26, 2024: 0.33, 2025: 0.41}
FACTOR_MES = {1: 0.90, 2: 0.85, 3: 0.95, 4: 1.00, 5: 1.20, 6: 1.05,
              7: 1.10, 8: 0.95, 9: 0.90, 10: 1.00, 11: 1.35, 12: 1.50}
FACTOR_DIA_SEMANA = (1.00, 0.95, 0.95, 1.00, 1.05, 1.05, 1.05)  # lunes .. domingo
PESO_HORA = [2.0, 1.2, 0.7, 0.5, 0.4, 0.5, 1.0, 2.0, 3.5, 4.5, 5.2, 5.6,
             5.8, 5.4, 5.0, 5.0, 5.2, 5.6, 6.2, 7.4, 8.4, 8.8, 7.0, 4.2]


def n_esimo_dia_semana(anio, mes, dia_semana, n):
    """n-esimo dia de la semana (0=lunes .. 6=domingo) de un mes."""
    d = date(anio, mes, 1)
    d += timedelta(days=(dia_semana - d.weekday()) % 7)
    return d + timedelta(weeks=n - 1)


def factor_evento(d):
    """Factor de demanda por fecha especial y si es dia promocional."""
    a = d.year
    black_friday = n_esimo_dia_semana(a, 11, 3, 4) + timedelta(days=1)  # viernes tras el 4.o jueves
    if black_friday <= d <= black_friday + timedelta(days=2):
        return 2.4, True
    if d == black_friday + timedelta(days=3):  # Cyber Monday
        return 2.0, True
    madre = n_esimo_dia_semana(a, 5, 6, 2)  # 2.o domingo de mayo
    if madre - timedelta(days=7) <= d <= madre:
        return 1.7, True
    padre = n_esimo_dia_semana(a, 6, 6, 3)  # 3.er domingo de junio
    if padre - timedelta(days=6) <= d <= padre:
        return 1.4, True
    if date(a, 7, 26) <= d <= date(a, 7, 29):  # Fiestas Patrias
        return 1.25, False
    if date(a, 12, 14) <= d <= date(a, 12, 24):  # campana navidena
        return 1.6, True
    if date(a, 12, 26) <= d <= date(a, 12, 31):
        return 0.8, False
    if d in (date(a, 1, 1), date(a, 12, 25)):
        return 0.55, False
    return 1.0, False


# ---------------------------------------------- pagos, canales, descuentos
PAGO_ANIO = {
    2023: {"Yape": 0.18, "Plin": 0.07, "Credito": 0.33, "Debito": 0.22, "PagoEfectivo": 0.12, "ContraEntrega": 0.08},
    2024: {"Yape": 0.26, "Plin": 0.10, "Credito": 0.28, "Debito": 0.19, "PagoEfectivo": 0.09, "ContraEntrega": 0.08},
    2025: {"Yape": 0.33, "Plin": 0.13, "Credito": 0.24, "Debito": 0.17, "PagoEfectivo": 0.07, "ContraEntrega": 0.06},
}
# En compras grandes casi no se usa billetera digital (limites de Yape/Plin) y sube la tarjeta de credito
AJUSTE_COMPRA_GRANDE = {"Yape": 0.15, "Plin": 0.15, "Credito": 1.8, "Debito": 1.0,
                        "PagoEfectivo": 0.6, "ContraEntrega": 0.5}
UMBRAL_COMPRA_GRANDE_CENTAVOS = 150_000  # S/ 1500.00

CANAL_ANIO = {
    2023: {"Web": 0.50, "App": 0.22, "Marketplace": 0.20, "WhatsApp": 0.08},
    2024: {"Web": 0.44, "App": 0.27, "Marketplace": 0.20, "WhatsApp": 0.09},
    2025: {"Web": 0.38, "App": 0.32, "Marketplace": 0.20, "WhatsApp": 0.10},
}

DESCUENTO_NORMAL = ([0, 5, 10, 15, 20, 30], [52, 12, 16, 9, 8, 3])
DESCUENTO_PROMO = ([0, 10, 15, 20, 30, 40], [14, 18, 18, 22, 20, 8])

PROB_CANCELAR_PAGO = {"PagoEfectivo": 0.13, "ContraEntrega": 0.10}
PROB_CANCELAR_BASE = 0.04


def construir_muestreadores():
    m = {}
    m["departamento"] = Muestreador([d for d, *_ in DEPARTAMENTOS], [p for _, p, *_ in DEPARTAMENTOS])
    m["hora"] = Muestreador(range(24), PESO_HORA)
    m["descuento_normal"] = Muestreador(*DESCUENTO_NORMAL)
    m["descuento_promo"] = Muestreador(*DESCUENTO_PROMO)
    nombres = list(CATEGORIAS)
    for a in PESO_ANIO:
        for mes in range(1, 13):
            pesos = [CATEGORIAS[c]["peso"] * ESTACIONALIDAD[c].get(mes, 1.0) * TENDENCIA[c][a] for c in nombres]
            m[("categoria", a, mes)] = Muestreador(nombres, pesos)
        m[("canal", a)] = Muestreador(list(CANAL_ANIO[a]), list(CANAL_ANIO[a].values()))
        for grande in (False, True):
            pesos = [p * (AJUSTE_COMPRA_GRANDE[k] if grande else 1.0) for k, p in PAGO_ANIO[a].items()]
            m[("pago", a, grande)] = Muestreador(list(PAGO_ANIO[a]), pesos)
    for nombre, info in CATEGORIAS.items():
        prods = info["productos"]
        m[("producto", nombre)] = Muestreador([(n, lo, hi) for n, _, lo, hi in prods], [p for _, p, _, _ in prods])
        m[("cantidad", nombre)] = Muestreador(range(1, len(info["cantidad"]) + 1), info["cantidad"])
    return m


def centavos_precio(precio):
    """Precio de vitrina: termina en .90 (S/ 45.90, S/ 1239.90)."""
    if precio >= 100:
        return (int(precio) // 10) * 1000 + 990
    return int(precio) * 100 + 90


def calificacion(rng, estado, dias):
    if estado == "Entregado":
        if rng.random() > 0.38:
            return ""
        puntaje = 4.55 - 0.17 * max(0, dias - 3) + rng.gauss(0, 0.85)
    else:  # Devuelto
        if rng.random() > 0.55:
            return ""
        puntaje = 2.2 + rng.gauss(0, 1.0)
    return str(min(5, max(1, round(puntaje))))


def generar():
    rng = random.Random(SEMILLA)
    m = construir_muestreadores()

    # Clientes: cada uno vive en un departamento y compra con distinta frecuencia (cola larga acotada)
    depto_cliente = [m["departamento"].sortear(rng) for _ in range(N_CLIENTES)]
    actividad = [min(rng.paretovariate(1.5), 12.0) for _ in range(N_CLIENTES)]
    muestreo_cliente = Muestreador(range(N_CLIENTES), actividad)

    # Calendario ponderado: crecimiento anual, mes, dia de semana y fechas especiales
    dias, pesos_dia, promo = [], [], set()
    d = date(2023, 1, 1)
    while d <= date(2025, 12, 31):
        dias_anio = 366 if d.year % 4 == 0 else 365
        factor, es_promo = factor_evento(d)
        pesos_dia.append(PESO_ANIO[d.year] / dias_anio * FACTOR_MES[d.month] * FACTOR_DIA_SEMANA[d.weekday()] * factor)
        dias.append(d)
        if es_promo:
            promo.add(d)
        d += timedelta(days=1)
    fechas = Muestreador(dias, pesos_dia)

    pares = sorted((fechas.sortear(rng), m["hora"].sortear(rng)) for _ in range(N_PEDIDOS))

    filas = []
    for i, (fecha, hora) in enumerate(pares):
        anio, mes = fecha.year, fecha.month
        es_promo = fecha in promo
        idx_cliente = muestreo_cliente.sortear(rng)
        depto = depto_cliente[idx_cliente]

        categoria = m[("categoria", anio, mes)].sortear(rng)
        info = CATEGORIAS[categoria]
        producto, p_min, p_max = m[("producto", categoria)].sortear(rng)
        precio = rng.triangular(p_min, p_max, p_min + (p_max - p_min) * 0.25) * INFLACION[anio]
        precio_c = centavos_precio(precio)

        descuento = (m["descuento_promo"] if es_promo else m["descuento_normal"]).sortear(rng)
        cantidad = m[("cantidad", categoria)].sortear(rng)
        if descuento >= 20 and cantidad < len(info["cantidad"]) and rng.random() < 0.12:
            cantidad += 1
        monto_c = (precio_c * cantidad * (100 - descuento) + 50) // 100  # redondeo half-up a centavos

        pago = m[("pago", anio, monto_c >= UMBRAL_COMPRA_GRANDE_CENTAVOS)].sortear(rng)
        canal = m[("canal", anio)].sortear(rng)

        p_cancelar = PROB_CANCELAR_PAGO.get(pago, PROB_CANCELAR_BASE) + (0.02 if canal == "WhatsApp" else 0.0)
        u = rng.random()
        if u < p_cancelar:
            estado = "Cancelado"
        elif u < p_cancelar + info["devolucion"]:
            estado = "Devuelto"
        else:
            estado = "Entregado"

        if estado == "Cancelado":
            dias_entrega, calif = "", ""
        else:
            media, desv = ENTREGA[depto]
            dias_n = max(1, int(round(rng.gauss(media, desv))))
            dias_n += (1 if canal == "Marketplace" else 0) + (1 if es_promo else 0)
            dias_n = min(dias_n, 25)
            dias_entrega, calif = str(dias_n), calificacion(rng, estado, dias_n)

        filas.append(",".join((
            str(PRIMER_ID_PEDIDO + i), fecha.isoformat(), str(hora),
            str(PRIMER_ID_CLIENTE + idx_cliente), depto, categoria, producto,
            "{}.{:02d}".format(precio_c // 100, precio_c % 100), str(cantidad), str(descuento),
            "{}.{:02d}".format(monto_c // 100, monto_c % 100), pago, canal, estado,
            dias_entrega, calif,
        )))
    return filas


def main():
    filas = generar()
    for fila in filas:
        assert fila.count(",") == 15 and fila.isascii(), fila
    with open(SALIDA, "w", encoding="utf-8", newline="\n") as f:
        f.write(ENCABEZADO + "\n")
        f.write("\n".join(filas) + "\n")
    mb = SALIDA.stat().st_size / 1_000_000
    print("OK: {} pedidos -> {} ({:.1f} MB)".format(len(filas), SALIDA, mb))
    return 0


if __name__ == "__main__":
    sys.exit(main())
