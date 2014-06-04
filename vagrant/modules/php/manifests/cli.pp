# Class: php::cli
#
# Command Line Interface PHP. Useful for console scripts, cron jobs etc.
# To customize the behavior of the php binary, see php::ini.
#
# Sample Usage:
#  include php::cli
#
class php::cli ( $inifile = '/etc/php.ini' ) {
    $phpcli = $osfamily ? { 'RedHat' => 'php-cli', 'Debian' => 'php5-cli', }
    package { $phpcli:
        ensure  => installed,
        require => File[$inifile],
    }
}

