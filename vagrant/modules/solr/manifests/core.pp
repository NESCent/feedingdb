# = Class: solr::core
#
# This class downloads and installs a Apache Solr
#
# == Parameters:
#
# $solr_version:: which version of solr to install
#
# $solr_home:: where to place solr
#
#
# == Requires:
#
#   wget
#
# == Sample Usage:
#
#   class {'solr::core':
#     solr_version           => '4.4.0'
#   }
#
class solr::core(
  $solr_version = $solr::params::solr_version,
  $solr_home = $solr::params::solr_home,
  $apache_mirror = $solr::params::apache_mirror,
  $core_name = $solr::params::core_name,
) inherits solr::params {

  # using the 'creates' option here against the finished product so we only download this once
  #
  $solr_basename = versioncmp($solr_version, '4.0.0') ? {
    1 => "solr-${solr_version}",
    default => "apache-solr-${solr_version}"
  }

  $solr_tgz_url = "http://${apache_mirror}/lucene/solr/${solr_version}/${solr_basename}.tgz"
  exec { "wget solr":
    command => "wget --output-document=/tmp/${solr_basename}.tgz ${solr_tgz_url}",
    creates => "${solr_home}/${solr_basename}"
  } ->

  user { "solr":
    ensure => present
  } ->
 
  file { "/opt/solr":
    ensure => directory,
    owner  => solr,
  } ->
  
  exec { "untar solr":
    command => "tar -xf /tmp/${solr_basename}.tgz -C ${solr_home}",
    creates => "${solr_home}/${solr_basename}"
  } ->

  file { "${solr_home}/current":
    ensure => link,
    target => "${solr_home}/${solr_basename}",
    owner  => solr,
  }

  # defaults if solr_conf is not provided
  # data will go to /var/lib/solr
  # conf will go to /etc/solr
  file { "/etc/solr":
    ensure => directory,
    owner  => solr,
  } ->

  file { "/var/lib/solr":
    ensure => directory,
    owner  => solr,
  } ->

  exec { "copy core files to collection1":
    command => "cp -rf /opt/solr/current/example/solr/* /etc/solr/",
    user    => solr,
    creates => "/etc/solr/conf/schema.xml"
  }
}

