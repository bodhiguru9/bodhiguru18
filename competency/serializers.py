from rest_framework import serializers
from competency.models import Competency, Sub_Competency, Senti


from words.serializers import PowerWordsSerializer, NegativeWordsSerializer, EmotionWordsSerializer

"""
class Sub_CompetencySerializer(serializers.ModelSerializer):
    subcompetency_name = serializers.JSONField()
    class Meta:
        model = Sub_Competency1
        fields = '__all__'

"""

class CompetencyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competency
        fields = ['id', 'competency_name']
        

class Sub_CompetencySerializer(serializers.ModelSerializer):
    power_words = serializers.SerializerMethodField()
    negative_words = serializers.SerializerMethodField()
    emotion_words = serializers.SerializerMethodField()
    
    def get_power_words(self, obj):
        power_words = obj.power_words.all()
        return PowerWordsSerializer(power_words, many=True).data
    
    def get_negative_words(self, obj):
        negative_words = obj.negative_words.all()
        return NegativeWordsSerializer(negative_words, many=True).data
    
    def get_emotion_words(self, obj):
        emotion_words = obj.emotion_words.all()
        return EmotionWordsSerializer(emotion_words, many=True).data
    
    class Meta:
        model = Sub_Competency
        fields = '__all__'
        
class SentiSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Senti
        fields = '__all__'


class CompetencySerializer(serializers.ModelSerializer):
    sub_compentency = serializers.SerializerMethodField()

    def get_sub_compentency(self, obj):
        sub_compentency = obj.sub_competency.all()
        return Sub_CompetencySerializer(sub_compentency, many=True).data

    def get_senti(self, obj):
        senti = obj.senti.all()
        return SentiSerializer(senti, many=True).data    
    
    class Meta:
        model = Competency
        fields = ['id', 'competency_name', 'sub_compentency', 'get_senti_as_string']    