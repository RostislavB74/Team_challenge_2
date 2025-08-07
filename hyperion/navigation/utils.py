def get_user_sql_role(request):
    return request.session.get('sql_role', 'sysadmin')  # тимчасово або визначай з request.user.username
