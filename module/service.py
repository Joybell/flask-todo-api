import module.database as database

class Tasks():
    def __init__(self):
        self.db = database.Database()

    def get_tasks(self, params):
        task_status = params['task_status']
        task_title = params['task_title']
        page = params['page']
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
        """ % ('%%Y-%%m-%%d %%h:%%i:%%s', '%%Y-%%m-%%d %%h:%%i:%%s', task_status)

        if task_title:
            sql += """
                AND task_title LIKE %s
            """ % ("'%%" + task_title + "%%'")

        sql += """
            ORDER BY %s
            LIMIT %s 
            OFFSET %s
        """ % (order_by, limit, offset)

        return self.db.executeAll(sql)

    def get_tasks_count(self, params):
        task_status = params['task_status']
        task_title = params['task_title']

        sql = """
            SELECT 
                SQL_CALC_FOUND_ROWS task_id
            FROM tasks
            WHERE task_status = '%s'
        """ % task_status

        if task_title:
            sql += """
                AND task_title LIKE %s
            """ % ("'%%" + task_title + "%%'")

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
    
    def get_pre_tasks(self):
        sql = """
            SELECT 
                a.task_id, 
                a.task_title,
                a.task_status, 
                GROUP_CONCAT(b.pre_task_id SEPARATOR  ',') as pre_tasks
            FROM 
                tasks as a
            INNER JOIN 
                pre_tasks AS b
            ON 
                a.task_id = b.task_id
            GROUP BY 
                a.task_id
        """

        return self.db.executeAll(sql)

    def get_active_pre_tasks(self, task_id):
        sql = """
            SELECT * 
            FROM 
                tasks AS a
            INNER JOIN (
                SELECT 
                    b1.pre_task_id 
                FROM 
                    tasks AS a1
                INNER JOIN 
                    pre_tasks AS b1
                ON 
                    a1.task_id = b1.task_id 
                And 
                    a1.task_id = %s
            ) b
            ON a.task_id = b.pre_task_id
            AND a.task_status = 'active'
        """ % task_id

        return self.db.executeAll(sql)

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

    def update_pre_tasks(self, task_id, pre_tasks):
        sql = """
            DELETE
            FROM
                pre_tasks
            WHERE 
                task_id = %s
        """ % task_id

        self.db.execute(sql)

        pre_task_ids = pre_tasks.split(",")
        for pre_task_id in pre_task_ids:
            sql = """
                INSERT INTO
                    pre_tasks (task_id, pre_task_id)
                VALUES (%s, %s)
            """ % (task_id, pre_task_id)

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
            
