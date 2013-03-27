%define gemname spruz
%define rubyver         1.9.3
%define ruby_dir /opt/ruby-%{rubyver}
%define ruby_sitelib %(%{ruby_dir}/bin/ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
%define gemdir %(%{ruby_dir}/bin/ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%define geminstdir %{gemdir}/gems/%{gemname}-%{version}

Summary: Useful stuff
Name: opt-ruby-%{rubyver}-rubygem-%{gemname}
Version: 0.2.13
Release: 1%{?dist}
Group: Development/Languages
License: GPLv2+ or Ruby
URL: http://flori.github.com/spruz
Source0: http://rubygems.org/gems/%{gemname}-%{version}.gem
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: opt-ruby-%{rubyver}
BuildRequires: opt-ruby-%{rubyver}
BuildArch: noarch
Provides: opt-ruby-%{rubyver}-rubygem(%{gemname}) = %{version}

%description
All the stuff that isn't good/big enough for a real library.


%prep

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}
%{ruby_dir}/bin/gem install --local --install-dir %{buildroot}%{gemdir} \
            --force --rdoc %{SOURCE0}
mkdir -p %{buildroot}/%{_bindir}
mv %{buildroot}%{gemdir}/bin/* %{buildroot}/%{_bindir}
rmdir %{buildroot}%{gemdir}/bin
find %{buildroot}%{geminstdir}/bin -type f | xargs chmod a+x

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%{_bindir}/enum
%{gemdir}/gems/%{gemname}-%{version}/
%doc %{gemdir}/doc/%{gemname}-%{version}
%doc %{geminstdir}/README.rdoc
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec


%changelog
* Tue Oct 19 2010 Erik Ogan <erik@stealthymonkeys.com> - 0.1.5-1
- Initial package
