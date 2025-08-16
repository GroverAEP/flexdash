from abc import ABC, abstractmethod

class OrderRepository(ABC):
    @abstractmethod
    def get_all_orders(self):
        """Debe devolver una lista de órdenes."""
        pass