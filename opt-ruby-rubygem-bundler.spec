%define gemname bundler
%define rubyver         1.9.3
%define ruby_dir /opt/ruby-%{rubyver}
%define ruby_sitelib %(%{ruby_dir}/bin/ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
%define gemdir %(%{ruby_dir}/bin/ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%define geminstdir %{gemdir}/gems/%{gemname}-%{version}

Summary: Bundler for Ruby %{rubyver}
Name: opt-ruby-%{rubyver}-rubygem-%{gemname}
Version: 1.1.5
Release: 1%{?dist}
Group: Development/Languages
License: GPLv2+ or Ruby
URL: http://getbundler.com
Source0: http://rubygems.org/gems/%{gemname}-%{version}.gem
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: opt-ruby-%{rubyver}
BuildRequires: opt-ruby-%{rubyver}
BuildArch: noarch
Provides: opt-ruby-%{rubyver}-rubygem(%{gemname}) = %{version}

%description
Bundler for Ruby %{rubyver}


%prep

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}
%{ruby_dir}/bin/gem install --local --install-dir %{buildroot}%{gemdir} --bindir %{buildroot}%{ruby_dir}/bin \
            --force --rdoc %{SOURCE0}

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%{ruby_dir}/bin/bundle
%{gemdir}/gems/%{gemname}-%{version}/
%doc %{gemdir}/doc/%{gemname}-%{version}
%doc %{geminstdir}/CHANGELOG.md
%doc %{geminstdir}/ISSUES.md
%doc %{geminstdir}/README.md
%doc %{geminstdir}/UPGRADING.md
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec


%changelog
* Mon Aug 13 2012 Marcel Haerry <haerry+rpm@puzzle.ch> - 1.0.5
- Initial package
