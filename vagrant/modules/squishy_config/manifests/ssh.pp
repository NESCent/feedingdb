class squishy_config::ssh {
  augeas { "sshd_config":
    context => "/files/etc/ssh/sshd_config",
    changes => [
      # track which key was used to logged in
      "set LogLevel VERBOSE",
      # permit root logins only using publickey
      "set PermitRootLogin without-password",
      # disable X11 forwarding
      "set X11Forwarding no",
      # Agent forwarding for gitolite
      "set AllowAgentForwarding yes",

      "set KerberosAuthentication no",
      "set GSSAPIAuthentication no",
    ],
    notify => Service["sshd"],
  }

  service { "sshd":
    name => $operatingsystem ? {
      /Debian|Ubuntu/ => "ssh",
      default => "sshd",
    },
    require => Augeas["sshd_config"],
    enable => true,
    ensure => running,
  }
}
