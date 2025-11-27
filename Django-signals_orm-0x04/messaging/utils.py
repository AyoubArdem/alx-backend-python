
def get_replies(message):
    replies = message.objects.all().select_related("sender", "receiver")
    tree = []

    for reply in replies:
        tree.append({
            "id": reply.id,
            "content": reply.content,
            "sender": reply.sender.username,
            "timestamp": reply.timestamp,
            "replies": get_replies(reply)    
        })

    return tree
