from rest_framework import serializers

from assessments.models import Question, Option, AssessmentType, Assessment
from assessments.models import AssessmentResult

from orgss.models import Org
from upgrade.models import Upgrade, UpgradeAssessment



class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'option', 'is_correct']

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)  # Nest the options within the question

    class Meta:
        model = Question
        fields = ['id', 'question', 'level', 'timer', 'options']

    def create(self, validated_data):
        options_data = validated_data.pop('options')  # Extract options data
        question = Question.objects.create(**validated_data)  # Create question instance
        
        # Create option instances for the question
        for option_data in options_data:
            Option.objects.create(question=question, **option_data)

        return question

    def update(self, instance, validated_data):
        options_data = validated_data.pop('options')
        instance.question = validated_data.get('question', instance.question)
        instance.level = validated_data.get('level', instance.level)
        instance.timer = validated_data.get('timer', instance.timer)
        instance.save()

        # Delete existing options and create new ones (simplified update logic)
        instance.options.all().delete()
        for option_data in options_data:
            Option.objects.create(question=instance, **option_data)

        return instance

class QuestionSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question', 'level']

class AssessmentSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Assessment
        fields = ['id', 'assessment_type', 'access', 'is_approved', 'is_live', 'questions']

    def validate(self, data):
        """
        Custom validation to check if the number of questions being mapped doesn't exceed
        the allowed limit based on the purchased package by the organization.
        """
        # Fetch the sub-org from assessment_type and then org
        suborg = data['assessment_type'].suborg  # Adjust this line if needed based on your models
        org = suborg.org  # Get the org from sub-org
        
        # Get the total number of existing questions mapped to this assessment
        current_question_count = data['questions'].__len__()

        # Fetch the organization's upgrade assessment package
        package = org.package_purchased  # Field in Org model that holds purchased package info
        
        # Validation for each package type
        if package == 'no_assessment' and current_question_count > 9:
            raise ValidationError("Only 9 questions can be mapped as no assessment package is purchased.")
        
        elif package == 'assessment30':
            if org.expires_on and org.expires_on < datetime.now().date():
                raise ValidationError("The assessment package has expired.")
            # Total questions mapped so far
            total_questions = self.instance.questions.count() if self.instance else 0
            if total_questions + current_question_count > 30:
                raise ValidationError("A maximum of 30 questions can be mapped for this assessment package.")

        elif package == 'assessment60':
            if org.expires_on and org.expires_on < datetime.now().date():
                raise ValidationError("The assessment package has expired.")
            # Total questions mapped so far
            total_questions = self.instance.questions.count() if self.instance else 0
            if total_questions + current_question_count > 60:
                raise ValidationError("A maximum of 60 questions can be mapped for this assessment package.")

        return data

    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        assessment = Assessment.objects.create(**validated_data)
        
        # Create the nested questions and options
        for question_data in questions_data:
            options_data = question_data.pop('options')
            question = Question.objects.create(**question_data)
            
            # Create options for each question
            for option_data in options_data:
                Option.objects.create(question=question, **option_data)
            
            assessment.questions.add(question)
        
        return assessment

    def update(self, instance, validated_data):
        questions_data = validated_data.pop('questions')
        instance.assessment_type = validated_data.get('assessment_type', instance.assessment_type)
        instance.access = validated_data.get('access', instance.access)
        instance.is_approved = validated_data.get('is_approved', instance.is_approved)
        instance.is_live = validated_data.get('is_live', instance.is_live)
        instance.save()

        # Update or create questions and options
        for question_data in questions_data:
            question_id = question_data.get('id')
            if question_id:
                question = Question.objects.get(id=question_id, assessment=instance)
                question.question = question_data.get('question', question.question)
                question.level = question_data.get('level', question.level)
                question.timer = question_data.get('timer', question.timer)
                question.save()

                # Update options
                options_data = question_data.get('options')
                for option_data in options_data:
                    option_id = option_data.get('id')
                    if option_id:
                        option = Option.objects.get(id=option_id, question=question)
                        option.option = option_data.get('option', option.option)
                        option.is_correct = option_data.get('is_correct', option.is_correct)
                        option.save()
                    else:
                        Option.objects.create(question=question, **option_data)
            else:
                # Create new question and options
                options_data = question_data.pop('options')
                question = Question.objects.create(**question_data)
                for option_data in options_data:
                    Option.objects.create(question=question, **option_data)
                instance.questions.add(question)

        return instance
        
class AssessmentListSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()
    assessment_type = serializers.SerializerMethodField()
    
    def get_questions(self, obj):
        questions_data = QuestionListSerializer(obj.questions, many=True)
        return questions_data.data
    
    def get_assessment_type(self, obj):
        return AssessmentTypeSerializer(obj.assessment_type).data
    
    class Meta:
        model = Assessment
        fields = ['id', 'questions', 'access', 'assessment_type', 'is_live', 'is_approved']

class AssessmentResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentResult
        fields = ['id', 'user', 'assessment', 'phase', 'result']


class AssessmentTypeSerializer(serializers.ModelSerializer):
    suborg_name = serializers.SerializerMethodField()

    class Meta:
        model = AssessmentType
        fields = ['id', 'name', 'suborg', 'suborg_name', 'passing_criteria', 'positive_marks', 'negative_marks', 'time', 'trigger_point', 'refresher_days']
        
    
    def get_suborg_name(self, obj):
        return obj.suborg.name