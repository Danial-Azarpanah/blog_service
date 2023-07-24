from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, phone_number, full_name, password):
        user = self.model(
            phone_number=phone_number,
            full_name=full_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, full_name, password):
        user = self.create_user(
            phone_number=phone_number,
            full_name=full_name,
            password=password
        )
        user.is_active = True
        user.is_admin = True
        user.save(using=self._db)
        return user
