class squishy_config::users {

  group { "sudo":
    ensure => present,
    #gid    => 501,
  }

  group { "dev":
    ensure => present,
    #gid    => 502,
  }

}
