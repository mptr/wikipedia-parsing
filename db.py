from orator import DatabaseManager, Schema

databases = {
    'postgres': {
        'driver': 'postgres',
        'host': 'localhost',
        'database': 'postgres',
        'user': 'postgres',
        'password': 'changeme',
        'prefix': ''
    }
}

db = DatabaseManager(databases)
schema = Schema(db)
