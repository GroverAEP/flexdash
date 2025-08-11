from datetime import datetime, timedelta
from collections import Counter

from threading import Lock
from statistics import mean


        


class AnalyticsCustomers:
    def __init__(self, customers=None):
        # customers ejemplo: [{"id": 1, "type": "nuevo"}, {"id": 2, "type": "recurrente"}]
        self.customers = customers or []

    def add_customer(self, customer_id, customer_type):
        self.customers.append({
            "id": customer_id,
            "type": customer_type
        })

    @property
    def total_customers(self):
        return len(self.customers)

    @property
    def new_customers(self):
        return len([c for c in self.customers if c["type"] == "nuevo"])

    @property
    def recurring_customers(self):
        return len([c for c in self.customers if c["type"] == "recurrente"])


class BusinessAnalytics:
    def __init__(self, orders=list, customers=list, business_hours=tuple):
        """
        orders: lista de pedidos (diccionario con estado, total, fecha, cliente_id)
        customers: lista de clientes (diccionario con fecha_registro, id_cliente, num_ordenes)
        business_hours: horario de apertura y cierre (tupla: hora_inicio, hora_fin)
        """
        self.orders = orders
        self.customers = customers
        self.business_hours = business_hours

    # =========================
    # ESTADO DEL NEGOCIO
    # =========================
    def business_status(self):
        now = datetime.now()
        start, end = self.business_hours

        status = "Abierto" if start <= now.hour < end else "Cerrado"
        reason = None

        if status == "Cerrado":
            if now.hour < start:
                reason = "Aún no abre"
            else:
                reason = "Horario de cierre alcanzado"

        return {
            "status": status,
            "hora_actual": now.strftime("%H:%M"),
            "horario_apertura": f"{start}:00",
            "horario_cierre": f"{end}:00",
            "razon": reason
        }

    # =========================
    # GANANCIAS
    # =========================
    def earnings(self):
        now = datetime.now()

        def sum_by_filter(start_date):
            return sum(order["total"] for order in self.orders if order["fecha"] >= start_date)

        return {
            "diario": sum_by_filter(now.replace(hour=0, minute=0, second=0)),
            "semanal": sum_by_filter(now - timedelta(days=7)),
            "mensual": sum_by_filter(now - timedelta(days=30)),
            "anual": sum_by_filter(now - timedelta(days=365)),
            "promedio_ticket": round(sum(order["total"] for order in self.orders) / max(len(self.orders), 1), 2)
        }

    # =========================
    # CLIENTES
    # =========================
    def customer_stats(self):
        now = datetime.now()

        nuevos = [c for c in self.customers if c["fecha_registro"] >= now - timedelta(days=30)]
        recurrentes = [c for c in self.customers if c["num_ordenes"] > 1]
        inactivos = [c for c in self.customers if c["num_ordenes"] == 0]

        return {
            "nuevos_mes": len(nuevos),
            "recurrentes": len(recurrentes),
            "totales": len(self.customers),
            "inactivos": len(inactivos)
        }

    # =========================
    # EXTRAS
    # =========================
    def top_products(self, n=5):
        products = []
        for order in self.orders:
            products.extend(order.get("productos", []))
        return Counter(products).most_common(n)

    def orders_per_hour(self):
        counter = Counter(order["fecha"].hour for order in self.orders)
        return dict(sorted(counter.items()))
