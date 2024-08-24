from rest_framework import serializers

from zola.models import Item
from competency.serializers import CompetencySerializer, CompetencyListSerializer


class ItemLiSerializer(serializers.ModelSerializer):
    suborg = serializers.StringRelatedField()
    class Meta:
        model = Item
        fields = ['id','item_name', 'thumbnail', 'category', 'scenario_type', 'item_gender', 
                  'role', 'item_type', 'level', 'suborg', 'item_answercount','item_video', 'expert', 'item_background', 'item_description']

class ItemListSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'item_emotion','coming_across_as']

class ItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'item_name', 'item_description', 'category', 'thumbnail', 'item_gender', 
                  'role', 'level', 'expert', 'competencys', 'is_live', 'is_approved', 'item_background']

class ItemSerializer(serializers.ModelSerializer):
    competencys = CompetencySerializer(many=True)

    class Meta:
        model = Item
        depth = 1
        fields = '__all__'   
        
class ItemUserSerializer(serializers.ModelSerializer):
    competencys = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    
    def get_competencys(self, obj):
        competencies = obj.competencys.all()
        return CompetencyListSerializer(competencies, many=True).data
    
    def get_role(self, obj):
        role = {}
        if hasattr(obj, 'role') and obj.role:
            role['id'] = getattr(obj.role, 'id', None)
            role['role_name'] = getattr(obj.role, 'name', None)
        return role

    
    class Meta:
        model = Item
        fields = ['id', 'item_name', 'item_answer', 'category', 'thumbnail', 'item_type', 'role',
                  'scenario_type', 'competencys', 'is_live', 'is_approved', 'level', 'expert', 'item_video',
                  'item_background', 'item_answercount', 'item_description']

class ItemEmotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = [ 'item_answer', 'coming_across_as']
        
class ItemRecommendSerializer(serializers.ModelSerializer):
    competencys = CompetencySerializer(many=True)

    class Meta:
        model = Item
        depth = 1
        fields = ['coming_across_as','competencys']   
