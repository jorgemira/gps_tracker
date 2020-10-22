from django.db import models


class Location(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    datetime = models.DateTimeField(db_index=True, unique=True)

    def __str__(self):
        return (f"Lat: {self.latitude}, "
                f"Long: {self.longitude} "
                f"Time: {self.datetime.strftime('%Y-%m-%d %H:%M:%S')}")
