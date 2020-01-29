from django.db import models

class Bucketlist(models.Model):
    """This class represents the bucketlist model."""
    name = models.CharField(max_length=255, blank=False, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.name)

class Vsl(models.Model):
    """This class represents the Vsl model."""
    vessel = models.CharField(max_length=255, blank=False, unique=True)
    speedB = models.DecimalField(max_digits=4,decimal_places=1,blank=True, null=True)
    consB = models.DecimalField(max_digits=4,decimal_places=1,blank=True, null=True)
    speedL = models.DecimalField(max_digits=4,decimal_places=1,blank=True, null=True)
    consL = models.DecimalField(max_digits=4,decimal_places=1,blank=True, null=True)
    ifo_port = models.DecimalField(max_digits=4,decimal_places=1,blank=True, null=True)
    aux_steam = models.DecimalField(max_digits=4,decimal_places=1,blank=True, null=True)
    aux_port = models.DecimalField(max_digits=4,decimal_places=1,blank=True, null=True)

    # speedB = models.FloatField(default=0)
    # consB = models.FloatField(default=0)
    # speedL = models.FloatField(default=0)
    # consL = models.FloatField(default=0)
    # ifo_port = models.FloatField(default=0)
    # aux_steam = models.FloatField(default=0)
    # aux_port = models.FloatField(default=0)


    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.vessel)