include squishy_config::minimum
include squishy_config::apache

package { ['postgresql-devel']: ensure => present }

class { 'postgresql::server':
  manage_firewall => false,
  postgres_password => 'postgres',
}

postgresql::server::db { 'feeddb':
  user => 'feed',
  password => postgresql_password('feed', 'feed'),
}

class { 'python':
  version => 'system',
  pip => true,
  dev => true,
  virtualenv => true,
  gunicorn => false,
}

python::virtualenv { '/virtualenv/feed-venv':
  owner => 'root',
  group => 'apache',
}

python::requirements { '/server/src/feeddb/dependencies.pip':
  virtualenv => '/virtualenv/feed-venv',
  owner => 'root',
  group => 'apache',
  forceupdate => true,
}

class { 'apache::mod::wsgi':
  wsgi_socket_prefix => '/var/run/wsgi',
  wsgi_python_home => '/virtualenv/feed-venv',
  wsgi_python_path => '/virtualenv/feed-venv/lib/python2.6',
}

apache::vhost { 'feeddb':
  priority => '10',
  port => '80',
  docroot => '/server/htdocs',
  wsgi_daemon_process => 'wsgi',
  wsgi_daemon_process_options => {
    processes => 2,
    threads => 15,
    display-name => '%{GROUP}',
  },
  wsgi_process_group => 'wsgi',
  wsgi_script_aliases => {
    '/' => '/server/src/feeddb/wsgi.py',
  },
  #aliases => [
  #  { alias => '/media', path => '/server/src/feedb' TODO ... }
  #],
}

# Ensure that apache::vhost doesn't clobber our docroot.
# Alternately, you can use `link` or `directory` if you want to be explicit.
file { '/server/htdocs':
  ensure => present,
}

# insecure settings for ssh client within vagrant
augeas { 'ssh_config':
  context => "/files/etc/ssh/ssh_config",
  changes => [
    "set Host *",
    "set Host[.='*']/StrictHostKeyChecking no",
    "set Host[.='*']/User $vagrant_ssh_user",
  ],
  require => File['/usr/share/augeas/lenses/ssh.aug'],
}

# vagrant boxes don't need iptables
service { 'iptables':
  ensure => stopped,
  enable => false,
}
