# requirements_force_update: set to `true` to force puppet to run `pip install -r ...` 
define squishy_config::django(
  $root = undef,
  $pg_user   = $title,
  $pg_pass   = $title,
  $pg_host   = 'localhost',
  $pg_name   = $title,
  $virtualenv = "/virtualenv/$title/",
  $requirements_file = undef,
  $requirements_force_update = true,
){
  include squishy_config::apache

  if ! $root {
    fail("You must specify a Django installation root")
  }

  if ($requirements_file) {
    $_requirements_file = $requirements_file
  }
  else {
    $_requirements_file = "$root/requirements.txt"
  }

  # TODO: move class configuration to hiera and use `include` here.
  class { 'postgresql::server':
    manage_firewall => false,
    postgres_password => 'postgres',
  }

  # TODO: move class configuration to hiera and use `include` here.
  class { 'python':
    version => 'system',
    pip => true,
    dev => true,
    virtualenv => true,
    gunicorn => false,
  }

  # TODO: make postgres optional; support mysql
  postgresql::server::db { $pg_name:
    user => $pg_user,
    password => postgresql_password($pg_user, $pg_pass),
  }

  python::virtualenv { $virtualenv:
    owner => 'root',
    group => 'apache',
  }

  python::requirements { $_requirements_file:
    virtualenv => $virtualenv,
    owner => 'root',
    group => 'apache',
    forceupdate => $requirements_force_update,
    require => Python::Virtualenv[$virtualenv],
  }

  # TODO: move class configuration to hiera and use `include` here.
  class { 'apache::mod::wsgi':
    wsgi_socket_prefix => '/var/run/wsgi',
    wsgi_python_home => $virtualenv,
  }

  # TODO: figure out how to expose some of these to the caller. Perhaps an override
  # hash and a create_resources call?
  apache::vhost { $title:
    priority => '10',
    port => '80',
    docroot => $root,
    wsgi_daemon_process => 'wsgi',
    wsgi_daemon_process_options => {
      processes => 2,
      threads => 15,
      display-name => '%{GROUP}',
    },
    wsgi_process_group => 'wsgi',
    wsgi_script_aliases => {
      '/' => "$root/wsgi.py"
    },
  }

  file { $root:
    ensure => present,
  }
}
