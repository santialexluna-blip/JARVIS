import datetime as dt
import platform
import psutil

class BasicTools:
    def time(self):
        now = dt.datetime.now().strftime("%H:%M:%S")
        return f"Son las {now}."

    def system_info(self):
        ram = psutil.virtual_memory()
        return (
            f"Sistema: {platform.system()} {platform.release()} | "
            f"CPU: {psutil.cpu_percent(interval=0.2):.0f}% | "
            f"RAM: {ram.percent:.0f}%"
        )

    def date(self):
        days = ("lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo")
        months = (
            "enero", "febrero", "marzo", "abril", "mayo", "junio",
            "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
        )
        today = dt.date.today()
        return f"Hoy es {days[today.weekday()]}, {today.day} de {months[today.month - 1]} de {today.year}."
