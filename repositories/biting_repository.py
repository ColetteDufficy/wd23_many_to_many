from db.run_sql import run_sql
from models.biting import Biting

import repositories.human_repository as human_repository
import repositories.zombie_repository as zombie_repository


# SAVE
def save(biting):
    sql = """INSERT INTO bitings ( zombie_id, human_id ) 
    VALUES ( %s, %s ) 
    RETURNING id"""
    values = [biting.zombie.id, biting.human.id]
    results = run_sql( sql, values )
    biting.id = results[0]['id']
    return biting


# #SELECT_ALL
def select_all():
    bitings = []

    sql = "SELECT * FROM bitings"
    results = run_sql(sql)

    for row in results:
        zombie = zombie_repository.select(row['zombie_id'])
        human = human_repository.select(row['human_id'])
        biting = Biting(zombie, human, row['id'])
        bitings.append(biting)
    return bitings


# #SELECT_BY_ID
def select(id):
    biting = None
    sql = """
        SELECT * FROM bitings 
        WHERE id = %s
    """ 
    values = [id] 
    result = run_sql(sql, values)[0]
    
    if result is not None:
        biting = Biting(
            result['zombie_id'], 
            result['human_id'], 
            result['id'] )
    return biting


# #DELETE
def delete(id):
    sql = "DELETE FROM bitings WHERE id = %s"
    values = [id]
    run_sql(sql, values)


# #DELETE_ALL
def delete_all():
    sql = "DELETE FROM bitings"
    run_sql(sql)


# #UPDATE 
def update(biting):
    sql = """
        UPDATE bitings 
        SET (zombie_id, human_id) = (%s, %s) 
        WHERE id = %s
    """
    values = [
        biting.zombie.id, 
        biting.human.id, 
        biting.id
        ]
    run_sql(sql, values) 