import  django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
  user = django_filters.NumberFilter(field_name = 'sender__id')
  start = django_filters.DateTimeFilter(field_name = 'Timestamp' , lookup_exp='gte')
  end = django_filters.DateTimeFilter(field_name = 'Timestamp' , lookup_exp='lte')
  class Meta:
    model = Message
    fields = ['user','start','end']
    
