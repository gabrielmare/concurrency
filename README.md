# Concurrencia en Python — Comparativa práctica

Implementación comparativa de los cuatro modelos de concurrencia en Python aplicados a un caso real: descarga de precios de cierre de tickers desde la API de Binance.

El mismo problema, cuatro soluciones distintas. Cada script mide su propio tiempo de ejecución para comparar performance directamente.

---

## Scripts

| Archivo | Modelo | Cuándo usarlo |
|---|---|---|
| `1_sync.py` | Secuencial | Baseline de referencia, tareas simples |
| `2_multithreading.py` | ThreadPoolExecutor | I/O bound — requests, APIs, archivos |
| `3_multiprocessing.py` | ProcessPoolExecutor | CPU bound — cálculos pesados, transformaciones |
| `4_asyncio.py` | AsyncIO | Muchas requests HTTP concurrentes |

---

## Caso de uso

Cada script descarga precios de cierre de N tickers de Binance y mide cuánto tarda.
La diferencia de tiempos entre el modo síncrono y los modos concurrentes ilustra en qué escenarios vale la pena paralelizar.

```
Sync:           ~45 seg
Multithreading: ~6 seg   ← ideal para este caso (I/O bound)
Multiprocessing: ~8 seg  ← overhead de procesos supera el beneficio
AsyncIO:        ~5 seg   ← óptimo para muchas requests simultáneas
```

> Nota: los tiempos varían según conexión y cantidad de tickers configurada en `general.py`.

---

## Estructura

```
├── 1_sync.py               # baseline secuencial
├── 2_multithreading.py     # ThreadPoolExecutor
├── 3_multiprocessing.py    # ProcessPoolExecutor
├── 4_asyncio.py            # asyncio + aiohttp
├── business/               # lógica de negocio (llamadas a Binance API)
├── model/                  # modelos de datos (ClosingPrices)
├── exceptions/             # excepciones custom
├── log/                    # archivos de log generados en ejecución
└── general.py              # configuración global (LIMIT_TICKERS, logging)
```

---

## Cómo ejecutar

```bash
pip install uv
uv sync
python 1_sync.py        # secuencial
python 2_multithreading.py
python 3_multiprocessing.py
python 4_asyncio.py
```

---

## Stack

- Python 3.12+
- `concurrent.futures` — ThreadPoolExecutor / ProcessPoolExecutor
- `asyncio` + `aiohttp` — modelo async
- Binance API — fuente de datos de mercado
