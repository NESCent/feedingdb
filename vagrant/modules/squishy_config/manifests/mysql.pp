class squishy_config::mysql {
  # `$mysql_server` is a custom fact derived from the contents
  # of a file named /etc/mysql_server on the agent.
  if $mysql_server {
    case $mysql_server {
      'percona-55': {
        package {'Percona-Server-server-55':
          ensure => 'installed',
        }
        package {'percona-xtrabackup':
          ensure => 'installed',
        }
      }
      'percona-51': {
        package {'Percona-Server-server-51':
          ensure => 'installed',
        }
        package {'percona-xtrabackup':
          ensure => 'installed',
        }
      }
      'mysql-55': {
        package {'mysql55-server':
          ensure => 'installed',
        }
      }
      default: { include mysql }
    }
  }
  else {
	  include mysql
  }

  # TODO: figure out how to set root password on first install
  # TODO: document / parameterize the root password 
  class { 'mysql::server':
    config_hash => {
      'bind_address' => '127.0.0.1',
      'root_password' => $mysql_root_password,
    }
  }
}
