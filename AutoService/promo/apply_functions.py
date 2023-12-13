from polls import models

def promo_1010(order):
    discount = 0.1
    result = 0

    for job in models.Job.objects.filter(order=order.id):
        result += job.service.price * discount
    for part in order.parts.all():
        result += part.price * discount

    return result