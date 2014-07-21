include squishy_config::minimum

package { ['postgresql-devel']: ensure => present }

squishy_config::django { 'feeddb':
  pg_user => 'feed',
  pg_pass => 'feed',
  root => '/server/src/feeddb',
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
