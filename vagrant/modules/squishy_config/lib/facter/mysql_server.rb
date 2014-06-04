require 'facter'
Facter.add(:mysql_server) do
	setcode do
		Facter::Util::Resolution.exec("test -f /etc/mysql_server && cat /etc/mysql_server")
	end
end
