class squishy_config::selinux {

  augeas { "selinux_config":
    context => "/files/etc/sysconfig/selinux",
    changes => [
      "set SELINUX disabled"
    ],
  }

  file { "/selinux/enforce":
    ensure => absent,
  }
}
