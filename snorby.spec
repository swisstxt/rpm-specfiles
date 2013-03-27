Name:           snorby
Version:        2.5.6
Release:        2%{?dist}
Summary:        Snorby
BuildArch:      x86_64
Group:          Application/Internet
License:        GPLv3
URL:            https://snorby.org
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: ruby
BuildRequires: gcc libxml2 ruby-devel libxml2-devel libxslt libxslt-devel
#BuildRequires: qt-devel qtwebkit-devel
#BuildRequires: libcurl-devel

%define git_repo https://github.com/Snorby/snorby.git
%define appdir /var/www/vhosts/%{name}
%define configdir %{appdir}/config
%define logdir %{appdir}/log
%define tmpdir %{appdir}/tmp


%description
Snorby - Snort web interface


%prep
rm -rf %{name}
git clone %{git_repo}
pushd %{name}
  git checkout v%{version}
popd


%build
pushd %{name}
  bundle install --deployment

  cat <<-EOD > gemrc
    gemhome: $PWD/vendor/bundle/ruby/1.9.3
    gempath:
    - $PWD/vendor/bundle/ruby/1.9.3
EOD

  gem --config-file ./gemrc install bundler
  rm ./gemrc
popd


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{appdir}
mkdir -p $RPM_BUILD_ROOT/%{logdir}
mkdir -p $RPM_BUILD_ROOT/%{tmpdir}
mkdir -p $RPM_BUILD_ROOT/%{configdir}

pushd %{name}
  mv * $RPM_BUILD_ROOT/%{appdir}
popd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{appdir}
%attr(755,apache,apache) %{logdir}
%attr(755,nobody,nobody) %{tmpdir}
%doc
