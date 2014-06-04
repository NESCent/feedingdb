/**
 * Basic system setup for running Drupal sites.
 *
 * Does not actually download Drupal; it's assumed you have this in git.
  $repo_url, 'ssh://git@git.squishyclients.net:22421/
 */
class squishy_config::drupal_deps {
  include squishy_config::lamp
  include pear

  Exec { path => "/usr/bin/" }

  pear::package { "PEAR": }

  pear::package { "drush":
    version => "5.9.0",
    repository => "pear.drush.org",
  }

  # need rsync for drush sql-sync and drush rsync
  if ! defined(Package['rsync']) {
    package { 'rsync': }
  }

  # Console_Table is required by drush and isn't installed by pear when we
  # install drush.
  pear::package { "Console_Table":
    version => "1.1.3",
  }

  # uploadprogress: pecl, php-devel, and uploadprogress.ini
  pear::package { "uploadprogress":
    repository => "pecl.php.net",
    require => [
      Pear::Package['PEAR'],
      Package['php-devel'],
    ],
    notify => Service['httpd'],
  }

  if ! defined(Package['php-devel']) {
    package { 'php-devel': }
  }

  file { '/etc/php.d/uploadprogress.ini':
    ensure => present,
    require => Pear::Package['uploadprogress'],
  }

  augeas { 'uploadprogress':
    context => "/files/etc/php.d/uploadprogress.ini/.anon",
    changes => [
      "set extension uploadprogress.so",
    ],
    require => File['/etc/php.d/uploadprogress.ini'],
    notify => Service['httpd'],
  }

  # memcache: seems to be installed always, so we just manage the .ini
  augeas { 'memcache':
    context => "/files/etc/php.d/memcache.ini/.anon",
    changes => [
      "set extension memcache.so",
    ],
    require => File['/etc/php.d/memcache.ini'],
  }

  file { '/etc/php.d/memcache.ini':
    ensure => present,
    require => Package['php-pecl-memcache'],
  }

}
