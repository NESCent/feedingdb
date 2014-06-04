class squishy_config::apc {
  Exec { path => '/usr/bin:/bin:/usr/sbin:/sbin' }

  package { "php-pecl-apc":
    ensure => latest,
    before => Exec["fix-the-apc.ini"],
  }

  augeas { "apc.ini" :
    notify  => Service['httpd'],
    context => "/files/etc/php.d/apc.ini/.anon/",
    require => Exec["fix-the-apc.ini"],
    changes => [
      'set extension apc.so',
      'set apc.enabled 1',
      'set apc.shm_size 128m',
    ],
  }

  # This is a hacky hack to fix invalid .ini syntax on the default apc.ini that
  # is distributed with CentOS. The file contains a couple lines, specifically
  # these:
  #
  #   apc.filters
  #   apc.preload_path
  #
  # Augeas refuses to edit `apc.ini` because these lines don't have a separator
  # and are not comments either. This exec {} block adds "=" signs to the end
  # of any non-comment lines that don't have it already.
  exec { 'fix-the-apc.ini':
    command => "cp -f /etc/php.d/apc.ini /tmp/apc.ini && cat /tmp/apc.ini | perl -pe 'm/^\s*;/ || s/^([^=\n]+)$/\$1=/s' > /etc/php.d/apc.ini",
    onlyif => "grep -v '^\s*;' /etc/php.d/apc.ini | grep -v = | grep -v '^$'"
  }
}
