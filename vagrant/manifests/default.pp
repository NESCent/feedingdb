include squishy_config::minimum

package { ['postgresql-devel']: ensure => present }

squishy_config::django { 'feeddb':
  pg_user => 'feed',
  pg_pass => 'feed',
  root => '/server/src/feeddb',
  settings_template => 'settings.py.erb',
}

package { 'java-1.7.0-openjdk':
  ensure => 'installed',
  before => Class['Solr::Jetty'],
}

class { 'solr::jetty':
  solr_version => '3.6.2',
  apache_mirror => 'archive.apache.org/dist',
}

# Solr requires this stopwords file but doesn't include it in 3.6.2, dummies.
file { '/etc/solr/conf/stopwords_en.txt':
  ensure => present,
}

file { '/etc/profile.d/feeddb-django.sh':
  content =>
    "source /virtualenv/feeddb/bin/activate
     cd /server/src
    "
}

file { '/usr/bin/feeddb-refresh-solr':
  ensure => link,
  target => "/server/bin/feeddb-refresh-solr.sh",
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
