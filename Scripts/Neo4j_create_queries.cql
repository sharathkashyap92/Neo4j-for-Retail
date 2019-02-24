LOAD CSV WITH HEADERS FROM "file:///item.csv" AS row
CREATE (n:Item)
SET n = row

CREATE INDEX ON :Item(item)

LOAD CSV WITH HEADERS FROM "file:///user.csv" AS row
CREATE (n:User)
SET n = row

CREATE INDEX ON :User(user)

LOAD CSV WITH HEADERS FROM "file:///agg.csv" AS row
MATCH (u:User), (i:Item) 
WHERE u.user = row.user_id AND i.item = row.Item_name
CREATE (u)-[details:PURCHASES]->(i)
SET details = row,
  details.quantity = toInteger(row.quantity)

match (n) return n limit 100



# Recommendation Query #

MATCH (u:User {user:'18710'})-[:PURCHASES]->(i:Item)<-
[:PURCHASES]-(peer:User)-[:PURCHASES]->(reco:Item)
WHERE not (u)-[:PURCHASES]->(reco)
RETURN reco as Recommendation, count(*) as Frequency
ORDER BY Frequency DESC LIMIT 5;