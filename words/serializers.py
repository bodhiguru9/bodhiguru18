from rest_framework import serializers

from words.models import Words, PowerWords, NegativeWords, EmotionWords

class WordSerializer(serializers.ModelSerializer):
    word_name = serializers.JSONField()
    class Meta:
        model = Words
        fields = '__all__'

class PowerWordsSerializer(serializers.ModelSerializer):
    word = serializers.StringRelatedField()
    class Meta:
        model = PowerWords
        fields = "__all__"

class PowerWordsListSerializer(serializers.ModelSerializer):
    word = serializers.StringRelatedField()
    
    class Meta:
        model = PowerWords
        fields = ['id', 'word']

class NegativeWordsSerializer(serializers.ModelSerializer):
    word = serializers.StringRelatedField()
    class Meta:
        model = NegativeWords
        fields = "__all__"
 
class NegativeWordsListSerializer(serializers.ModelSerializer):
    word = serializers.StringRelatedField()
    
    class Meta:
        model = NegativeWords
        fields = ['id', 'word']
       
class EmotionWordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmotionWords
        fields = "__all__"        

class PowerWordScenariosSerializer(serializers.ModelSerializer):
    word = serializers.SerializerMethodField()
    
    def get_word(self, obj):
        return obj.word.word_name
    
    class Meta:
        model = PowerWords
        fields = ['word']
        
class NegativeWordScenarioSerializer(serializers.ModelSerializer):
    word = serializers.SerializerMethodField()
    
    def get_word(self, obj):
        return obj.word.word_name
    
    class Meta:
        model = NegativeWords
        fields = ['word']

class PowerWordCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PowerWords
        fields = ['word', 'weight', 'sentence', 'power_word_name']

class NegativeWordCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NegativeWords
        fields = ['word', 'weight', 'sentence', 'negative_word_name']
