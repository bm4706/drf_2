from rest_framework import serializers
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        
    def create(self, validated_data):
        user =  super().create(validated_data)
        password = user.password
        user.set_password(password) # 비밀번호 해싱
        user.save() # db에 저장
        return user
    
    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        password = user.password
        user.set_password(password) 
        user.save() 
        return user