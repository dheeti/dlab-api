from webargs import fields


class Args(object):
    
    """
    GET /api/user
    GET /api/issue
    GET /api/value
    GET /api/objective/policy

    node in user, community, issue, value, objective, policy
    """
    get_node = {
        'id':fields.Str(required=True),
    }
    
    """
    GET /api/community/issue
    GET /api/issue/value
    GET /api/issue/objective
    GET /api/issue/policy
    """
    get_nodes = {
        'filter_id':fields.Str(required=True),
        'user_id':fields.Str(required=False)
    }
   
    """
    GET /api/community
    """
    get_community = {
        'id':fields.Str(required=False),
    }

    """
    POST /api/user
    """
    post_user = {
        'username':fields.Str(required=True),
        'password':fields.Str(required=True),
        'name':fields.Str(required=True),
        'city':fields.Str(required=True)
    }
    
    """
    POST /api/login
    """
    post_login = {
        'username':fields.Str(required=True),
        'password':fields.Str(required=True)
    }
    
    """
    POST /api/logout
    """
    post_logout = {
        'username':fields.Str(required=True)
    }
  
    """
    POST /api/rank/<node>
    
    node in issue, value, objective, policy
    """
    post_rank = {
        'user_id':fields.Str(required=True),
        'node_id':fields.Str(required=True),
        'issue_id':fields.Str(required=False),
        'rank':fields.Int(required=True)
    }

    """
    POST /api/map/value/objective
    POST /api/map/objective/policy
    """
    post_map = {
        'user_id':fields.Str(required=True),
        'src_id':fields.Str(required=True),
        'dst_id':fields.Str(required=True),
        'strength':fields.Int(required=True)
    }

    get_summary = {
        'issue_id':fields.Str(required=True)
    }

    post_issue_creation = {
        'issue_name': fields.Str(required=True),
        'desc': fields.Str(required=False),
	'values':fields.List(fields.Str,required=False),
        'objectives':fields.List(fields.Str,required=False),
        'policies': fields.List(fields.Str,required=False)
    }
