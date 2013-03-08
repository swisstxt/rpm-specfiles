# Generated from daemon_controller-0.2.5.gem by gem2rpm -*- rpm-spec -*-
%define gemname daemon_controller
%define rubyver 1.9.3
%define ruby_dir /opt/ruby-%{rubyver}
%define ruby_sitelib %(%{ruby_dir}/bin/ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
%define gemdir %(%{ruby_dir}/bin/ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%define geminstdir %{gemdir}/gems/%{gemname}-%{version}

Summary: A library for implementing daemon management capabilities
Name: opt-ruby-%{rubyver}-rubygem-%{gemname}
Version: 1.0.0
Release: 1%{?dist}
Group: Development/Languages
License: GPLv2+ or Ruby
URL: http://github.com/FooBarWidget/daemon_controller/tree/master
Source0: http://rubygems.org/gems/%{gemname}-%{version}.gem
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: opt-ruby-%{rubyver}
BuildRequires: opt-ruby-%{rubyver}
BuildArch: noarch
Provides: opt-ruby-%{rubyver}-rubygem(%{gemname}) = %{version}

%description
A library for robust daemon management.


%prep

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}
%{ruby_dir}/bin/gem install --local --install-dir %{buildroot}%{gemdir} \
            --force --rdoc %{SOURCE0}

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%{gemdir}/gems/%{gemname}-%{version}/
%doc %{gemdir}/doc/%{gemname}-%{version}
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec


%changelog
* Tue Oct 19 2010 Erik Ogan <erik@stealthymonkeys.com> - 0.2.5-1
- Initial package
