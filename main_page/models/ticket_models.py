from django.db import models

class TicketSeller(models.Model):
    seller_name = models.CharField(max_length=15, primary_key=True)
    gform_url = models.URLField(max_length=50, db_column='Google Form url')

    def __str__(self):
        return self.seller_name