from app import app, db
from app.models import Supply, Delivery

def check_database():
    with app.app_context():
        print("\n=== Estado de Suministros ===")
        supplies = Supply.query.all()
        for supply in supplies:
            print(f"ID: {supply.id}")
            print(f"Nombre: {supply.name}")
            print(f"Cantidad: {supply.quantity}")
            print("-" * 30)

        print("\n=== Últimas Entregas ===")
        deliveries = Delivery.query.order_by(Delivery.id.desc()).limit(5).all()
        for delivery in deliveries:
            print(f"ID: {delivery.id}")
            print(f"Suministro ID: {delivery.supply_id}")
            print(f"Cantidad entregada: {delivery.quantity}")
            print(f"Fecha: {delivery.date}")
            print("-" * 30)

if __name__ == "__main__":
    check_database() 