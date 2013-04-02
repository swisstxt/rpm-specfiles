Name:           geostream
Version:        0.1.0
Release:        1%{?dist}
Summary:        Geostream Rails App
BuildArch:      x86_64
Group:          Application/Internet
License:        Private
URL:            https://bitbucket.org/swisstxt/geostream
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: opt-ruby-1.9.3 opt-ruby-1.9.3-rubygem-bundler
BuildRequires: gcc libxml2 ruby-devel libxml2-devel libxslt libxslt-devel
#BuildRequires: qt-devel qtwebkit-devel
#BuildRequires: libcurl-devel

%define git_repo https://bitbucket.org/swisstxt/%{name}.git
%define appdir /opt/%{name}
%define configdir %{appdir}/config
%define logdir %{appdir}/log
%define tmpdir %{appdir}/tmp

%description
Geostream Rails App

%prep
rm -rf %{name}
git clone %{git_repo}
pushd %{name}
  git checkout %{version}
popd


%build
pushd %{name}
  /opt/ruby-1.9.3/bin/bundle install --deployment

	cat <<-EOD > gemrc
    gemhome: $PWD/vendor/bundle/ruby/1.9.3
    gempath:
    - $PWD/vendor/bundle/ruby/1.9.3
EOD

  /opt/ruby-1.9.3/bin/gem --config-file ./gemrc install bundler
	rm ./gemrc
popd


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{appdir}
mkdir -p $RPM_BUILD_ROOT/%{logdir}
mkdir -p $RPM_BUILD_ROOT/%{tmpdir}
mkdir -p $RPM_BUILD_ROOT/%{configdir}

pushd %{name}
  mv config/mongoid.yml.example config/mongoid.yml
	mv app config* lib public script vendor \
    Rakefile README Gemfile* \
    $RPM_BUILD_ROOT/%{appdir}
popd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{appdir}
%attr(755,apache,apache) %{logdir}
%attr(755,nobody,nobody) %{tmpdir}
%doc
