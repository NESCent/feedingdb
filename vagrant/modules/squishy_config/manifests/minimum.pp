class squishy_config::minimum {
  Exec { path => '/usr/bin:/bin:/usr/sbin:/sbin' }

  class {'epel': }
  class {'squishy_config::shell_prompt': }
  class {'squishy_config::selinux': }

  # Centos 6.4 doesn't include this lens by default.
  # We got it from https://github.com/estahn/augeas/blob/master/lenses/ssh.aug
  file { "/usr/share/augeas/lenses/ssh.aug":
    mode => 644,
    owner => root,
    group => root,
    source => "puppet:///modules/squishy_config/ssh.aug"
  }

  # Vagrant takes care of users, ssh, and puppet configuration, so we
  # only set these things up if we're on a real server.
  if (!$vagrant) {
    class {'squishy_config::users': }
    class {'squishy_config::ssh': }

    # set puppet master
    #augeas { "puppet.conf":
    #  context => "/files/etc/puppet/puppet.conf",
    #  changes => [
    #    "set agent/server puppet.squishyclients.net"
    #  ]
    #}

    #cron { "puppet":
    #  command => "/usr/bin/puppet agent --onetime --no-daemonize --logdest syslog > /dev/null 2>&1",
    #  user => "root",
    #  minute => fqdn_rand( 60 ),
    #  ensure => present,
    #}
  }
}
