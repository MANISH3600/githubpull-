# accounts/signals.py

# from django.dispatch import receiver
# from allauth.account.signals import user_logged_in
# from allauth.socialaccount.models import SocialAccount, SocialToken

# @receiver(user_logged_in)
# def on_user_logged_in(request, user, **kwargs):
#     print("User logged in:", user)
#     print("running the signal")
#     # Fetch the social account associated with the user
#     try:
#         social_account = SocialAccount.objects.get(user=user, provider='github')
#         access_token = SocialToken.objects.get(account=social_account)  # Get the token associated with the social account
        
#         if access_token:
#             print("GitHub Access Token:", access_token.token)  # Print or handle the access token
#             # You can also save this token to the user's profile or handle it as needed
#         else:
#             print("No GitHub Access Token found.")
#     except SocialAccount.DoesNotExist:
#         print("User does not have a GitHub social account.")
#     except SocialToken.DoesNotExist:
#         print("No token associated with the GitHub social account.")
