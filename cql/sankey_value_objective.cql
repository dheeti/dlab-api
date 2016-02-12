MATCH (o:Objective)-[r_obj:RANKS]-(u:User)-[r_val:RANKS]-(v:Value)
RETURN
    v.node_id AS vid,
    v.name AS vname,
    o.node_id AS oid,
    o.name AS oname,
    collect(r_val.rank) AS vranks,
    collect(r_obj.rank) AS oranks
order by vid, oid, vranks, oranks
