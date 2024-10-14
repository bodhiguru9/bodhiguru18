from rest_framework import serializers

from assessments.models import Question, Option, AssessmentType, Assessment, AssessmentResult

from orgss.models import Org, SubOrg1
from upgrade.models import Upgrade, UpgradeAssessment
from accounts.models import Account
from datetime import date
from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework import serializers
from upgrade.models import Upgradedetail


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'option', 'option_image', 'is_correct']      

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'question', 'level', 'suborg', 'options']

    def create(self, validated_data):
        options_data = validated_data.pop('options')
        question = Question.objects.create(**validated_data)
        for option_data in options_data:
            Option.objects.create(question=question, **option_data)
        return question

    def update(self, instance, validated_data):
        options_data = validated_data.pop('options')
        instance.question = validated_data.get('question', instance.question)
        instance.level = validated_data.get('level', instance.level)
        #instance.timer = validated_data.get('timer', instance.timer)
        instance.save()

        # Delete existing options and create new ones
        instance.options.all().delete()
        for option_data in options_data:
            Option.objects.create(question=instance, **option_data)

        return instance

class QuestionSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question', 'level']

class AssessmentSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = ['id', 'assessment_type', 'access', 'is_approved', 'is_live', 'org']


class AssessmentSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Assessment
        fields = ['id', 'assessment_type', 'questions', 'access', 'is_approved', 'is_live', 'org']

    def validate(self, data):
        request = self.context['request']

        # Access the user's account and then the org
        userprofile = request.user.userprofile  # Get the UserProfile linked to the logged-in user
        org = userprofile.user.org  # Access the org through the account model

        # Get the organization's purchased package
        if org.package_purchased == 'no_assessment':
            max_questions = 2
        elif org.package_purchased == 'assessment30':
            max_questions = 30
        elif org.package_purchased == 'assessment60':
            max_questions = 60
        else:
            max_questions = 2  # Default to 9 questions if no package found

        # Get the total number of questions already mapped to assessments
        total_mapped_questions = Assessment.objects.filter(org=org).values_list('questions', flat=True).count()
        new_questions = len(data['questions'])

        # Check if adding these questions exceeds the allowed limit
        if total_mapped_questions + new_questions > max_questions:
            raise serializers.ValidationError(f"Exceeded the question limit. Maximum {max_questions} questions allowed for your package.")

        return data

    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        
        # Create the assessment instance first
        assessment = Assessment.objects.create(**validated_data)
        
        # Loop through the questions data
        for question_data in questions_data:
            # Check if 'options' key exists and handle the case where it might be missing
            options_data = question_data.get('options', [])  # Default to an empty list if options are not present

            # Fetch the SubOrg1 instance using the provided ID; default to a specific instance if necessary
            suborg_id = question_data.get('suborg1', 1)  # Replace with the appropriate key based on your input structure
            suborg_instance = SubOrg1.objects.get(id=suborg_id)  # Make sure to handle the case where this might not exist

            # Create the question instance
            question_instance = Question.objects.create(
                question=question_data['question'],
                level=question_data['level'],  # Ensure all required fields are included
                #timer=question_data.get('timer'),  # Handle optional fields if needed
                suborg=suborg_instance  # Assign the fetched SubOrg1 instance here
            )

            # If you need to create options associated with this question, do it here
            for option in options_data:
                Option.objects.create(
                    question=question_instance,
                    option=option['option'],  # Ensure you are accessing the correct key
                    is_correct=option.get('is_correct', False)  # Optional field
                )

            # Add the created question to the assessment
            assessment.questions.add(question_instance)

        return assessment


    def update(self, instance, validated_data):
        questions_data = validated_data.pop('questions')
        instance.assessment_type = validated_data.get('assessment_type', instance.assessment_type)
        instance.access = validated_data.get('access', instance.access)
        instance.is_approved = validated_data.get('is_approved', instance.is_approved)
        instance.is_live = validated_data.get('is_live', instance.is_live)
        instance.save()

        # Remove all previous questions and add new ones
        instance.questions.clear()
        for question_data in questions_data:
            instance.questions.add(question_data['id'])

        return instance

class OptionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['option', 'is_correct']

class QuestionListSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()
    
    def get_options(self, obj):
        options_data = Option.objects.filter(question=obj)
        serializers = OptionListSerializer(options_data, many=True)
        return serializers.data
    
    class Meta:
        model = Question
        fields = ['question', 'level', 'timer', 'options']
        

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
        fields = ['id', 'user', 'assessment',  'result']


class AssessmentTypeSerializer(serializers.ModelSerializer):
    suborg_name = serializers.SerializerMethodField()

    class Meta:
        model = AssessmentType
        fields = ['id', 'name', 'suborg', 'suborg_name', 'is_live', 'is_approved']

    def get_suborg_name(self, obj):
        return obj.suborg.name if obj.suborg else None


class AssessmentResultSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(write_only=True)
    assessment_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = AssessmentResult
        fields = ['user_email', 'assessment_id', 'result', 'created_at']
    
    def create(self, validated_data):
        # Fetch user by email
        try:
            user = Account.objects.get(email=validated_data['user_email'])
        except Account.DoesNotExist:
            raise serializers.ValidationError({"user_email": "User does not exist."})

        # Fetch assessment by id
        try:
            assessment = Assessment.objects.get(id=validated_data['assessment_id'])
        except Assessment.DoesNotExist:
            raise serializers.ValidationError({"assessment_id": "Assessment does not exist."})

        # Create the AssessmentResult instance
        assessment_result = AssessmentResult.objects.create(
            user=user,
            assessment=assessment,
            result=validated_data['result'],
            created_at=validated_data.get('created_at', date.today())  # Use today's date if not provided
        )
        return assessment_result        

class AssessmentResultSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    assessment_name = serializers.SerializerMethodField()  # New field for assessment name

    class Meta:
        model = AssessmentResult
        fields = ['user', 'user_name', 'result', 'assessment', 'assessment_name', 'created_at']

    def get_user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    def get_assessment_name(self, obj):
        return obj.assessment.assessment_type.name if obj.assessment.assessment_type else "No Assessment Type"  # Safely get the assessment name


class AssessmentQuestionMappingSerializer(serializers.ModelSerializer):
    questions = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), many=True)

    class Meta:
        model = Assessment
        fields = ['id', 'questions']

    def update(self, instance, validated_data):
        # Access the logged-in user and their organization
        user = self.context['request'].user
        org = user.org  # Assuming the user's org is directly available from the Account model
        print(f"Logged-in User's Organization: {org.name}")  # Debug: print the org of the logged-in user

        # Fetch the package purchased by the user's organization
        package_purchased = org.package_purchased
        new_questions = validated_data.get('questions', [])
        new_question_count = len(new_questions)

        # Get the count of already mapped questions
        existing_question_count = instance.questions.count()

        # Handle default case if no package is purchased
        if not package_purchased:
            if existing_question_count + new_question_count > 2:
                raise serializers.ValidationError({
                    'questions': 'You are only allowed to map up to 9 questions without a package.'
                })

        # Check for bronze/silver package upgrades
        elif package_purchased in ['bronze', 'silver']:
            try:
                upgradedetail = Upgradedetail.objects.get(org=org)
                assessment_package = upgradedetail.assessment_package

                # Get the last 30 days' assessments
                last_30_days = timezone.now() - timedelta(days=30)
                mapped_questions_last_30_days = instance.questions.filter(
                    assessment__created_at__gte=last_30_days).count()

                if assessment_package == 'assessment30':
                    # Allow up to 30 questions on a rolling 30-day basis
                    if mapped_questions_last_30_days + new_question_count > 30:
                        raise serializers.ValidationError({
                            'questions': 'You are only allowed to map up to 30 questions within the last 30 days.'
                        })

                elif assessment_package == 'assessment60':
                    # Allow up to 60 questions on a rolling 30-day basis
                    if mapped_questions_last_30_days + new_question_count > 60:
                        raise serializers.ValidationError({
                            'questions': 'You are only allowed to map up to 60 questions within the last 30 days.'
                        })

            except Upgradedetail.DoesNotExist:
                raise serializers.ValidationError({
                    'upgrade': 'No upgrade details found for this organization.'
                })

        # Append new questions to the existing questions
        instance.questions.add(*new_questions)
        
        # Calculate total questions after appending
        total_questions = instance.questions.count()

        # Save the assessment
        instance.save()

        return instance
