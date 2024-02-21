from django.db import models
from Category.models import Category
from django.urls import reverse




class Product (models.Model):
    product_name=models.CharField( max_length=200,blank=True)
    slug=models.SlugField(max_length=200,blank=True)
    price= models.DecimalField(max_digits=10, decimal_places=2)
    cat_image=models.ImageField(null=True,blank=True)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    description=models.TextField(max_length=500)
    old_price= models.DecimalField(max_digits=10, decimal_places=2)
    stock=models.IntegerField()
    is_available=models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name
    def get_url(self):
        return reverse('product_detail',args=[self.category.slug,self.slug])
    @property
    def imageURL(self) :
        try :
            url=self.cat_image.url
        except :
            url=''
        return url
class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager,self).filter(variation_category='color',Is_active=True)
    def sizes(self):
        return super(VariationManager,self).filter(variation_category='size',Is_active=True)

variation_category_choice =(
    ('color', 'color'), 
  ('size', 'size'),
)
class Variation(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category= models.CharField(max_length=100, choices=variation_category_choice)
    variation_value=models.CharField( max_length=100)
    Is_active=models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now=True)
    objects=VariationManager()

    


    def __str__(self):
        return self.variation_value


