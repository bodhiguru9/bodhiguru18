# assessments/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from assessments.models import AssessmentResult
from accounts.models import UserProfile  # Import UserProfile from the accounts app


@receiver(post_save, sender=AssessmentResult)
def update_assessment_score(sender, instance, created, **kwargs):
    if created:
        # Ensure the UserProfile exists
        try:
            user_profile = UserProfile.objects.get(user=instance.user)
        except UserProfile.DoesNotExist:
            return  # You can log an error here if needed

        # Update the assessment score in UserProfile
        assessment_info = f"{instance.assessment.assessment_type.name}: {instance.result}"
        
        if user_profile.assessment_score:
            # Append the new result
            user_profile.assessment_score += f", {assessment_info}"
        else:
            # First result being added
            user_profile.assessment_score = assessment_info
        
        print(f"Signal triggered for user: {instance.user.email}")
        print(f"Assessment info: {assessment_info}")

        user_profile.save()