Install Fedora41

root enable and use SSH

minimam package and install disk selet

check ipaddress login and ip add command

#login SSH

# check current version

# kernel 6.11

uname -r

# change hopstame

echo Fedora42 > /etc/hostname

#s witch fedora preview

dnf upgrade --refresh

dnf update

dnf system-upgrade download --releasever=42

dnf5 offline reboot

# after reboot

# check current version

# kernel 6.12

uname -r

# kernel rebuild

# https://fedoraproject.org/wiki/Building_a_custom_kernel

# Install required packages

dnf install fedpkg fedora-packager rpmdevtools ncurses-devel pesign grubby

# make packege dependencies

fedpkg clone -a kernel

cd kernel

# switch spec to realtime kernel

sed -i '1s/^/\%define _with_rtonly 1\n/' ./kernel.spec

# install dependencies kernal package make

dnf builddep kernel.spec

# build kerbel and make package

fedpkg local

# about 1 houre

#check package

#kernel-rt-6.12.0-0.rc7.20241115gitcfaaa7d010d1.62.fc42.x86_64.rpm

#kernel-rt-core-6.12.0-0.rc7.20241115gitcfaaa7d010d1.62.fc42.x86_64.rpm

#kernel-rt-devel-6.12.0-0.rc7.20241115gitcfaaa7d010d1.62.fc42.x86_64.rpm

#kernel-rt-devel-matched-6.12.0-0.rc7.20241115gitcfaaa7d010d1.62.fc42.x86_64.rpm

#kernel-rt-kvm-6.12.0-0.rc7.20241115gitcfaaa7d010d1.62.fc42.x86_64.rpm

#kernel-rt-modules-6.12.0-0.rc7.20241115gitcfaaa7d010d1.62.fc42.x86_64.rpm

#kernel-rt-modules-core-6.12.0-0.rc7.20241115gitcfaaa7d010d1.62.fc42.x86_64.rpm

#kernel-rt-modules-extra-6.12.0-0.rc7.20241115gitcfaaa7d010d1.62.fc42.x86_64.rpm

#kernel-rt-modules-internal-6.12.0-0.rc7.20241115gitcfaaa7d010d1.62.fc42.x86_64.rpm

ls x86_64/

#install kernel package

dnf install --nogpgcheck ./x86_64/*

#show grub boot list

grubby --info=ALL | grep -E "^kernel|^index"

#change boot default index

grubby --set-default-index=0

#stop selinux

sed -i s/^SELINUX=.*$/SELINUX=disabled/ /etc/selinux/config

#stop firewall

systemctl disable firewalld.service

#reboot new kernel

reboot


#check new kernel

#6.12.0-XXXXXXXX+rt

uname -r


#check selinux

#Disabled

getenforce


#check firewall

#disabled

systemctl is-enabled firewalld.service
