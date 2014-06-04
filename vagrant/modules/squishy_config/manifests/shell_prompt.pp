class squishy_config::shell_prompt {
  file { "/etc/profile.d/servertype-prompt.sh":
    mode => 644,
    owner => root,
    group => root,
    source => "puppet:///modules/squishy_config/servertype-prompt.sh"
  }

  # delete legacy name of this file
  file { "/etc/profile.d/squishy-servertype.sh":
    ensure => absent
  }
}
