from . import admin, auth, cart, incidents, orders, products, system

all_routers = [auth.router, products.router, cart.router, orders.router, admin.router, incidents.router, system.router]
