from celery import shared_task
import datetime
from recsystem.settings import updated_model_data
from .models import RecommendationData, RecommendationModel, Category, Client


@shared_task
def update_recommendation_model():
    model = RecommendationModel.objects.get(name='version1')
    model_data, f = updated_model_data()
    for i in model_data.keys():
        category = Category.objects.get(id=i)
        if model.data.filter(category=category).exists():
            data = RecommendationData.objects.get(category=category)
            for client_id in model_data[i]:
                client = Client.objects.get(id=client_id)
                data.clients.add(client)
            data.save()
        else:
            data = RecommendationData.objects.create(category=category)
            for client_id in model_data[i]:
                client = Client.objects.get(id=client_id)
                data.clients.add(client)
            data.save()
            model.data.add(data)
        model.last_update = datetime.datetime.now()
        model.f_score = f
        model.save()
    result = {}
    print(model.data.values('category', 'clients'))
    for i in model.data.values('category', 'clients'):
        result[i['category']] = i['clients']
    return result
