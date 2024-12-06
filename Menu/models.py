from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Grade(models.Model):
    name = models.CharField(max_length=50, unique=True)  # Номи синф (масалан, "10A")
    description = models.TextField(blank=True, null=True)  # Тавсифи иловагӣ (ихтиёрӣ)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True, related_name="students")  # Алоқаманд бо Grade
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_actives = models.BooleanField(default=False)  # Фаъолият (True/False)

    def __str__(self):
        return f"{self.username} ({self.grade.name if self.grade else 'No Grade'})"


class Wallet(models.Model):
    student = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="wallet")  # Пайванд бо талабагӣ
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Баланс (маблағи мавҷуда)

    def __str__(self):
        return f"Wallet of {self.student.username} - {self.balance} сомонӣ"

    def add_balance(self, amount):
        self.balance += amount
        self.save()

    def subtract_balance(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.save()
        else:
            raise ValueError("Маблағи кофӣ дар ҳисоб нест!")

    def has_enough_balance(self, amount):
        return self.balance >= amount


# Сигнал барои назорати Wallet ва навсозии is_actives
@receiver(post_save, sender=Wallet)
def check_wallet_balance(sender, instance, **kwargs):
    # Пас аз сабт, ҳолати Wallet-ро санҷида, is_actives-ро навсозӣ мекунем
    if instance.balance == 0:
        instance.student.is_actives = True
        instance.student.save()
    elif instance.balance != 0:
        instance.student.is_actives = False
        instance.student.save()
        


class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Нархи китоб
    stock = models.PositiveIntegerField(default=0)  # Шумораи мавҷуда
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE ,null=True,blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def reduce_stock(self, quantity):
        if self.stock >= quantity:
            self.stock -= quantity
            self.is_available = self.stock > 0
            self.save()
        else:
            raise ValueError("Китоб кофӣ нест дар саҳом!")

    def is_in_stock(self):
        return self.stock > 0


class Purchase(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="purchases")  # Харидор
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="purchases")  # Китоб
    purchase_date = models.DateTimeField(auto_now_add=True)  # Таърихи харид
    quantity = models.PositiveIntegerField(default=1)  # Шумораи китоб
    price_paid = models.DecimalField(max_digits=10, decimal_places=2)  # Нархи пардохтшуда
    is_paid = models.BooleanField(default=False)  # Оё пардохт шудааст ё не

    def __str__(self):
        return f"{self.student.username} - {self.book.title} ({'Paid' if self.is_paid else 'Not Paid'})"

    def make_purchase(self):
        total_price = self.quantity * self.book.price

        if self.book.stock < self.quantity:
            raise ValueError("Китоб кофӣ нест дар саҳом!")
        
        self.book.reduce_stock(self.quantity)

        self.student.wallet.add_balance(total_price)
        self.price_paid = total_price
        self.save()

    def pay(self):
        if self.is_paid:
            raise ValueError("Харид аллакай пардохт шудааст!")
        
        if not self.student.wallet.has_enough_balance(self.price_paid):
            raise ValueError("Маблағи кофӣ дар ҳисоби талабагӣ нест!")
        
        self.student.wallet.subtract_balance(self.price_paid)
        self.is_paid = True
        self.save()

class Payment(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="payments")  
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name="payments")  
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)  # Amount paid
    payment_date = models.DateTimeField(auto_now_add=True)  # Payment date
    payment_method = models.CharField(max_length=50, choices=[('cash', 'Cash'), ('card', 'Card'), ('online', 'Online')])  # Payment method
    status = models.CharField(max_length=20, choices=[('completed', 'Completed'), ('failed', 'Failed'), ('pending', 'Pending')], default='pending')  

    def __str__(self):
        return f"Payment of {self.amount_paid} by {self.student.username} for {self.purchase.book.title} on {self.payment_date}"

    def save(self, *args, **kwargs):
        wallet = self.student.wallet  
        if wallet.balance >= self.amount_paid:
            wallet.subtract_balance(self.amount_paid)
            self.status = 'completed'  
            super().save(*args, **kwargs)  
        else:
            raise ValueError("Insufficient funds in the wallet")

def create_payment(purchase):
    if purchase.is_paid:  
        payment = Payment.objects.create(
            student=purchase.student, 
            purchase=purchase, 
            amount_paid=purchase.price_paid, 
            payment_method='card',  
            status='completed'
        )
        return payment
    else:
        raise ValueError("Харид то ҳол пардохт нашудааст!")
