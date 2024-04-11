class FloatUrlParameterConverter:
    regex = '[0-9]+\.?[0-9]+'  # Regex mønsteret der matcher en float-værdi

    def to_python(self, value):
        return float(value)  # Konverterer værdien til en float

    def to_url(self, value):
        # Konverterer værdien til en streng før den inkluderes i en URL
        return str(value)
