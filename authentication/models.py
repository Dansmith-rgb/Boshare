from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, related_name="user" ,on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    friends = models.ManyToManyField(User, blank=True, default=None, related_name="friends")
    visibility = (
        ('pr', 'private'),
        ('pu', 'public')
    )
    access = models.CharField(max_length=2,choices=visibility, default='pr', null=True)

    def __str__(self):
        return self.user.username

    def add_friend(self, account):
        """
        Add a new friend
        """
        if account.access == "pr":
            if not account in self.friends.all():
                self.friends.add(account)
                self.save()

    def remove_friend(self, account):
        """
        Remove a friend
        """
        if account.access == "pr":
            if account in self.friends.all():
                self.friends.remove(account)

    def unfriend(self, remove):
        """
        Initiate the action of unfriending someone
        """
        remover_friends_list = self # Person terminating the friendship

        # Remove friend from remover friend list
        remover_friends_list.remove_friend(remove)

        # Remove friend from remove friends list
        friends_list = Profile.objects.get(user=remove)
        friends_list.remove_friend(remover_friends_list.user)

    def is_mutual_friend(self, friend):
        """
        Is this a friend?
        """
        if friend in self.friends.all():
            return True
        return False


class FriendRequest(models.Model):
	"""
	A friend request consists of two main parts:
		1. SENDER
			- Person sending/initiating the friend request
		2. RECIVER
			- Person receiving the friend friend
	"""

	sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="sender")
	receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="receiver")

	is_active = models.BooleanField(blank=False, null=False, default=True)

	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.sender.user.username

	def accept(self):
		"""
		Accept a friend request.
		Update both SENDER and RECEIVER friend lists.
		"""
		receiver_friend_list = Profile.objects.get(user=self.receiver)
		if receiver_friend_list:
			receiver_friend_list.add_friend(self.sender)
			sender_friend_list = Profile.objects.get(user=self.sender)
			if sender_friend_list:
				sender_friend_list.add_friend(self.receiver)
				self.is_active = False
				self.save()

	def decline(self):
		"""
		Decline a friend request.
		Is it "declined" by setting the `is_active` field to False
		"""
		self.is_active = False
		self.save()


	def cancel(self):
		"""
		Cancel a friend request.
		Is it "cancelled" by setting the `is_active` field to False.
		This is only different with respect to "declining" through the notification that is generated.
		"""
		self.is_active = False
		self.save()
