class pxp_ssh_authorized_key::hetzeneckerl( $accounts = ['root'] ){

  pxp_ssh_authorized_key { 
   'AAAAB3NzaC1yc2EAAAADAQABAAABAQDMb53EaVztIglbVMXCohMIEGBQgSCmUq8+wSOuO8gRwv5onDDLAssTHoyUPIBnenEPTyGkgm/RUlG9DGfO+FFs63k7rkUpsYJtRk7rB/+37EnYhVjDv5fBujKlT0d7CBaj3iEFcXmurEPhCCc9zPBcaCA5j46axKSwSmBH0hLFHOVDzM9t+FSqK1flZ7q+PncGyvqWFv2u5pIanQtD3f26kcx0l/xsSWzv3iu/5CcLXBm5+UxzbMPUZdZxZ+H2o/GnhyMjU8Rq+TE47ra6Y4X7GlMtBZ5AWIE3M8fTwRnk6hxKSUaQECnOGZUwUYdWN0vlggFm6U5Fu3vGW2+2RMi7':
     key_comment => 'lukas.hetzenecker@wunderman.com',
     key_type    => 'ssh-rsa',
     accounts    => $accounts;
  }

}

