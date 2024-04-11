from django.apps import AppConfig


class StocksConfig(AppConfig):
    # Definerer en ny klasse kaldet StocksConfig, som arver fra AppConfig.

    default_auto_field = "django.db.models.BigAutoField"
    # Angiver det automatiske felt, der skal bruges som primær nøgle i modellen

    name = "stocks"
    # Angiver navnet på denne app
