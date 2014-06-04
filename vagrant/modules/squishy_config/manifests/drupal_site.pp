/**
 * Definition: squishy_config::drupal_site
 *
 * Currently very limited in scope; this is all we do:
 *  * Ensure pear and drush are installed (via drupal_deps)
 *  * Manage the database by using puppetlabs/mysql
 *  * Create a matching settings.php
 *  * Ensure the files directory is writable
 */
define squishy_config::drupal_site(
  $root      = undef,
  $site_name = $title,
  $db_user   = $title,
  $db_pass   = $title,
  $db_host   = 'localhost',
  $db_name   = $title,
  $update_free_access = false,
  $settings_file = undef,
  $writable_dirs = undef,
){
  include squishy_config::drupal_deps

  if ! $root {
    fail("You must specify a Drupal root for Squishy_config::Drupal_site[$site_name]")
  }

  if $settings_file {
    $_settings_file = $settings_file
  }
  else {
    $_settings_file = "$root/sites/$site_name/settings.php"
  }

  if $writable_dirs {
    $_writable_dirs = $writable_dirs
  }
  else {
    $_writable_dirs = [ "$root/sites/$site_name/files" ]
  }

  ###

  # TODO: chmod doesn't work from inside vagrant; the user has to
  # do it manually. Figure out why and see if it can be fixed.
  if ! $vagrant {
    file { $_writable_dirs:
      ensure => directory,
      owner => 'apache',
      group => 'squishydev',
      mode => 'ug+w,o-w',
      recurse => true,
    }
  }

  # make the database (requires puppetlabs/mysql)
  mysql::db { $db_name:
    user     => $db_user,
    password => $db_pass,
  }

  # create settings.php using the database credentials specified
  file { $_settings_file:
    content => template('squishy_config/settings.php.erb'),
    group => $vagrant ? { 1 => undef, default => 'squishydev' },
    mode => 'ug+w,o-w',
  }
}
