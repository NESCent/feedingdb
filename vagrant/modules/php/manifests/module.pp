# Define: php::module
#
# Manage optional PHP modules which are separately packaged.
# See also php::module:ini for optional configuration.
#
# Sample Usage :
#  php::module { [ 'ldap', 'mcrypt', 'xml' ]: }
#  php::module { 'odbc': ensure => absent }
#  php::module { 'pecl-apc': }
#
define php::module ( $ensure = installed ) {
    $prefix = $osfamily ? { 'RedHat' => 'php-', 'Debian' => 'php5-' }
    if $osfamily == 'Debian' {
      $suffix = $title ? {
        'pecl-apc' => 'apc',
        default => $title,
      }
    }
    else {
      $suffix = $title
    }
      
    package { "${prefix}${suffix}":
        ensure => $ensure,
    }
}

