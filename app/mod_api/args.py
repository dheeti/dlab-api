from webargs import fields


class Args(object):

    get_node = {
        'id':fields.Str(required=True),
    }

    post_user = {
        'username':fields.Str(required=True),
        'name':fields.Str(required=True),
        'city':fields.Str(required=True)
    }
    
    post_rank = {
        'user_id':fields.Str(required=True),
        'node_id':fields.Str(required=True),
        'issue_id':fields.Str(required=True),
        'rank':fields.Int(required=True)
    }
