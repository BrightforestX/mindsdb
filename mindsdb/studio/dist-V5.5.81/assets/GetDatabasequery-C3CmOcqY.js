const r=e=>{var a;return t[e.id]?`--- After you fill all the mandatory fields run the query with the top button or shift + enter.
    ${t[e.id]}

    `.trim().replace(/display_name/g,`my_${e.name}`):`--- After you fill all the mandatory fields run the query with the top button or shift + enter.

CREATE DATABASE my_${e.name}   --- display name for database.
WITH ENGINE = '${e.id}',
PARAMETERS = {
  ${Object.entries(((a=e==null?void 0:e.aditional_data)==null?void 0:a.connection_args_example)||{}).map(([s,o])=>`"${s}": "${o}"`).join(`,
  `)}
};`},t={"Demo Database":`
CREATE DATABASE datasource
WITH ENGINE = "postgres",
PARAMETERS = {
  "user": "demo_user",
  "password": "demo_password",
  "host": "samples.mindsdb.com",
  "port": "5432",
  "database": "demo",
  "schema": "demo_data"
};`,binance:`
CREATE DATABASE display_name --- display name for database.
WITH ENGINE = 'binance'
  PARAMETERS = {};`,cassandra:`
CREATE DATABASE display_name  --- display name for database.
WITH ENGINE = 'cassandra',    --- name of the mindsdb handler
PARAMETERS = {
    "user": " ",              --- Your Keyspace user.
    "password": " ",          --- Your Keyspace password.
    "host": " ",              --- host, it can be an ip or an url.
    "port": "9043",           --- common port is 9043.
    "keyspace": " "           --- The name of your database *optional.
};`,clickhouse:`
CREATE DATABASE display_name  --- display name for database.
WITH ENGINE = 'clickhouse',   --- name of the mindsdb handler
PARAMETERS = {
  "host": " ",                --- host name or IP address
  "port": " ",                --- port used to make TCP/IP connection
  "database": " ",            --- database name
  "user": " ",                --- database user
  "password": " ",            --- database password
  "protocol": " "             --- optional, http or https (defaults to native)
};`,cockroachdb:`
CREATE DATABASE display_name  --- display name for database.
WITH ENGINE = 'cockroachdb',  --- name of the mindsdb handler
PARAMETERS = {
    "user": " ",              --- Your database user.
    "password": " ",          --- Your password.
    "host": " ",              --- host, it can be an ip or an url.
    "port": "26257",          --- common port is 26257.
    "database": " ",          --- The name of your database *optional.
    "publish": ""             --- publish
};`,kafka:`
CREATE DATABASE display_name  --- display name for database.
WITH ENGINE = 'kafka',        --- name of the mindsdb handler
PARAMETERS = {
    "password": " ",          --- Your password.
    "host": " ",              --- host, it can be an ip or an url.
    "port": "9092",           --- common port is 9092.
    "database": " "           --- The name of your database *optional.
};`,mariadb:`
CREATE DATABASE display_name  --- display name for database.
WITH ENGINE = 'mariadb',      --- name of the mindsdb handler
PARAMETERS = {
    "user": " ",              --- Your database user.
    "password": " ",          --- Your password.
    "host": " ",              --- host, it can be an ip or an url.
    "port": "3306",           --- common port is 3306.
    "database": " "           --- The name of your database *optional.
};`,mongodb:`
CREATE DATABASE display_name  --- display name for database.
WITH ENGINE = 'mongodb',      --- name of the mindsdb handler
PARAMETERS = {
    "user": " ",              --- Your database user.
    "password": " ",          --- Your password.
    "host": " ",              --- host, it can be an ip or an url.
    "port": "27017"           --- common port is 27017.
};`,mssql:`
CREATE DATABASE display_name  --- display name for database.
WITH ENGINE = 'mssql',        --- name of the mindsdb handler
PARAMETERS = {
    "user": " ",              --- Your database user.
    "password": " ",          --- Your password.
    "host": " ",              --- host, it can be an ip or an url.
    "port": "1433",           --- common port is 1433.
    "database": " "           --- The name of your database *optional.
};`,mysql:`
CREATE DATABASE display_name  --- display name for database.
WITH ENGINE = 'mysql',        --- name of the mindsdb handler
PARAMETERS = {
    "user": " ",              --- Your database user.
    "password": " ",          --- Your password.
    "host": " ",              --- host, it can be an ip or an url.
    "port": "3306",           --- common port is 3306.
    "database": " "           --- The name of your database *optional.
};`,postgres:`
CREATE DATABASE display_name  --- display name for database.
WITH ENGINE = 'postgres',     --- name of the mindsdb handler
PARAMETERS = {
    "user": " ",              --- Your database user.
    "password": " ",          --- Your password.
    "host": " ",              --- host, it can be an ip or an url.
    "port": "5432",           --- common port is 5432.
    "database": " "           --- The name of your database *optional.
};`,redis:`
CREATE DATABASE display_name  --- display name for database.
WITH ENGINE = 'redis',        --- name of the mindsdb handler
PARAMETERS = {
    "password": " ",          --- Your password.
    "host": " ",              --- host, it can be an ip or an url.
    "port": "6379",           --- common port is 6379.
    "database": " "           --- The name of your database *optional.
};`,scylladb:`
CREATE DATABASE display_name  --- display name for database.
WITH ENGINE = 'scylladb',     --- name of the mindsdb handler
PARAMETERS = {
    "user": " ",              --- Your database user.
    "password": " ",          --- Your password.
    "host": " ",              --- host, it can be an ip or an url.
    "port": "9042",           --- common port is 9042.
    "keyspace": " "           --- The name of your Keyspace .
};`,snowflake:`
CREATE DATABASE display_name  --- display name for database.
WITH ENGINE = 'snowflake',    --- name of the mindsdb handler
PARAMETERS = {
    "user": " ",              --- Your database user.
    "account": " ",           --- Snowflake account.
    "warehouse": " ",         --- warehouse account.
    "protocol": " ",          --- Common https
    "schema": " ",            --- common schema PUBLIC.
    "password": " ",          --- Your password.
    "host": " ",              --- host, it can be an ip or an url.
    "port": "443",            --- common port is 443.
    "database": " "           --- The name of your database *optional.
};`,singlestore:`
CREATE DATABASE display_name  --- display name for database.
WITH ENGINE = 'singlestore',  --- name of the mindsdb handler
PARAMETERS = {
    "user": " ",              --- Your database user.
    "password": " ",          --- Your password.
    "host": " ",              --- host, it can be an ip or an url.
    "port": "3306",           --- common port is 3306.
    "database": " "           --- The name of your database *optional.
};`,questdb:`
CREATE DATASOURCE display_name  --- display name for database.
WITH ENGINE = 'questdb',        --- name of the mindsdb handler.
PARAMETERS = {
  "user": " ",                  --- Your database user.
  "password": " ",              --- Your password.
  "host": " ",                  --- host, it can be an ip or an url.
  "port": "8812",               --- common port is 8812.
  "database": " ",              --- The name of your database
  "public": true
};`,trino:`
CREATE DATABASE display_name    --- display name for database.
WITH ENGINE = 'trinodb',        --- name of the mindsdb handler.
PARAMETERS={
  "user":" ",                   --- Your database user.
  "password": " ",              --- Your password.
  "host": " ",                  --- host, it can be an ip or an url.
  "port": "8080",               --- common port is 8080.
  "catalog": " ",
  "schema": " "
};`,firebird:`
CREATE DATABASE display_name    --- display name for database.
WITH ENGINE = 'firebird',       --- name of the mindsdb handler.
PARAMETERS={
  "user":" ",                   --- the user to authenticate the user with the Firebird server
  "database": " ",              --- the port to use when connecting with the Firebird server
  "password": " ",              --- the password to authenticate the user with the Firebird server.
  "host": " "                  --- the host name or IP address of the Firebird server
};`,redshift:`
CREATE DATABASE display_name    --- display name for database.
WITH ENGINE = 'redshift',       --- name of the mindsdb handler.
PARAMETERS={
  "user":" ",                   --- the user to authenticate the user with the Redshift cluster
  "database": " ",              --- the database name to use when connecting with the Redshift cluster
  "port": " ",                  --- the port to use when connecting with the Redshift cluster
  "password": " ",              --- the password to authenticate the user with the Redshift cluster
  "host": " "                  --- the host name or IP address of the Redshift cluster
};`,databricks:`
CREATE DATABASE display_name    --- display name for database.
WITH ENGINE = 'databricks',     --- name of the mindsdb handler.
PARAMETERS={
  "server_hostname":" ",        --- the server hostname for the cluster or SQL warehouse
  "http_path": " ",             --- the HTTP path of the cluster or SQL warehouse
  "access_token": " ",          --- a Databricks personal access token for the workspace for the cluster or SQL warehouse
  "schema": " "                --- schema (database) to use for the connection. If left blank, the default schema default will be used
};`,tidb:`
CREATE DATABASE display_name  --- display name for database.
WITH ENGINE = 'tidb',         --- name of the mindsdb handler
PARAMETERS = {
    "user": " ",              --- Your database user.
    "password": " ",          --- Your password.
    "host": " ",              --- host, it can be an ip or an url.
    "port": "4000",           --- common port is 4000.
    "database": " "           --- The name of your database.
};`,supabase:`
CREATE DATABASE display_name  --- display name for database.
WITH ENGINE = 'supabase',     --- name of the mindsdb handler
PARAMETERS = {
    "user": " ",              --- the user to authenticate
    "password": " ",          --- the password to authenticate the user
    "host": " ",              --- the host name of the Supabase connection
    "port": "5432",           --- the port to use when connecting
    "database": " "           --- database name
};`,oracle:`
CREATE DATABASE display_name  --- display name for database.
WITH ENGINE = 'oracle',       --- name of the mindsdb handler
PARAMETERS = {
    "host": " ",              --- host, it can be an ip or an url
    "port": "1521",           --- the port to use when connecting
    "sid": " ",               --- the connection accepts either sid or service_name arguments to target to the right DB instance.
    "user": " ",              --- the user to authenticate
    "password": " "          --- the password to authenticate the user
};`,ckan:`
CREATE DATABASE display_name  --- display name for database.
WITH ENGINE = 'ckan',         --- name of the mindsdb handler
PARAMETERS = {
    "url": " ",               --- host, it can be an ip or an url
    "apikey": " "             --- the api key authentication
};`,access:`
CREATE DATABASE display_name  --- display name for database.
WITH ENGINE = 'access',       --- name of the mindsdb handler
PARAMETERS = {
    "db_file": " "           --- db_file, this points to the database file that the connection is to be made to
};`,couchbase:`
CREATE DATABASE display_name  --- display name for database.
WITH ENGINE = 'couchbase',    --- name of the mindsdb handler
PARAMETERS = {
    "host": " ",              --- the host name or IP address of the Couchbase server
    "bucket": " ",            --- the port to use when connecting with the Couchbase server
    "user": " ",              --- the user to authenticate
    "password": " ",          --- the password to authenticate the user
    "scope": " "             --- the scope to use for making queries based on a scoped context because, couchbase uses scope just like schema in mysql, but scopes are mandatory. N.B the scope is optional, if omitted, will default to "_default"
};`,bigquery:`
CREATE DATABASE display_name       --- display name for database.
WITH ENGINE = 'bigquery',          --- name of the mindsdb handler
PARAMETERS = {
    "project_id": " ",             --- the project_id
    "service_account_keys": " "    --- the service_account_keys
};`,db2:`
CREATE DATABASE display_name  --- display name for database.
WITH ENGINE='DB2',
PARAMETERS={
    "user":" ",               --- username associated with database
    "password":" ",           --- password to authenticate your access
    "host":" ",               --- host to server IP Address or hostname
    "port":"25000",           --- port through which TCP/IP connection is to be made
    "schema_name":" ",        --- database name to be connected
    "database":" "            --- schema name to get tables
};
`,airtable:`
CREATE DATABASE display_name  --- display name for database.
WITH ENGINE='airtable',
PARAMETERS={
    "base_id": " ",           --- the Airtable base ID
    "table_name": " ",        --- the Airtable table name
    "api_key": " "            --- the API key for the Airtable API
};
`,vertica:`
CREATE DATABASE display_name  --- display name for database.
WITH ENGINE='vertica',
PARAMETERS={
    "user": " ",              --- username associated with database
    "password": " ",          --- password to authenticate your access
    "host": " ",              --- host to server IP Address or hostname
    "port": "5433",           --- port through which TCPIP connection is to be made
    "database": " ",          --- database name to be connected
    "schema": " "             --- schema name to get tables
};
`,dynamodb:`
CREATE DATABASE display_name         --- display name for database.
WITH ENGINE='dynamodb',
PARAMETERS={
    "aws_access_key_id": " ",        --- the AWS access key
    "aws_secret_access_key": " ",    --- the AWS secret access key
    "region_name": " "               --- the AWS region
};
`,crate:`
CREATE DATABASE display_name   --- display name for database.
WITH ENGINE='crate',
PARAMETERS={
    "user": " ",               --- username associated with database
    "password": " ",           --- password to authenticate your access
    "host": " ",               --- host to server IP Address or hostname
    "port": "4200",            --- port through which connection is to be made
    "schema_name": " "         --- schema name to get tables
};
`,pinot:`
CREATE DATABASE display_name      --- display name for database.
WITH ENGINE='pinot',
PARAMETERS={
    "host": " ",                   --- the host name or IP address of the Apache Pinot cluster
    "broker_port": "8000",         --- the port that the Broker of the Apache Pinot cluster is running on
    "controller_port": "9000",     --- the port that the Controller of the Apache Pinot cluster is running on
    "path": "",                    --- the query path
    "scheme": " "                  --- schema name to get tables
};
`,sqlite:`
CREATE DATABASE display_name      --- display name for database.
WITH ENGINE='sqlite',
PARAMETERS={
    "db_file": " "               --- this points to the database file that the connection is to be made to
};
`,astra:`
CREATE DATABASE display_name           --- display name for database.
WITH ENGINE = 'astra',
PARAMETERS = {
    "user": " ",                       --- the user to authenticate
    "password": " ",                   --- the password to authenticate the user
    "secure_connection_bundle": " "    --- path to the secure_connection_bundle zip file
};
`,matrixone:`
CREATE DATABASE display_name           --- display name for database.
WITH ENGINE = 'matrixone',
PARAMETERS = {
    "user": " ",                       --- the username associated with database
    "password": " ",                   --- the password to authenticate your access
    "host": " ",                       --- the host to server IP Address or hostname
    "port": "6001",                    --- the port through which TCPIP connection is to be made
    "database": " "                    --- the database name to be connected
};
`,elasticsearch:`
CREATE DATABASE display_name           --- display name for database.
WITH ENGINE = 'elasticsearch',
PARAMETERS = {
    "host": " "                        --- the host name(s) or IP address(es) of the Elasticsearch server(s). If multiple host name(s) or IP address(es) exist, they should be separated by commas. This parameter is optional, but it should be provided if cloud_id is no
};
`,druid:`
CREATE DATABASE display_name           --- display name for database.
WITH ENGINE = 'druid',
PARAMETERS = {
    "host": " ",                       --- the host name or IP address of Apache Druid
    "port": "8888",                    --- the port that Apache Druid is running on
    "path": " ",                       --- the query path
    "scheme": "http"                   --- the URI schema. This parameter is optional and the default will be http
};
`,s3:`
CREATE DATABASE display_name        --- display name for database.
WITH ENGINE = 's3',
PARAMETERS = {
    "aws_access_key_id": " ",       --- the AWS access key
    "aws_secret_access_key": " ",   --- the AWS secret access key
    "region_name": " ",             --- the AWS region
    "bucket": " ",                  --- the name of the S3 bucket
    "key": " ",                     --- the key of the object to be queried
    "input_serialization": " "      --- the format of the data in the object that is to be queried
};
`,d0lt:`
CREATE DATABASE display_name    --- display name for database.
WITH ENGINE = 'd0lt',
PARAMETERS = {
    "user": " ",                --- username associated with database
    "password": " ",            --- password to authenticate your access
    "host": " ",                --- host to server IP Address or hostname
    "port": "3306",             --- port through which TCPIP connection is to be made
    "database": " "             --- Database name to be connected
};
`,duckdb:`
CREATE DATABASE duckdb_datasource
WITH
    engine = 'duckdb',
    parameters = {
        "database": "db.duckdb"
    };
`,teams:`
  CREATE DATABASE teams_datasource
  WITH ENGINE = 'teams',
  PARAMETERS = {
    "client_id": "your-client-id",          --- The client ID of the registered Microsoft Entra ID application.
    "client_secret": "your-client-secret",  --- The client secret of the registered Microsoft Entra ID application.
    "tenant_id": "your-tenant-id"           --- The tenant ID of the registered Microsoft Entra ID application.
  };
`,monetdb:`
CREATE DATABASE display_name    --- display name for database.
WITH ENGINE = 'monetdb',
PARAMETERS = {
    "user": " ",                --- username associated with database
    "password": " ",            --- password to authenticate your access
    "host": " ",                --- host to server IP Address or hostname
    "port": "50000",            --- port through which TCPIP connection is to be made
    "schema_name": " ",         --- schema name to get tables. (Optional) Default it will select current schema.
    "database": " "             --- Database name to be connected
};
`,yugabyte:`
CREATE DATABASE display_name   --- display name for database.
WITH ENGINE = 'yugabyte',
PARAMETERS = {
  "user":" ",                  --- Username associated with database
  "password":" ",              --- Password to authenticate your access
  "host":" ",                  --- Host to server IP Address or hostname
  "port":"5433",               --- Port through which TCPIP connection is to be made
  "database":" "               --- Database name to be connected
};
`,hive:`
CREATE DATABASE display_name   --- display name for database.
WITH ENGINE = 'hive',
PARAMETERS = {
  "user":" ",                  --- Username associated with database
  "password":" ",              --- Password to authenticate your access
  "host":" ",                  --- Host to server IP Address or hostname
  "port":10000,                --- Port through which TCPIP connection is to be made
  "database":" ",              --- Database name to be connected
  "auth":" "                   --- Defaults to CUSTOM in case not provided. Check for other options in https://pypi.org/project/PyHive/
};
`,timescaledb:`
CREATE DATABASE display_name   --- display name for database.
WITH ENGINE = 'timescaledb',
PARAMETERS = {
  "user":" ",                  --- Username associated with database
  "password":" ",              --- Password to authenticate your access
  "host":" ",                  --- Host to server IP Address or hostname
  "port":36806,                --- Port through which TCPIP connection is to be made
  "database":" "               --- Database name to be connected
};
`,skysql:`
CREATE DATABASE skysql            --- display name for database.
WITH ENGINE = 'mariadb',
PARAMETERS = {
  "user":" ",                     --- Username associated with database
  "password":" ",                 --- Password to authenticate your access
  "host":" ",                     --- Host to server IP Address or hostname
  "port": "5001",                 --- Port through which TCPIP connection is to be made
  "ssl": True/False,              --- optional, the 'ssl' parameter value indicates whether SSL is enabled ('True') or disabled ('False')
  "ssl-ca": {  "path": " " },     --- Optional, SSL Certificate Authority
  "database":" "                  --- Database name to be connected
};
`,hana:`
CREATE DATABASE display_name    --- display name for database.
WITH ENGINE = 'hana',
PARAMETERS = {
  "user": " ",                  --- Username associated with database
  "password": " ",              --- Password to authenticate your access
  "host": " ",                  --- Host to server IP Address or hostname
  "port": "443",                --- Port through which TCPIP connection is to be made
  "schema": " ",                --- schema name to get tables
  "encrypt": true
};
`,teradata:`
CREATE DATABASE display_name    --- display name for database.
WITH ENGINE = 'teradata',
PARAMETERS = {
  "host": " ",                  --- Host to server IP Address or hostname
  "user": " ",                  --- Username associated with database
  "password": " ",              --- Password to authenticate your access
  "database": " "              --- Port through which TCPIP connection is to be made
};
`,databend:`
CREATE DATABASE display_name   --- display name for database.
WITH ENGINE = 'databend',
PARAMETERS = {
  "protocol": " ",              --- the protocol to query Databend. Supported: native, http, https. Default: native'.
  "user": " ",                  --- the username used to authenticate with the Databend warehouse
  "port": 443,                  --- the TCP/IP port of the Databend warehouse
  "password": "",               --- the password to authenticate the user with the Databend warehouse
  "host": " ",                  --- the host name or IP address of the Databend warehouse. NOTE: use '127.0.0.1' instead of 'localhost' to connect to local server
  "database": ""               --- the database name to use when connecting with the Databend warehouse
};
`,impala:`
CREATE DATABASE display_name   --- display name for database.
WITH ENGINE = 'impala',
PARAMETERS = {
  "user": " ",                 --- username associated with database
  "password": " ",             --- password to authenticate your access
  "host": 21050,               --- host to server IP Address or hostname
  "port" : "",                 --- port through which TCP/IP connection is to be made
  "database" : ""             --- database name to be connected
};
`,sqlany:`
CREATE DATABASE display_name   --- display name for database.
WITH ENGINE = 'sqlany',
PARAMETERS = {
  "user": " ",                 --- specifies the user name
  "password": " ",             --- specifies the password for the user
  "host": "",                  --- the host name or IP address of the SAP SQL Anywhere instance
  "port": "55505",             --- the port number of the SAP SQL Anywhere instance
  "server": " ",               --- sets the current server
  "database": ""              --- sets the current database
};
`,orioledb:`
CREATE DATABASE display_name   --- display name for database.
WITH ENGINE = 'orioledb',
PARAMETERS = {
  "user": " ",                 --- specifies the user name
  "password": " ",             --- specifies the password for the user
  "host": "",                  --- the host name or IP address of the SAP SQL Anywhere instance
  "port": "55505",             --- the port number of the SAP SQL Anywhere instance
  "server": " ",               --- sets the current server
  "database": ""              --- sets the current database
};
`,sheets:`
CREATE DATABASE display_name   --- display name for database.
WITH ENGINE = 'sheets',
PARAMETERS = {
  "spreadsheet_id": " ",       --- the unique ID of the Google Sheet
  "sheet_name": " "           --- the name of the sheet within the Google Sheet
};
`,solr:`
CREATE DATABASE display_name   --- display name for database.
WITH ENGINE = 'solr',
PARAMETERS = {
  "username": " ",             --- The username used to authenticate with the Solr server. This parameter is optional
  "password": " ",             --- The password to authenticate the user with the Solr server. This parameter is optional
  "host": " ",                 --- The host name or IP address of the Solr serve
  "port": "8981",              --- The port number of the Solr server
  "server_path": " ",          --- Defaults to solr in case not provided
  "collection": " ",           --- Solr Collection name
  "use_ssl": " "              --- Defaults to false in case not provide. true|false Refer https://pypi.org/project/sqlalchemy-solr/
};
`,planet_scale:`
CREATE DATABASE display_name   --- display name for database.
WITH ENGINE = 'planet_scale',
PARAMETERS = {
  "host": " ",                 --- host to server IP Address or hostname
  "port": "3306",              --- port through which TCP/IP connection is to be made
  "user": " ",                 --- username associated with database
  "password": " ",             --- password to authenticate your access
  "database": " "             --- database name to be connected
};
`,tdengine:`
CREATE DATABASE display_name   --- display name for database.
WITH ENGINE = 'tdengine',
PARAMETERS = {
  "user": "",                  --- Username associated with server
  "password": " ",             --- Password to authenticate your access
  "url": " ",                  --- Url to TDEngine server. For local server url is localhost:6041 (Default)
  "token": " ",                --- Unique token provide while using TDEngine Cloud
  "database": " "             --- Database name to be connected
};
`,opengauss:`
CREATE DATABASE display_name   --- display name for database.
WITH ENGINE = 'opengauss',
PARAMETERS = {
  "host": " ",                  --- Host to server IP Address or hostname
  "user": " ",                  --- Username associated with database
  "password": " ",              --- Password to authenticate your access
  "port": 5432,               --- Port through which TCPIP connection is to be made
  "database": " "              --- Database name to be connected
};
`,starrocks:`
CREATE DATABASE display_name   --- display name for database.
WITH ENGINE = 'starrocks',
PARAMETERS = {
  "host": " ",                  --- Host to server IP Address or hostname
  "user": " ",                  --- Username associated with database
  "password": " ",              --- Password to authenticate your access
  "port": "9030",               --- Port through which TCPIP connection is to be made
  "database": " "              --- Database name to be connected
};
`,oceanbase:`
CREATE DATABASE display_name   --- display name for database.
WITH ENGINE = 'oceanbase',
PARAMETERS = {
  "host": " ",                  --- Host to server IP Address or hostname
  "user": " ",                  --- Username associated with database
  "password": " ",              --- Password to authenticate your access
  "port": "9030",               --- Port through which TCPIP connection is to be made
  "database": " "              --- Database name to be connected
};
`,vitess:`
CREATE DATABASE display_name   --- display name for database.
WITH ENGINE = 'vitess',
PARAMETERS = {
  "host": " ",                  --- Host to server IP Address or hostname
  "user": " ",                  --- Username associated with database
  "password": " ",              --- Password to authenticate your access
  "port": "33577",              --- Port through which TCPIP connection is to be made
  "database": " "              --- Database name to be connected
};
`,informix:`
CREATE DATABASE informix_datasource       --- Display name for the database
WITH ENGINE = 'informix',                 --- Name of the MindsDB handler
PARAMETERS = {
  "server": " ",                          --- Server name
  "host": " ",                            --- Host name or IP address
  "port": " ",                            --- Port used to make TCP/IP connection
  "database": " ",                        --- Database name
  "user": " ",                            --- Database user
  "password": " ",                        --- Database password
  "schema_name": " ",                     --- Database schema name
  "logging_enabled": " "                  --- Indicates whether logging is enabled (defaults to "True" if left blank)
};
`,twitter:`
CREATE DATABASE my_twitter
With
ENGINE = 'twitter',
PARAMETERS = {
  "bearer_token": " ",                    --- Twitter bearer TOKEN
  'consumer_key': " ",                    --- Twitter consumer key *optional.
  'consumer_secret': " ",                 --- Twitter consumer secret *optional.
  'access_token':" ",                     --- Twitter access token *optional.
  'access_token_secret':" "               --- Twitter access secret token *optional.
};
`,github:`
CREATE DATABASE mindsdb_github
WITH ENGINE = 'github',
PARAMETERS = {
  "repository": "mindsdb/mindsdb",
  "api_key": "your_api_key",    -- optional GitHub API key
};`,derby:`
CREATE DATABASE derby_datasource
WITH engine='derby',
parameters={
    "host": "",                           --- Host name or IP address
    "port": "1527",                       --- Port used to make TCP/IP connection
    "database": ""                        --- Database name
};`,edgelessdb:`CREATE DATABASE edgelessdb_datasource
WITH ENGINE = "EdgelessDB",
PARAMETERS = {
  "user": " ",
  "password": " ",
  "host": " ",
  "port": " ",
  "database": " "
}`,sqreamdb:`
CREATE DATABASE sqreamdb_datasource
WITH
engine='sqreamdb',
parameters={
    "user": " ",
    "password": " ",
    "host": " ",
    "port": "5000",
    "database": " "
};`,huggingface:`
-- How to Bring the Hugging Face Model to MindsDB
-- We use the CREATE MODEL statement to bring the Hugging Face models to MindsDB.
-- More Info: https://docs.mindsdb.com/nlp/nlp-mindsdb-hf#how-to-bring-the-hugging-face-model-to-mindsdb

-- Generally, it looks like this:

CREATE MODEL project_name.predictor_name        -- AI TABLE TO STORE THE MODEL
PREDICT target_column                           -- NAME OF THE COLUMN TO STORE PREDICTED VALUES
USING
  engine = 'huggingface',                       -- USING THE HUGGING FACE ENGINE
  task = 'task',                                -- TASK OF CLASSIFYING TEXT (OPTIONAL)
  model_name = 'model_name_from_hugging_face',  -- MODEL NAME UNDER THE HUGGING FACE MODEL HUB
  input_column = 'input_column',                -- COLUMN NAME OF THE INPUT DATA
  labels = ['label', 'label_1'];                -- ARRAY OF LABELS
`,pgvector:`
CREATE DATABASE pgvector_datasource
WITH
engine='pgvector',
parameters={
    "host": " ",          -- the host name or IP address of the postgres instance
    "port": " ",          -- the port to use when connecting
    "database": " ",      -- the name of the database to connect to
    "user": "postgres"    -- the username to use when connecting
    "password": " "       -- the password to use when connecting
};
`};export{r as GetDbQuery};
