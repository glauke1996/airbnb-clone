from django.shortcuts import redirect, render
from django.http import Http404
from django.db.models import Q
from django.urls import path, reverse
from django.views.generic import View, DetailView
from users import models as user_model
from . import models
from . import forms

# Create your views here.


def go_conversation(request, a_pk, b_pk):
    user_one = user_model.User.objects.get(pk=a_pk)
    user_two = user_model.User.objects.get(pk=b_pk)
    if user_one != None and user_two != None:
        try:
            conversation = models.Conversation.objects.get(
                Q(participants=user_one) and Q(participants=user_two)
            )
        except models.Conversation.DoesNotExist:
            conversation = models.Conversation.objects.create()
            conversation.participants.add(user_one, user_two)

        return redirect(reverse("conversations:detail", kwargs={"pk": conversation.pk}))


# class ConversationDetailView(DetailView):
#     model=models.Conversation


class ConversationDetailView(View):
    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        try:
            conversation = models.Conversation.objects.get(pk=pk)
        except models.Conversation.DoesNotExist:
            raise Http404
        form = forms.AddCommentForm()
        return render(
            self.request,
            "conversations/conversation_detail.html",
            {"conversation": conversation, "form": form},
        )

    def post(self, *args, **kwargs):
        message = self.request.POST.get("message", None)
        pk = kwargs.get("pk")
        try:
            conversation = models.Conversation.objects.get(pk=pk)
        except models.Conversation.DoesNotExist:
            raise Http404
        if message != None:
            models.Message.objects.create(
                text=message, user=self.request.user, conversation=conversation
            )
        return redirect(reverse("conversations:detail", kwargs={"pk": pk}))
