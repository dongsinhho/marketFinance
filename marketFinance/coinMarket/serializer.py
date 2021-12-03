from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username" ,"email", "password"]

    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username","email", "created"]


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username",]
    def update(self, instance, validated_data):
        
        instance.username = validated_data.get('username',instance.username)
        if validated_data.get('password'):
            print(validated_data.get('password'))
            instance.password = make_password(validated_data.get('password'))
        #instance.password = make_password(validated_data.get('password', instance.password))
        instance.save()
        return instance


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]
    username = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)


class CoinInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeCoin
        fields = ["pk", "name", "icon", "ranked"]

class CoinDataSerializer(serializers.ModelSerializer):
    typeCoin = serializers.SlugRelatedField(read_only=True, slug_field="name")
    class Meta:
        model = Coin
        fields = ["time", "typeCoin", "value"]


class NotifySerializer(serializers.ModelSerializer):
    typeCoin = serializers.SlugRelatedField(read_only=True, slug_field="name")
    class Meta:
        model = Notify
        fields = ["pk","typeCoin","max_threshold","min_threshold", "isNotify", "created"]
    

class CreateNotifySerializer(serializers.ModelSerializer):   
    typeCoin = serializers.RelatedField(source='TypeCoin', read_only=True)
    owner = serializers.RelatedField(source='User', read_only=True)
    class Meta:
        model = Notify
        fields = ["owner", "typeCoin", "max_threshold", "min_threshold"] 

    def create(self, validated_data):
        try:
            user = User.objects.get(id=validated_data.get('userid'))
            typecoin = TypeCoin.objects.get(id=validated_data.get('typecoin'))
            checkNotify = Notify.objects.filter(owner=user,isNotify=False, typeCoin=typecoin)
            if checkNotify:
                return {"status": False, "message": "You have created notification about this coin before, delete before creating new" }
            validated_data['owner'] = user
            validated_data['typeCoin'] = typecoin
            validated_data['max_threshold'] = validated_data.get('max_threshold')
            validated_data['min_threshold'] = validated_data.get('min_threshold')
            notify = Notify.objects.create(owner=validated_data['owner'], typeCoin=validated_data['typeCoin'],max_threshold=validated_data['max_threshold'],min_threshold=validated_data['min_threshold'])
            notify.save()
            return {"status": True, "message": "Create successful !" }
        except:
            return {"status": False, "message": "Validated error, check your data !" }


class GetFavoriteCoinSerializer(serializers.ModelSerializer):
    coin = serializers.SlugRelatedField(read_only=True, slug_field="name")
    class Meta:
        model = FavoriteCoin
        fields = ["coin"]

class FavoriteCoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteCoin
        fields = ["coin", "user"]