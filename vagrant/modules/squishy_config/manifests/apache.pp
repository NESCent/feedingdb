class squishy_config::apache {
  $vhosts_d = $osfamily ? {
    'RedHat' => "/etc/httpd/vhosts.d",
    'Debian' => "/etc/apache2/sites-available",
  }

  class { '::apache':
    default_mods => false,
    default_vhost => true,
    default_ssl_vhost => false,
    vhost_dir => $vhosts_d,
    service_enable => true,
  }

  # We have to list apache modules manually because we are turning down the
  # default modules in the block above.
  include ::apache::mod::mime
  include ::apache::mod::dir
  include ::apache::mod::rewrite

  if (!$vagrant) {
    file { '/server':
      ensure	=> directory,
      mode	=> 2775,
      owner	=> 'root',
      group	=> 'dev',
    }
    file { '/server/www/':
      ensure => directory,
      mode   => 2775,
      owner  => 'root',
      group  => 'dev',
    }
  }
}
