from django.db import models
from django.utils.timezone import now


# Create your models here.

class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30, default='NoName' )
    des = models.CharField(null=True, max_length=200,)

    def __str__(self):
        return name + ' ' + des
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object


class CarModel(models.Model):
    name = models.CharField(max_length=50)
    dealer_id = models.IntegerField()
    carmake= models.ForeignKey('CarMake', on_delete=models.CASCADE)
    year = models.DateField()

    SEDAN = 'SEDAN'
    SUV = 'SUV'
    WAGON = 'WAGON'
    cartype=[
        (SEDAN, 'Sedan'),
        (SUV, 'Suv'),
        (WAGON,'Wagon'),
    ]
    type = models.CharField(max_length=20, choices=cartype, default=SEDAN)

    def __str__(self):
        return f"{self.name} ({self.carmake.name}, {self.year.year})"
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
