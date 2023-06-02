Prerequisites
-------------

Before you install and configure the replace with the service it implements service,
you must create a database, service credentials, and API endpoints.

#. To create the database, complete these steps:

   * Use the database access client to connect to the database
     server as the ``root`` user:

     .. code-block:: console

        $ mysql -u root -p

   * Create the ``obs_jira`` database:

     .. code-block:: none

        CREATE DATABASE obs_jira;

   * Grant proper access to the ``obs_jira`` database:

     .. code-block:: none

        GRANT ALL PRIVILEGES ON obs_jira.* TO 'obs_jira'@'localhost' \
          IDENTIFIED BY 'OBS_JIRA_DBPASS';
        GRANT ALL PRIVILEGES ON obs_jira.* TO 'obs_jira'@'%' \
          IDENTIFIED BY 'OBS_JIRA_DBPASS';

     Replace ``OBS_JIRA_DBPASS`` with a suitable password.

   * Exit the database access client.

     .. code-block:: none

        exit;

#. Source the ``admin`` credentials to gain access to
   admin-only CLI commands:

   .. code-block:: console

      $ . admin-openrc

#. To create the service credentials, complete these steps:

   * Create the ``obs_jira`` user:

     .. code-block:: console

        $ openstack user create --domain default --password-prompt obs_jira

   * Add the ``admin`` role to the ``obs_jira`` user:

     .. code-block:: console

        $ openstack role add --project service --user obs_jira admin

   * Create the obs_jira service entities:

     .. code-block:: console

        $ openstack service create --name obs_jira --description "replace with the service it implements" replace with the service it implements

#. Create the replace with the service it implements service API endpoints:

   .. code-block:: console

      $ openstack endpoint create --region RegionOne \
        replace with the service it implements public http://controller:XXXX/vY/%\(tenant_id\)s
      $ openstack endpoint create --region RegionOne \
        replace with the service it implements internal http://controller:XXXX/vY/%\(tenant_id\)s
      $ openstack endpoint create --region RegionOne \
        replace with the service it implements admin http://controller:XXXX/vY/%\(tenant_id\)s
