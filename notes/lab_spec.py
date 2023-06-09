"""
This is an attempt to brainstorm how lab developers could specify the configuration
of a lab for a given course.
"""

import pip
pip.main(['install', "git+https://github.com/databricks-academy/dbacademy@main"])

lab_spec = {
    "lab_name": "data-analysis-with-databricks",
    "max_users_per_workspace": 250,

    "user_dbcs_to_import": {
        "data-anaysis-with-databricks": "https://..."
    },

    "datasets-mount": {
        "/mnt/dbacademy-datasets": "s3://...",
    },

   "user_cluster_spec": {
        "num_workers": 0,
        "spark_version": "11.3.x-cpu-ml-scala2.12",
        "spark_conf": {
            "spark.master": "local[*, 4]",
            "spark.databricks.cluster.profile": "singleNode"
        },
        "custom_tags": {
            "ResourceClass": "SingleNode"
        },
        "autotermination_minutes": 120,
        "policy_name": "DBAcademy",
        "instance_pool_name": "DBAcademy Pool",
        "data_security_mode": "SINGLE_USER",
        "runtime_engine": "STANDARD",
    },

    "workspace_setup_jobs": {
        "DBAcademy Workspace Setup": {...},
    },
}


class LabDefinition(VocareumLabDefinition):
    def prompt_for_inputs(self):
        """
        Return a list of configuration values to UI should prompt the user to input.
        """
        return [{
            "variable-name": "$RUNTIME_VERSION",
            "input-name": "DBR-Version",
            "input-type": "text",
            "default-value": "11.3.x-cpu-ml-lt",
        }]
    def on_lab_setup(lab_id):
        """
        Fires whenever a lab is created or a lab's settings are changed.
        Idempotent.  Reruns anytime a lab's settings are changed.
        """
        ws = dbacademy.workspaces_3_0.vocareum_lab_setup(lab_spec)
        ws.do_something_custom()

    def on_user_create(username):
        """
        Fires whenever a user is registered for the lab.  This should add the user to a workspace
        and create the user's cluster in a stopped state.
        Idemponent.  Reruns anytime a user's registration details changes.
        """
        dbacademy.workspaces_3_0.vocareum_user_create(lab_spec)

    def on_user_resume(username):
        """
        Fires when the user begins using the lab.  This should start/restart the user's cluster.
        This function should be idempotent as the user can pause and resume their lab anytime.
        """
        dbacademy.workspaces_3_0.vocareum_user_resume(lab_spec)

    def on_user_lab_submission(username, step_id):
        """
        Fires when the user requests a lab be gradedd.
        This function should be idempotent.
        """
        dbacademy.workspaces_3_0.vocareum_grade_lab(lab_spec)

    def on_user_pause(username):
        """
        Fires when the user puts their lab on hold for the night.
        This function should be idempotent.
        """
        dbacademy.workspaces_3_0.vocareum_user_pause(lab_spec)

    def on_user_destroy(username):
        """
        Fires when the user is 100% finished with the lab.  Tear down the cluster, cleanup after the user.
        This function does NOT need to be called if on_lab_destroy() is about to be called.
        """
        dbacademy.workspaces_3_0.vocareum_user_destroy(lab_spec)

    def on_lab_destroy()
        """
        Fires when all labs in the event are complete should be torn down.  on_user_destroy need to be called
        if the event is ending.
        """
        ws = dbacademy.workspaces_3_0.vocareum_lab_destroy(lab_spec)


databricks_account_url = os.env["DATABRICKS_ACCOUNT_URL"]
databricks_account_user = os.env["DATABRICKS_ACCOUNT_USER"]
databricks_account_pass = os.env["DATABRICKS_ACCOUNT_PASS"]

if __name__=="__main__":
    dbacademy.workspaces_3_0.vocareum_main(LabDefinition)
