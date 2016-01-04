from webargs import fields


class Args(object):
    
    """
    GET /api/<node>

    node in user, community, issue, value, objective, policy
    """
    get_node = {
        'id':fields.Str(required=True),
    }

    """
    POST /api/user
    """
    post_user = {
        'username':fields.Str(required=True),
        'name':fields.Str(required=True),
        'city':fields.Str(required=True)
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
