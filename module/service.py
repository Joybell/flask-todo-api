import module.database as database

class Tasks():
    def __init__(self):
        self.db = database.Database()

    def get_active_tasks(self):
        sql = """
            SELECT 
                task_id, 
                task_title, 
                task_status, 
                date_format(createdAt, '%s') as createdAt, 
                date_format(updatedAt, '%s') as updatedAt 
            FROM tasks
        """ % ('%%Y-%%m-%%d %%h:%%i:%%s', '%%Y-%%m-%%d %%h:%%i:%%s')

        return self.db.executeAll(sql)

    def get_active_task(self, task_id):
        sql = """
            SELECT 
                task_id, 
                task_title, 
                task_status, 
                date_format(createdAt, '%s') as createdAt, 
                date_format(updatedAt, '%s') as updatedAt 
            FROM 
                tasks
            WHERE 
                task_id = %s
        """ % ('%%Y-%%m-%%d %%h:%%i:%%s', '%%Y-%%m-%%d %%h:%%i:%%s', task_id)

        print sql

        return self.db.executeOne(sql)

    def create_task(self, task_title):
        sql = """
            INSERT INTO 
                tasks (task_title, task_status, createdAt, updatedAt) 
            VALUES 
                ('%s', 'active', NOW(), NOW())
        """ % task_title

        self.db.execute(sql)
        self.db.commit()

        return self.db.cursor.rowcount

    def update_task(self, task_id, task_title):
        sql = """
            UPDATE 
                tasks 
            SET 
                task_title = '%s' 
            WHERE 
                task_id = %s
        """ % (task_title, task_id)
                
        self.db.execute(sql)
        self.db.commit()

        return self.db.cursor.rowcount

    def delete_task(self, task_id):
        sql = """
            DELETE
            FROM
                tasks
            WHERE 
                task_id = %s
        """ % task_id

        self.db.execute(sql)
        self.db.commit()

        return self.db.cursor.rowcount

    def update_task_status(self, task_id, task_status):
        sql = """
            UPDATE 
                tasks 
            SET 
                task_status = '%s' 
            WHERE 
                task_id = %s
        """ % (task_status, task_id)
                
        self.db.execute(sql)
        self.db.commit()

        return self.db.cursor.rowcount
            
