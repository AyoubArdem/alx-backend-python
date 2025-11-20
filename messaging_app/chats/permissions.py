from rest_framework.permissions import BasePermission

class IsParticipantOfConversation(BasePermission):

  def has_object_permission(self,request,view,obj):
      user = request.user
      if not user or not user.is_authenticated:
        return False
        
      if hasatter(obj,'participant1') and (obj,'participant2'):
        return obj.participant1 == user  or obj.participant2 == user
        
      if hasatter(obj,"conversation") :
        return obj.conversation.participant1 == user  or obj.conversation.participant2 == user

  return False

     
