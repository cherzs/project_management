from odoo import models, tools

class ProjectDashboard(models.Model):
    _name = 'project.dashboard'
    _description = 'Project Dashboard'
    _auto = False

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE or REPLACE VIEW %s as (
                WITH done_stage AS (
                    SELECT id 
                    FROM project_task_stage 
                    WHERE name::text = 'Done'::text 
                    LIMIT 1
                )
                SELECT
                    p.id,
                    p.name,
                    COUNT(t.id) as task_count,
                    SUM(CASE 
                        WHEN t.stage_id = (SELECT id FROM done_stage) THEN 1 
                        ELSE 0 
                    END) as completed_tasks,
                    AVG(CASE 
                        WHEN t.stage_id = (SELECT id FROM done_stage) 
                        THEN DATE_PART('day', t.write_date::timestamp - t.create_date::timestamp)
                        ELSE NULL 
                    END) as avg_completion_days
                FROM project_management p
                LEFT JOIN projects_task t ON t.project_id = p.id
                GROUP BY p.id, p.name
            )
        """ % self._table)