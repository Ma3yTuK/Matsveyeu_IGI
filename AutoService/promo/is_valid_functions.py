from polls import models
from django import forms

def promo_1010(order):
    return len(order.parts.all()) > 1