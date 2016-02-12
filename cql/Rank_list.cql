match (o:Objective) -[r_obj:RANKS]- (u:User) -[r_val:RANKS]- (v:Value)
return u.node_id, v.name, o.name, r_val.rank, r_obj.rank
order by v.name, o.name

match (o:Objective) -[r_obj:RANKS]- (u:User) -[r_pol:RANKS]- (p:Policy)
return u.node_id, o.name, p.name, r_obj.rank, r_pol.rank
order by o.name,p.name
