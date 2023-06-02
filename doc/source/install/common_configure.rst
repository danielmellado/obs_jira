2. Edit the ``/etc/obs_jira/obs_jira.conf`` file and complete the following
   actions:

   * In the ``[database]`` section, configure database access:

     .. code-block:: ini

        [database]
        ...
        connection = mysql+pymysql://obs_jira:OBS_JIRA_DBPASS@controller/obs_jira
