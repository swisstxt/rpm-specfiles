%define gemname file-tail
%define rubyver         1.9.3
%define ruby_dir /opt/ruby-%{rubyver}
%define ruby_sitelib %(%{ruby_dir}/bin/ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
%define gemdir %(%{ruby_dir}/bin/ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%define geminstdir %{gemdir}/gems/%{gemname}-%{version}

Summary: File::Tail for Ruby
Name: opt-ruby-%{rubyver}-rubygem-%{gemname}
Version: 1.0.8
Release: 1%{?dist}
Group: Development/Languages
License: GPLv2+ or Ruby
URL: http://flori.github.com/file-tail
Source0: http://rubygems.org/gems/%{gemname}-%{version}.gem
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: opt-ruby-%{rubyver}
Requires: opt-ruby-%{rubyver}-rubygem(spruz) >= 0.2.13
BuildRequires: opt-ruby-%{rubyver}
BuildArch: noarch
Provides: opt-ruby-%{rubyver}-rubygem(%{gemname}) = %{version}

%description
Library to tail files in Ruby


%prep

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}
%{ruby_dir}/bin/gem install --local --install-dir %{buildroot}%{gemdir} \
            --force --rdoc %{SOURCE0}
mkdir -p %{buildroot}/%{ruby_dir}/bin
mv %{buildroot}%{geminstdir}/bin/* %{buildroot}/%{ruby_dir}/bin
find %{buildroot}/%{ruby_dir}/bin -type f | xargs -n 1 sed -i  -e 's"^#!/usr/bin/env ruby"#!%{ruby_dir}/bin/ruby"'
rmdir %{buildroot}%{geminstdir}/bin

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%{ruby_dir}/bin/rtail
%{gemdir}/gems/%{gemname}-%{version}/
%doc %{gemdir}/doc/%{gemname}-%{version}
%doc %{geminstdir}/README.rdoc
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec


%changelog
* Tue Oct 19 2010 Erik Ogan <erik@stealthymonkeys.com> - 1.0.5-1
- Initial package
