from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . models import employees
from . serializers import employeesSerializer
from quickstart.newmsg import *
from quickstart.hello import *

class employeelist(APIView):
    def get(self,request):
        employees1=employees.objects.all()
        employees1 = serializers.serialize('python',employees1)

        main123()
        main456()


        #return HttpResponse(employees1, content_type="application/json")
        """
        serializer= employeesSerializer(employees1,many= True)
        json_serializer = serializers.serialize('json', employees1)
        response = HttpResponse(json_serializer, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename=export.json'
        """
        """
        with open("file.json", "w") as out:
             
             #employees1 = serializers.serialize('json', employees.objects.all())
             #out.write(employees1)
             json_serializer = serializers.serialize('json',employees1)
             response = HttpResponse(json_serializer,content_type='application/json')
             response['Content-Disposition']='attachment; filename=export.json'
             #json_serializer = serializers.get_serializer('json')()
            #json_serializer.serialize(employees.objects.all(), stream=out)
        """
        #return Response(serializer.data)
        return JsonResponse(employees1,safe=False)





    def post(self):
        pass

# Create your views here.
