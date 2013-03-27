%define gemname rack
%define rubyver         1.9.3
%define ruby_dir /opt/ruby-%{rubyver}
%define ruby_sitelib %(%{ruby_dir}/bin/ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
%define gemdir %(%{ruby_dir}/bin/ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%define geminstdir %{gemdir}/gems/%{gemname}-%{version}

Name:           opt-ruby-%{rubyver}-rubygem-%{gemname}
Summary:        Common API for connecting web frameworks, web servers and layers of software
Version:        1.4.1
Release:        1%{?dist}
Group:          Development/Languages
License:        MIT
URL:            http://rubyforge.org/projects/%{gemname}/
Source0:        http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       opt-ruby-%{rubyver}
BuildRequires:  opt-ruby-%{rubyver}
BuildArch:      noarch
Provides:       opt-ruby-%{rubyver}-rubygem(%{gemname}) = %{version}

%description
Rack provides a common API for connecting web frameworks,
web servers and layers of software in between

%prep

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}
%{ruby_dir}/bin/gem install --local --install-dir %{buildroot}/%{gemdir} \
            --force %{SOURCE0}

chmod 755 %{buildroot}/%{geminstdir}/test/cgi/test.fcgi
chmod 755 %{buildroot}/%{geminstdir}/test/cgi/test.ru
chmod 755 %{buildroot}/%{geminstdir}/test/cgi/test
chmod 755 %{buildroot}/%{geminstdir}/bin/rackup

mkdir -p %{buildroot}/%{ruby_dir}/bin
mv %{buildroot}/%{gemdir}/bin/rackup %{buildroot}/%{ruby_dir}/bin
rm -rf %{buildroot}/%{gemdir}/bin/

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%dir %{geminstdir}
%doc %{gemdir}/doc/%{gemname}-%{version}
%doc %{geminstdir}/COPYING
%doc %{geminstdir}/README.rdoc
%doc %{geminstdir}/Rakefile
%doc %{geminstdir}/KNOWN-ISSUES
%doc %{geminstdir}/SPEC
%doc %{geminstdir}/example
%doc %{geminstdir}/test
%doc %{geminstdir}/contrib
%{geminstdir}/lib
%{geminstdir}/bin
%{ruby_dir}/bin/rackup
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec
#%{gemdir}/%{gemname}-%{version}/%{gemname}.gemspec
%{ruby_dir}/lib/ruby/gems/1.9.1/gems/%{gemname}-%{version}/%{gemname}.gemspec

%changelog
* Mon May 23 2011 mh - 1.3.2-1
- Update to 1.3.2

* Sun Nov 09 2008 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 0.4.0-2
- Remove unused macro (#470694)
- Add ruby(abi) = 1.8 as required by package guidelines (#470694)
- Move %%{gemdir}/bin/rackup to %%{install_dir}/bin (#470694)

* Sat Nov 08 2008 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 0.4.0-1
- Initial package
