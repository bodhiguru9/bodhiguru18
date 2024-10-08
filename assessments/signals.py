# assessments/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from assessments.models import AssessmentResult
from accounts.models import UserProfile  # Import UserProfile from the accounts app

@receiver(post_save, sender=AssessmentResult)
def update_user_profile_assessment_score(sender, instance, created, **kwargs):
    if created:
        # Get the user profile associated with the user
        try:
            user_profile = UserProfile.objects.get(user=instance.user)
        except UserProfile.DoesNotExist:
            return  # Handle case where UserProfile does not exist

        # Format the new assessment score (e.g., "AssessmentTypeName: score")
        new_score_entry = f"{instance.assessment.assessment_type.name}: {instance.result}"

        # Append the new score entry to the existing assessment_score field
        if user_profile.assessment_score:
            user_profile.assessment_score += f", {new_score_entry}"
        else:
            user_profile.assessment_score = new_score_entry

        # Save the updated user profile
        user_profile.save()
