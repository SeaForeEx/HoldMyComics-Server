# from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from holdmycomicsapi.models import User

class UserView(ViewSet):
    """HMC Users View"""

    def create(self, request):
        """CREATE User"""
        
        user = User.objects.create(
            user_name=request.data["userName"],
            store_name=request.data["storeName"],
            email=request.data["email"],
            uid=request.data["uid"],
        )
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk):
        """GET Single User"""
        
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
    def destroy(self, request, pk):
        """DELETE User"""
        
        user = User.objects.get(pk=pk)
        user.delete()
        return Response('User Deleted', status=status.HTTP_204_NO_CONTENT)

class UserSerializer(serializers.ModelSerializer):
    """JSON Serializer for Users"""
      
    class Meta:
        model = User
        fields = ('id', 'user_name', 'store_name', 'email', 'uid')
