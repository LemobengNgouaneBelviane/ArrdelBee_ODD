from django.db import models

class Region(models.Model):
    name = models.CharField(max_length=120, unique=True)
    code = models.CharField(max_length=20, blank=True, default="")

    def __str__(self):
        return self.name


class Department(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="departments")
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=20, blank=True, default="")

    class Meta:
        unique_together = ("region", "name")

    def __str__(self):
        return f"{self.name} ({self.region.name})"


class Commune(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="communes")
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=20, blank=True, default="")

    class Meta:
        unique_together = ("department", "name")

    def __str__(self):
        return f"{self.name} ({self.department.name})"
