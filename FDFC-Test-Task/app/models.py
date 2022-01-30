from enum import unique
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

STATE_STEP1 = "Step 1"
STATE_STEP2 = "Step 2"
STATE_STEP3 = "Step 3"
STATE_COMPLETED = "Completed"

STATE_CHOICES = (
    (STATE_STEP1, STATE_STEP1),
    (STATE_STEP2, STATE_STEP2),
    (STATE_STEP3, STATE_STEP3),
    (STATE_COMPLETED, STATE_COMPLETED)
)

TRANSITIONS = {
    STATE_STEP1: [STATE_STEP2,],
    STATE_STEP2: [STATE_STEP3,STATE_STEP1],
    STATE_STEP3: [STATE_COMPLETED, STATE_STEP2],
    STATE_COMPLETED: [],
}

# Create your models here.
class CustomUser(AbstractUser):
    # pass
    __current_state = None
    
    state = models.CharField(
        max_length=20, choices=STATE_CHOICES, default=STATE_STEP1
    )
    username = models.CharField(_("username"), max_length=150, unique=True)
    
    # Step 1 - 
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    # Step 2
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    # Step 3
    email = models.EmailField(_('email address'), blank=True)
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
    
    # Step 2 - 
    # location = models.CharField(max_length=30, null=True, blank=True)
    # birth_date = models.DateField(null=True, blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__current_state = self.state
        
    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        allowed_next = TRANSITIONS[self.__current_state]

        updated = self.state != self.__current_state
        if self.pk and updated and self.state not in allowed_next:
            raise Exception("Invalid transition.", self.state, allowed_next)

        if self.pk and updated:
            self.__current_state = self.state

        return super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )
    
    def _transition(self, state):
        self.state = state
        print('going step 2')
        self.save()

    def submit1(self, first_name):
        # we omit storing the driver on the model for simplicity of the example
        self.first_name = first_name
        self._transition(STATE_STEP2)

    def submit2(self):
        self._transition(STATE_STEP3)

    def submit3(self):
        self._transition(STATE_COMPLETED)

    def back1(self):
        self._transition(STATE_STEP1)

    def back2(self):
        self._transition(STATE_STEP2)
    
    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
