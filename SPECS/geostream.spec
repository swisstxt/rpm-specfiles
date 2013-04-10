Name:           geostream
Version:        0.1.0
Release:        1%{?dist}
Summary:        Geostream Rails App
BuildArch:      noarch
Group:          Application/Internet
License:        Commercial
URL:            https://bitbucket.org/swisstxt/geostream
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: opt-ruby-1.9.3 opt-ruby-1.9.3-rubygem-bundler
BuildRequires: gcc libxml2 libxml2-devel libxslt libxslt-devel

Requires: opt-ruby-1.9.3 opt-ruby-1.9.3-rubygem-bundler


%define git_repo https://bitbucket.org/swisstxt/%{name}.git
%define appdir /opt/%{name}
%define cfgdir %{appdir}/config
%define logdir %{appdir}/log
%define tmpdir %{appdir}/tmp

%description
Geostream Rails App

%prep
rm -rf %{name}
git clone %{git_repo}
pushd %{name}
  git checkout master
popd


%build
pushd %{name}
  # install all dependencies via bundler
  /opt/ruby-1.9.3/bin/bundle install --deployment --shebang=/opt/ruby-1.9.3/bin/ruby

  # install bundler itself
  cat <<-EOD > gemrc
    gemhome: $PWD/vendor/bundle/ruby/1.9.1
    gempath:
    - $PWD/vendor/bundle/ruby/1.9.1
EOD
  /opt/ruby-1.9.3/bin/gem --config-file ./gemrc install bundler
  rm ./gemrc

  # correct shebangs for opt-ruby
  egrep -rl '#!/usr/bin/env ruby' . \
  | xargs sed -ri 's@#!/usr/bin/env ruby@#!/opt/ruby-1.9.3/bin/ruby@g'

  egrep -rl '#!/usr/local/bin/ruby' . \
  | xargs sed -ri 's@#!/usr/local/bin/ruby@#!/opt/ruby-1.9.3/bin/ruby@g'
popd


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{appdir}
mkdir -p $RPM_BUILD_ROOT/%{logdir}
mkdir -p $RPM_BUILD_ROOT/%{tmpdir}

pushd %{name}
  mv * .bundle $RPM_BUILD_ROOT/%{appdir}
popd

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{appdir}
%attr(755,apache,apache) %{logdir}
%attr(755,nobody,nobody) %{tmpdir}
%doc