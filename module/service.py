import module.database as database

class Tasks():
    def __init__(self):
        self.db = database.Database()

    def get_tasks(self, task_status, page):
        limit = 5
        offset = (page - 1) * limit
        order_by = 'task_id ASC'

        if task_status == 'closed':
            limit = 1000
            offset = 0
            order_by = 'updated_at DESC'

        sql = """
            SELECT 
                task_id, 
                task_title, 
                task_status, 
                date_format(created_at, '%s') as created_at, 
                date_format(updated_at, '%s') as updated_at 
            FROM tasks
            WHERE task_status = '%s'
            ORDER BY %s
        """ % ('%%Y-%%m-%%d %%h:%%i:%%s', '%%Y-%%m-%%d %%h:%%i:%%s', task_status, order_by)

        sql += """
            LIMIT %s 
            OFFSET %s
        """ % (limit, offset)

        return self.db.executeAll(sql)

    def get_tasks_count(self, task_status):
        sql = """
            SELECT 
                SQL_CALC_FOUND_ROWS task_id
            FROM tasks
            WHERE task_status = '%s'
        """ % task_status

        self.db.execute(sql)

        sql = """SELECT FOUND_ROWS() as totalCount"""
        return self.db.executeOne(sql)

    def get_task(self, task_id):
        sql = """
            SELECT 
                task_id, 
                task_title, 
                task_status, 
                date_format(created_at, '%s') as created_at, 
                date_format(updated_at, '%s') as updated_at 
            FROM 
                tasks
            WHERE 
                task_id = %s
        """ % ('%%Y-%%m-%%d %%h:%%i:%%s', '%%Y-%%m-%%d %%h:%%i:%%s', task_id)

        return self.db.executeOne(sql)

    def create_task(self, task_title):
        sql = """
            INSERT INTO 
                tasks (task_title, task_status, created_at, updated_at) 
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
                task_title = '%s',
                updated_at = NOW() 
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
                task_status = '%s',
                updated_at = NOW() 
            WHERE 
                task_id = %s
        """ % (task_status, task_id)
                
        self.db.execute(sql)
        self.db.commit()

        return self.db.cursor.rowcount
            
