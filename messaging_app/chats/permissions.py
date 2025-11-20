from rest_framework import permissions 

class IsParticipantOfConversation(permissions.BasePermission):

  def has_object_permission(self,request,view,obj):
      user_id = request.user.id
      if not user or not user.is_authenticated:
        return False
        
      if hasatter(obj,'participant_id_user_id'):
        return obj.participant_id_user_id == user_id 
        
      if hasatter(obj,"conversation") :
        return obj.conversation.participant_id_user_id == user_id

      if request.method in ["GET","Patch","PUT","DELETE"]:
         return True
   return False
        
 

     
