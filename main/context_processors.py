def user_role(request):
    user = request.user
    is_editor = user.is_authenticated and user.groups.filter(name="Editor").exists()

    if not user.is_authenticated:
        role = None
    elif user.is_superuser:
        role = "owner"
    elif is_editor:
        role = "editor"
    else:
        role = "user"

    return {
        "is_editor": is_editor,  
        "user_role": role,
    }