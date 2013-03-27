# Generated from fastthread-0.6.4.1.gem by gem2rpm -*- rpm-spec -*-
%define gemname fastthread
%define rubyver         1.9.3
%define ruby_dir /opt/ruby-%{rubyver}
%define ruby_sitelib %(%{ruby_dir}/bin/ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']" 2>/dev/null)
%define ruby_sitearch %(%{ruby_dir}/bin/ruby -rrbconfig -e "puts Config::CONFIG['sitearchdir']" 2>/dev/null)
%define gemdir %(%{ruby_dir}/bin/ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%define geminstdir %{gemdir}/gems/%{gemname}-%{version}
%define _enable_debug_packages 0

Summary: Optimized replacement for thread.rb primitives
Name: opt-ruby-%{rubyver}-rubygem-%{gemname}
Version: 1.0.7
Release: 1%{?dist}
Group: Development/Languages
License: GPLv2+ or Ruby
URL: http://mongrel.rubyforge.org
Source0: http://gems.rubyforge.org/gems/%{gemname}-%{version}.gem
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: opt-ruby-%{rubyver}
BuildRequires: opt-ruby-%{rubyver}
Provides: opt-ruby-%{rubyver}-rubygem(%{gemname}) = %{version}

%description
Optimized replacement for thread.rb primitives

%prep

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}
%{ruby_dir}/bin/gem install --local --install-dir %{buildroot}%{gemdir} --force %{SOURCE0}
#mv %{buildroot}%{geminstdir}/lib/fastthread.so %{buildroot}%{ruby_sitearch}
sed -i s@%{buildroot}@@ %{buildroot}%{gemdir}/doc/fastthread-%{version}/rdoc/ext/fastthread/Makefile.html
#chmod 0755 %{buildroot}%{ruby_sitearch}/fastthread.so
rm -rf %{buildroot}%{geminstdir}/ext
rm -rf %{buildroot}%{geminstdir}/.require_paths
#strip %{buildroot}%{ruby_sitearch}/fastthread.so

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%doc %{gemdir}/doc
#%{ruby_sitearch}/fastthread.so
%{gemdir}/gems/%{gemname}-%{version}/
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%changelog
* Fri Jul 24 2009 Scott Seago <sseago@redhat.com> - 1.0.7-1
- Upgraded to 1.0.7

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 08 2008 Jeroen van Meeuwen <j.van.meeuwen@ogd.nl> - 1.0.1-1
- New upstream version

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0-2
- Autorebuild for GCC 4.3

* Thu Aug 23 2007  <sseago@redhat.com> - 1.0-1
- Updated gem to Version 1.0

* Tue Mar  6 2007  <sseago@redhat.com> - 0.6.4.1-1
- Initial packaging.
