#Oprettelse af ny custom URL converter med typen float. kilde: https://docs.djangoproject.com/en/5.0/topics/http/urls/
class FloatUrlParameterConverter:
    regex = '[0-9]+\.?[0-9]+'  # Regex mønsteret der matcher en float-værdi

    def to_python(self, value):
        return float(value)  # Konverterer værdien til en float

    def to_url(self, value):
        # Konverterer værdien til en streng før den inkluderes i en URL
        return str(value)
