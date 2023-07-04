from django.db import models



class Password(models.Model):
    password = models.CharField(max_length=25)
    
    
    def __str__(self) -> str:
        return f"{self.id}"
    
    