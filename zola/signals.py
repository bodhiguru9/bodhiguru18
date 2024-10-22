# zola/signals.py

# zola/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum
from .models import ItemResult
from accounts.models import UserProfile

@receiver(post_save, sender=ItemResult)
def update_user_profile_score(sender, instance, created, **kwargs):
    if created:  # Only update if a new item result is created
        # Get the user profile for the instance's user
        user_profile = instance.user.userprofile
        item_level = instance.item.level

        # Calculate total score for all items of the same level
        total_score = ItemResult.objects.filter(user=instance.user, item__level=item_level).aggregate(
            total_score=Sum('score'))['total_score'] or 0

        # Update user's current level score for this level
        user_profile.current_level_score = total_score

        # Check if the total score crosses the thresholds
        if item_level == 1 and total_score >= 180:
            user_profile.current_level = 2
        elif item_level == 2 and total_score >= 360:
            user_profile.current_level = 3

        # Save the updated user profile
        user_profile.save()
