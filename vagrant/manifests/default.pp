include squishy_config::minimum
include squishy_config::apache

class { 'python':
  version => 'system',
  pip => true,
  dev => true,
  virtualenv => true,
  gunicorn => false,
}

python::virtualenv { '/home/vagrant/feed-venv':
  owner => 'vagrant',
  group => 'vagrant',
}

python::requirements { '/server/src/feeddb/dependencies.pip':
  virtualenv => '/home/vagrant/feed-venv',
  owner => 'vagrant',
  forceupdate => true,
}

apache::vhost { 'feeddb':
  priority => '10',
  port => '80',
  docroot => '/server/src',
  wsgi_daemon_process => 'wsgi',
  wsgi_daemon_process_options => {
    processes => 2,
    threads => 15,
    display_name => '%{GROUP}',
  },
  wsgi_process_group => 'wsgi',
  wsgi_script_aliases => {
    '/' => '/server/src/feedb/wsgi.py',
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
