class pxp_ssh_authorized_key::testmannt( $accounts = ['root'] ){

  pxp_ssh_authorized_key { 
   'dummykey' :
     ensure      => absent,
     key_comment => 'test.testmann@wunderman.com',
     key_type    => 'ssh-rsa',
     accounts    => $accounts,
  }

}

