# 🍔 FoodOrder API

API REST para gestión de restaurante — pedidos y platos — construida con **Django + Django REST Framework**.

---

## 📋 Descripción

Sistema backend para administrar el menú y los pedidos de un restaurante.  
Permite crear, listar, editar y eliminar platos y pedidos, con relación Many-to-Many entre ambos.

---

## 🛠 Tecnologías

| Tecnología | Versión |
|---|---|
| Python | 3.10+ |
| Django | 4.x |
| Django REST Framework | 3.x |
| django-filter | 23.x |
| SQLite | (incluido) |

---

## 🚀 Instrucciones para ejecutar

```bash
# 1. Clonar el repositorio
git clone https://github.com/TU_USUARIO/foodorder_api.git
cd foodorder_api

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# 3. Instalar dependencias
pip install django djangorestframework django-filter

# 4. Aplicar migraciones
python manage.py migrate

# 5. (Opcional) Cargar datos de prueba
python manage.py shell < seed_data.py

# 6. Ejecutar servidor
python manage.py runserver
```

La API estará disponible en: `http://localhost:8000/api/`

---

## 📡 Endpoints disponibles

### 🍽 Platos (`/api/platos/`)

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/api/platos/` | Lista todos los platos |
| POST | `/api/platos/` | Crea un nuevo plato |
| GET | `/api/platos/{id}/` | Detalle de un plato |
| PUT | `/api/platos/{id}/` | Actualiza un plato completo |
| PATCH | `/api/platos/{id}/` | Actualiza parcialmente |
| DELETE | `/api/platos/{id}/` | Elimina un plato |
| GET | `/api/platos/?search=lomo` | Busca por nombre o categoría |

### 📦 Pedidos (`/api/pedidos/`)

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/api/pedidos/` | Lista todos los pedidos (con platos relacionados) |
| POST | `/api/pedidos/` | Crea un nuevo pedido |
| GET | `/api/pedidos/{id}/` | Detalle con platos incluidos |
| PUT | `/api/pedidos/{id}/` | Actualiza un pedido |
| PATCH | `/api/pedidos/{id}/` | Actualiza parcialmente |
| DELETE | `/api/pedidos/{id}/` | Elimina un pedido |
| GET | `/api/pedidos/?search=juan` | Busca por cliente o estado |
| POST | `/api/pedidos/{id}/cambiar-estado/` | Cambia el estado del pedido |

---

## 💡 Ejemplos de uso (cURL)

### Listar todos los platos
```bash
curl http://localhost:8000/api/platos/
```

### Crear un plato
```bash
curl -X POST http://localhost:8000/api/platos/ \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Lomo Saltado",
    "precio": 32.50,
    "categoria": "plato_principal",
    "descripcion": "Clásico peruano"
  }'
```

### Crear un pedido con platos
```bash
curl -X POST http://localhost:8000/api/pedidos/ \
  -H "Content-Type: application/json" \
  -d '{
    "cliente": "Ana Torres",
    "estado": "pendiente",
    "items": [
      {"plato": 1, "cantidad": 2},
      {"plato": 3, "cantidad": 1}
    ]
  }'
```

**Respuesta:**
```json
{
  "id": 3,
  "cliente": "Ana Torres",
  "fecha": "2024-05-09T20:00:00Z",
  "estado": "pendiente",
  "estado_display": "Pendiente",
  "total": "73.00",
  "detalles": [
    {"plato": 1, "plato_nombre": "Lomo Saltado", "plato_precio": "32.50", "cantidad": 2, "subtotal": 65.0},
    {"plato": 3, "plato_nombre": "Inca Kola", "plato_precio": "8.00", "cantidad": 1, "subtotal": 8.0}
  ],
  "platos_resumen": ["2x Lomo Saltado", "1x Inca Kola"]
}
```

### Buscar pedidos por cliente
```bash
curl "http://localhost:8000/api/pedidos/?search=Ana"
```

### Editar estado de un pedido
```bash
curl -X PATCH http://localhost:8000/api/pedidos/3/ \
  -H "Content-Type: application/json" \
  -d '{"estado": "entregado"}'
```

### Eliminar un plato
```bash
curl -X DELETE http://localhost:8000/api/platos/1/
# Respuesta: {"mensaje": "Plato 'Lomo Saltado' eliminado correctamente."}
```

### Filtrar platos por categoría
```bash
curl "http://localhost:8000/api/platos/?categoria=postre"
```

---

## 🗂 Estructura del proyecto

```
foodorder_api/
├── foodorder_api/
│   ├── settings.py
│   └── urls.py
├── restaurant/
│   ├── models.py       # Plato, Pedido, DetallePedido
│   ├── serializers.py  # PlatoSerializer, PedidoSerializer
│   ├── views.py        # PlatoViewSet, PedidoViewSet
│   └── urls.py
├── manage.py
└── README.md
```

---

## 🌟 Funcionalidades extras

- `platos_resumen`: campo personalizado en la respuesta de Pedidos que muestra los nombres de los platos directamente (ej: `"2x Lomo Saltado"`)
- `estado_display` y `categoria_display`: versiones legibles de los campos con choices
- Cálculo automático del `total` al crear/actualizar un pedido
- Endpoint adicional `POST /api/pedidos/{id}/cambiar-estado/` para gestionar el flujo del pedido
