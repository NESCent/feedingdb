# Class: php::mod_php5
#
# Apache httpd PHP module. Requires the 'httpd' service and package to be
# declared somewhere, usually from the apache_httpd module.
#
# Sample Usage :
#  php::ini { '/etc/php-httpd.ini': }
#  class { 'php::mod_php5': inifile => '/etc/php-httpd.ini' }
#
class php::mod_php5 ( $inifile = '/etc/php.ini' ) {
    $php = $osfamily ? { 
      'RedHat' => 'php', 
      'Debian' => [ 'php5', 'libapache2-mod-php5' ] 
    }
    package { $php:
        ensure  => installed,
        require => File[$inifile],
        notify  => Service['httpd'],
    }

    # Custom httpd conf snippet
    if $osfamily == 'RedHat' {
      file { '/etc/httpd/conf.d/php.conf':
          content => template('php/httpd/php.conf.erb'),
          require => Package['httpd'],
          notify  => Service['httpd'],
      }
    }
    # TODO: do something appropriate for debian-based systems
    
    # Notify the httpd service for any php.ini changes too
    File[$inifile] ~> Service['httpd']
}

