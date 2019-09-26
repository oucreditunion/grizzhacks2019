Vagrant.configure("2") do |config|

	config.vm.box = "ubuntu/xenial64"
	config.vm.box_url = "https://app.vagrantup.com/ubuntu/boxes/xenial64"	
	config.vm.box_download_insecure = true
	
	config.vm.network "forwarded_port", guest:80, host:8080
	config.vm.network "forwarded_port", guest:8081, host:8081
	
	config.vm.synced_folder "php/", "/var/www/html/php/"
	config.vm.provision :shell, path: "provisioners/wsgi.sh"
	
end
