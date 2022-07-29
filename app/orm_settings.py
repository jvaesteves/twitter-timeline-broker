TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": "localhost",
                "port": "5432",
                "user": "tortoise",
                "password": "qwerty123",
                "database": "tweets",
            },
        }
    },
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],
            "default_connection": "default",
        }
    },
}
