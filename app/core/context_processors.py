def user_session(request):
    return {
        "user": request.session.get("user", {}),
        "business": request.session.get("business", [])
    }