from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import CustomUser


class Task(models.Model):
    """Model representing a task."""

    class TaskStatus(models.TextChoices):
        """
        A class that represents the possible status options for a task.

        The available status options are:
        - TO_DO: The task is to be done.
        - IN_PROGRESS: The task is currently in progress.
        - DONE: The task has been completed.
        - ARCHIVED: The task has been archived.
        - HOLD: The task is on hold.
        """

        TO_DO = 'to do', _('to do')
        IN_PROGRESS = 'in progress', _('in progress')
        DONE = 'done', _('done')
        ARCHIVED = 'archived', _('archived')
        HOLD = 'hold', _('hold')

    creator = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name=_('creator'),
        help_text=_('The creator of the task'),
    )
    performers = models.ManyToManyField(
        CustomUser,
        related_name='performers',
        verbose_name=_('performers'),
        help_text=_('The performers of the task'),
    )
    description = models.TextField(
        max_length=100,
        verbose_name=_('description'),
        help_text=_('The description of the task'),
    )
    comment = models.TextField(
        max_length=100,
        verbose_name=_('comment'),
        help_text=_('The comment of the task'),
        blank=True,
    )
    link = models.URLField(
        max_length=100,
        verbose_name=_('link'),
        help_text=_('The link of the task'),
        blank=True,
    )
    status = models.CharField(
        max_length=15,
        choices=TaskStatus.choices,
        default=TaskStatus.TO_DO,
        verbose_name=_('status'),
        help_text=_('The status of the task'),
    )
    start_date = models.DateField(
        auto_now_add=True,
        verbose_name=_('start date'),
        help_text=_('The start date of the task'),
    )
    inprogress_date = models.DateField(
        verbose_name=_('"in progress" date'),
        help_text=_('The "in progress" date of the task'),
        blank=True,
        null=True,
    )
    finish_date = models.DateField(
        verbose_name=_('finish date'),
        help_text=_('The finish date of the task'),
        blank=True,
        null=True,
    )
    deadline_date = models.DateField(
        verbose_name=_('deadline date'),
        help_text=_('The deadline date of the task'),
    )
    archive_date = models.DateField(
        verbose_name=_('archive date'),
        help_text=_('The archive date of the task'),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _('task')
        verbose_name_plural = _('tasks')
        ordering = ('-start_date',)

    def __str__(self):
        return self.description[:15]
